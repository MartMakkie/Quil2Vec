from version import version


from PySide6.QtGui import QPainterPath
# from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import (QPainterPath)
from PySide6.QtGui import QPixmap

import svg
# from svg.path.path import Line, Move, CubicBezier, QuadraticBezier, Arc, Close
# from io import StringIO
import xml.etree.ElementTree as ET
from svg.path import parse_path
from Quil2VecGlobals import *
# from canvasHandler import Quil2VecCanvasScene

# from typing import Literal

# from matplotlib import pyplot as plt

# import pdf2image 

from svg.path.path import Line, Move, CubicBezier, QuadraticBezier, Arc, Close, PathSegment, Path

# from martsLoggingHandler import handleLogFiles, loggingDir
# import logging

# loggingFile = 'Q2VFileHandler.log'
# fullFileName = loggingDir+'/'+loggingFile
# handleLogFiles(loggingDir, loggingFile, maxCache=5)
# # Configure this module's logger
# logger = logging.getLogger("fileHandler")
# logger.setLevel(logging.INFO)

# # Log to its own file
# file_handler = logging.FileHandler(fullFileName)
# file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# logger.addHandler(file_handler)

# # Avoid double logging if added to root
# logger.propagate = False
from app.core.martsLoggingHandler import get_logger

# You can optionally pass the shared status handler if MainWindow provides it
logger = get_logger(__name__)



# logging.basicConfig(filename=fullFileName, 
#                     format="%(asctime)s %(message)s", 
#                     encoding="utf-8", 
#                     level=logging.DEBUG, 
#                     datefmt="%Y-%m-%d %H:%M:%S", 
#                     force=True)


'''
Two possible ways of handling the file:
Option 1 (DocumentManager as a Container) if:

    You have a small to medium number of pages.
    You frequently switch between pages and need quick access.
    Memory usage isn't a concern.
Pros:

    Direct access to all QGraphicsScene objects for efficient management.
    Easier serialization since all scenes are stored in one place.
    Simpler navigation between pages.
Cons:
    Memory usage can be higher if all pages are loaded at once.
    If you have a large document, managing many QGraphicsScene objects in memory could be inefficient.

Option 2 (SceneLoader Class) if:

    You have a large document with many pages.
    You want to optimize memory usage by loading only one page at a time.
    You don't need frequent page switching.
Pros:
    More memory-efficient, as only the current page is loaded into memory.
    Ideal for large projects with many pages.

Cons:
    Slightly more complex as you need to handle scene swapping.
    If switching between pages frequently, it may introduce small delays.

For now we are going to try and implement option 1. If this turns out to be too heavy for users, I will rebuilt to option 2. To make this easier I should make the fileHandler as flexible as possible and move most functions into generally named functions (including flipping page functions etc.)

'''

#######
# OLD #
#######
# def pathLayerFromShapes(shapes: QGraphicsItemGroup):
#     pass

# def vectorFromShapes(shapes: QGraphicsItemGroup):
#     pass

# class vectorPage(QGraphicsScene):
#     def __init__(self, parent, shapes: QGraphicsItemGroup, img:Image):
#         super().__init__(self, parent)
#         self.shapes = shapes
#         self.img = img
#         self.setOriginalImage()
#         self.setPathLayer()
#         self.setVectorLayer()
#     @classmethod
#     def fromSVG(self, inSVG):

#         svg = sM.SVGobject.fromXMLElementTree(inSVG)
#         paths = svg.paths 
#         return self

#     def toSVG(self):
#         outSVG = ''
#         return outSVG
#     def draw(self):
#         pass

#     def updateShapes(self, shapes):
#         self.shapes = shapes
#         self.setPathLayer()
#         self.setVectorLayer()

#     def setPathLayer(self):
#         self.pathLayer = pathLayerFromShapes(self.shapes)
#     def setVectorLayer(self, vectorLayer):
#         self.vectorLayer = vectorFromShapes(self.shapes)
#     def setOriginalImage(self, img):
#         if img:
#             self.img = img
#         self.imgLayer = self.img

# class fileHandler:
#     def __init__(self, pages:dict[str:vectorPage]):
#         self.pages = pages

#     @classmethod
#     def loadFile(self, filePath):
#         with open(filePath, 'r') as infile:
#             inxml =  ET.fromstring(infile.read())
#         root = inxml.root
#         for page in root.iterfind('vectorPage'):
#             self.pages[page.index](vectorPage.fromSVG(page))
#         return self
    
#     def saveFile(self, fileName, filePath):
#         root = ET.Element()
#         root.set('version', version)
#         root.tag = 'Quil2VecFileContainer'
#         for index, page in self.pages.items():
#             pageElement = ET.Element('vectorPage', {'index':index})
#             pageElement.text = page.toSVG()
#             root.append(pageElement)
#         outXML = ET.ElementTree(root)

#         with open(filePath+fileName, 'w') as outfile:
#             outXML.write(outfile)
        
    
#     def flipPage(self, currIndex):
#         pass

#     def getPage(self, index):
#         return self.pages[index]
    
#     def __getitem__(self, index):
#         return self.pages[index]

#     def __setitem__(self, index, page):
#         self.pages[index] = page
    
#     def __delitem__(self, index):
#         del self.pages[index]

class shapeTest:
    def __init__(self, path):
        self.path = path
    @classmethod
    def fromPath(self, path):
        return self(path)
    def toPath(self):
        if type(self.path) == str:
            return self.path
        elif type(self.path) == svg.path.Path:
            return self.d()
        else:
            return str(self.path)
class CommandNotSupportedError(Exception):
    pass

class Quil2VecVectorPath(Path):
    '''
    Acts as the main translator between each version of the path object (SVG, QGraphicsItem) and acts as the cannoncial shape all other represenations of the shape refer back to
        - this allows this class to handle saving and loading of data
    REMINDER TO ALWAYS UPDATE TO AND FROM THIS OBJECT WHEN RENDERING/EXPORTING/LOADING
    '''
    # to do, maybe, handle pen and colour stuff here
    def __init__(self, *segments):
        super().__init__(*segments)
        if any([isinstance(segment, Arc) for segment in self._segments]):
            raise CommandNotSupportedError('Command Arc not supported in Vector Path')
        for seg in segments:
            if type(seg) == str:
                logger.info(f'Segment as string in Quil2VecVectorPath: {seg}')
                print(seg)
    @classmethod
    def fromSVG(self, d:str):
        '''Takes SVG path (d attribute) and parses that path'''
        return self(parse_path(d))
    # @classmethod
    # def from_qpath(self, QPath:Quil2VecQPathItem):

    #     pass
    def append(self, value):
        self._segments.append(value)

    def paintToQPath(self, painter:QPainterPath):
        for segment in self._segments:
            if isinstance(segment, Move):
                painter.moveTo(segment.start.real, segment.start.imag)
            elif isinstance(segment, Line):
                painter.lineTo(segment.end.real, segment.end.imag)
            elif isinstance(segment, CubicBezier):
                painter.cubicTo(
                    segment.control1.real, segment.control1.imag,
                    segment.control2.real, segment.control2.imag,
                    segment.end.real, segment.end.imag
                )
            elif isinstance(segment, QuadraticBezier):
                painter.quadTo(
                    segment.control.real, segment.control.imag,
                    segment.end.real, segment.end.imag
                )
            elif isinstance(segment, Close):
                painter.closeSubpath()
            else:
                raise CommandNotSupportedError(f'unsupported path: {segment}')
        return painter
    
    def to_qpath(self):
        path_item = QPainterPath()
        out_segments = []
        for segment in self._segments:
            if isinstance(segment, Move):
                path_item.moveTo(segment.start.real, segment.start.imag)
                # out_segments.append((QPainterPath().moveTo(segment.start.real, segment.start.imag), segment))
            elif isinstance(segment, Line):
                path_item.lineTo(segment.end.real, segment.end.imag)
                new_segment = QPainterPath()
                new_segment.moveTo(segment.start.real, segment.start.imag)
                new_segment.lineTo(segment.end.real, segment.end.imag)
                out_segments.append((new_segment, segment))
            elif isinstance(segment, CubicBezier):
                path_item.cubicTo(
                    segment.control1.real, segment.control1.imag,
                    segment.control2.real, segment.control2.imag,
                    segment.end.real, segment.end.imag
                    )
                new_segment = QPainterPath()
                new_segment.moveTo(segment.start.real, segment.start.imag)
                new_segment.cubicTo(
                            segment.control1.real, segment.control1.imag,
                            segment.control2.real, segment.control2.imag,
                            segment.end.real, segment.end.imag
                        )
                out_segments.append(
                    (
                        new_segment, segment
                    )
                )
                
            elif isinstance(segment, QuadraticBezier):
                path_item.quadTo(
                    segment.control.real, segment.control.imag,
                    segment.end.real, segment.end.imag
                )
                new_segment = QPainterPath()
                new_segment.moveTo(segment.start.real, segment.start.imag)
                new_segment.quadTo(
                            segment.control.real, segment.control.imag,
                            segment.end.real, segment.end.imag
                        )
                out_segments.append(
                    (
                        new_segment, segment
                    )
                )
            # https://github.com/inkcut/inkcut/issues/45
            # For some reason Qt's arcTo is not using the same format as SVG Arc. In all applications Arc's seem to be converted to something else. 
            # I have decided to just not support Arcs..... 
            # elif isinstance(segment, Arc):
            #     path_item.arcTo(
            #         QRect()
            #     )
            elif isinstance(segment, Close):
                path_item.closeSubpath()
            else:
                raise CommandNotSupportedError(f'unsupported path: {segment}')
            
        # outpath = Quil2VecQPathItem(path_item, self, out_segments)
        
        return path_item, out_segments
        # logger.info(f'Outsegments: {str(out_segments)}')
        # return QPainterPath(), out_segments
    def to_svg(self) -> ET.Element:
        d = self.d()
        outSVG = ET.Element('path', {'d':d})
        return outSVG
    
    def update_control_point(self, segment_index, point_index, new_pos):
        """Update the internal SVG Path for one control point."""
        logger.info(f"Translator updating segment {segment_index} point {point_index} to {new_pos}")

        # Assuming segment_data[segment_index] is a CubicBezier or similar
        segment = self.segments[segment_index]

        if isinstance(segment, svg.path.CubicBezier):
            points = [segment.start, segment.control1, segment.control2, segment.end]
            points[point_index] = complex(new_pos.x(), new_pos.y())
            segment.start, segment.control1, segment.control2, segment.end = points
        elif isinstance(segment, svg.path.Line):
            if point_index == 0:
                segment.start = complex(new_pos.x(), new_pos.y())
            else:
                segment.end = complex(new_pos.x(), new_pos.y())
        else:
            logger.warning(f"Unknown segment type {type(segment)}")

        # Update cached path representation
        # self.rebuild_qpath()

    def update_segment(self, index, updated_segment):
        logger.info(f"Translator updating segment {index}")
        self._segments[index] = updated_segment
        self.rebuild_qpath()
    
    def rebuild_qpath(self):
        """Rebuild the QPainterPath representation of the SVG Path."""
        # self.qpath, self.out_segments = self.to_qpath()
        pass
        # logger.info(f"Rebuilt QPainterPath: {self.qpath}, Out segments: {self.out_segments}")

    ##################
    # Tools handling #
    ##################
    def cut_path(self, cut_point1, cut_point2):
        pass
        '''
        Should, somehow, have the following return structure
        (
            (
                newVectorPath, newQVectorPath
            ),
            (
                newVectorPath, newQVectorPath
            )
        )
        Problem: circular importing... The file containing the QVectorPath classes will likely have to import this file....
        '''

class Quill2VecFileLayer:
    def __init__(self, name:str, visible=True, active = False, opacity = 100):
        self.name = name
        # self.paths = paths
        self.visible = visible
        self.active = active
        self.opacity = opacity
    @classmethod
    def fromSVGFile(self, insvg, name):
        # paths = []
        # name = insvg.attrib['id']
        _visible = int(insvg.attrib['visible'])
        if _visible == 1:
            visible = True
        else:
            visible = False
        _active = int(insvg.attrib['active'])
        if _active == 1:
            active = True
        else:
            active = False
        # for path in insvg.findall('path'):
        #     paths.append(Quil2VecVectorPath.fromSVG(path.attrib['d']))
        opacity = int(insvg.attrib['opacity'])
        return self(name,visible, active, opacity)
    def toSVGFile(self, layerID):
        if self.visible:
            _visible = 1
        else:
            _visible = 0
        if self.active:
            _active = 1
        else:
            _active = 0
        outSVG = ET.Element('layer', {'id':layerID, 'visible': str(_visible), 'active':str(_active), 'opacity':str(self.opacity)})
        for path in self.paths:
            outSVG.append(path.to_svg())
        return outSVG
    def toggle_visibility(self):
        self.visible = not self.visible
    
    # def add_path(self, vector_path:Quil2VecVectorPath):
    #     self.paths.append(vector_path)

class Quil2VecImage(Quill2VecFileLayer):
    def __init__(self, x, y, width, height, filepath, visible, loadedImage:QPixmap| None = None, name= "Original Image",  active = False, opacity = 100):
        super().__init__(name, visible, active, opacity)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.filepath = filepath
        # self.visible = visible
        self.loadedImage = loadedImage

        # self.backgroundImage = backgroundImage
    @classmethod
    def fromSVGImage(self, inSVG):
        x = inSVG.attrib['x']
        y = inSVG.attrib['y']
        width = inSVG.attrib['width']
        height = inSVG.attrib['height']
        filepath = inSVG.attrib['path']
        visible = True if inSVG.attrib['BackgroundVisibilty'] == "1" else False
        opacity = int(inSVG.attrib['BackgroundOpacity']) 
        return self(x, y, width, height, filepath, visible, opacity=opacity)#, Quilll2VecBackgroundImage.fromLoadState(filepath, backgroundVisibility))
    def toSVGImage(self):
        attribs = {
            'x' : self.x,
            'y' : self.y,
            'width' : self.width,
            'height' : self.height,
            'path' : self.filepath,
            'BackgroundVisibilty' : "1" if self.visible else "0",
            "BackgroundOpacity" : str(self.opacity)# self.backgroundImage.visibile
        }
        return ET.Element('image', attribs)
    
    def aspect_ratio(self):
        '''Returns the aspect ratio of the image'''
        if not self.loadedImage:
            self.loadImage()
        aspect_ratio = self.loadedImage.width() / self.loadedImage.height()
        return aspect_ratio
    
    def getImageSize(self):
        '''Returns the size of the image as a tuple (width, height)'''
        if not self.loadedImage:
            self.loadImage()
        return (self.loadedImage.width(), self.loadedImage.height())
    
    def loadImage(self):
        '''Loads the image from the filepath and returns a QPixmap'''
        return QPixmap(self.filepath)
    
# class Quill2VecImageLayer(Quill2VecFileLayer):
#     def __init__(self, name, image:Quil2VecImage, visible=True, active=False, opacity=100):
#         super().__init__(name, visible, active, opacity)
#         self.image = image  # This should be a Quil2VecImage object

class Quill2VecPathLayer(Quill2VecFileLayer):
    def __init__(self, name, paths:list[Quil2VecVectorPath], visible=True, active=False, opacity=100):
        super().__init__(name, visible, active, opacity)
        self.paths = paths  # This should be a list of Quil2VecVectorPath objects

    @classmethod
    def fromSVGFile(self, insvg, name):
        paths = []
        _visible = int(insvg.attrib['visible'])
        if _visible == 1:
            visible = True
        else:
            visible = False
        _active = int(insvg.attrib['active'])
        if _active == 1:
            active = True
        else:
            active = False
        opacity = int(insvg.attrib['opacity'])
        for path in insvg.findall('path'):
            paths.append(Quil2VecVectorPath.fromSVG(path.attrib['d']))
        return self(name, paths, visible, active, opacity)

    def add_path(self, vector_path:Quil2VecVectorPath):
        self.paths.append(vector_path)

class Quill2VecFileSettings:
    def __init__(self, background, pageFocus, zoom, coordinates):
        self.background = background
        self.pageFocus = pageFocus
        self.zoom = zoom
        self.coordinates = coordinates
    @classmethod
    def fromSVGSettings(self, inSVG):
        background = inSVG.attrib['background']
        pageFocus = inSVG.attrib['pageFocus']
        zoom = inSVG.attrib['zoom']
        coordinates = inSVG.attrib['coordinates']
        return self(background, pageFocus, zoom, coordinates)
    def toSVGSettings(self):
        attribs = {
            'background':self.background,
            'pageFocus':self.pageFocus,
            'zoom':self.zoom,
            'coordinates':self.coordinates
        }
        return ET.Element('settings', attribs)
    
class Quill2VecPage:
    def __init__(self, layers:dict[str:Quill2VecFileLayer], image:Quil2VecImage):
        self.layers = layers
        self.image = image

        # self.settings = settings
    @classmethod
    def fromSVGFIle(self, inSVG:str):
        # root = ET.fromstring(inSVG).getroot()
        layers = {}
        for layer in inSVG.findall('layer'):
            name = layer.attrib['id']
            layers[name] = Quill2VecPathLayer.fromSVGFile(layer, name)
        image = Quil2VecImage.fromSVGImage(inSVG.find('image')) 
        # settings = Quill2VecFileSettings.fromSVGSettings(root.find('settings'))
        return self(layers, image)#, settings)
    
    def toSVGfile(self, pageIndex):
        outSVG = ET.Element('page', {'pageIndex':pageIndex})
        for layerID, layer in self.layers.items():
            outSVG.append(layer.toSVGFile(layerID))
        outSVG.append(self.image.toSVGImage())
        return outSVG
        
class Quill2VecSaveFile:
    def __init__(self, filename:str,version:str,createTimeStamp:str,lastEditTimeStamp:str,encoding:str, pages:dict[str:Quill2VecPage], settings:Quill2VecFileSettings, projectName:str):
        self.filename = filename
        self.version = version
        self.createTimeStamp = createTimeStamp
        self.lastEditTimeStamp = lastEditTimeStamp
        self.encoding = encoding
        self.pages = pages
        self.settings = settings
        self.projectName = projectName

    @classmethod
    def fromSave(self, save, filename:str):
        root = ET.fromstring(save)
        version = root.attrib['version']
        encoding = root.attrib['encoding']
        pages = {}
        for page in root.findall('page'):
            pages[page.attrib['pageIndex']] = Quill2VecPage.fromSVGFIle(page)
        settings = Quill2VecFileSettings.fromSVGSettings(root.find('settings'))
        projectName = root.attrib['projectName']
        return self(filename,version,encoding, pages, settings, projectName)
    def updateCanvas(self, MainWindow):
        MainWindow.svgEditorScene.fromFile(MainWindow)
        # MainWindow.svgView.setScene(self.svgEditorScene)
    def toSave(self, savePath=None):
        if not savePath:
            savePath = self.filename
        # outXML = ET.ElementTree()
        atribs = {
            'version':self.version,
            'createDate':self.createTimeStamp,
            'lastEdit':self.lastEditTimeStamp,
            'encoding':self.encoding,
            'projectName':self.projectName
        }
        rootElement = ET.Element( 'Quill2VecFile', atribs)
        settingsElement = self.settings.toSVGSettings()
        rootElement.append(settingsElement)
        for pageIndex, page in self.pages.items():
            # pageElement = ET.Element('page', {'path':pagePath})
            pageElement = page.toSVGfile(pageIndex)
            rootElement.append(pageElement)
        outXML = ET.ElementTree(rootElement)
        ET.indent(outXML, space="\t", level=0)
        try:
            with open(savePath, 'wb') as outFile:
                outXML.write(outFile, xml_declaration=False)
        except:
            try:
                with open(savePath, 'w') as outFile:
                    outXML.write(outFile, xml_declaration=False)
                print('saved with w')
                logger.error('saved XML with \'w\'')
            except:
                try:
                    with open(savePath, 'w') as outfile:
                        outFile.write(str(outXML))
                    logger.error('saved XML with force stringing')
                    print('saved XML with force stringing')
                except:
                    import pickle
                    with open('ERRORPICKLE.pypickle', 'wb') as outFile:
                        pickle.Pickler(outFile).dump(outXML)
                    logger.error('saved XML to: \'ERRORPICKLE.pypickle\'')
                    print('saved XML with force stringing')
    def updateVersion(self, newVersion=version):
        '''Should become the handler to make sure to verify difference between verions if necessary'''
        self.version = newVersion
    def getCurrentPage(self):
        returnPage = self.pages[self.settings.pageFocus]
        return returnPage
    def nextPage(self, returnPage = True):
        pageFlag = False
        for id in self.pages.keys():
            if pageFlag:
                self.settings.pageFocus = id
                if returnPage:
                    return self.pages[id]
            elif id == self.settings.pageFocus:
                pageFlag = True
    def previousPage(self, returnPage = True):
        pageFlag = False
        for id in reversed(self.pages.keys()):
            if pageFlag:
                self.settings.pageFocus = id
                if returnPage:
                    return self.pages[id]
            elif id == self.settings.pageFocus:
                pageFlag = True
    def goToPage(self, pageID):
        self.settings.pageFocus=pageID
        return self.pages[pageID]
    
    def generateLayerHandles(self):
        pass
#########################################################
# Functions to handle the file conversions              #
# Import image turn it into a Quil2VecSaveFile          #
# Known issues:                                         #
# - currently outputs way too few paths                 #
# - doesnt handle the QGraphicsScene yet                #
#########################################################

