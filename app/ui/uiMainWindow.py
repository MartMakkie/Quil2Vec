# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGraphicsView,
    QGridLayout, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QStatusBar, QToolBar,
    QToolBox, QVBoxLayout, QWidget)
import Resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1758, 1197)
        MainWindow.setDocumentMode(False)
        self.actionopen = QAction(MainWindow)
        self.actionopen.setObjectName(u"actionopen")
        self.actionopen.setEnabled(True)
        self.actionsave = QAction(MainWindow)
        self.actionsave.setObjectName(u"actionsave")
        self.actionclose = QAction(MainWindow)
        self.actionclose.setObjectName(u"actionclose")
        self.actioncopy = QAction(MainWindow)
        self.actioncopy.setObjectName(u"actioncopy")
        self.actioncut = QAction(MainWindow)
        self.actioncut.setObjectName(u"actioncut")
        self.actionpaste = QAction(MainWindow)
        self.actionpaste.setObjectName(u"actionpaste")
        self.actionundo = QAction(MainWindow)
        self.actionundo.setObjectName(u"actionundo")
        self.actionredo = QAction(MainWindow)
        self.actionredo.setObjectName(u"actionredo")
        self.actionsave_as = QAction(MainWindow)
        self.actionsave_as.setObjectName(u"actionsave_as")
        self.actionimage = QAction(MainWindow)
        self.actionimage.setObjectName(u"actionimage")
        self.actionIIIF = QAction(MainWindow)
        self.actionIIIF.setObjectName(u"actionIIIF")
        self.actiondemo_object = QAction(MainWindow)
        self.actiondemo_object.setObjectName(u"actiondemo_object")
        self.actionsave_as_demo_object = QAction(MainWindow)
        self.actionsave_as_demo_object.setObjectName(u"actionsave_as_demo_object")
        self.actionSelect = QAction(MainWindow)
        self.actionSelect.setObjectName(u"actionSelect")
        self.actionSelect.setCheckable(True)
        self.actionPath_Cutter = QAction(MainWindow)
        self.actionPath_Cutter.setObjectName(u"actionPath_Cutter")
        self.actionPath_Cutter.setCheckable(True)
        self.actionMove = QAction(MainWindow)
        self.actionMove.setObjectName(u"actionMove")
        self.actionMove.setCheckable(True)
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionPath_editor = QAction(MainWindow)
        self.actionPath_editor.setObjectName(u"actionPath_editor")
        self.actionPath_editor.setCheckable(True)
        self.actionGroup = QAction(MainWindow)
        self.actionGroup.setObjectName(u"actionGroup")
        self.actionUngroup = QAction(MainWindow)
        self.actionUngroup.setObjectName(u"actionUngroup")
        self.actionAdd_Line_Path = QAction(MainWindow)
        self.actionAdd_Line_Path.setObjectName(u"actionAdd_Line_Path")
        self.actionAdd_Curve_Path = QAction(MainWindow)
        self.actionAdd_Curve_Path.setObjectName(u"actionAdd_Curve_Path")
        self.actionDelete_2 = QAction(MainWindow)
        self.actionDelete_2.setObjectName(u"actionDelete_2")
        self.actionSave_selected_object_as_demo_object = QAction(MainWindow)
        self.actionSave_selected_object_as_demo_object.setObjectName(u"actionSave_selected_object_as_demo_object")
        self.actionZoom_in = QAction(MainWindow)
        self.actionZoom_in.setObjectName(u"actionZoom_in")
        self.actionZoom_out = QAction(MainWindow)
        self.actionZoom_out.setObjectName(u"actionZoom_out")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.toolBox = QToolBox(self.centralwidget)
        self.toolBox.setObjectName(u"toolBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.Layers = QWidget()
        self.Layers.setObjectName(u"Layers")
        self.Layers.setGeometry(QRect(0, 0, 409, 1030))
        self.LayersGridLayout = QGridLayout(self.Layers)
        self.LayersGridLayout.setObjectName(u"LayersGridLayout")
        self.LayersScrollArea = QScrollArea(self.Layers)
        self.LayersScrollArea.setObjectName(u"LayersScrollArea")
        self.LayersScrollArea.setWidgetResizable(True)
        self.LayersScrollAreaContent = QWidget()
        self.LayersScrollAreaContent.setObjectName(u"LayersScrollAreaContent")
        self.LayersScrollAreaContent.setGeometry(QRect(0, 0, 383, 1004))
        self.verticalLayout_3 = QVBoxLayout(self.LayersScrollAreaContent)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.LayerGridLayout = QGridLayout()
        self.LayerGridLayout.setObjectName(u"LayerGridLayout")
        self.DemoObjectLayerLayout = QGridLayout()
        self.DemoObjectLayerLayout.setObjectName(u"DemoObjectLayerLayout")
        self.DemoObjectLayerPreview = QGraphicsView(self.LayersScrollAreaContent)
        self.DemoObjectLayerPreview.setObjectName(u"DemoObjectLayerPreview")

        self.DemoObjectLayerLayout.addWidget(self.DemoObjectLayerPreview, 0, 0, 1, 1)

        self.DemoObjectVisibilityCheckbox = QCheckBox(self.LayersScrollAreaContent)
        self.DemoObjectVisibilityCheckbox.setObjectName(u"DemoObjectVisibilityCheckbox")

        self.DemoObjectLayerLayout.addWidget(self.DemoObjectVisibilityCheckbox, 0, 1, 1, 1)


        self.LayerGridLayout.addLayout(self.DemoObjectLayerLayout, 0, 0, 1, 1)

        self.DemoObjectOpacitySlider = QSlider(self.LayersScrollAreaContent)
        self.DemoObjectOpacitySlider.setObjectName(u"DemoObjectOpacitySlider")
        self.DemoObjectOpacitySlider.setOrientation(Qt.Horizontal)

        self.LayerGridLayout.addWidget(self.DemoObjectOpacitySlider, 1, 0, 1, 1)

        self.LayerDemoObjectLabel = QLabel(self.LayersScrollAreaContent)
        self.LayerDemoObjectLabel.setObjectName(u"LayerDemoObjectLabel")

        self.LayerGridLayout.addWidget(self.LayerDemoObjectLabel, 2, 0, 1, 1)

        self.PathLayerLayout = QHBoxLayout()
        self.PathLayerLayout.setObjectName(u"PathLayerLayout")
        self.PathsLayerPreview = QGraphicsView(self.LayersScrollAreaContent)
        self.PathsLayerPreview.setObjectName(u"PathsLayerPreview")

        self.PathLayerLayout.addWidget(self.PathsLayerPreview)

        self.PathsVisibilityCheckbox = QCheckBox(self.LayersScrollAreaContent)
        self.PathsVisibilityCheckbox.setObjectName(u"PathsVisibilityCheckbox")

        self.PathLayerLayout.addWidget(self.PathsVisibilityCheckbox)


        self.LayerGridLayout.addLayout(self.PathLayerLayout, 3, 0, 1, 1)

        self.PathsOpacitySlider = QSlider(self.LayersScrollAreaContent)
        self.PathsOpacitySlider.setObjectName(u"PathsOpacitySlider")
        self.PathsOpacitySlider.setOrientation(Qt.Horizontal)

        self.LayerGridLayout.addWidget(self.PathsOpacitySlider, 4, 0, 1, 1)

        self.IndividualPathsLayerLabel = QLabel(self.LayersScrollAreaContent)
        self.IndividualPathsLayerLabel.setObjectName(u"IndividualPathsLayerLabel")

        self.LayerGridLayout.addWidget(self.IndividualPathsLayerLabel, 5, 0, 1, 1)

        self.VectorGroupLayerLayout = QHBoxLayout()
        self.VectorGroupLayerLayout.setObjectName(u"VectorGroupLayerLayout")
        self.VectorGroupsLayerPreview = QGraphicsView(self.LayersScrollAreaContent)
        self.VectorGroupsLayerPreview.setObjectName(u"VectorGroupsLayerPreview")

        self.VectorGroupLayerLayout.addWidget(self.VectorGroupsLayerPreview)

        self.VectorGroupsVisibilityCheckbox = QCheckBox(self.LayersScrollAreaContent)
        self.VectorGroupsVisibilityCheckbox.setObjectName(u"VectorGroupsVisibilityCheckbox")

        self.VectorGroupLayerLayout.addWidget(self.VectorGroupsVisibilityCheckbox)


        self.LayerGridLayout.addLayout(self.VectorGroupLayerLayout, 6, 0, 1, 1)

        self.VectorGroupsOpacitySlider = QSlider(self.LayersScrollAreaContent)
        self.VectorGroupsOpacitySlider.setObjectName(u"VectorGroupsOpacitySlider")
        self.VectorGroupsOpacitySlider.setOrientation(Qt.Horizontal)

        self.LayerGridLayout.addWidget(self.VectorGroupsOpacitySlider, 7, 0, 1, 1)

        self.VectorGroupLayerLabel = QLabel(self.LayersScrollAreaContent)
        self.VectorGroupLayerLabel.setObjectName(u"VectorGroupLayerLabel")

        self.LayerGridLayout.addWidget(self.VectorGroupLayerLabel, 8, 0, 1, 1)

        self.FullVectorLayerLayout = QHBoxLayout()
        self.FullVectorLayerLayout.setObjectName(u"FullVectorLayerLayout")
        self.FullVectorLayerPreview = QGraphicsView(self.LayersScrollAreaContent)
        self.FullVectorLayerPreview.setObjectName(u"FullVectorLayerPreview")

        self.FullVectorLayerLayout.addWidget(self.FullVectorLayerPreview)

        self.FullVectorVisibilityCheckbox = QCheckBox(self.LayersScrollAreaContent)
        self.FullVectorVisibilityCheckbox.setObjectName(u"FullVectorVisibilityCheckbox")

        self.FullVectorLayerLayout.addWidget(self.FullVectorVisibilityCheckbox)


        self.LayerGridLayout.addLayout(self.FullVectorLayerLayout, 9, 0, 1, 1)

        self.FullVectorOpacitySlider = QSlider(self.LayersScrollAreaContent)
        self.FullVectorOpacitySlider.setObjectName(u"FullVectorOpacitySlider")
        self.FullVectorOpacitySlider.setOrientation(Qt.Horizontal)

        self.LayerGridLayout.addWidget(self.FullVectorOpacitySlider, 10, 0, 1, 1)

        self.FullVectorLayoutLabel = QLabel(self.LayersScrollAreaContent)
        self.FullVectorLayoutLabel.setObjectName(u"FullVectorLayoutLabel")

        self.LayerGridLayout.addWidget(self.FullVectorLayoutLabel, 11, 0, 1, 1)

        self.OriginalImageLayerLayout = QHBoxLayout()
        self.OriginalImageLayerLayout.setObjectName(u"OriginalImageLayerLayout")
        self.OriginalImageLayerPreview = QGraphicsView(self.LayersScrollAreaContent)
        self.OriginalImageLayerPreview.setObjectName(u"OriginalImageLayerPreview")

        self.OriginalImageLayerLayout.addWidget(self.OriginalImageLayerPreview)

        self.OriginalImageVisibilityCheckbox = QCheckBox(self.LayersScrollAreaContent)
        self.OriginalImageVisibilityCheckbox.setObjectName(u"OriginalImageVisibilityCheckbox")

        self.OriginalImageLayerLayout.addWidget(self.OriginalImageVisibilityCheckbox)


        self.LayerGridLayout.addLayout(self.OriginalImageLayerLayout, 12, 0, 1, 1)

        self.OriginalImageOpacitySlider = QSlider(self.LayersScrollAreaContent)
        self.OriginalImageOpacitySlider.setObjectName(u"OriginalImageOpacitySlider")
        self.OriginalImageOpacitySlider.setOrientation(Qt.Horizontal)

        self.LayerGridLayout.addWidget(self.OriginalImageOpacitySlider, 13, 0, 1, 1)

        self.OriginalImageLayerLabel = QLabel(self.LayersScrollAreaContent)
        self.OriginalImageLayerLabel.setObjectName(u"OriginalImageLayerLabel")

        self.LayerGridLayout.addWidget(self.OriginalImageLayerLabel, 14, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.BackgroundLayerPreview = QGraphicsView(self.LayersScrollAreaContent)
        self.BackgroundLayerPreview.setObjectName(u"BackgroundLayerPreview")

        self.horizontalLayout_2.addWidget(self.BackgroundLayerPreview)

        self.BackgroundVisibilityCheckbox = QCheckBox(self.LayersScrollAreaContent)
        self.BackgroundVisibilityCheckbox.setObjectName(u"BackgroundVisibilityCheckbox")

        self.horizontalLayout_2.addWidget(self.BackgroundVisibilityCheckbox)


        self.LayerGridLayout.addLayout(self.horizontalLayout_2, 15, 0, 1, 1)

        self.BackgroundComboBox = QComboBox(self.LayersScrollAreaContent)
        self.BackgroundComboBox.addItem("")
        self.BackgroundComboBox.addItem("")
        self.BackgroundComboBox.addItem("")
        self.BackgroundComboBox.addItem("")
        self.BackgroundComboBox.setObjectName(u"BackgroundComboBox")

        self.LayerGridLayout.addWidget(self.BackgroundComboBox, 16, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.LayerGridLayout)

        self.LayersScrollArea.setWidget(self.LayersScrollAreaContent)

        self.LayersGridLayout.addWidget(self.LayersScrollArea, 0, 0, 1, 1)

        self.toolBox.addItem(self.Layers, u"Layers")
        self.PageNav = QWidget()
        self.PageNav.setObjectName(u"PageNav")
        self.PageNav.setGeometry(QRect(0, 0, 248, 1030))
        self.gridLayout_2 = QGridLayout(self.PageNav)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.PageNavScrollArea = QScrollArea(self.PageNav)
        self.PageNavScrollArea.setObjectName(u"PageNavScrollArea")
        self.PageNavScrollArea.setWidgetResizable(True)
        self.PageNavScrollAreaWidgetContents = QWidget()
        self.PageNavScrollAreaWidgetContents.setObjectName(u"PageNavScrollAreaWidgetContents")
        self.PageNavScrollAreaWidgetContents.setGeometry(QRect(0, 0, 222, 1004))
        self.PagesGridLayout = QGridLayout(self.PageNavScrollAreaWidgetContents)
        self.PagesGridLayout.setObjectName(u"PagesGridLayout")
        self.label_2 = QLabel(self.PageNavScrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.PagesGridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.pushButton = QPushButton(self.PageNavScrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")

        self.PagesGridLayout.addWidget(self.pushButton, 0, 0, 1, 1)

        self.PageNavScrollArea.setWidget(self.PageNavScrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.PageNavScrollArea, 0, 0, 1, 1)

        self.toolBox.addItem(self.PageNav, u"Page Navigator")

        self.horizontalLayout_3.addWidget(self.toolBox)

        self.SVGScrollArea = QScrollArea(self.centralwidget)
        self.SVGScrollArea.setObjectName(u"SVGScrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SVGScrollArea.sizePolicy().hasHeightForWidth())
        self.SVGScrollArea.setSizePolicy(sizePolicy1)
        self.SVGScrollArea.setMinimumSize(QSize(0, 0))
        self.SVGScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1484, 1096))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.svgView = QGraphicsView(self.scrollAreaWidgetContents)
        self.svgView.setObjectName(u"svgView")

        self.gridLayout_3.addWidget(self.svgView, 0, 1, 1, 1)

        self.SVGScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.SVGScrollArea)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1758, 24))
        self.menufile = QMenu(self.menubar)
        self.menufile.setObjectName(u"menufile")
        self.menuedit = QMenu(self.menubar)
        self.menuedit.setObjectName(u"menuedit")
        self.menuimport = QMenu(self.menubar)
        self.menuimport.setObjectName(u"menuimport")
        self.menuExport = QMenu(self.menubar)
        self.menuExport.setObjectName(u"menuExport")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        QWidget.setTabOrder(self.SVGScrollArea, self.BackgroundLayerPreview)

        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuedit.menuAction())
        self.menubar.addAction(self.menuimport.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menufile.addAction(self.actionopen)
        self.menufile.addAction(self.actionsave)
        self.menufile.addAction(self.actionsave_as)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionclose)
        self.menuedit.addAction(self.actioncopy)
        self.menuedit.addAction(self.actioncut)
        self.menuedit.addAction(self.actionpaste)
        self.menuedit.addSeparator()
        self.menuedit.addAction(self.actionundo)
        self.menuedit.addAction(self.actionredo)
        self.menuimport.addAction(self.actionimage)
        self.menuimport.addAction(self.actionIIIF)
        self.menuimport.addSeparator()
        self.menuimport.addAction(self.actiondemo_object)
        self.toolBar.addAction(self.actionSelect)
        self.toolBar.addAction(self.actionPath_Cutter)
        self.toolBar.addAction(self.actionMove)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionRedo)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPath_editor)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGroup)
        self.toolBar.addAction(self.actionUngroup)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAdd_Line_Path)
        self.toolBar.addAction(self.actionAdd_Curve_Path)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave_selected_object_as_demo_object)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoom_in)
        self.toolBar.addAction(self.actionZoom_out)

        self.retranslateUi(MainWindow)

        self.toolBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionopen.setText(QCoreApplication.translate("MainWindow", u"open", None))
        self.actionsave.setText(QCoreApplication.translate("MainWindow", u"save", None))
        self.actionclose.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.actioncopy.setText(QCoreApplication.translate("MainWindow", u"copy", None))
        self.actioncut.setText(QCoreApplication.translate("MainWindow", u"cut", None))
        self.actionpaste.setText(QCoreApplication.translate("MainWindow", u"paste", None))
        self.actionundo.setText(QCoreApplication.translate("MainWindow", u"undo", None))
        self.actionredo.setText(QCoreApplication.translate("MainWindow", u"redo", None))
        self.actionsave_as.setText(QCoreApplication.translate("MainWindow", u"save as", None))
        self.actionimage.setText(QCoreApplication.translate("MainWindow", u"image", None))
        self.actionIIIF.setText(QCoreApplication.translate("MainWindow", u"IIIF", None))
        self.actiondemo_object.setText(QCoreApplication.translate("MainWindow", u"demo object", None))
        self.actionsave_as_demo_object.setText(QCoreApplication.translate("MainWindow", u"save as demo object", None))
        self.actionSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
#if QT_CONFIG(tooltip)
        self.actionSelect.setToolTip(QCoreApplication.translate("MainWindow", u"Select Tpp;", None))
#endif // QT_CONFIG(tooltip)
        self.actionPath_Cutter.setText(QCoreApplication.translate("MainWindow", u"Path Cutter", None))
#if QT_CONFIG(tooltip)
        self.actionPath_Cutter.setToolTip(QCoreApplication.translate("MainWindow", u"Used to cut a vector path", None))
#endif // QT_CONFIG(tooltip)
        self.actionMove.setText(QCoreApplication.translate("MainWindow", u"Move", None))
#if QT_CONFIG(tooltip)
        self.actionMove.setToolTip(QCoreApplication.translate("MainWindow", u"Move selected object", None))
#endif // QT_CONFIG(tooltip)
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(tooltip)
        self.actionDelete.setToolTip(QCoreApplication.translate("MainWindow", u"Delete Object", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionDelete.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
#if QT_CONFIG(tooltip)
        self.actionUndo.setToolTip(QCoreApplication.translate("MainWindow", u"Undo", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("MainWindow", u"Meta+Z, Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
#if QT_CONFIG(tooltip)
        self.actionRedo.setToolTip(QCoreApplication.translate("MainWindow", u"Redo action", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("MainWindow", u"Meta+Shift+Z, Meta+Ctrl+Shift+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionPath_editor.setText(QCoreApplication.translate("MainWindow", u"Path editor", None))
#if QT_CONFIG(tooltip)
        self.actionPath_editor.setToolTip(QCoreApplication.translate("MainWindow", u"Switch to Path Editing Mode", None))
#endif // QT_CONFIG(tooltip)
        self.actionGroup.setText(QCoreApplication.translate("MainWindow", u"Group", None))
#if QT_CONFIG(tooltip)
        self.actionGroup.setToolTip(QCoreApplication.translate("MainWindow", u"Group Selected Paths to new Object", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionGroup.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+G, Meta+G", None))
#endif // QT_CONFIG(shortcut)
        self.actionUngroup.setText(QCoreApplication.translate("MainWindow", u"Ungroup", None))
#if QT_CONFIG(tooltip)
        self.actionUngroup.setToolTip(QCoreApplication.translate("MainWindow", u"Ungroup selected object to individual Paths", None))
#endif // QT_CONFIG(tooltip)
        self.actionAdd_Line_Path.setText(QCoreApplication.translate("MainWindow", u"Add Line Path", None))
#if QT_CONFIG(tooltip)
        self.actionAdd_Line_Path.setToolTip(QCoreApplication.translate("MainWindow", u"Add a new line vector path", None))
#endif // QT_CONFIG(tooltip)
        self.actionAdd_Curve_Path.setText(QCoreApplication.translate("MainWindow", u"Add Curve Path", None))
#if QT_CONFIG(tooltip)
        self.actionAdd_Curve_Path.setToolTip(QCoreApplication.translate("MainWindow", u"Add new Cubic Bezier Curve vector path", None))
#endif // QT_CONFIG(tooltip)
        self.actionDelete_2.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionSave_selected_object_as_demo_object.setText(QCoreApplication.translate("MainWindow", u"Save selected object as demo object", None))
#if QT_CONFIG(tooltip)
        self.actionSave_selected_object_as_demo_object.setToolTip(QCoreApplication.translate("MainWindow", u"Save selected object as demo object", None))
#endif // QT_CONFIG(tooltip)
        self.actionZoom_in.setText(QCoreApplication.translate("MainWindow", u"Zoom in", None))
#if QT_CONFIG(tooltip)
        self.actionZoom_in.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom In", None))
#endif // QT_CONFIG(tooltip)
        self.actionZoom_out.setText(QCoreApplication.translate("MainWindow", u"Zoom out", None))
#if QT_CONFIG(tooltip)
        self.actionZoom_out.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom Out", None))
#endif // QT_CONFIG(tooltip)
        self.DemoObjectVisibilityCheckbox.setText(QCoreApplication.translate("MainWindow", u"Visible", None))
        self.LayerDemoObjectLabel.setText(QCoreApplication.translate("MainWindow", u"Demo Objects", None))
        self.PathsVisibilityCheckbox.setText(QCoreApplication.translate("MainWindow", u"Visible", None))
        self.IndividualPathsLayerLabel.setText(QCoreApplication.translate("MainWindow", u"Individual Paths", None))
        self.VectorGroupsVisibilityCheckbox.setText(QCoreApplication.translate("MainWindow", u"Visible", None))
        self.VectorGroupLayerLabel.setText(QCoreApplication.translate("MainWindow", u"Vector Groups", None))
        self.FullVectorVisibilityCheckbox.setText(QCoreApplication.translate("MainWindow", u"Visible", None))
        self.FullVectorLayoutLabel.setText(QCoreApplication.translate("MainWindow", u"Full Vector", None))
        self.OriginalImageVisibilityCheckbox.setText(QCoreApplication.translate("MainWindow", u"Visible", None))
        self.OriginalImageLayerLabel.setText(QCoreApplication.translate("MainWindow", u"Original Image", None))
        self.BackgroundVisibilityCheckbox.setText(QCoreApplication.translate("MainWindow", u"Visible", None))
        self.BackgroundComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Blue Grid", None))
        self.BackgroundComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"White Grid", None))
        self.BackgroundComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Grey Grid", None))
        self.BackgroundComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"White", None))

        self.toolBox.setItemText(self.toolBox.indexOf(self.Layers), QCoreApplication.translate("MainWindow", u"Layers", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.PageNav), QCoreApplication.translate("MainWindow", u"Page Navigator", None))
        self.menufile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuedit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menuimport.setTitle(QCoreApplication.translate("MainWindow", u"&Import", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

