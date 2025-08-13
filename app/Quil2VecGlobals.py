from PySide6.QtGui import QPainterPath, QPen, QBrush, QColor
from PySide6.QtCore import Qt
from typing import List, Literal, Dict


globalDefaultPen = QPen(QColor("black"), 0)

globalDefaultBrush =QBrush(QColor("black"))

globalHoverPen = QPen(QColor("yellow"),1)#(255, 0, 0, 127), 1, )

globalSelectPen = QPen(QColor("red"), 1, Qt.DashLine)

# toolModes = Literal["qGroupMove", "qCpEdit", "qSegCut"]
toolModes = Literal["qCuttingMode", "qTransformMode", "qNavmode", "qBaseMode"