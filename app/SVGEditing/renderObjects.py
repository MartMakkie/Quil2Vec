###############################################
# Qt Implementation of Tool sensitive Classes #
###############################################
from PySide6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsObject
from PySide6.QtGui import QPainterPath
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphics
from PySide6.QtCore import QPointF, QRect

from FileHandling.fileHandler import Quil2VecVectorPath
from Quil2VecGlobals import *

class Quil2VecQEditPoint(QGraphicsItem):
    pass

class Quil2VecQControlPoint(Quil2VecQEditPoint, QGraphicsEllipseItem):
    pass

class Quil2VecQAncherPoint(Quil2VecQEditPoint, QRect):
    pass

class Quil2VecQSegmentItem(QGraphicsPathItem):
    def __init__(self, segment_data, parent_path, index):
        self.segment_data = segment_data
        self.parent_path = parent_path
        self.index = index

        self.control_points = []
        self.control_lines = []
        self.control_points_visible = False
        self._hovered = False
        self._path_selected = False
        self._active = False

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(1)


class Quil2VecQPathItem(QGraphicsPathItem):
    def __init__(self, translator:Quil2VecVectorPath, index, parentCanvas, parent = None):
        super().__init__(parent)
        self.toolActive:toolModes = None
        self.index = index
        self.parentCanvas = parentCanvas
        self.translator = translator
        self._path, self.segment_data = self.translator.to_qpath()
        self.setPath(self._path)
        self.activeSegment = None
        # self.path_visual = QGraphicsPathItem(self.path, parent=self)
        # self.path_visual.setBrush(globalDefaultBrush)
        # self.path_visual.setPen(globalDefaultPen)
        self.setBrush(globalDefaultBrush)
        self.setPen(globalDefaultPen)
        self.setFlag(QGraphicsObject.ItemIsSelectable, True)
        self.setFlag(QGraphicsObject.ItemIsFocusable, True)
        # self.setFlag(QGraphicsObject.ItemHasNoContents, True)
        self.setAcceptHoverEvents(True)
        self.segments = []
        self.setToolMode()

    ######################################
    # General Property related functions #
    ######################################

    def boundingRect(self):
        return self.path_visual.boundingRect().adjusted(-3, -3, 3, 3)
    
    def shape(self):
        """Return shape if debug_disable_shape is False."""
        if self.debug_disable_shape or self.isSelected():
            return QPainterPath()  # Empty shape: does not intercept
        return self.path_visual.shape()
    
    def redraw(self):
        # Get updated path and segments from translator
        self._path, self.segment_data = self.translator.to_qpath()
        self.setPath(self._path)
        self.path_visual.setPath(self.path)

        for i, segment in enumerate(self.segments):
            seg_path, seg_data = self.segment_data[i]
            segment.setPath(seg_path, seg_data)
            # segment.segment_data = seg_data

    def refresh_from_translator(self):
        self._path, segments = self.translator.to_qpath()
        self.setPath(self._path)

        # segment_paths = self.translator.to_segment_paths()

        # self.shape_item.setPath(full_path)
        for seg_item, new_path in zip(self.segments, segments):
            seg_item.setPath(new_path)
    
    ################
    # Mouse events #
    ################

    def mousePressEvent(self, event):
        if self.toolActive == "qTransformMode":
            self.setupSegmentsForCpEdit()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def hoverEnterEvent(self, event):
        if self.toolActive == "qTransformMode":
            self.setPen(globalHoverPen)
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.setPen(globalDefaultPen)
        super().hoverLeaveEvent(event)

    ###########################################################################################
    # Transform mode prep -> setup and delete segments                                        #
    # Segements should be created upon mouse hover                                            #
    # Segments should get deleted agian when the toolmode is switched away from transformmode #
    ###########################################################################################

    def setupSegmentsForTransformMode(self):
        for i, _seg in enumerate(self.segment_data):
            seg_path, seg_data = _seg
            segment = Quil2VecQSegmentItem(seg_path, seg_data, i, self)
            # logger.info(str((seg_path, seg_data, i)))
            segment.setParentItem(self)
            # self.scene().addItem(segment)
            self.segments.append(segment)

    def removeSegmentsForTransformMode(self):
        # for seg in self.segments:
        pass
         
class selectionPoint(QGraphicsEllipseItem):
    def __init__(self, pos: QPointF, parent = None, radius = 5):
        pass