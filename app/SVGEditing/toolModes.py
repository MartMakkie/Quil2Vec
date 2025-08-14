from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QGraphicsScene, QGraphicsLineItem
from PySide6.QtCore import QLineF

from commands import *
from renderObjects import *

class ToolMode:
    def mousePressEvent(self, scene:QGraphicsScene, event):pass
    def mouseMoveEvent(self, scene:QGraphicsScene, event):pass
    def mouseReleaseEvent(self, scene:QGraphicsScene, event):pass

class TransformMode(ToolMode):
    dragging = False
    def mousePressEvent(self, scene:QGraphicsScene, event):
        # Scene-level transform logic
        clicked_item = scene.itemAt(event.scenePos(), QTransform())

        # If it’s a selectable item and not already selected
        if isinstance(clicked_item, Quil2VecQPathItem):
            # Deselect all others
            for item in scene.selectedItems():
                if item is not clicked_item:
                    item.setSelected(False)
            clicked_item.setSelected(True)
        elif isinstance(clicked_item, Quil2VecQSegmentItem):
            # select the Quil2VecQSegmentItem
            pass
        elif isinstance(clicked_item, Quil2VecQEditPoint):
            # start the drag event
            pass
        else:
            # If clicking empty space, deselect everything
            for item in scene.selectedItems():
                item.setSelected(False)
        return super().mousePressEvent(scene, event)
    

class NavMode(ToolMode):
    def mousePressEvent(self, scene:QGraphicsScene, event):
        # Navigation logic
        pass

class CuttingMode(ToolMode):
    def mousePressEvent(self, scene:QGraphicsScene, event):
        if scene.selected_path:
                # mouse_x = event.position().x()
                # mouse_y = event.position().y()
                # Q = complex(mouse_x, mouse_y)

                # nearest_pt = closest_point_on_path(Q, self.selected_path)
                if scene.cut_point1:
                    scene.cut_point2 = scene.highlight_point
                    cut_command = qCuttingModeCommand(self, scene.selected_path, scene.cut_point1, scene.cut_point2)
                    scene.undo_stack.push(cut_command)
                    scene.removeItem(self.cut_point1)
                    # self.selected_path.cut_path(self.cut_point1, self.cut_point2)
                    scene.cut_point1 = None
                    scene.cut_point2 = None
                    scene.cut_line = None
                    # self.emit(Signal("cut_segment"), self.cut_point1, self.cut_point2, self.selected_path)
                else:
                    scene.cut_point1 = self.highlight_point
                    # change appearance of self.cut_point1 
                    scene.addItem(self.cut_point1)
                    
                # self.highlight_point = nearest_pt
                scene.update()  # trigger paintEvent
        return super().mousePressEvent(scene, event)
    def mouseMoveEvent(self, scene:QGraphicsScene, event):
        # Handle segment cutting
        if scene.selected_path:
            mouse_x = event.position().x()
            mouse_y = event.position().y()
            Q = complex(mouse_x, mouse_y)

            nearest_pt = closest_point_on_path(Q, scene.selected_path)
            scene.highlight_point = nearest_pt
            if scene.cut_point1:
                if not scene.cut_line:
                    scene.cut_line = QGraphicsLineItem(QLineF(scene.cut_point1, scene.highlight_point))
                    scene.addItem(self.cut_line)
                else:
                    scene.cut_line.setLine(QLineF(scene.cut_point1, scene.highlight_point))
            scene.update()  # trigger paintEvent
        return super().mouseMoveEvent(scene, event)
    
class BaseToolMode(ToolMode):
    pass