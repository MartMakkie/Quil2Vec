# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QToolBar, QWidget)

class Ui_qMainWindow(object):
    def setupUi(self, qMainWindow):
        if not qMainWindow.objectName():
            qMainWindow.setObjectName(u"qMainWindow")
        qMainWindow.resize(1023, 1135)
        self.actionOpen = QAction(qMainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(qMainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(qMainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionExport = QAction(qMainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.toolBar = QToolBar(qMainWindow)
        self.toolBar.setObjectName(u"toolBar")
        qMainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.menuBar = QMenuBar(qMainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1023, 24))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        qMainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionExport)

        self.retranslateUi(qMainWindow)

        QMetaObject.connectSlotsByName(qMainWindow)
    # setupUi

    def retranslateUi(self, qMainWindow):
        qMainWindow.setWindowTitle(QCoreApplication.translate("qMainWindow", u"qMainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("qMainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("qMainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("qMainWindow", u"Save As", None))
        self.actionExport.setText(QCoreApplication.translate("qMainWindow", u"Export", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("qMainWindow", u"toolBar", None))
        self.menuFile.setTitle(QCoreApplication.translate("qMainWindow", u"File", None))
    # retranslateUi

