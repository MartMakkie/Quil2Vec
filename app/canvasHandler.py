from PySide6.QtGui import QPainterPath, QPen, QColor, QBrush, QTransform, QPainterPathStroker
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsScene, QGraphicsItemGroup, QGraphicsItem, QGraphicsObject, QGraphicsEllipseItem, QGraphicsLineItem
from PySide6.QtGui import (QPainterPath, QPainter)
from PySide6.QtCore import QRectF, Qt, QPointF, QLineF
import svg.path
from Quil2VecGlobals import *
from app.FileHandling.fileHandler import Quill2VecFileLayer, Quil2VecVectorPath
import svg
from app.core.martsLoggingHandler import get_logger

logger = get_logger(__name__)

class Quil2VecQSegmentItem(QGraphicsPathItem):
    def __init__(self, path, segment_data, index, parent_path):
        super().__init__(path)
        self.segment_data = segment_data
        self.index = index
        self._parent_path = parent_path

        self.control_points = []
        self.control_lines = []
        self.control_points_visible = False

        self._hovered = False
        self._path_selected = False
        self._active = False

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(1)

        self.updateAppearance()

    def setPath(self, path, segment_data):
        if segment_data != self.segment_data:
            super().setPath(path)
            self.segment_data = segment_data
            self.updateAppearance()

    # Selection Handling
    def setPathSelected(self, selected: bool):
        self._active = selected
        if selected:
            self.show_control_points()
        else:
            self.remove_control_points()
        self.updateAppearance()

    # Control Point Creation
    def create_control_points(self):
        """Create control points & connector lines for current segment."""
        if self.control_points_visible:
            return
        
        point_positions = self.get_control_points(self.segment_data)
        self.control_points.clear()
        self.control_lines.clear()

        # last_point_item = None
        for i, pos in enumerate(point_positions):
            
            cp_item = Quil2VecControlPointItem(pos, self, i)
            cp_item.setParentItem(self)
            cp_item.setPos(pos)
            cp_item.show()
            self.control_points.append(cp_item)

        if isinstance(self.segment_data, svg.path.CubicBezier):
            # anchor → control1
            line1 = QGraphicsLineItem(QLineF(
                self.control_points[0].pos(),
                self.control_points[1].pos()
            ), parent=self)
            line1.setPen(QPen(QColor("gray"), 0, Qt.DashLine))
            self.control_lines.append(line1)

            # control2 → anchor(end)
            line2 = QGraphicsLineItem(QLineF(
                self.control_points[2].pos(),
                self.control_points[3].pos()
            ), parent=self)
            line2.setPen(QPen(QColor("gray"), 0, Qt.DashLine))
            self.control_lines.append(line2)

        elif isinstance(self.segment_data, svg.path.QuadraticBezier):
            # anchor → control
            line1 = QGraphicsLineItem(QLineF(
                self.control_points[0].pos(),
                self.control_points[1].pos()
            ), parent=self)
            line1.setPen(QPen(QColor("gray"), 0, Qt.DashLine))
            self.control_lines.append(line1)

            # control → anchor(end)
            line2 = QGraphicsLineItem(QLineF(
                self.control_points[1].pos(),
                self.control_points[2].pos()
            ), parent=self)
            line2.setPen(QPen(QColor("gray"), 0, Qt.DashLine))
            self.control_lines.append(line2)
        

            # # If we have a previous point, add a line between them
            # if last_point_item:
            #     line_item = QGraphicsLineItem(
            #         QLineF(last_point_item.pos(), cp_item.pos()), parent=self
            #     )
            #     line_item.setPen(QPen(QColor("gray"), 1, Qt.DashLine))
            #     line_item.setZValue(0)  # under the control points
            #     self.control_lines.append(line_item)

            # last_point_item = cp_item

        self.control_points_visible = True

    def show_control_points(self):
        self.create_control_points()

    def remove_control_points(self):
        """Remove control points & connector lines from the scene."""
        for cp in self.control_points:
            self.scene().removeItem(cp)
        for line in self.control_lines:
            self.scene().removeItem(line)

        self.control_points.clear()
        self.control_lines.clear()
        self.control_points_visible = False

    # Live Update on Move
    def control_point_moved(self, point_index, new_pos: QPointF):
        """Update both visual connector lines & actual segment_data."""
        # Update connector lines

        if isinstance(self.segment_data, svg.path.CubicBezier):
            if point_index in (0, 1):  # start anchor or first handle
                if len(self.control_lines) > 0:
                    self.control_lines[0] = QGraphicsLineItem(
                    # .setLine(
                    QLineF(
                        self.control_points[0].pos(),
                        self.control_points[1].pos()
                    ))
                else:
                    self.control_lines.append(   
                # self.control_lines[0] = 
                QGraphicsLineItem(
                # .setLine(
                QLineF(
                    self.control_points[0].pos(),
                    self.control_points[1].pos()
                ))
                )
            if point_index in (2, 3):  # second handle or end anchor
                if len(self.control_lines) > 1:
                    self.control_lines[1] = QGraphicsLineItem(
                    # .setLine(
                    QLineF(
                        self.control_points[2].pos(),
                        self.control_points[3].pos()
                    ))
                else:
                    self.control_lines.append(
                # self.control_lines[1] = 
                QGraphicsLineItem(
                # .setLine(
                QLineF(
                    self.control_points[2].pos(),
                    self.control_points[3].pos()
                ))
                )
        elif isinstance(self.segment_data, svg.path.QuadraticBezier):
            if point_index in (0, 1):
                if len(self.control_lines) > 0:
                    self.control_lines[0] = QGraphicsLineItem(
                    # .setLine(
                    QLineF(
                        self.control_points[0].pos(),
                        self.control_points[1].pos()
                    ))
                else:
                    self.control_lines.append(
                # self.control_lines[0] = 
                QGraphicsLineItem(
                # .setLine(
                QLineF(
                    self.control_points[0].pos(),
                    self.control_points[1].pos()
                ))
                )
            if point_index in (1, 2):
                if len(self.control_lines) > 1:
                    self.control_lines[1] = QGraphicsLineItem(
                    # .setLine(
                    QLineF(
                        self.control_points[1].pos(),
                        self.control_points[2].pos()
                    ))
                else:
                    self.control_lines.append(
                # self.control_lines[1] = 
                QGraphicsLineItem(
                # .setLine(
                QLineF(
                    self.control_points[1].pos(),
                    self.control_points[2].pos()
                ))
                )
        # if point_index > 0 and point_index - 1 < len(self.control_lines):
        #     self.control_lines[point_index - 1].setLine(
        #         QLineF(self.control_points[point_index - 1].pos(), new_pos)
        #     )
        # if point_index < len(self.control_points) - 1:
        #     self.control_lines[point_index].setLine(
        #         QLineF(new_pos, self.control_points[point_index + 1].pos())
        #     )

        # Update actual segment data
        self.update_control_point_in_segment(point_index, new_pos)
        if point_index == 0:  # start point
            prev_seg = self._parent_path.get_segment(self.index - 1)
            if prev_seg:
                prev_seg.update_control_point_in_segment(len(prev_seg.get_control_points()) - 1, new_pos)

        elif point_index == len(self.control_points) - 1:  # end point
            next_seg = self._parent_path.get_segment(self.index + 1)
            if next_seg:
                next_seg.update_control_point_in_segment(0, new_pos)
        # Notify path & redraw
        self._parent_path.translator.update_segment(self.index, self.segment_data)
        self._parent_path.redraw()

    # Segment Control Point Data Extraction
    def get_control_points(self, seg):
        """Convert svg.path PathSegments to list of QPointF control points."""
        points = []
        if hasattr(seg, "start"):
            points.append(QPointF(seg.start.real, seg.start.imag))
        if isinstance(seg, svg.path.CubicBezier):
            points.append(QPointF(seg.control1.real, seg.control1.imag))
            points.append(QPointF(seg.control2.real, seg.control2.imag))
        elif isinstance(seg, svg.path.QuadraticBezier):
            points.append(QPointF(seg.control.real, seg.control.imag))
        if hasattr(seg, "end"):
            points.append(QPointF(seg.end.real, seg.end.imag))
        # outPoints = []
        # for i, point in enumerate(points):
        #     newPointPathItem = Quil2VecControlPointItem(point, self, i-1)
        #     outPoints.append(newPointPathItem)
        # return outPoints
        return points
    #     """Extract QPointF positions from self.segment_data."""
    #     seg = self.segment_data
    #     points = []
    #     if hasattr(seg, "start"):
    #         points.append(QPointF(seg.start.real, seg.start.imag))
    #     if isinstance(seg, svg.path.CubicBezier):
    #         points.append(QPointF(seg.control1.real, seg.control1.imag))
    #         points.append(QPointF(seg.control2.real, seg.control2.imag))
    #     elif isinstance(seg, svg.path.QuadraticBezier):
    #         points.append(QPointF(seg.control.real, seg.control.imag))
    #     if hasattr(seg, "end"):
    #         points.append(QPointF(seg.end.real, seg.end.imag))
    #     return points

    def update_control_point_in_segment(self, point_index, new_pos: QPointF):
        """Push new QPointF into self.segment_data."""
        seg = self.segment_data
        complex_pos = complex(new_pos.x(), new_pos.y())

        if isinstance(seg, svg.path.CubicBezier):
            if point_index == 0: seg.start = complex_pos
            elif point_index == 1: seg.control1 = complex_pos
            elif point_index == 2: seg.control2 = complex_pos
            elif point_index == 3: seg.end = complex_pos
        elif isinstance(seg, svg.path.QuadraticBezier):
            if point_index == 0: seg.start = complex_pos
            elif point_index == 1: seg.control = complex_pos
            elif point_index == 2: seg.end = complex_pos
        elif isinstance(seg, svg.path.Line):
            if point_index == 0: seg.start = complex_pos
            elif point_index == 1: seg.end = complex_pos
        elif isinstance(seg, svg.path.Arc):
            if point_index == 0: seg.start = complex_pos
            elif point_index == 1: seg.end = complex_pos

    # Hover / Appearance
    def hoverEnterEvent(self, event):
        if self._path_selected:
            self._hovered = True
            self.updateAppearance()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._hovered = False
        self.updateAppearance()
        super().hoverLeaveEvent(event)

    def updateAppearance(self):
        if self._active and self._path_selected:
            logger.info(f'Updating appereance of segment {self.index} to be active')
            self.setPen(QPen(QColor("blue"), 1))
            logger.info(f'Updating appereance of segment {self.index} to represent parent being selected')
        elif self._hovered and self._path_selected:
            # logger.info(f'Updating appereance of segment {self.index} to being hovered')
            self.setPen(globelHoverPen)
        elif self._path_selected:
            self.setPen(globalSelectPen)
        else:
            logger.info(f'Updating appereance of segment {self.index} to default')
            self.setPen(globalDefaultPen)
    # def updateAppearance(self):
    #     if self._path_selected:
    #         self.setPen(QPen(QColor("blue") if self._hovered else QColor("green"), 1))
    #     else:
    #         self.setPen(QPen(QColor("black"), 1))

class Quil2VecControlPointItem(QGraphicsEllipseItem):
    def __init__(self, pos: QPointF, segment_item: Quil2VecQSegmentItem, point_index, radius=5):
        super().__init__(-radius, -radius, radius * 2, radius * 2)
        self.setBrush(QBrush(QColor("red")))
        self.setPen(QPen(QColor("black"), 1))
        self.setZValue(10)
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges |
            QGraphicsItem.ItemIgnoresTransformations
        )
        self.segment_item = segment_item
        self.point_index = point_index
        self.setPos(pos)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if self.segment_item.control_points_visible:
                self.segment_item.control_point_moved(self.point_index, value)
        return super().itemChange(change, value)


class ShapeDebugOverlay(QGraphicsPathItem):
    def __init__(self, shape_path, color, parent=None):
        super().__init__(shape_path, parent)
        self.setPen(QPen(QColor(color), 1, Qt.DashLine))
        self.setBrush(QColor(color).lighter(170))
        self.setZValue(9999)  # Always on top
        self.setOpacity(0.3)  # Semi-transparent
        self.setFlag(QGraphicsPathItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsPathItem.ItemIsMovable, False)
        self.setAcceptedMouseButtons(Qt.NoButton)

class Quil2VecQPathItem(QGraphicsObject):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.path, self.segment_data = self.translator.to_qpath()
        self.active_segment = None
        self.path_visual = QGraphicsPathItem(self.path, parent=self)
        self.path_visual.setBrush(globalDefaultBrush)
        self.path_visual.setPen(globalDefaultPen)
        self.segments = []
        for i, _seg in enumerate(self.segment_data):
            seg_path, seg_data = _seg
            segment = Quil2VecQSegmentItem(seg_path, seg_data, i, self)
            # logger.info(str((seg_path, seg_data, i)))
            segment.setParentItem(self)
            # self.scene().addItem(segment)
            self.segments.append(segment)

        # Debug hitboxes
        self.debug_show_hitboxes = False
        self.debug_disable_shape = False
        self.debug_path_hitbox = None
        self.debug_segment_hitboxes = []
        self.setFlag(QGraphicsObject.ItemIsSelectable, True)
        self.setFlag(QGraphicsObject.ItemIsFocusable, True)
        # self.setFlag(QGraphicsObject.ItemHasNoContents, True)
        self.setAcceptHoverEvents(True)

    def toggle_debug_hitboxes(self, show: bool):
        """Show/hide debug hitboxes."""
        if show and not self.debug_show_hitboxes:
            # Path hitbox
            path_shape = self.shape()
            self.debug_path_hitbox = ShapeDebugOverlay(path_shape, "magenta", parent=self)
            # Segment hitboxes
            for segment in self.segments:
                seg_shape = segment.shape()
                overlay = ShapeDebugOverlay(seg_shape, "cyan", parent=segment)
                self.debug_segment_hitboxes.append(overlay)
            self.debug_show_hitboxes = True
        elif not show and self.debug_show_hitboxes:
            if self.debug_path_hitbox:
                self.scene().removeItem(self.debug_path_hitbox)
                self.debug_path_hitbox = None
            for overlay in self.debug_segment_hitboxes:
                self.scene().removeItem(overlay)
            self.debug_segment_hitboxes.clear()
            self.debug_show_hitboxes = False

    def toggle_debug_disable_shape(self, disable: bool):
        """Enable/disable PathItem shape interception."""
        self.debug_disable_shape = disable
        logger.info(f"Debug: Path shape {'disabled' if disable else 'enabled'}")
        self.update()

    def boundingRect(self):
        return self.path_visual.boundingRect().adjusted(-3, -3, 3, 3)

    def shape(self):
        """Return shape if debug_disable_shape is False."""
        if self.debug_disable_shape or self.isSelected():
            return QPainterPath()  # Empty shape: does not intercept
        return self.path_visual.shape()
    
    def paint(self, painter, option, widget=None):
        pass  # Nothing to paint directly

    def setSelected(self, selected):
        if selected:
            logger.info('Path item selected')
        super().setSelected(selected)
        for seg in self.segments:
            seg.setPathSelected(selected)
        if not selected:
            self.clear_active_segment()

    def set_active_segment(self, segment):
        if self.active_segment and self.active_segment != segment:
            self.active_segment.setActive(False)
        self.active_segment = segment
        self.active_segment.setActive(True)

    def clear_active_segment(self):
        if self.active_segment:
            self.active_segment.setActive(False)

        self.active_segment = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.isSelected():
            # Ensure only this path is selected
            for item in self.scene().selectedItems():
                if item != self:
                    item.setSelected(False)
            self.setSelected(True)
            event.accept()
        else:
            event.ignore()
        super().mousePressEvent(event)

    def get_segment(self, index):
        """Get segment by index."""
        if 0 <= index < len(self.segments):
            return self.segments[index]
        return None

    def redraw(self):
        # Get updated path and segments from translator
        self.path, self.segment_data = self.translator.to_qpath()
        self.path_visual.setPath(self.path)

        for i, segment in enumerate(self.segments):
            seg_path, seg_data = self.segment_data[i]
            segment.setPath(seg_path, seg_data)
            # segment.segment_data = seg_data

    def refresh_from_translator(self):
        path_item, segments = self.translator.to_qpath()
        for seg_item, new_path in zip(self.segments, segments):
            seg_item.setPath(new_path)

class Quil2VecCanvasScene(QGraphicsScene):
    def __init__(self, parent):
        parent = parent
        super().__init__()
        self.layers = {}
        self.active_layer = None  # Current working layer as dict key in layers dictionary

    def drawBackground(self, painter: QPainter, rect: QRectF):
        painter.fillRect(rect, QColor("white"))

    def fromFile(self, parent):
        # outself = self(parent)
        curPage = parent.file.getCurrentPage() 
        # curPage:Quill2VecPage
        for layer in curPage.layers.items():
            self.layers[layer[0]] = layer[1]
            if layer[1].active:
                self.active_layer = layer[0]
        self.update()
        # return outself

    def add_layer(self, name="New Layer"):
        # default active layer to the newly created layer 
        self.active_layer = name
        layer = Quill2VecFileLayer(name)
        self.layers.append(layer)
        if not self.active_layer:
            self.active_layer[name] = layer  # Set the first layer as active

    def add_path_to_active_layer(self, vector_path):
        if self.active_layer:
            self.active_layer.add_path(vector_path)
            path_item = Quil2VecQPathItem(vector_path)
            self.addItem(path_item)  # Add to scene for rendering

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
        for path in actLayer.paths:
            path:Quil2VecVectorPath
            # qpath = Quil2VecQPathItem(path)
            self.addItem(Quil2VecQPathItem(path))

    def mousePressEvent(self, event):
        # Get the item under the mouse
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
        # Pass event to base class to handle item selection normally
        super().mousePressEvent(event)

debug_mode = {
    "show_hitboxes": False,
    "disable_path_shape": False,
}

def toggle_debug_hitboxes(scene):
    debug_mode["show_hitboxes"] = not debug_mode["show_hitboxes"]
    logger.info(f"Debug hitboxes {'ON' if debug_mode['show_hitboxes'] else 'OFF'}")
    for item in scene.items():
        if isinstance(item, Quil2VecQPathItem):
            item.toggle_debug_hitboxes(debug_mode["show_hitboxes"])

def toggle_path_shape_disable(scene):
    debug_mode["disable_path_shape"] = not debug_mode["disable_path_shape"]
    logger.info(f"Path shape blocking {'DISABLED' if debug_mode['disable_path_shape'] else 'ENABLED'}")
    for item in scene.items():
        if isinstance(item, Quil2VecQPathItem):
            item.toggle_debug_disable_shape(debug_mode["disable_path_shape"])

