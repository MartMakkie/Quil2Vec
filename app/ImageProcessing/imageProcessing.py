import numpy as np
import os
from dataclasses import dataclass, asdict
from typing import Tuple
from xml.etree import ElementTree as ET
from PySide6.QtGui import QImage, QPixmap
from typing import List, Literal, Dict
import datetime

# from matplotlib import pyplot as plt 
import os.path as OSPATH
from pathlib import Path as PATH

import pdf2image 
from app.FileHandling.fileHandler import *

import cv2
import potracecffi
from svg.path import path as pt
# from svgManip import SVGobject
from shapely.geometry import Polygon#, LineString
# import svgManip as sM


# from PIL import Image
from rtree import index
# import pyvips


from app.core.martsLoggingHandler import get_logger, createDirCheckNotExist

# You can optionally pass the shared status handler if MainWindow provides it
logger = get_logger(__name__)

@dataclass
class imagePreProcessSettings:
    '''
    - thresholdBlockSize (int): Block size for adaptive thresholding (odd number like 35).
    - thresholdC (int): Constant subtracted from mean in adaptive thresholding.
    - applyClahe (bool): Whether to apply CLAHE (contrast enhancement). Default is True.
    - claheClipLimit (float): Clip limit for CLAHE, higher values enhance contrast more.
    - claheTileGridSize (tuple): Tile grid size for CLAHE (usually (8, 8)).
    - applyBlur (bool): Whether to apply Gaussian blur to reduce noise. Default is True.
    - blurKernelSize (tuple): Kernel size for the Gaussian blur (typically (5, 5)).
    - applyAdaptiveThreshold (bool): Whether to apply adaptive thresholding for binarization. Default is True. Currently not available
    - applyMorphology (bool): Whether to apply morphological cleaning (e.g., noise removal). Default is True.
    - morphologyKernelSize (int): Kernel size for morphological operations (typically 1 or 2).
    - invertImage (bool): Whether to invert the image (black ink on white background). Default is True.
    '''
    thresholdBlockSize:int=35
    thresholdC:int=11
    applyClahe: bool = False
    claheClipLimit:float = 3.0
    claheTileGridSize:Tuple[int,int]=(8,8)
    applyBlur:bool=True
    blurKernelSize:Tuple[int,int]=(5, 5)
    # applyAdaptiveThreshold=True,
    applyMorphology:bool=False
    morphologyKernelSize:int=1
    invertImage:bool=False
    @classmethod
    def loadFromFile(self, loadPath:str):
        with open(loadPath, 'r') as infile:
            inXML = ET.fromstring(infile.read())
        root = inXML.find('imagePreProcessSettings')
        return self(**root.attrib)
    @classmethod
    def loadFromXML(self, inXML:ET.ElementTree):
        root = inXML.find('imagePreProcessSettings')
        return self(**root.attrib)
    def export(self,exportPath:str):
        outRoot = ET.Element('imagePreProcessSettings', asdict(self))
        outxml = ET.ElementTree(outRoot)
        outxml.write(exportPath)

class imagePreview:
    def __init__(self, originalImagePath:str|PATH, settings=imagePreProcessSettings(), uniqueSettings = False):
        self.originalImagePath = originalImagePath
        self.settings = settings
        self.uniqueSettings = uniqueSettings

def getMultiplePresetsFromFile(loadPath:str):
    with open(loadPath, 'r') as infile:
        inXML = ET.fromstring(infile.read())
    outPresets = []
    presets = inXML.findall('imagePreProcessSettings')
    for el in presets:
        settings = el.attrib
        outPresets.append(imagePreProcessSettings(**settings))
    logger.info(f'getMultiplePresetsFromFile: got presets from {loadPath}')
    return outPresets

def binarizeForVectorTracing(
    imagePath:str,
    settings=imagePreProcessSettings()
    # applyClahe=True,
    # claheClipLimit=3.0,
    # claheTileGridSize=(8,8),
    # applyBlur=True,
    # blurKernelSize=(5, 5),
    # # applyAdaptiveThreshold=True,
    # thresholdBlockSize=35,
    # thresholdC=11,
    # applyMorphology=True,
    # morphologyKernelSize=1,
    # invertImage=True
):
    """
    Binarizes an image for preview or further processing with optional preprocessing steps.
    
    Parameters:
    - imagePath (str): Path to the input image.
    - applyClahe (bool): Whether to apply CLAHE (contrast enhancement). Default is True.
    - claheClipLimit (float): Clip limit for CLAHE, higher values enhance contrast more.
    - claheTileGridSize (tuple): Tile grid size for CLAHE (usually (8, 8)).
    - applyBlur (bool): Whether to apply Gaussian blur to reduce noise. Default is True.
    - blurKernelSize (tuple): Kernel size for the Gaussian blur (typically (5, 5)).
    - applyAdaptiveThreshold (bool): Whether to apply adaptive thresholding for binarization. Default is True. Currently not available
    - thresholdBlockSize (int): Block size for adaptive thresholding (odd number like 35).
    - thresholdC (int): Constant subtracted from mean in adaptive thresholding.
    - applyMorphology (bool): Whether to apply morphological cleaning (e.g., noise removal). Default is True.
    - morphologyKernelSize (int): Kernel size for morphological operations (typically 1 or 2).
    - invertImage (bool): Whether to invert the image (black ink on white background). Default is True.
    
    Returns:
    - processedImage (numpy array): The processed binary image ready for further use or preview.
    """
    
    # print(f"Starting binarization with parameters:\n"
    #       f"Apply CLAHE: {applyClahe}, Apply Blur: {applyBlur}, Apply Adaptive Thresholding: {applyAdaptiveThreshold}, "
    #       f"Apply Morphology: {applyMorphology}, Invert Image: {invertImage}")

    # 1. Load image and convert to grayscale

    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    applyClahe = settings.applyClahe
    claheClipLimit = settings.claheClipLimit
    claheTileGridSize = settings.claheTileGridSize
    applyBlur = settings.applyBlur
    blurKernelSize=settings.blurKernelSize
    # applyAdaptiveThreshold=True,
    thresholdBlockSize=settings.thresholdBlockSize
    thresholdC=settings.thresholdC
    applyMorphology=settings.applyMorphology
    morphologyKernelSize=settings.morphologyKernelSize
    invertImage=settings.invertImage
    # 2. Apply CLAHE if selected (Contrast enhancement for faded ink)
    if applyClahe:
        clahe = cv2.createCLAHE(clipLimit=claheClipLimit, tileGridSize=claheTileGridSize)
        img = clahe.apply(img)
    
    # 3. Apply Gaussian blur if selected (reduces noise and helps thresholding)
    if applyBlur:
        img = cv2.GaussianBlur(img, blurKernelSize, 0)

    # 4. Apply adaptive thresholding if selected
    # if applyAdaptiveThreshold:
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=thresholdBlockSize,
        C=thresholdC
    )
    
    # 5. Apply morphological operation if selected (removes noise)
    if applyMorphology:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morphologyKernelSize, morphologyKernelSize))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    # 6. Invert the image if selected (potrace expects black ink on white background)
    ## For some reasong the inversion works the other way around than expected. I can't be bothered to find the actual fix, so I am just doing the opposite as expected
    if not invertImage:
        img = cv2.bitwise_not(img)

    # 7. Save the processed image (optional step for debugging or visualization purposes)
    # os.makedirs(outputDir, exist_ok=True)
    # pbmPath = os.path.join(outputDir, "binarized.pbm")
    # cv2.imwrite(pbmPath, img)

    # print(f"Saved processed image for preview at: {pbmPath}")

    # Return the processed image for further use or preview
    return img

def cv2_to_qpixmap(cvImg):
    if len(cvImg.shape) == 2:
        # Grayscale image
        height, width = cvImg.shape
        bytesPerLine = width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
    
    elif len(cvImg.shape) == 3 and cvImg.shape[2] == 3:
        # Color image (BGR to RGB)
        rgbImage = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        height, width, channels = rgbImage.shape
        bytesPerLine = channels * width
        qImg = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
    
    else:
        raise ValueError("Unsupported image format: must be grayscale or 3-channel BGR")
    
    return QPixmap.fromImage(qImg)


def loadImagesForImport(imagePaths:List[str], fileType:Literal['*.jpg', '.*pdf', '*.png'], projectName:str=None,cacheFolder = '/imageCache'):
    logger.info("loadImagesForImport: entered function")
    outImages = []
    logger.info(f'Importing image from {imagePaths}, fileType: {fileType}')
    for imagePath in imagePaths:
        fileType = PATH(imagePath).suffix
        imName = PATH(imagePath).stem
        
        if fileType == '.jpg' or fileType == '.png':
        # for path in imagePaths:
            outImages.append(imagePreview(imagePath))
        elif fileType == '.pdf':
            createDirCheckNotExist(cacheFolder, logger)
            if not projectName:
                projectName = imagePaths[0]
            cacheDir = PATH(cacheFolder) / projectName
            if not cacheDir.exists():
                cacheDir.mkdir(parents=True, exist_ok=True)
        # for path in imagePaths:
            images = pdf2image.convert_from_path(imName)
            for pageNr, image in enumerate(images):
                savePath = PATH(cacheDir)/imName+str(pageNr+1)
                logger.info(f'Saved image from pdf to cache as {imagePath}')
                image.save(savePath)
                outImages.append(imagePreview(savePath))
    logger.info(f'loadImagesForImport: amount of returned outImages: {len(outImages)}, length of imagePaths: {len(imagePaths)}')
    return outImages

#### For vector tracing:
class PathValidityException(Exception):
    pass

def checkQPathValidity(inList:list[Quil2VecVectorPath]):
    for p in inList:
        # if any([])
        for s in p:
            if isinstance(s, Quil2VecVectorPath):
                # print(p,s)
                raise PathValidityException
def iterSVGETreePaths(root):
       for child in root:
            if child.tag == 'path':
                yield child
            else:
                yield from iterSVGETreePaths(child)

def savePathsToSampleSVGXML(inPaths:list[pt.Path],filename:str, viewbox="0 0 300 300"):
    logger.info(f'Saving a SVG backup as {filename}')
    root = ET.Element('svg', width="100%", height="100%", viewBox=viewbox, version='1.1', xmlns='http://www.w3.org/2000/svg')
    for path in inPaths:
        pathobj = ET.SubElement(root, "path")
        path_desc = path.d()
        pathobj.set('d', path_desc)   
        pathobj.set('fill-rule', 'evenodd')
    tSVG = ET.ElementTree(root)
    tSVG.write(filename)
def pathSorter(svg:ET.Element) -> list[pt.Path]:
# pathcounter = 0
    shapes = []
    logger.info('sorting paths')
    for path in iterSVGETreePaths(svg):
        # shape = []
        paths = parse_path(path.attrib['d'])
        # print(paths)
        # shapes.append(paths)
        # segments = sM.parse_path_segments()
        segments = []
        thisSegment = Quil2VecVectorPath()#pt.Path()#Quil2VecVectorPath()#
        for _path in paths:
        #     command = _tokenize_path(path)[0]
        #     if command == 'C':
        #         thisSegment.insert(-1, path)
        #         segments.append(thisSegment)
        #         thisSegment = pt.Path()
        #     else:
        #         segments.append(thisSegment)
        # for seg in segments:
        #     shapes.append(seg)
            # pathcounter+=1
            if type(_path) == pt.Close or type(_path) == pt.Move:
                if len(thisSegment) != 0:
                    # print(thisSegment)
                    thisSegment.append(_path)
                    # print(thisSegment)
                    segments.append(thisSegment)
                    thisSegment = Quil2VecVectorPath() #pt.Path()# Quil2VecVectorPath()#pt.Path()
                else:
                    thisSegment.append(_path)
                # print(f'close Path {_path}')
            # elif type(_path) == pt.Move:
            #     # print(f'move Path {_path}')
            #     thisSegment.insert(-1, _path)
            #     segments.append(thisSegment)
            #     thisSegment = pt.Path()
            else:
                # print(thisSegment)
                # thisSegment.insert(-1, _path)
                thisSegment.append(_path)
                # print(thisSegment)
        if len(thisSegment) != 0:
            segments.append(thisSegment)
    # print(f'Total amount of commands {pathcounter}')
        for segment in segments:
            shapes.append(segment)
    savePathsToSampleSVGXML(shapes, 'sortedPaths.svg')
    return shapes

def sample_curve(segment, num_samples=10):
    """Returns sampled points along an SVG path segment."""
    return [segment.point(t) for t in np.linspace(0, 1, num_samples)]

def path_to_shapely(svg_path, num_samples=20):
    """Converts an SVG path into a Shapely LineString with sampled Bezier curves."""
    points = []
    
    for seg in svg_path:
        if isinstance(seg, (pt.CubicBezier, pt.QuadraticBezier, pt.Arc)):
            points.extend(sample_curve(seg, num_samples))
        elif isinstance(seg, pt.Line):
            points.append(seg.start)
        else:
            pass
            # print(type(seg))
    
    points.append(svg_path[-1].end)  # Ensure last point is included
    # print(points)
    shapely_obj = Polygon([(p.real, p.imag) for p in points])
    
    return shapely_obj if len(points) > 1 else None  # Ignore single-point paths)

def potracerSVGOutlineToVectorObjects(root):
        #inPaths:list[pt.Path]):
    # start with boundingBox filtering
    
    
    # shapes = [path_to_shapely(parse_path(svg)) for svg in svg_paths]
    shapes = []
    sortedPaths = pathSorter(root)
    checkQPathValidity(sortedPaths)
    # print(len(sortedPaths))
    for path in sortedPaths:
        # print(path)
        shapes.append(path_to_shapely(path))
    # Initialize R-tree index
    # print(shapes[0])
    idx = index.Index()
    for i, shape in enumerate(shapes):
        idx.insert(i, shape.bounds)  # Insert bounding box into R-tree

    overlapping_pairs = set()
    # overlappingIndexes = []
    for i, shape in enumerate(shapes):
        possible_matches = list(idx.intersection(shape.bounds))  # Get nearby paths
        for j in possible_matches:
            if i != j and shape.intersects(shapes[j]):  # Check precise intersection
                overlapping_pairs.add(tuple(sorted((i, j))))  # Store sorted tuple to avoid duplicates
                # overlappingIndexes.append(i)
                # overlappingIndexes.append(j)

    outputPaths = []
    # print(len(sortedPaths))
    # insert the paths which do not intersect
    for ipth, pth in enumerate(sortedPaths):
        if not any(ipth in x for x in overlapping_pairs):
            outputPaths.append(pth)
    pthProcess = {}
    # Group paths together to get a full path again
    for pairs in overlapping_pairs:
        if pairs[0] in pthProcess.keys():
            pthProcess[pairs[0]].append(pairs[1])
        elif pairs[1] in pthProcess.keys():
            pthProcess[pairs[1]].append(pairs[0])
        else:
            pthProcess[pairs[0]] = [pairs[1]]
    # print(pthProcess)
    # print(overlapping_pairs)
    # create full paths from overlapping paths and inserting them into the outputPaths list
    for imainPath, isecondairyPaths in pthProcess.items():
        mainPath = sortedPaths[imainPath]
        for iscnd in isecondairyPaths:
            scnd = sortedPaths[iscnd]
            for s in scnd:
                mainPath.insert(-1, s)
        outputPaths.append(mainPath)
    # print(outputPaths[0])
    # _outPutPaths = []
    # close all the paths
    # print(len(pthProcess))
    for i in range(0,len(outputPaths)):
        # _path:pt.Path
        if type(outputPaths[i][-1])!= pt.Close:
            outputPaths[i].insert(-1, pt.Close(outputPaths[i][-1].end, outputPaths[i][-1].end))
        # _path[-1]
        # _outPutPaths
    # print(len(outputPaths))
    return outputPaths

def traceImage(image):
    trace_result = potracecffi.trace(image) # potrace is used here to perform the trace of the bitmap
    return trace_result

def convertTraceToSVG(trace_result, viewbox="0 0 300 300"):

    root = ET.Element('svg', width="100%", height="100%", viewBox=viewbox, version='1.1', xmlns='http://www.w3.org/2000/svg')
    # root.set("height", str(28))
    # root.set("width", str(28))
    # path_desc = ""
    for i, path in enumerate(potracecffi.iter_paths(trace_result)):
        pathobj = ET.SubElement(root, "path")
        path_desc = ''
        # print(f'Reading path {i}', end = '\r')
        logger.info(f'Reading path {i+1}')
        curveStartPoint = potracecffi.curve_start_point(path.curve)
        path_desc = path_desc + " M " + str(curveStartPoint[0]) + "," + str(curveStartPoint[1])
        for segment in potracecffi.iter_curve(path.curve):
            if segment.tag == potracecffi.CORNER:
                path_desc = path_desc + " L " + str(segment.c1[0]) + "," + str(segment.c1[1]) \
                                + " L " + str(segment.c2[0]) + "," + str(
                        segment.c2[1])
            if segment.tag == potracecffi.CURVETO:
                path_desc = path_desc + " C " + str(segment.c0[0]) + "," + str(segment.c0[1]) + " " + str(
                        segment.c1[0]) + "," + str(segment.c1[1]) + " " + str(segment.c2[0]) + "," + str(
                        segment.c2[1])
        path_desc = path_desc+' Z'
        pathobj.set('d', path_desc)   
        pathobj.set('fill-rule', 'evenodd')
    # print('\r')
    return root

def getViewBoxFromImage(inImage:np.ndarray):#:pyvips.Image):
    width, height = inImage.shape[:2]
    return f"0 0 {width} {height}"

def imageToSVGPaths(image):#: pyvips.Image|cv2.):
    # print('tracing Image')
    logger.info('tracing Image')
    traceResult = traceImage(image)
    logger.info('converting traced image to SVG')
    # print('converting traced image to SVG')
    traceSVG = convertTraceToSVG(traceResult, getViewBoxFromImage(image))
    logger.info('Writing traceSVG to test.svg')
    testxml = ET.ElementTree(traceSVG)
    testxml.write('test.svg')
    logger.info('sorting out paths of image')
    # print('sorting out paths of image')
    SVGPaths = potracerSVGOutlineToVectorObjects(traceSVG)
    checkQPathValidity(SVGPaths)
    return SVGPaths
        
class fileTypeError(Exception):
    pass

def importImageFromPreviewImage(fname:str,previewImages:Dict[str,imagePreview], projectName:str,saveToPath:str|bool):
    logger.info("importImage: entered function")
    print("importImage: entered function")
    try:
        pages = {}
        settings = None# Quill2VecFileSettings('default', '1', '100', "")
        for i, prevImageKeyVal in enumerate(previewImages.items()):
            imageName, prevImage = prevImageKeyVal
            logger.info(f'Processing Image {i+1} of {len(previewImages)}')
            imagePath = prevImage.originalImagePath
            preprocessSettings = prevImage.settings
            # print(f'Processing Image {i+1} of {len(imagePaths)}')
            if not settings:
                logger.info('Setting up settings for first image')
                # print('Setting up settings for first image')
                settings = Quill2VecFileSettings('default', imageName, '100', "")
            # image = pyvips.Image.new_from_file(imagepath)
            imageBinarized = binarizeForVectorTracing(imagePath, preprocessSettings)
            imageSVGPath = imageToSVGPaths(imageBinarized)
            # shapes = [Quil2VecVectorPath(str(shape)) for shape in imageSVGPath]
            layer1 = Quill2VecPathLayer('layer1',imageSVGPath
                                        #shapes
                                        , True, True, 100)
            width, height = imageBinarized.shape[:2]
            _image = Quil2VecImage("0","0",str(width), str(height), imagePath, True)
            pages[imageName] = Quill2VecPage({'layer1':layer1}, _image)
        now = str(datetime.datetime.now())
        saveFile = Quill2VecSaveFile(fname,now,now,version, "utf-8", pages,settings, projectName)
        if saveToPath:
            saveFile.toSave(saveToPath)
        else:
            return saveFile
    except Exception as e:
        logger.error(f"Error during image import: {e}", exc_info=True)
        raise
