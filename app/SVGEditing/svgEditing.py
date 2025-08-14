from PySide6.QtGui import QUndoCommand

from core.martsLoggingHandler import get_logger


logger = get_logger(__name__)


###################
# TOOL DELEGATION #
###################

class qCuttingModeCommand(QUndoCommand):
    def __init__(self, scene, original_path, cut_point1, cut_point2, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.original_path = original_path
        self.cut_point1 = cut_point1
        self.cut_point2 = cut_point2

        self.resulting_paths = None
        self.original_path_data = None
        
        self.setText("Cut Path")

    def redo(self):
        # Excecute the cut path operation
        if self.resulting_paths is None:
            # First time excecution
            self.resulting_paths = self.original_path_data.cut_path(self.cut_point1, self.cut_point2)
            self.scene.removeItem(self.original_path)

            for path_data_path in self.resulting_paths:
                self.scene.addItem(path_data_path[2])
        else:
            # Subsequent redo - restore the cut state
            self.scene.removeItem(self.original_path)
            for path_data_path in self.resulting_paths:
                self.scene.addItem(path_data_path[2])
    
    def undo(self):
        # Undo the original operation and restore original state
        for path_data_path in self.resulting_paths:
            self.scene.removeItem(path_data_path[1])
        
        self.scene.addItem(self.original_path)

class qmoveCommand(QUndoCommand):
    pass

class qPathTransformCommand(QUndoCommand):
    pass

class qGroupCommand(QUndoCommand):
    pass

class qMovePathCommand(QUndoCommand):
    pass


'''
Path Cutting
'''
from PySide6.QtWidgets import QGraphicsEllipseItem 
from PySide6.QtCore import QPointF
import numpy as np

class selectionPoint(QGraphicsEllipseItem):
    def __init__(self, pos: QPointF, parent = None, radius = 5):
        pass

def segment_point(t, segment):
    return segment.point(t)  # Works for Line, QuadraticBezier, CubicBezier

def closest_point_on_segment(Q, segment, samples=10):
    """
    Fast nearest point finder on a segment.
    1. Sample points evenly along t=[0,1].
    2. Find the closest sample point.
    3. Refine search in the small range around that t.
    """
    ts = np.linspace(0, 1, samples)
    pts = [segment_point(t, segment) for t in ts]
    dists_sq = [abs(p - Q)**2 for p in pts]

    # Step 1: closest sample
    i_min = int(np.argmin(dists_sq))
    t_guess = ts[i_min]

    # Step 2: refine search in a small window
    t_min = max(0, t_guess - 1/samples)
    t_max = min(1, t_guess + 1/samples)

    # Do a quick ternary search for min distance
    for _ in range(10):  # refine iterations
        t1 = t_min + (t_max - t_min) / 3
        t2 = t_max - (t_max - t_min) / 3
        d1 = abs(segment_point(t1, segment) - Q)**2
        d2 = abs(segment_point(t2, segment) - Q)**2
        if d1 < d2:
            t_max = t2
        else:
            t_min = t1

    t_closest = (t_min + t_max) / 2
    return segment_point(t_closest, segment), t_closest

def closest_point_on_path(Q, path):
    closest_pt = None
    min_dist_sq = float('inf')

    for segment in path:
        pt, _ = closest_point_on_segment(Q, segment)
        dist_sq = abs(pt - Q)**2
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            closest_pt = pt

    return closest_pt    

################
# CANVAS STUFF #
################
from PySide6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsObject, QGraphicsScene, QGraphicsLineItem
from PySide6.QtGui import QColor, QPainter, QTransform, QUndoStack
from PySide6.QtCore import QRectF, QLineF


from FileHandling.fileHandler import Quill2VecFileLayer, Quil2VecVectorPath, Quill2VecFileLayer, Quill2VecPathLayer
from renderObjects import *

class Quil2VecCanvasScene(QGraphicsScene):
    '''
    the graphic scene handles:
    - Rendering of the physical objects
    - Selection managment of objects
    - Tool selection
    - Mouse events for tools
    - Layer management
        + Layer panel stuff in other file?
    '''
    def __init__(self, parent = None):
        super.__init__(parent)
        # just for conveniences sake, lets make qGroupMove the default fallback tool when toolselection delegation from the toolbar does not work
        self.selectedTool: toolModes = "qGroupMove"
        self.layers = {}
        self.pageIndex:str = None
        self.activeLayer:Quill2VecFileLayer = None # Current working layer as dict key in layers dictionary
        # self.backgroundImage = None
        self.undo_stack = QUndoStack(self)
        # for cutting paths 
        self.highlight_point = None  # Point on the path that is highlighted for cutting
        self.selected_path = None  # The path currently selected for cutting
        self.cut_point1 = None  # First point selected for cutting
        self.cut_point2 = None  # Second point selected for cutting
        self.cut_line = None # Line to indicate the cut that will happen

    def drawBackground(self, painter: QPainter, rect: QRectF):
        painter.fillRect(rect, QColor("white"))  
    
    def fromFile(self, parent):
        # outself = self(parent)
        curPage = parent.file.getCurrentPage()
        self.pageIndex = curPage.pageIndex
        # curPage:Quill2VecPage
        for layer in curPage.layers.items():
            self.layers[layer[0]] = layer[1]
            if layer[1].active:
                self.active_layer = layer[0]
        self.update()
    
    def add_layer(self, name="New Layer"):
        # default active layer to the newly created layer 
        self.active_layer = name
        layer = Quill2VecFileLayer(name)
        self.layers.append(layer)
        if not self.active_layer:
            self.active_layer[name] = layer  # Set the first layer as active

    def backUpSave(self):
        '''Should MAYBE handle the moving of stuff from the CanvasScene to the savefile
        I'd rather have it update the savefile upon finishing an action, so little actual saving of data is done in the scene itself'''
        pass

    def update(self):
        self.backUpSave()
        for item in self.items():
            logger.info('removing item from scene')
            self.removeItem(item)
        
        if not self.active_layer:
            for k in self.layers:
                self.active_layer = k
                break
        actLayer = self.layers[self.active_layer]
        actLayer:Quill2VecFileLayer
        logger.info('adding vectorpaths to Scene')
        for i, path in enumerate(actLayer.paths):
            path:Quil2VecVectorPath
            # qpath = Quil2VecQPathItem(path)
            self.addItem(Quil2VecQPathItem(path, self, i))
    
    ################
    # Mouse events #
    ################

    def mousePressEvent(self, event):
        # Get the item under the mouse
        if self.selectedTool == "qTransformMode":
            clicked_item = self.itemAt(event.scenePos(), QTransform())

            # If it’s a selectable item and not already selected
            if isinstance(clicked_item, Quil2VecQPathItem):
                # Deselect all others
                for item in self.selectedItems():
                    if item is not clicked_item:
                        item.setSelected(False)
                clicked_item.setSelected(True)
            else:
                # If clicking empty space, deselect everything
                for item in self.selectedItems():
                    item.setSelected(False)
        # elif self.selectedTool == "qGroupMove":
        #     pass
        elif self.selectedTool == "qCuttingMode":
            if self.selected_path:
                # mouse_x = event.position().x()
                # mouse_y = event.position().y()
                # Q = complex(mouse_x, mouse_y)

                # nearest_pt = closest_point_on_path(Q, self.selected_path)
                if self.cut_point1:
                    self.cut_point2 = self.highlight_point
                    cut_command = qCuttingModeCommand(self, self.selected_path, self.cut_point1, self.cut_point2)

                    self.selected_path.cut_path(self.cut_point1, self.cut_point2)
                    self.cut_point1 = None
                    self.cut_point2 = None
                    self.cut_line = None
                    # self.emit(Signal("cut_segment"), self.cut_point1, self.cut_point2, self.selected_path)
                else:
                    self.cut_point1 = self.highlight_point
                    
                # self.highlight_point = nearest_pt
                self.update()  # trigger paintEvent
        elif self.selectedTool == "qNavmode":
            pass
        elif self.selectedTool == "qBaseMode":
            pass
        # Pass event to base class to handle item selection normally
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selectedTool == "qTransformMode":
            # Handle path transform
            pass
        elif self.selectedTool == "qGroupMove":
            # Handle group moving
            pass
        elif self.selectedTool == "qCuttingMode":
            # Handle segment cutting
            if self.selected_path:
                mouse_x = event.position().x()
                mouse_y = event.position().y()
                Q = complex(mouse_x, mouse_y)

                nearest_pt = closest_point_on_path(Q, self.selected_path)
                self.highlight_point = nearest_pt
                if self.cut_point1:
                    if not self.cut_line:
                        self.cut_line = QGraphicsLineItem(QLineF(self.cut_point1, self.highlight_point))
                        self.addItem(self.cut_line)
                    else:
                        self.cut_line.setLine(QLineF(self.cut_point1, self.highlight_point))
                self.update()  # trigger paintEvent
        elif self.selectedTool == "qNavmode":
            pass
        elif self.selectedTool == "qBaseMode":
            pass
        super().mouseMoveEvent(event)

    

    # Undostack stuff
    def get_undo_stack(self):
        """Return the undo stack for integration with main window"""
        return self.undo_stack
    
    def can_undo(self):
        return self.undo_stack.canUndo()
    
    def can_redo(self):
        return self.undo_stack.canRedo()
    
    def undo(self):
        self.undo_stack.undo()
    
    def redo(self):
        self.undo_stack.redo()

def getPathLocationInFile(scene:Quil2VecCanvasScene, path):
    if scene.activeLayer == Quill2VecPathLayer:
        pathInLayerLoc = scene.activeLayer.paths.index(path)
        layername = scene.activeLayer.name
        pageIndex = scene.pageIndex
        return pageIndex, layername, pathInLayerLoc
    else:
        logger.error("Tried to get a path from a Quill2VecFileLayer which is not a Quill2VecPathLayer")

def replacePathInFile(pathToReplace, scene, *replaceMentPaths):
    pageIndex, layername, pathInLayerLoc = getPathLocationInFile(scene, pathToReplace)
    scene.parent().file.pages[pageIndex].layers[layername].paths[pathInLayerLoc:pathInLayerLoc+len(replaceMentPaths)-1] = replaceMentPaths