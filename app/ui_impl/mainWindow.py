from PySide6.QtWidgets import QMainWindow, QFileDialog, QGraphicsPathItem, QGraphicsView, QGraphicsScene, QGraphicsItemGroup, QStatusBar, QDialog, QWidget
# from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QShortcut, QKeySequence
from app.Unused.vectorLayers import getPathsFromFile
from ui.ui_MainWindow import Ui_MainWindow
# from ui.ui_image_popup import
from app.core.status import *
from app.ui_impl.image_popup import ImportImageWindow
from app.FileHandling.fileHandler import *
from canvasHandler import *
# from canvasHandler import *
from app.core.threadutils import Worker
from app.core.martsLoggingHandler import handleLogFiles, loggingDir, createDirCheckNotExist
from functools import partial
from app.ImageProcessing.imageProcessing import loadImagesForImport, importImageFromPreviewImage
import os
from pathlib import Path as PATH
from app.Unused.costumWidgets import *

from layering import LayerGridLayout


loggingFile = 'main.log'
fullFileName = loggingDir+'/'+loggingFile
handleLogFiles(loggingDir, loggingFile, maxCache=5)
# Configure this module's logger
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

# Log to its own file
file_handler = logging.FileHandler(fullFileName)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Avoid double logging if added to root
logger.propagate = False

'''
To Implemenet/ built
High priority
    - tools.py
    - centralized logger for errors and own messages
    - Different layers loaded from SVG
    - apply backgrounds
    - layer original image
    - Layer editing selection

Mid priotity
    - save file before closing splash window when opening a new file/ closing unsaved file
    - saveFile function
    - importing demo objects (Simple SVG files probably
    - icons for tools
    - A context viewer/ logging thing at the bottom of the main window (statusbar)

Low priority
    - Handling multiple pages
    - connection to IIIF handling

'''

# class EmittingStream(QObject):
#     textWritten = Signal(str)

#     def write(self, text):
#         self.textWritten.emit(str(text))

#     def flush(self):
#         pass  # This can remain empty unless needed for compatibility

def dummy_long_function():
    import time
    print("[dummy_long_function] Starting")
    for i in range(5):
        print(f"[dummy_long_function] Step {i+1}")
        time.sleep(1)
    print("[dummy_long_function] Done")
    return "Done"
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app, file = None):
        super().__init__()
        self.setupUi(self)
        self.projectName = ''
        self.cacheFolder:str = None
        curFolder = PATH('Quil2Vec')
        self.curFolder = os.path.expanduser(curFolder)
        createDirCheckNotExist(self.curFolder, logger)
        self.app = app
        # self.svgPathsScene = QGraphicsScene(self)
        self.file = file # Quill2VecSaveFile()
        if self.file:
            self.svgEditorScene = Quil2VecCanvasScene.fromFile(self)
            self.svgEditorScene.setSelectionMode(QGraphicsScene.SingleSelection)

        else:
            self.svgEditorScene = Quil2VecCanvasScene(self)

        self.svgView = Quil2VecGraphicsView(self.scrollAreaWidgetContents)
        self.debugShortcutHitboxes = QShortcut(QKeySequence("Ctrl+D"), self.svgView)
        self.debugShortcutHitboxes.activated.connect(lambda: toggle_debug_hitboxes(self.svgEditorScene))

        self.debugShortcutShapes = QShortcut(QKeySequence("Ctrl+Shift+D"), self.svgView)
        self.debugShortcutShapes.activated.connect(lambda: toggle_path_shape_disable(self.svgEditorScene))

        self.svgView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setObjectName(u"svgView")
        self.gridLayout_3.addWidget(self.svgView, 0, 1, 1, 1)

        self.svgView.setScene(self.svgEditorScene)
        # self.svgView.setScene(self.svgPathsScene)
        self.actionopen.triggered.connect(self.openFile)
        self.actionimage.triggered.connect(self.importImage)
        self.actionsave.triggered.connect(self.saveFile)
        self.actionsave_as.triggered.connect(self.saveFileAs)
        self.svgPathLayer = QGraphicsItemGroup()
        self.svgEditorScene.addItem(self.svgPathLayer)
        # self.setStatusBar(QStatusBar(self))
        # self.stat
        # self.statusbar = QStatusBar()
        # self.setStatusBar(self.statusbar)
        # self.status_handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
        self.statusbar.showMessage("Hello from log!")
        self.status_emitter = StatusEmitter()
        self.status_handler = StatusBarHandler(self.status_emitter)
        self.status_emitter.newMessage.connect(self.show_status_message)
        # self.Layers
        for name in logging.root.manager.loggerDict.keys():
            get_logger(name, self.status_handler)
        # mainLogger = logging.getLogger('main')
        # fileHandlerLogger = logging.getLogger('fileHandler')
        # mainLogger.addHandler(self.status_handler)
        # fileHandlerLogger.addHandler(self.status_handler)
        # self.output_stream = EmittingStream()


        # self.output_stream.textWritten.connect(self.on_print)
        # self.svgView = Quil
        self._threads = []

    
    def openFile(self):

        ## to implement: save file before closing splash window when opening a new file
        if len(self.svgPathLayer.childItems())!=0:
            print('Warning just destroyed existing layers!!! Need to implement a save option and add a save file splash window here!!!!')
            self.svgPathLayer = QGraphicsItemGroup()
        
        
        filename = QFileDialog.getOpenFileNames(self,"Open Image", "", "Quil2Vec Files (*.xqv)")
        svg_filename = filename[0]
        with open(svg_filename, 'r') as inFile:
            file = Quill2VecSaveFile.fromSave(inFile.read(), svg_filename)
        self.file = file
        self.file.updateCanvas(self)

        # path_items = getPathsFromFile(svg_filename)
        # for path_graphics_item in path_items:
        #     # globalPaths.append(path_graphics_item)
        #     self.svgPathLayer.addToGroup(path_graphics_item)
        # self.view = QGraphicsView(self.svgEditorScene)
        '''
        Function needs a lot of work:
            - import window which handles all the tools from the importImage function
        '''
    def importImage(self):
        filenames = QFileDialog.getOpenFileNames(self,"Load Images for Import", "", "Image files (*.jpg *.pdf *.png)")
        imageFileNames = filenames[0]
        logger.info(f'Opening files for import at paths: {imageFileNames}')
        fileType = filenames[1]
        if len(self.projectName)>=1:
            pName = self.projectName
        else:
            pName = None
            projectName = imageFileNames[0]
        if self.cacheFolder:
            previewImages = loadImagesForImport(imagePaths=imageFileNames, fileType=fileType, projectName=pName, cacheFolder=self.cacheFolder)
        else:
            previewImages = loadImagesForImport(imagePaths=imageFileNames, fileType=fileType, projectName=pName)
        
        importWindow = ImportImageWindow(self, previewImages, projectName)
        if importWindow.exec() == QDialog.Accepted:
            imagesToImport = importWindow.getImages()
        else:
            logger.info("[MainWindow] Import Image cancelled by user")
            return
        # import_job = partial(importImage, [imageFileName], '.png', 'Test', False)
        logger.info("[MainWindow] Starting threaded import")
        self.run_in_thread(importImageFromPreviewImage, '',
                        imagesToImport, projectName, False, 
                        on_result=self.handleImageImportResult, 
                        on_error=lambda err: self.statusbar.showMessage(f"Error during vectorTrace: {err}")
                        )

        
    def handleImageImportResult(self, saveFile:Quill2VecSaveFile):
        print("[MainWindow] handleImageImportResult triggered")
        self.file = saveFile
        # layerHandles = self.file.generateLayerHandles()
        # Remove and delete the old layout if it exists
        old_layout = self.Layers.layout()
        if old_layout is not None:
            QWidget().setLayout(old_layout)  # Detach the layout from the widget
            # Optionally, delete the old layout to free memory
            # import sip
            # sip.delete(old_layout)
            del old_layout
        self.layerGridLayout = LayerGridLayout(self.file.getCurrentPage(), self)
        self.Layers.setLayout(self.layerGridLayout)
        self.file.updateCanvas(self)
        # self.run_in_thread(lambda: self.file.updateCanvas(self))

    def saveFile(self):
        if len(self.file.filename)>0:
            _dir = os.path.dirname(self.file.filename)
            if not os.path.isdir(_dir):
                os.makedirs(_dir)
            self.file.toSave()
        else:
            self.saveFileAs()

    def saveFileAs(self):
        filename = QFileDialog.getSaveFileName(self,"Save File as", "", "Quil2Vec File (,*.xqv)", "Quil2Vec File (*.xqv)")
        try:
            t = self.run_in_thread(self.file.toSave(filename[0]))
        except:
            print(filename)
            self.file.toSave(filename[0])
        
        
    def show_status_message(self, text):
        # print(f"STATUS SLOT RECEIVED: {text}")
        self.statusbar.showMessage(text)


    def run_in_thread(self, func,*args, on_result=None, on_error=None, **kwargs):
        print("[run_in_thread] Preparing thread...")
        thread = QThread()
        worker = Worker(func, *args, **kwargs)
        worker.moveToThread(thread)

        # thread.started.connect(worker.run)
        thread.started.connect(lambda: worker.run())
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        if on_result:
            worker.result.connect(on_result)
        if on_error:
            worker.error.connect(on_error)

        if not hasattr(self, "_threads"):
            self._threads = []

        self._threads.append(thread)
        print(f"[run_in_thread] Starting thread ({len(self._threads)} active)...")

        def cleanup():
            print("[run_in_thread] Thread cleanup")
            self._threads.remove(thread)

        thread.finished.connect(cleanup)
        thread.start()