from ui.ui_image_popup import Ui_importImageWindow
from ui.ui_presetSelecter import Ui_Dialog as Ui_PresetSelecter
from PySide6.QtWidgets import (QFileDialog, QGraphicsScene, 
                               QGraphicsPixmapItem, QWidget, 
                               QDialog, QGraphicsView, QSizePolicy)
from PySide6.QtGui import QImage, QPixmap, QTransform
from PySide6.QtCore import Qt, Signal
from PySide6 import QtCore
from app.FileHandling.fileHandler import *
from xml.etree import ElementTree as ET
from app.ImageProcessing.imageProcessing import *
from typing import List, Dict
from pathlib import Path as PATH
from PySide6.QtGui import QGuiApplication

class presetSelecter(QDialog,Ui_PresetSelecter):
    def __init__(self, parent, presets: List[imagePreProcessSettings]):
        super().__init__(parent)
        self.setupUi(self)
        self.presets = presets
        self.current_index = 0
        # Setup connections
        self.NextPageButton.clicked.connect(self.next_page)
        self.PrevPageButton.clicked.connect(self.prev_page)
        self.PageComboBox.currentIndexChanged.connect(self.set_page_from_combo)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # Populate combo box
        self.PageComboBox.clear()
        for i in range(len(presets)):
            self.PageComboBox.addItem(f"Preset {i + 1}")

        # self.disable_all_inputs()
        # SpinBoxes
        self.ThresholdBlockSizeSpinBox.setReadOnly(True)
        self.TresholdCSpinBox.setReadOnly(True)
        # DoubleSpinBox
        self.ClaheClipLimitDoubleSpinBox.setReadOnly(True)

        # Sliders
        self.ThresholdBlockSizeSlider.setEnabled(False)
        self.TresholdCSlider.setEnabled(False)
        # Fake read-only slider
        self.ThresholdBlockSizeSlider.setEnabled(True)
        self.ThresholdBlockSizeSlider.blockSignals(True)
        self.ThresholdBlockSizeSlider.setFocusPolicy(Qt.NoFocus)
        self.ThresholdBlockSizeSlider.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.ApplyClaheCheckBox.setFocusPolicy(Qt.NoFocus)
        self.ApplyClaheCheckBox.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.update_page()

    def disable_all_inputs(self):
        for widget in self.findChildren(QWidget):
            widget.setEnabled(False)

        # Re-enable nav + OK/Cancel
        self.NextPageButton.setEnabled(True)
        self.PrevPageButton.setEnabled(True)
        self.PageComboBox.setEnabled(True)
        self.buttonBox.setEnabled(True)

    def update_page(self):
        settings = self.presets[self.current_index]
        self.PageComboBox.setCurrentIndex(self.current_index)
        self.loadSettings(settings)

    def next_page(self):
        if self.current_index < len(self.presets) - 1:
            self.current_index += 1
            self.update_page()

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_page()

    def set_page_from_combo(self, index):
        self.current_index = index
        self.update_page()

    def loadSettings(self, settings: imagePreProcessSettings):
        # Load all values into UI widgets
        self.ThresholdBlockSizeSpinBox.setValue(settings.thresholdBlockSize)
        self.ThresholdBlockSizeSlider.setValue(settings.thresholdBlockSize)
        self.ThresholdBlockSizeSpinBox.setValue(settings.thresholdC)
        self.TresholdCSlider.setValue(settings.thresholdC)
        self.ApplyClaheCheckBox.setChecked(settings.applyClahe)
        self.ClaheClipLimitDoubleSpinBox.setValue(settings.claheClipLimit)
        self.ClaheTileGridSizeXSpinBox.setValue(settings.claheTileGridSize[0])
        self.ClaheTileGridSizeXSlider.setValue(settings.claheTileGridSize[0])
        self.ClaheTileGridSizeYSpinBox.setValue(settings.claheTileGridSize[1])
        self.ClaheTileGridSizeYSlider.setValue(settings.claheTileGridSize[1])
        self.ApplyBlurCheckBox.setChecked(settings.applyBlur)
        self.BlurKernalSizeXSpinBox.setValue(settings.blurKernelSize[0])
        self.BlurKernalSizeXSlider.setValue(settings.blurKernelSize[0])
        self.BlurKernalSizeYSpinBox.setValue(settings.blurKernelSize[1])
        self.BlurKernalSizeYSlider.setValue(settings.blurKernelSize[1])
        self.ApplyMorphCheckBox.setChecked(settings.applyMorphology)
        self.MorphKernalSizespinBox.setValue(settings.morphologyKernelSize)
        self.InvertImageCheckBox.setChecked(settings.invertImage)

    def get_selected_settings(self) -> imagePreProcessSettings:
        return self.presets[self.current_index]

class imagePreviewView(QGraphicsView):

    transformChanged = Signal(QTransform)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom_factor = 1.15


    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.scale(self.zoom_factor, self.zoom_factor)
            else:
                self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
            self.transformChanged.emit(self.transform())
        else:
            super().wheelEvent(event)

# def sync_views(view1: imagePreviewView, view2: imagePreviewView):
#     # Connect their transformChanged signals to each other
#     view1.transformChanged.connect(view2.setTransform)
#     view2.transformChanged.connect(view1.setTransform)

class ImportImageWindow(QDialog, Ui_importImageWindow):
    def __init__(self, parent, imagePreviews:List[imagePreview],projectName:str=None, globalSettings=imagePreProcessSettings()):
        if len(imagePreviews) == 0:
            raise Exception('ImportImageWindow cannot handle empty imagePreviews')
        super(ImportImageWindow, self).__init__(parent)
        self.setupUi(self)
        # self.verticalLayoutWidget.setMinimumSize(0, 0)
        # self.verticalLayoutWidget.setMaximumSize(QtCore.QSize(QtCore.QWIDGETSIZE_MAX, QtCore.QWIDGETSIZE_MAX))
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect())  # Remove fixed size
        # self.verticalLayoutWidget.setSizePolicy(
        #     QSizePolicy.Expanding,
        #     QSizePolicy.Expanding
        # )

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        self.setLayout(self.verticalLayout)
        self.setMaximumSize(
            screen_geometry.width(), 
            screen_geometry.height()
            )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.verticalLayout.setStretch()
        # self.scrollAreaWidgetContents.setLayout(self.settingsGridLayout)

        self.scrollArea.setSizePolicy(
            self.scrollArea.sizePolicy().horizontalPolicy(),
            self.scrollArea.sizePolicy().verticalPolicy()
        )
        self.scrollAreaWidgetContents.setMinimumSize(400, 550)
        # self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        old_view = self.BinarizedPreviewGraphicsView
        self.BinarizedPreviewGraphicsView = imagePreviewView(self.verticalLayoutWidget)
        self.BinarizedPreviewGraphicsView.setObjectName("BinarizedPreviewGraphicsView")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.verticalPolicy = QSizePolicy.Policy.Fixed
        sizePolicy.horizontalPolicy = QSizePolicy.Policy.Fixed
        # sizePolicy.setHeightForWidth(self.BinarizedPreviewGraphicsView.sizePolicy().hasHeightForWidth())
        # self.BinarizedPreviewGraphicsView.setSizePolicy(sizePolicy)
        self.BinarizedPreviewGraphicsView.setSizePolicy(
            self.BinarizedPreviewGraphicsView.sizePolicy().horizontalPolicy(),
            self.BinarizedPreviewGraphicsView.sizePolicy().verticalPolicy()
        )
        self.gridLayout.replaceWidget(old_view, self.BinarizedPreviewGraphicsView)
        old_view.setParent(None)  # Remove old widget from layout
        old_view.deleteLater()

        # self.BinarizedPreviewGraphicsView = imagePreviewView(self.verticalLayoutWidget)
        # sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        # sizePolicy.setHorizontalStretch(5)
        # sizePolicy.setVerticalStretch(35)
        # sizePolicy.setHeightForWidth(self.BinarizedPreviewGraphicsView.sizePolicy().hasHeightForWidth())
        # self.BinarizedPreviewGraphicsView.setObjectName("BinarizedPreviewGraphicsView")
        # self.gridLayout.addWidget(self.BinarizedPreviewGraphicsView, 0, 3, 1, 1)

        # Replace the placeholder widget with subclass
        old_view = self.PreviewImageGraphicsView
        self.PreviewImageGraphicsView = imagePreviewView(self.verticalLayoutWidget)
        self.PreviewImageGraphicsView.setObjectName("PreviewImageGraphicsView")
        sizePolicy.setHeightForWidth(self.BinarizedPreviewGraphicsView.sizePolicy().hasHeightForWidth())
        
        # self.PreviewImageGraphicsView.setSizePolicy(sizePolicy)
        self.PreviewImageGraphicsView.setSizePolicy(
            self.PreviewImageGraphicsView.sizePolicy().horizontalPolicy(),
            self.PreviewImageGraphicsView.sizePolicy().verticalPolicy()
        )
        # Keep the same layout position
        self.gridLayout.replaceWidget(old_view, self.PreviewImageGraphicsView)
        old_view.setParent(None)  # Remove old widget from layout
        old_view.deleteLater()  # Clean up old widget
        # self.PreviewImageGraphicsView = imagePreviewView(self.verticalLayoutWidget)
        # sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        # sizePolicy.setHorizontalStretch(5)
        # sizePolicy.setVerticalStretch(35)
        # sizePolicy.setHeightForWidth(self.PreviewImageGraphicsView.sizePolicy().hasHeightForWidth())
        # self.PreviewImageGraphicsView.setSizePolicy(sizePolicy)
        # self.PreviewImageGraphicsView.setObjectName("PreviewImageGraphicsView")
        # self.gridLayout.addWidget(self.PreviewImageGraphicsView, 0, 1, 1, 1)

        # syncing zoom between binarized and preview image views
        self.BinarizedPreviewGraphicsView.transformChanged.connect(self.PreviewImageGraphicsView.setTransform)
        self.PreviewImageGraphicsView.transformChanged.connect(self.BinarizedPreviewGraphicsView.setTransform)

        # syncing scroll/panning between binarized and preview image views
        self.BinarizedPreviewGraphicsView.verticalScrollBar().valueChanged.connect(
            self.PreviewImageGraphicsView.verticalScrollBar().setValue
        )
        self.BinarizedPreviewGraphicsView.horizontalScrollBar().valueChanged.connect(
            self.PreviewImageGraphicsView.horizontalScrollBar().setValue
        )
        
        self.PreviewImageGraphicsView.verticalScrollBar().valueChanged.connect(
            self.BinarizedPreviewGraphicsView.verticalScrollBar().setValue
        )
        self.PreviewImageGraphicsView.horizontalScrollBar().valueChanged.connect(
            self.BinarizedPreviewGraphicsView.horizontalScrollBar().setValue
        )


        images = {}
        self.imageOrder = []
        # pageNumber = 0
        for preView in imagePreviews:
            imageName=PATH(preView.originalImagePath).stem
            self.imageOrder.append(imageName)
            # pageNumber+=1
            # self.pageSelectComboBox.addItem(imageName)
            images[imageName]=preView
        if projectName:
            self.ProjectNameLineEdit.setText(projectName)
        self.images = images
        self.globalSettings = globalSettings
        self.curPage = 0
        self.oldImageName = None

        #### Page Navigation
        self.initPageControls()
        self.PreviousPageButton.clicked.connect(lambda: self.setPage(self.curPage - 1))
        self.NextPageButton.clicked.connect(lambda: self.setPage(self.curPage + 1))
        self.pageSelectComboBox.currentIndexChanged.connect(self.setPage)
        self.PageScrollBar.valueChanged.connect(self.setPage)

        self.SavePresetButton.clicked.connect(self.savePreset)
        self.ImportButton.clicked.connect(self.accept)
        self.CancelButton.clicked.connect(self.close)
        # Binarize preview
        self.PreviewButton.clicked.connect(self.loadBinarizedPreview)

        #### Value Syncing
        # Treshold
        self.ThresholdBlockSizeSlider.valueChanged.connect(self.tresholdBlockSliderSyncToSpinbox)
        self.ThresholdBlockSizeSpinBox.valueChanged.connect(self.tresholdBlockSpinboxSyncToSlider)
        self.TresholdCSlider.valueChanged.connect(self.tresholdCSliderSyncToSpinbox)
        self.TresholdCSpin.valueChanged.connect(self.tresholdCSpinboxSyncToSlider)
        # CLAHE
        self.ApplyClaheCheckBox.stateChanged.connect(self.activClahe)
        # Tile Grid X
        self.ClaheTileGridSizeXSlider.valueChanged.connect(self.claheTileXSlideryncToSpin)
        self.ClaheTileGridSizeXSpinBox.valueChanged.connect(self.claheTileXSpinSyncToSlider)
        # Tile Grid Y
        self.ClaheTileGridSizeYSlider.valueChanged.connect(self.claheTileYSlideryncToSpin)
        self.ClaheTileGridSizeYSpinBox.valueChanged.connect(self.claheTileYSpinSyncToSlider)
        # Blur
        self.ApplyBlurCheckBox.stateChanged.connect(self.activBlur)
        # Kernal Size X
        self.BlurKernalSizeXSlider.valueChanged.connect(self.blurXSliderSyncToSpinbox)
        self.BlurKernalSizeXSpinBox.valueChanged.connect(self.blurXSpinboxSyncToSlider)
        # Kernal Size Y
        self.BlurKernalSizeYSlider.valueChanged.connect(self.blurYSliderSyncToSpinbox)
        self.BlurKernalSizeYSpinBox.valueChanged.connect(self.blurYSpinboxSyncToSlider)
        ## Morphology
        self.ApplyMorphCheckBox.stateChanged.connect(self.activMorph)
        self.reload()

    def __importImage__(self,):
        pass

    def addFile(self, fileName:str, index:int):
        # self.filenames.append(fileName)
        pass

    def loadSettings(self, settings:imagePreProcessSettings):
        ## Treshold
        # Blocksize
        self.ThresholdBlockSizeSlider.setValue(settings.thresholdBlockSize)
        self.ThresholdBlockSizeSpinBox.setValue(settings.thresholdBlockSize)
        # C
        self.TresholdCSlider.setValue(settings.thresholdC)
        self.TresholdCSpin.setValue(settings.thresholdC)
        ## CLAHE
        self.ApplyClaheCheckBox.setChecked(settings.applyClahe)
        # Clip
        self.ClaheClipLimitDoubleSpinBox.setValue(settings.claheClipLimit)
        # Tile Grid Size X
        self.ClaheTileGridSizeXSlider.setValue(settings.claheTileGridSize[0])
        self.ClaheTileGridSizeXSpinBox.setValue(settings.claheTileGridSize[0])
        # Tile Grid Size Y
        self.ClaheTileGridSizeYSlider.setValue(settings.claheTileGridSize[1])
        self.ClaheTileGridSizeYSpinBox.setValue(settings.claheTileGridSize[1])
        ## Blur
        self.ApplyBlurCheckBox.setChecked(settings.applyBlur)
        # Kernal Size X
        self.BlurKernalSizeXSlider.setValue(settings.blurKernelSize[0])
        self.BlurKernalSizeXSpinBox.setValue(settings.blurKernelSize[0])
        # Kernal Size Y
        self.BlurKernalSizeYSlider.setValue(settings.blurKernelSize[1])
        self.BlurKernalSizeYSpinBox.setValue(settings.blurKernelSize[1])
        ## Morphology
        self.ApplyMorphCheckBox.setChecked(settings.applyMorphology)
        self.MorphKernalSizespinBox.setValue(settings.morphologyKernelSize)
        ## Inverted
        self.InvertImageCheckBox.setChecked(settings.invertImage)

    def getSettings(self) -> imagePreProcessSettings:
        return imagePreProcessSettings(
            # Threshold
            thresholdBlockSize=self.ThresholdBlockSizeSpinBox.value(),
            thresholdC=self.TresholdCSpin.value(),

            # CLAHE
            applyClahe=self.ApplyClaheCheckBox.isChecked(),
            claheClipLimit=self.ClaheClipLimitDoubleSpinBox.value(),
            claheTileGridSize=(
                self.ClaheTileGridSizeXSpinBox.value(),
                self.ClaheTileGridSizeYSpinBox.value()
            ),

            # Blur
            applyBlur=self.ApplyBlurCheckBox.isChecked(),
            blurKernelSize=(
                self.BlurKernalSizeXSpinBox.value(),
                self.BlurKernalSizeYSpinBox.value()
            ),

            # Morphology
            applyMorphology=self.ApplyMorphCheckBox.isChecked(),
            morphologyKernelSize=self.MorphKernalSizespinBox.value(),

            # Inversion
            invertImage=self.InvertImageCheckBox.isChecked()
        )
    
    def getCurImage(self):
        return self.images[self.imageOrder[self.curPage]]
    
    def reload(self):
        if self.curPage==0:
            self.PreviousPageButton.setEnabled(False)
        else:
            self.PreviousPageButton.setEnabled(True)
        if self.curPage == len(self.images)-1:
            self.NextPageButton.setEnabled(False)
        else:
            self.NextPageButton.setEnabled(True)
        self.ImageNameLineEdit.setText(self.imageOrder[self.curPage])
        self.oldImageName = self.imageOrder[self.curPage]
        imagePrev = self.getCurImage()
        imagePrev:imagePreview
        self.loadSettings(imagePrev.settings)
        image = cv2.imread(imagePrev.originalImagePath)
        pixmap = cv2_to_qpixmap(image)
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.PreviewImageGraphicsView.setScene(scene)
        self.PreviewImageGraphicsView.setRenderHint(self.PreviewImageGraphicsView.renderHints())
        self.loadBinarizedPreview()

    def loadBinarizedPreview(self):
        imagePrev = self.getCurImage()
        imagePrev:imagePreview
        settings = self.getSettings()
        bin_image = binarizeForVectorTracing(imagePrev.originalImagePath, settings)
        bin_pixmap = cv2_to_qpixmap(bin_image)
        bin_scene = QGraphicsScene()
        bin_item = QGraphicsPixmapItem(bin_pixmap)
        bin_scene.addItem(bin_item)
        self.BinarizedPreviewGraphicsView.setScene(bin_scene)
        self.BinarizedPreviewGraphicsView.setRenderHint(self.BinarizedPreviewGraphicsView.renderHints())

    def applyGlobalSettings(self):
        # for i in range(0,len(self.images)-1):
        #     if not self.images[i].uniqueSettings:
        #         self.images[i].settings = self.globalSettings
        for imageName, image in self.images.items():
            image:imagePreview
            if not image.uniqueSettings:
                image.settings = self.globalSettings

    def loadPresets(self):
        filename = QFileDialog.getOpenFileName(self,"Open Presets", "", "Quil2Vec image preprocessing presets (*.xqvps) ;; Quil2Vec Files (*.xqv)")
        if filename:
            if filename[1] == '*.xqvps':
                presets = imagePreProcessSettings.loadFromFile(filename[0])
                # presets = 
                self.globalSettings = presets
                self.applyGlobalSettings()
                self.reload()
            elif filename[1] == '*.xqv':
                allPresets = getMultiplePresetsFromFile(filename[0])
                presetDialog = presetSelecter(self, allPresets)
                if presetDialog.exec() == QDialog.Accepted:
                    self.globalSettings = presetDialog.get_selected_settings()
                    self.applyGlobalSettings()
                    self.reload()
        else:
            return None
        
    def processUniqueAction(self):
        if self.ProcessPageUniqueButton.isChecked():
            self.images[self.curPage].uniqueSettings=True
            self.images[self.curPage].settings = self.getSettings()
        else:
            self.images[self.curPage].uniqueSettings=False 

    def processImageNameChange(self):
        imageName = self.ImageNameLineEdit.text()
        self.applySettingsOfCurPage()
        self.images[imageName] = self.images[self.oldImageName]
        del self.images[self.oldImageName]
        self.reload()

    ### Page Navigation
    def initPageControls(self):
        self.pageSelectComboBox.clear()
        for key in self.imageOrder:
            self.pageSelectComboBox.addItem(key)  # Or a friendly name

        self.PageScrollBar.setMinimum(0)
        self.PageScrollBar.setMaximum(len(self.imageOrder) - 1)
        self.PageScrollBar.setSingleStep(1)
        self.PageScrollBar.setPageStep(1)

    def setPage(self, index: int):
        # Make sure we get our settings saved first
        self.applySettingsOfCurPage()
        index = max(0, min(index, len(self.imageOrder) - 1))  # Clamp to range
        self.curPage = index
        self.reload()  # Load the page content

        # Sync all UI elements
        self.pageSelectComboBox.setCurrentIndex(index)
        self.PageScrollBar.setValue(index)
    # def pageNext(self):
    #     self.curPage+=1
    #     self.reload()
    # def pagePrev(self):
    #     self.curPage-=1
    #     self.reload()
    # def goToPage(self)

    def applySettingsOfCurPage(self):
        self.images[self.imageOrder[self.curPage]].settings = self.getSettings()
        if not self.ProcessPageUniqueButton.isChecked():
            self.globalSettings = self.getSettings()
            self.applyGlobalSettings()
        else:
            self.images[self.imageOrder[self.curPage]].uniqueSettings = True

    def savePreset(self):
        preset = self.getSettings()
        filepath = QFileDialog.getSaveFileName(self, 'Quil2Vec image preprocessing preset', self.parent.curFoler, '*.xqvps')
        preset.export(filepath[0])
    
    def getImages(self) -> Dict[str,imagePreview]:
        self.applySettingsOfCurPage()
        return self.images








    ###### stuff for settings to sync up ######
    ## BLUR
    # Checking
    def activBlur(self):
        if self.ApplyBlurCheckBox.isChecked():
            self.BlurKernalSizeXLabel.setEnabled(True)
            self.BlurKernalSizeXSlider.setEnabled(True)
            self.BlurKernalSizeXSpinBox.setEnabled(True)
            self.BlurKernalSizeYLabel.setEnabled(True)
            self.BlurKernalSizeYSlider.setEnabled(True)
            self.BlurKernalSizeYSpinBox.setEnabled(True)
        else:
            self.BlurKernalSizeXLabel.setEnabled(False)
            self.BlurKernalSizeXSlider.setEnabled(False)
            self.BlurKernalSizeXSpinBox.setEnabled(False)
            self.BlurKernalSizeYLabel.setEnabled(False)
            self.BlurKernalSizeYSlider.setEnabled(False)
            self.BlurKernalSizeYSpinBox.setEnabled(False)
    def blurXSliderSyncToSpinbox(self, value):
        self.BlurKernalSizeXSpinBox.setValue(value)
    def blurXSpinboxSyncToSlider(self, value):
        self.BlurKernalSizeXSlider.setValue(value)
    def blurYSliderSyncToSpinbox(self, value):
        self.BlurKernalSizeYSpinBox.setValue(value)
    def blurYSpinboxSyncToSlider(self, value):
        self.BlurKernalSizeYSlider.setValue(value)
    ### Treshold
    def tresholdBlockSliderSyncToSpinbox(self, value):
        self.ThresholdBlockSizeSpinBox.setValue(value)
    def tresholdBlockSpinboxSyncToSlider(self, value):
        self.ThresholdBlockSizeSlider.setValue(value)
    def tresholdCSliderSyncToSpinbox(self, value):
        self.TresholdCSpin.setValue(value)
    def tresholdCSpinboxSyncToSlider(self, value):
        self.TresholdCSlider.setValue(value)
    ### CLAHE
    def activClahe(self):
        if self.ApplyClaheCheckBox.isChecked():
            self.ClaheClipLimitDoubleSpinBox.setEnabled(True)
            self.ClaheClipLimitLabel.setEnabled(True)
            self.ClaheClipLimitXLabel.setEnabled(True)
            self.ClaheClipLimitYLabel.setEnabled(True)
            self.ClaheTileGridSizeXSlider.setEnabled(True)
            self.ClaheTileGridSizeXSpinBox.setEnabled(True)
            self.ClaheTileGridSizeYSlider.setEnabled(True)
            self.ClaheTileGridSizeYSpinBox.setEnabled(True)
        else:
            self.ClaheClipLimitDoubleSpinBox.setEnabled(False)
            self.ClaheClipLimitLabel.setEnabled(False)
            self.ClaheClipLimitXLabel.setEnabled(False)
            self.ClaheClipLimitYLabel.setEnabled(False)
            self.ClaheTileGridSizeXSlider.setEnabled(False)
            self.ClaheTileGridSizeXSpinBox.setEnabled(False)
            self.ClaheTileGridSizeYSlider.setEnabled(False)
            self.ClaheTileGridSizeYSpinBox.setEnabled(False)

    def claheTileXSpinSyncToSlider(self, value):
        self.ClaheTileGridSizeXSlider.setValue(value)
    def claheTileXSlideryncToSpin(self, value):
        self.ClaheTileGridSizeXSpinBox.setValue(value)
    def claheTileYSpinSyncToSlider(self, value):
        self.ClaheTileGridSizeYSlider.setValue(value)
    def claheTileYSlideryncToSpin(self, value):
        self.ClaheTileGridSizeYSpinBox.setValue(value)
    ### Morphology
    def activMorph(self):
        if self.ApplyMorphCheckBox.isChecked():
            self.MorphKernalSizeLabel.setEnabled(True)
            self.MorphKernalSizespinBox.setEnabled(True)
        else:
            self.MorphKernalSizeLabel.setEnabled(False)
            self.MorphKernalSizespinBox.setEnabled(False)





# def previewImage(image:str, threshold:int, reverse:bool, noiseFilter:int, GaussianBlurFilter:tuple[int,int,int], medianBlurFilter:int, morphoFilter:tuple[int,int], contrast:int, cannyEdge:tuple[min:int,max:int]):
#     '''
#     image(str): path to input image
#     threshold(int): base binarization threshold value
#     reverse(bool): True: reverse the binarization threshold (dark becomes white, white becomes black) | False: not reverse binarization threshold (white becomes white, dark becomes black)
#     noiseFilter(int): value for intensity of basic denoising algorithm (bilateralFilter)
#     GaussianBlurFilter(Tuple[kerne_size:int,kernal_size:int, sigmaX]): values to feed Gaussian blur algorithm
#     medianBlurFilter(int:ksize): ksize to feed to medianBlurFilter
#     morphoFilter
#     '''

# def basicImagePreProcess(imagePath:str, threshold:int, reverse:bool, medianBlurFilter:int, GaussianBlurFilter:tuple[int,int,int], blockSize:int, sensitivityThreshold: int, )

# def basicImagePreProcess(image_path:str,
#     applyContrast:
#     contrastLimit:float,
#     tileGridSize:tuple[int, int],
#     threshold_block_size:int,
#     threshold_C:int,
#     cleanup_kernel_size:int,
#     Gaussian_blur_filter = (5,5,0)
# ):
#     '''
#     Basic image prepocessing function (with help from ChatGPT)
#     image_path: path to image
#     contrastLimit: for CLAHE contrast; Controls amplification — higher = stronger; Typical Range = 2.0-4.0
#     tileGridSize: Controls local patch size (detail vs smoothing); Typical Range = (8,8)–(16,16)
#     threshold_block_size: recommend to start at 35, try 25-51; size of blocks for edge detections
#     threshold_C: sensitvity of adaptiveThreshold
#     cleanup_kernel_size: 
#     Gaussian_blur_filter: tuple of (kernal_size_x:int,kernal_size_y:int, sigmaX:float)
#     '''
#     # 1. Load image and convert to grayscale
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

#     # 2. Apply Gaussian blur to reduce noise
#     kernalSize = (Gaussian_blur_filter[0], Gaussian_blur_filter[1])
#     sigmaX = Gaussian_blur_filter[2]
#     blurred = cv2.GaussianBlur(img, kernalSize, sigmaX)

#     # 3. Adaptive thresholding to binarize
#     binary = cv2.adaptiveThreshold(
#         blurred, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         blockSize=threshold_block_size,
#         C=threshold_C
#     )

#     # 4. Morphological cleanup
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cleanup_kernel_size, cleanup_kernel_size))
#     cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

#     # 5. Invert colors (potrace expects black strokes on white)
#     inverted = cv2.bitwise_not(cleaned)

#     return inverted