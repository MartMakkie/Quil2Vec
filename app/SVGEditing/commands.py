from typing import Literal
import numpy as np

from PySide6.QtGui import QUndoCommand

from renderObjects import *
from svgEditing import Quil2VecCanvasScene, replacePathInFile, getPathLocationInFile
from FileHandling.fileHandler import Quil2VecVectorPath, Quill2VecSaveFile
from svg.path import Path as SVGpath

###################
# TOOL DELEGATION #
###################
toolModes = Literal[
    "qCuttingMode", 
    "qTransformMode", 
    "qNavmode", 
    "qBaseMode", 
    None
    ]

class qCuttingModeCommand(QUndoCommand):
    def __init__(self, scene:Quil2VecCanvasScene, original_path, cut_point1:QPointF, cut_point2:QPointF, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.original_path = original_path
        self.cut_point1 = cut_point1
        self.cut_point2 = cut_point2

        self.resulting_paths = None
        self.resulting_qPaths = None
        self.original_path_data = None
        
        self.setText("Cut Path")

    def redo(self):
        # Excecute the cut path operation
        if self.resulting_paths is None:
            # First time excecution
            self.original_path:Quil2VecQPathItem
            pathSVG = self.original_path.translator
            cut_point1 = complex(self.cut_point1.x(), self.cut_point1.y())
            cut_point2 = complex(self.cut_point2.x(), self.cut_point2.y())
            self.resulting_paths = cutPath(pathSVG, cut_point1, cut_point2)
            # self.scene.parent.file:Quill2VecSaveFile
            # Replace in save-file
            pathIndex = getPathLocationInFile(self.scene, self.original_path.translator)[-1]
            replacePathInFile(self.original_path.translator, self.scene, self.resulting_paths)
            self.scene.removeItem(self.original_path)
            self.resulting_qPaths = []
            for i, _p in enumerate(self.resulting_paths):
                newQPath = Quil2VecQPathItem(_p,pathIndex+i-1, self.scene)
                self.resulting_qPaths.append(newQPath)
            # for qPath in self.resulting_qPaths:
                self.scene.addItem(newQPath)
        else:
            # Subsequent redo - restore the cut state
            # self.scene.removeItem(self.original_path)
            # for path_data_path in self.resulting_paths:
            #     self.scene.addItem(path_data_path[2])
            pathIndex = getPathLocationInFile(self.scene, self.original_path)[-1]
            replacePathInFile(self.original_path.translator, self.scene, self.resulting_paths)
            self.scene.removeItem(self.original_path)
            self.resulting_qPaths = []
            for i, _p in enumerate(self.resulting_paths):
                newQPath = Quil2VecQPathItem(_p,pathIndex+i-1, self.scene)
                self.resulting_qPaths.append(newQPath)
            # for qPath in self.resulting_qPaths:
                self.scene.addItem(newQPath)

    def undo(self):
        # Undo the original operation and restore original state
        pageIndex, layername, pathInLayerLoc = getPathLocationInFile(self.scene, self.resulting_paths[0])
        for qPath in self.resulting_qPaths:
            self.scene.removeItem(qPath)
        self.scene.addItem(self.original_path)

        self.scene.parent().file.pages[pageIndex].layers[layername].paths[pathInLayerLoc] = self.original_path.translator
        del self.scene.parent().file.pages[pageIndex].layers[layername].paths[pathInLayerLoc+1:pathInLayerLoc+len(self.resulting_paths)-1]
        # for path_data_path in self.resulting_paths:
        #     self.scene.removeItem(path_data_path[1])
        
        # self.scene.addItem(self.original_path)

class qmoveCommand(QUndoCommand):
    def redo(self):
        # excecute command
        pass
    def undo(self):
        # undo the original operation
        pass
class qPathTransformCommand(QUndoCommand):
    def redo(self):
        # excecute command
        pass
    def undo(self):
        # undo the original operation
        pass

class qGroupCommand(QUndoCommand):
    def redo(self):
        # excecute command
        pass
    def undo(self):
        # undo the original operation
        pass

class qMovePathCommand(QUndoCommand):
    def redo(self):
        # excecute command
        pass
    def undo(self):
        # undo the original operation
        pass

class qDrawPathCommand(QUndoCommand):
    def redo(self):
        # excecute command
        pass
    def undo(self):
        # undo the original operation
        pass

####################
# Actual functions #
####################


'''
CUTTING
'''
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

def cutPath(inPath:SVGpath, cut_point1:complex, cut_point2:complex) -> tuple[Quil2VecVectorPath, Quil2VecVectorPath]:
    pass
    '''
    Should be Qt-agnostic. So we could use it in other contexts as well
    How it should work:
        1. check for intersection (the cutting should be performed along a line)
        2. Group the segments along the cutting-line, with segments being intersected belonging to both groups
        3. Cut each of the intersected segments, discarding the part not belonging in the group
        4. From the SVG-paths, construct new cannonical versions
        5. Return the new paths
    '''