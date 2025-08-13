# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_image_popup.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGraphicsView, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QScrollArea, QScrollBar, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QToolButton, QVBoxLayout,
    QWidget)

class Ui_importImageWindow(object):
    def setupUi(self, importImageWindow):
        if not importImageWindow.objectName():
            importImageWindow.setObjectName(u"importImageWindow")
        importImageWindow.resize(950, 678)
        self.verticalLayoutWidget = QWidget(importImageWindow)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 951, 681))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formLayout.setHorizontalSpacing(0)
        self.formLayout.setVerticalSpacing(0)
        self.projectNameLabel = QLabel(self.verticalLayoutWidget)
        self.projectNameLabel.setObjectName(u"projectNameLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectNameLabel.sizePolicy().hasHeightForWidth())
        self.projectNameLabel.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.projectNameLabel)

        self.ProjectNameLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.ProjectNameLineEdit.setObjectName(u"ProjectNameLineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(24)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ProjectNameLineEdit.sizePolicy().hasHeightForWidth())
        self.ProjectNameLineEdit.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ProjectNameLineEdit)

        self.ImageNameLabel = QLabel(self.verticalLayoutWidget)
        self.ImageNameLabel.setObjectName(u"ImageNameLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ImageNameLabel.sizePolicy().hasHeightForWidth())
        self.ImageNameLabel.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.ImageNameLabel)

        self.ImageNameLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.ImageNameLineEdit.setObjectName(u"ImageNameLineEdit")
        sizePolicy1.setHeightForWidth(self.ImageNameLineEdit.sizePolicy().hasHeightForWidth())
        self.ImageNameLineEdit.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ImageNameLineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.PreviewImageGraphicsView = QGraphicsView(self.verticalLayoutWidget)
        self.PreviewImageGraphicsView.setObjectName(u"PreviewImageGraphicsView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(5)
        sizePolicy3.setVerticalStretch(100)
        sizePolicy3.setHeightForWidth(self.PreviewImageGraphicsView.sizePolicy().hasHeightForWidth())
        self.PreviewImageGraphicsView.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.PreviewImageGraphicsView, 0, 1, 1, 1)

        self.OriginalImageLabel = QLabel(self.verticalLayoutWidget)
        self.OriginalImageLabel.setObjectName(u"OriginalImageLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.OriginalImageLabel.sizePolicy().hasHeightForWidth())
        self.OriginalImageLabel.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.OriginalImageLabel, 1, 1, 1, 1)

        self.BinarizedImageLabel = QLabel(self.verticalLayoutWidget)
        self.BinarizedImageLabel.setObjectName(u"BinarizedImageLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.BinarizedImageLabel.sizePolicy().hasHeightForWidth())
        self.BinarizedImageLabel.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.BinarizedImageLabel, 1, 3, 1, 1)

        self.BinarizedPreviewGraphicsView = QGraphicsView(self.verticalLayoutWidget)
        self.BinarizedPreviewGraphicsView.setObjectName(u"BinarizedPreviewGraphicsView")
        sizePolicy3.setHeightForWidth(self.BinarizedPreviewGraphicsView.sizePolicy().hasHeightForWidth())
        self.BinarizedPreviewGraphicsView.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        self.BinarizedPreviewGraphicsView.setFont(font)

        self.gridLayout.addWidget(self.BinarizedPreviewGraphicsView, 0, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.PresetHorizontalLayout = QHBoxLayout()
        self.PresetHorizontalLayout.setObjectName(u"PresetHorizontalLayout")
        self.LoadPresetButton = QPushButton(self.verticalLayoutWidget)
        self.LoadPresetButton.setObjectName(u"LoadPresetButton")

        self.PresetHorizontalLayout.addWidget(self.LoadPresetButton)

        self.SavePresetButton = QPushButton(self.verticalLayoutWidget)
        self.SavePresetButton.setObjectName(u"SavePresetButton")

        self.PresetHorizontalLayout.addWidget(self.SavePresetButton)

        self.PreviewButton = QPushButton(self.verticalLayoutWidget)
        self.PreviewButton.setObjectName(u"PreviewButton")

        self.PresetHorizontalLayout.addWidget(self.PreviewButton)


        self.verticalLayout.addLayout(self.PresetHorizontalLayout)

        self.SettingsLayout = QGridLayout()
        self.SettingsLayout.setObjectName(u"SettingsLayout")
        self.PageNavLayout = QHBoxLayout()
        self.PageNavLayout.setObjectName(u"PageNavLayout")
        self.PreviousPageButton = QToolButton(self.verticalLayoutWidget)
        self.PreviousPageButton.setObjectName(u"PreviousPageButton")
        self.PreviousPageButton.setArrowType(Qt.ArrowType.LeftArrow)

        self.PageNavLayout.addWidget(self.PreviousPageButton)

        self.PageScrollBar = QScrollBar(self.verticalLayoutWidget)
        self.PageScrollBar.setObjectName(u"PageScrollBar")
        self.PageScrollBar.setOrientation(Qt.Orientation.Horizontal)

        self.PageNavLayout.addWidget(self.PageScrollBar)

        self.pageSelectComboBox = QComboBox(self.verticalLayoutWidget)
        self.pageSelectComboBox.setObjectName(u"pageSelectComboBox")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(5)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pageSelectComboBox.sizePolicy().hasHeightForWidth())
        self.pageSelectComboBox.setSizePolicy(sizePolicy6)

        self.PageNavLayout.addWidget(self.pageSelectComboBox)

        self.bottomSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.PageNavLayout.addItem(self.bottomSpacer)

        self.NextPageButton = QToolButton(self.verticalLayoutWidget)
        self.NextPageButton.setObjectName(u"NextPageButton")
        self.NextPageButton.setArrowType(Qt.ArrowType.RightArrow)

        self.PageNavLayout.addWidget(self.NextPageButton)


        self.SettingsLayout.addLayout(self.PageNavLayout, 2, 0, 1, 1)

        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 945, 186))
        self.layoutWidget = QWidget(self.scrollAreaWidgetContents)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, -10, 931, 524))
        self.settingsGridLayout = QGridLayout(self.layoutWidget)
        self.settingsGridLayout.setObjectName(u"settingsGridLayout")
        self.settingsGridLayout.setContentsMargins(0, 0, 0, 0)
        self.TresholdCLayout = QGridLayout()
        self.TresholdCLayout.setObjectName(u"TresholdCLayout")
        self.TresholdCSlider = QSlider(self.layoutWidget)
        self.TresholdCSlider.setObjectName(u"TresholdCSlider")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(9)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.TresholdCSlider.sizePolicy().hasHeightForWidth())
        self.TresholdCSlider.setSizePolicy(sizePolicy7)
        self.TresholdCSlider.setMaximum(50)
        self.TresholdCSlider.setValue(11)
        self.TresholdCSlider.setSliderPosition(11)
        self.TresholdCSlider.setOrientation(Qt.Orientation.Horizontal)

        self.TresholdCLayout.addWidget(self.TresholdCSlider, 0, 0, 1, 1)

        self.TresholdCSpin = QSpinBox(self.layoutWidget)
        self.TresholdCSpin.setObjectName(u"TresholdCSpin")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(1)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.TresholdCSpin.sizePolicy().hasHeightForWidth())
        self.TresholdCSpin.setSizePolicy(sizePolicy8)
        self.TresholdCSpin.setMaximum(50)
        self.TresholdCSpin.setValue(11)

        self.TresholdCLayout.addWidget(self.TresholdCSpin, 0, 1, 1, 1)


        self.settingsGridLayout.addLayout(self.TresholdCLayout, 2, 2, 1, 1)

        self.TresholdCLabel = QLabel(self.layoutWidget)
        self.TresholdCLabel.setObjectName(u"TresholdCLabel")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.TresholdCLabel.sizePolicy().hasHeightForWidth())
        self.TresholdCLabel.setSizePolicy(sizePolicy9)

        self.settingsGridLayout.addWidget(self.TresholdCLabel, 2, 0, 1, 1)

        self.ApplyClaheCheckBox = QCheckBox(self.layoutWidget)
        self.ApplyClaheCheckBox.setObjectName(u"ApplyClaheCheckBox")
        self.ApplyClaheCheckBox.setMouseTracking(False)

        self.settingsGridLayout.addWidget(self.ApplyClaheCheckBox, 3, 0, 1, 1)

        self.CLAHEFormLayout = QFormLayout()
        self.CLAHEFormLayout.setObjectName(u"CLAHEFormLayout")
        self.CLAHEFormLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.ClaheClipLimitLabel = QLabel(self.layoutWidget)
        self.ClaheClipLimitLabel.setObjectName(u"ClaheClipLimitLabel")

        self.CLAHEFormLayout.setWidget(0, QFormLayout.LabelRole, self.ClaheClipLimitLabel)

        self.ClaheClipLimitDoubleSpinBox = QDoubleSpinBox(self.layoutWidget)
        self.ClaheClipLimitDoubleSpinBox.setObjectName(u"ClaheClipLimitDoubleSpinBox")
        self.ClaheClipLimitDoubleSpinBox.setEnabled(False)
        self.ClaheClipLimitDoubleSpinBox.setKeyboardTracking(True)
        self.ClaheClipLimitDoubleSpinBox.setDecimals(1)
        self.ClaheClipLimitDoubleSpinBox.setMinimum(1.000000000000000)
        self.ClaheClipLimitDoubleSpinBox.setMaximum(10.000000000000000)
        self.ClaheClipLimitDoubleSpinBox.setSingleStep(0.100000000000000)

        self.CLAHEFormLayout.setWidget(0, QFormLayout.FieldRole, self.ClaheClipLimitDoubleSpinBox)

        self.ClaheTileGridXLayout = QGridLayout()
        self.ClaheTileGridXLayout.setObjectName(u"ClaheTileGridXLayout")
        self.ClaheTileGridXLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.ClaheTileGridSizeXSpinBox = QSpinBox(self.layoutWidget)
        self.ClaheTileGridSizeXSpinBox.setObjectName(u"ClaheTileGridSizeXSpinBox")
        self.ClaheTileGridSizeXSpinBox.setEnabled(False)
        sizePolicy8.setHeightForWidth(self.ClaheTileGridSizeXSpinBox.sizePolicy().hasHeightForWidth())
        self.ClaheTileGridSizeXSpinBox.setSizePolicy(sizePolicy8)
        self.ClaheTileGridSizeXSpinBox.setKeyboardTracking(True)
        self.ClaheTileGridSizeXSpinBox.setMinimum(1)
        self.ClaheTileGridSizeXSpinBox.setMaximum(64)
        self.ClaheTileGridSizeXSpinBox.setValue(8)

        self.ClaheTileGridXLayout.addWidget(self.ClaheTileGridSizeXSpinBox, 0, 1, 1, 1)

        self.ClaheTileGridSizeXSlider = QSlider(self.layoutWidget)
        self.ClaheTileGridSizeXSlider.setObjectName(u"ClaheTileGridSizeXSlider")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(30)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.ClaheTileGridSizeXSlider.sizePolicy().hasHeightForWidth())
        self.ClaheTileGridSizeXSlider.setSizePolicy(sizePolicy10)
        self.ClaheTileGridSizeXSlider.setMinimum(1)
        self.ClaheTileGridSizeXSlider.setMaximum(64)
        self.ClaheTileGridSizeXSlider.setValue(8)
        self.ClaheTileGridSizeXSlider.setOrientation(Qt.Orientation.Horizontal)

        self.ClaheTileGridXLayout.addWidget(self.ClaheTileGridSizeXSlider, 0, 0, 1, 1)


        self.CLAHEFormLayout.setLayout(1, QFormLayout.FieldRole, self.ClaheTileGridXLayout)

        self.ClaheClipLimitYLabel = QLabel(self.layoutWidget)
        self.ClaheClipLimitYLabel.setObjectName(u"ClaheClipLimitYLabel")

        self.CLAHEFormLayout.setWidget(2, QFormLayout.LabelRole, self.ClaheClipLimitYLabel)

        self.ClaheTileGridYLayout = QGridLayout()
        self.ClaheTileGridYLayout.setObjectName(u"ClaheTileGridYLayout")
        self.ClaheTileGridSizeYSpinBox = QSpinBox(self.layoutWidget)
        self.ClaheTileGridSizeYSpinBox.setObjectName(u"ClaheTileGridSizeYSpinBox")
        self.ClaheTileGridSizeYSpinBox.setEnabled(False)
        sizePolicy8.setHeightForWidth(self.ClaheTileGridSizeYSpinBox.sizePolicy().hasHeightForWidth())
        self.ClaheTileGridSizeYSpinBox.setSizePolicy(sizePolicy8)
        self.ClaheTileGridSizeYSpinBox.setKeyboardTracking(True)
        self.ClaheTileGridSizeYSpinBox.setMinimum(1)
        self.ClaheTileGridSizeYSpinBox.setMaximum(64)
        self.ClaheTileGridSizeYSpinBox.setValue(8)

        self.ClaheTileGridYLayout.addWidget(self.ClaheTileGridSizeYSpinBox, 0, 1, 1, 1)

        self.ClaheTileGridSizeYSlider = QSlider(self.layoutWidget)
        self.ClaheTileGridSizeYSlider.setObjectName(u"ClaheTileGridSizeYSlider")
        sizePolicy10.setHeightForWidth(self.ClaheTileGridSizeYSlider.sizePolicy().hasHeightForWidth())
        self.ClaheTileGridSizeYSlider.setSizePolicy(sizePolicy10)
        self.ClaheTileGridSizeYSlider.setMinimum(1)
        self.ClaheTileGridSizeYSlider.setMaximum(64)
        self.ClaheTileGridSizeYSlider.setValue(8)
        self.ClaheTileGridSizeYSlider.setOrientation(Qt.Orientation.Horizontal)

        self.ClaheTileGridYLayout.addWidget(self.ClaheTileGridSizeYSlider, 0, 0, 1, 1)


        self.CLAHEFormLayout.setLayout(2, QFormLayout.FieldRole, self.ClaheTileGridYLayout)

        self.ClaheClipLimitXLabel = QLabel(self.layoutWidget)
        self.ClaheClipLimitXLabel.setObjectName(u"ClaheClipLimitXLabel")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.ClaheClipLimitXLabel.sizePolicy().hasHeightForWidth())
        self.ClaheClipLimitXLabel.setSizePolicy(sizePolicy11)

        self.CLAHEFormLayout.setWidget(1, QFormLayout.LabelRole, self.ClaheClipLimitXLabel)


        self.settingsGridLayout.addLayout(self.CLAHEFormLayout, 3, 2, 1, 1)

        self.ThresholdBlockLayout = QGridLayout()
        self.ThresholdBlockLayout.setObjectName(u"ThresholdBlockLayout")
        self.ThresholdBlockSizeSlider = QSlider(self.layoutWidget)
        self.ThresholdBlockSizeSlider.setObjectName(u"ThresholdBlockSizeSlider")
        sizePolicy7.setHeightForWidth(self.ThresholdBlockSizeSlider.sizePolicy().hasHeightForWidth())
        self.ThresholdBlockSizeSlider.setSizePolicy(sizePolicy7)
        self.ThresholdBlockSizeSlider.setMinimum(1)
        self.ThresholdBlockSizeSlider.setMaximum(41)
        self.ThresholdBlockSizeSlider.setSingleStep(2)
        self.ThresholdBlockSizeSlider.setValue(15)
        self.ThresholdBlockSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.ThresholdBlockLayout.addWidget(self.ThresholdBlockSizeSlider, 0, 0, 1, 1)

        self.ThresholdBlockSizeSpinBox = QSpinBox(self.layoutWidget)
        self.ThresholdBlockSizeSpinBox.setObjectName(u"ThresholdBlockSizeSpinBox")
        sizePolicy8.setHeightForWidth(self.ThresholdBlockSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.ThresholdBlockSizeSpinBox.setSizePolicy(sizePolicy8)
        self.ThresholdBlockSizeSpinBox.setKeyboardTracking(True)
        self.ThresholdBlockSizeSpinBox.setMinimum(1)
        self.ThresholdBlockSizeSpinBox.setMaximum(41)
        self.ThresholdBlockSizeSpinBox.setSingleStep(2)
        self.ThresholdBlockSizeSpinBox.setValue(15)

        self.ThresholdBlockLayout.addWidget(self.ThresholdBlockSizeSpinBox, 0, 1, 1, 1)


        self.settingsGridLayout.addLayout(self.ThresholdBlockLayout, 1, 2, 1, 1)

        self.ApplyMorphCheckBox = QCheckBox(self.layoutWidget)
        self.ApplyMorphCheckBox.setObjectName(u"ApplyMorphCheckBox")
        self.ApplyMorphCheckBox.setCheckable(True)

        self.settingsGridLayout.addWidget(self.ApplyMorphCheckBox, 5, 0, 1, 1)

        self.MorphKernalLayout = QGridLayout()
        self.MorphKernalLayout.setObjectName(u"MorphKernalLayout")
        self.MorphKernalSizeLabel = QLabel(self.layoutWidget)
        self.MorphKernalSizeLabel.setObjectName(u"MorphKernalSizeLabel")

        self.MorphKernalLayout.addWidget(self.MorphKernalSizeLabel, 0, 0, 1, 1)

        self.MorphKernalSizespinBox = QSpinBox(self.layoutWidget)
        self.MorphKernalSizespinBox.setObjectName(u"MorphKernalSizespinBox")
        self.MorphKernalSizespinBox.setKeyboardTracking(False)
        self.MorphKernalSizespinBox.setMinimum(1)
        self.MorphKernalSizespinBox.setMaximum(10)

        self.MorphKernalLayout.addWidget(self.MorphKernalSizespinBox, 0, 1, 1, 1)


        self.settingsGridLayout.addLayout(self.MorphKernalLayout, 5, 2, 1, 1)

        self.InvertImageCheckBox = QCheckBox(self.layoutWidget)
        self.InvertImageCheckBox.setObjectName(u"InvertImageCheckBox")
        self.InvertImageCheckBox.setCheckable(True)

        self.settingsGridLayout.addWidget(self.InvertImageCheckBox, 6, 0, 1, 1)

        self.TresholdBlockSizeLabel = QLabel(self.layoutWidget)
        self.TresholdBlockSizeLabel.setObjectName(u"TresholdBlockSizeLabel")
        sizePolicy4.setHeightForWidth(self.TresholdBlockSizeLabel.sizePolicy().hasHeightForWidth())
        self.TresholdBlockSizeLabel.setSizePolicy(sizePolicy4)

        self.settingsGridLayout.addWidget(self.TresholdBlockSizeLabel, 1, 0, 1, 1)

        self.ApplyBlurCheckBox = QCheckBox(self.layoutWidget)
        self.ApplyBlurCheckBox.setObjectName(u"ApplyBlurCheckBox")
        self.ApplyBlurCheckBox.setMouseTracking(False)
        self.ApplyBlurCheckBox.setCheckable(True)

        self.settingsGridLayout.addWidget(self.ApplyBlurCheckBox, 4, 0, 1, 1)

        self.BlurKernalLayout = QGridLayout()
        self.BlurKernalLayout.setObjectName(u"BlurKernalLayout")
        self.BlurKernalSizeXSpinBox = QSpinBox(self.layoutWidget)
        self.BlurKernalSizeXSpinBox.setObjectName(u"BlurKernalSizeXSpinBox")
        sizePolicy8.setHeightForWidth(self.BlurKernalSizeXSpinBox.sizePolicy().hasHeightForWidth())
        self.BlurKernalSizeXSpinBox.setSizePolicy(sizePolicy8)
        self.BlurKernalSizeXSpinBox.setKeyboardTracking(False)
        self.BlurKernalSizeXSpinBox.setMinimum(1)
        self.BlurKernalSizeXSpinBox.setMaximum(41)
        self.BlurKernalSizeXSpinBox.setSingleStep(2)
        self.BlurKernalSizeXSpinBox.setValue(5)

        self.BlurKernalLayout.addWidget(self.BlurKernalSizeXSpinBox, 0, 2, 1, 1)

        self.BlurKernalSizeYSlider = QSlider(self.layoutWidget)
        self.BlurKernalSizeYSlider.setObjectName(u"BlurKernalSizeYSlider")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy12.setHorizontalStretch(8)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.BlurKernalSizeYSlider.sizePolicy().hasHeightForWidth())
        self.BlurKernalSizeYSlider.setSizePolicy(sizePolicy12)
        self.BlurKernalSizeYSlider.setMinimum(1)
        self.BlurKernalSizeYSlider.setMaximum(41)
        self.BlurKernalSizeYSlider.setSingleStep(2)
        self.BlurKernalSizeYSlider.setValue(5)
        self.BlurKernalSizeYSlider.setOrientation(Qt.Orientation.Horizontal)

        self.BlurKernalLayout.addWidget(self.BlurKernalSizeYSlider, 1, 1, 1, 1)

        self.BlurKernalSizeXSlider = QSlider(self.layoutWidget)
        self.BlurKernalSizeXSlider.setObjectName(u"BlurKernalSizeXSlider")
        sizePolicy12.setHeightForWidth(self.BlurKernalSizeXSlider.sizePolicy().hasHeightForWidth())
        self.BlurKernalSizeXSlider.setSizePolicy(sizePolicy12)
        self.BlurKernalSizeXSlider.setMinimum(1)
        self.BlurKernalSizeXSlider.setMaximum(41)
        self.BlurKernalSizeXSlider.setSingleStep(2)
        self.BlurKernalSizeXSlider.setValue(5)
        self.BlurKernalSizeXSlider.setOrientation(Qt.Orientation.Horizontal)

        self.BlurKernalLayout.addWidget(self.BlurKernalSizeXSlider, 0, 1, 1, 1)

        self.BlurKernalSizeYSpinBox = QSpinBox(self.layoutWidget)
        self.BlurKernalSizeYSpinBox.setObjectName(u"BlurKernalSizeYSpinBox")
        sizePolicy8.setHeightForWidth(self.BlurKernalSizeYSpinBox.sizePolicy().hasHeightForWidth())
        self.BlurKernalSizeYSpinBox.setSizePolicy(sizePolicy8)
        self.BlurKernalSizeYSpinBox.setKeyboardTracking(False)
        self.BlurKernalSizeYSpinBox.setMinimum(1)
        self.BlurKernalSizeYSpinBox.setMaximum(41)
        self.BlurKernalSizeYSpinBox.setSingleStep(2)
        self.BlurKernalSizeYSpinBox.setValue(5)

        self.BlurKernalLayout.addWidget(self.BlurKernalSizeYSpinBox, 1, 2, 1, 1)

        self.BlurKernalSizeYLabel = QLabel(self.layoutWidget)
        self.BlurKernalSizeYLabel.setObjectName(u"BlurKernalSizeYLabel")

        self.BlurKernalLayout.addWidget(self.BlurKernalSizeYLabel, 1, 0, 1, 1)

        self.BlurKernalSizeXLabel = QLabel(self.layoutWidget)
        self.BlurKernalSizeXLabel.setObjectName(u"BlurKernalSizeXLabel")
        sizePolicy9.setHeightForWidth(self.BlurKernalSizeXLabel.sizePolicy().hasHeightForWidth())
        self.BlurKernalSizeXLabel.setSizePolicy(sizePolicy9)

        self.BlurKernalLayout.addWidget(self.BlurKernalSizeXLabel, 0, 0, 1, 1)


        self.settingsGridLayout.addLayout(self.BlurKernalLayout, 4, 2, 1, 1)

        self.ProcessPageUniqueButton = QCheckBox(self.layoutWidget)
        self.ProcessPageUniqueButton.setObjectName(u"ProcessPageUniqueButton")

        self.settingsGridLayout.addWidget(self.ProcessPageUniqueButton, 6, 2, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.SettingsLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.MainVerticalLayout = QVBoxLayout()
        self.MainVerticalLayout.setSpacing(0)
        self.MainVerticalLayout.setObjectName(u"MainVerticalLayout")
        self.MainVerticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        self.SettingsLayout.addLayout(self.MainVerticalLayout, 0, 0, 1, 1)

        self.BottomHorizontalLayoutBaseButtons = QHBoxLayout()
        self.BottomHorizontalLayoutBaseButtons.setObjectName(u"BottomHorizontalLayoutBaseButtons")
        self.CancelButton = QPushButton(self.verticalLayoutWidget)
        self.CancelButton.setObjectName(u"CancelButton")

        self.BottomHorizontalLayoutBaseButtons.addWidget(self.CancelButton)

        self.horizontalSpacer_2 = QSpacerItem(650, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.BottomHorizontalLayoutBaseButtons.addItem(self.horizontalSpacer_2)

        self.AddImageButton = QPushButton(self.verticalLayoutWidget)
        self.AddImageButton.setObjectName(u"AddImageButton")

        self.BottomHorizontalLayoutBaseButtons.addWidget(self.AddImageButton)

        self.ImportButton = QPushButton(self.verticalLayoutWidget)
        self.ImportButton.setObjectName(u"ImportButton")
        self.ImportButton.setCheckable(False)

        self.BottomHorizontalLayoutBaseButtons.addWidget(self.ImportButton)


        self.SettingsLayout.addLayout(self.BottomHorizontalLayoutBaseButtons, 3, 0, 1, 1)


        self.verticalLayout.addLayout(self.SettingsLayout)

        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(3, 1)

        self.retranslateUi(importImageWindow)

        self.ImportButton.setDefault(True)


        QMetaObject.connectSlotsByName(importImageWindow)
    # setupUi

    def retranslateUi(self, importImageWindow):
        importImageWindow.setWindowTitle(QCoreApplication.translate("importImageWindow", u"ImportImage", None))
        self.projectNameLabel.setText(QCoreApplication.translate("importImageWindow", u"Project Name: ", None))
#if QT_CONFIG(tooltip)
        self.ProjectNameLineEdit.setToolTip(QCoreApplication.translate("importImageWindow", u"Project name", None))
#endif // QT_CONFIG(tooltip)
        self.ImageNameLabel.setText(QCoreApplication.translate("importImageWindow", u"Image Name:", None))
        self.OriginalImageLabel.setText(QCoreApplication.translate("importImageWindow", u"Original Image", None))
        self.BinarizedImageLabel.setText(QCoreApplication.translate("importImageWindow", u"Binarized Image Preview", None))
        self.LoadPresetButton.setText(QCoreApplication.translate("importImageWindow", u"Load Preset", None))
        self.SavePresetButton.setText(QCoreApplication.translate("importImageWindow", u"Save Preset", None))
        self.PreviewButton.setText(QCoreApplication.translate("importImageWindow", u"Preview Settings", None))
        self.PreviousPageButton.setText(QCoreApplication.translate("importImageWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.pageSelectComboBox.setToolTip(QCoreApplication.translate("importImageWindow", u"Select image to preview", None))
#endif // QT_CONFIG(tooltip)
        self.NextPageButton.setText(QCoreApplication.translate("importImageWindow", u"...", None))
        self.TresholdCLabel.setText(QCoreApplication.translate("importImageWindow", u"Treshold Sensitivity", None))
        self.ApplyClaheCheckBox.setText(QCoreApplication.translate("importImageWindow", u"Apply CLAHE", None))
        self.ClaheClipLimitLabel.setText(QCoreApplication.translate("importImageWindow", u"Clip Limit", None))
        self.ClaheClipLimitYLabel.setText(QCoreApplication.translate("importImageWindow", u"Tile Grid Size Y", None))
        self.ClaheClipLimitXLabel.setText(QCoreApplication.translate("importImageWindow", u"Tile Grid Size X", None))
        self.ApplyMorphCheckBox.setText(QCoreApplication.translate("importImageWindow", u"Apply Morphology", None))
        self.MorphKernalSizeLabel.setText(QCoreApplication.translate("importImageWindow", u"Kernal Size", None))
        self.InvertImageCheckBox.setText(QCoreApplication.translate("importImageWindow", u"Invert Image", None))
        self.TresholdBlockSizeLabel.setText(QCoreApplication.translate("importImageWindow", u"Treshold Block Size", None))
        self.ApplyBlurCheckBox.setText(QCoreApplication.translate("importImageWindow", u"Apply Blur", None))
        self.BlurKernalSizeYLabel.setText(QCoreApplication.translate("importImageWindow", u"Kernal Size y", None))
        self.BlurKernalSizeXLabel.setText(QCoreApplication.translate("importImageWindow", u"Kernal Size X", None))
        self.ProcessPageUniqueButton.setText(QCoreApplication.translate("importImageWindow", u"Process Page Unique", None))
        self.CancelButton.setText(QCoreApplication.translate("importImageWindow", u"Cancel", None))
        self.AddImageButton.setText(QCoreApplication.translate("importImageWindow", u"Add Image", None))
        self.ImportButton.setText(QCoreApplication.translate("importImageWindow", u"Import", None))
    # retranslateUi

