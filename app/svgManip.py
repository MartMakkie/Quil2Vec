import xml.etree.ElementTree as ET
import numpy as np
from math import ceil
import math
# from eulxml import xmlmap
from svg.path import parse_path
from svg.path import path as pt
from svg.path import Path as SVGpath
import svg.path
from IPython.display import SVG, display
from io import StringIO

from typing import Literal
# from svg.path import path
from svg.path.parser import _tokenize_path


def iterSVGETreePaths(root):
    
    for child in root:
        if child.tag == 'path':
            yield child
        else:
            yield from iterSVGETreePaths(child)

def showPath(path: SVGpath):
    viewbox = ''
    for thing in path.boundingbox():
        viewbox+=f' {str(ceil(thing))}'

    # SVG(f'<path d=\" {path.d()} \" />')
    # display(SVG(f'<svg     viewBox="0 0 2261.81 3290.89"><path d=\" {path.d()} \" /></svg>'))
    display(SVG(f'<svg viewBox="{viewbox}"><path d=\" {path.d()} \" /></svg>'))

class SVGobject():
    def __init__(self, header:dict, paths:list[SVGpath]):
        self.header = header
        self.paths = paths
    @classmethod
    def fromXMLElementTree(cls, root: ET.Element):
        # root = inputObject.getroot()
        if root.tag != 'svg':
            print('cannot parse xml, please remove namespace or make sure root.tag == \'svg\'')
        header = root.attrib
        paths = []
        for path in iterSVGETreePaths(root):
            paths.append(parse_path(path.attrib['d']))
        return cls(header = header, paths = paths)
    @classmethod
    def convertSegmentsToPaths(cls, inobj):
        paths = []
        for path in inobj.paths:
            path: SVGpath
            for _path in parse_path_segments(path):
                paths.append(_path)
        #     thisPath = SVGpath()
        #     for segment in path._segments:
        #         if type(segment) == svg.path.Move:
        #             if len(thisPath)!=0:
        #                 # thisPath = tuple(thisPath)
        #                 paths.append(SVGpath(thisPath))
        #             thisPath = [segment]
        #         else:
        #             thisPath.append(segment)
        #     # paths.append(SVGpath(tuple(thisPath)))
        #     paths.append(SVGpath(thisPath))
        # # paths = tuple(paths)
        return cls(inobj.header, paths)

    def exportSVG(self):
        outstr = '<svg '
        for key, item in self.header.items():
            if 'namespace' in item:
                # print(key, item)
                # item = 'xml:'
                continue
            elif 'namespace' in key:
                # print(key, item)
                # key = 'xml:'
                continue
            outstr+=f' {key} = \"{item}\"'
        outstr+='>'
        for path in self.paths:
            outstr+=f'<path d=\" {path.d()} \" />'
            # print(path.d())
            # break
        outstr+='</svg>'
        return SVG(outstr) #utstr # SVG(outstr)
    
def parse_path_segments(inpath):
    if type(inpath) == pt.Path:
        pathdef = inpath.d()
    elif type(inpath) ==  str:
        pathdef = inpath
    else:
        # raise f'inpath of type {type(inpath)} not supported by parse_path_segments()'
        print(f'inpath of type {type(inpath)} not supported by parse_path_segments()')
    outpaths = []
    segments = pt.Path()
    start_pos = None
    last_command = None
    current_pos = 0

    for token in _tokenize_path(pathdef):
        command = token[0]
        relative = command.islower()
        command = command.upper()
        if command == "M":
            if len(segments) != 0:
                outpaths.append(segments)
                segments = pt.Path()
            pos = token[1]
            if relative:
                current_pos += pos
            else:
                current_pos = pos
            segments.append(pt.Move(current_pos, relative=relative))
            start_pos = current_pos

        elif command == "Z":
            # For Close commands the "relative" argument just preserves case,
            # it has no different in behavior.
            segments.append(pt.Close(current_pos, start_pos, relative=relative))
            current_pos = start_pos

        elif command == "L":
            pos = token[1]
            if relative:
                pos += current_pos
            segments.append(pt.Line(current_pos, pos, relative=relative))
            current_pos = pos

        elif command == "H":
            hpos = token[1]
            if relative:
                hpos += current_pos.real
            pos = complex(hpos, current_pos.imag)
            segments.append(
                pt.Line(current_pos, pos, relative=relative, horizontal=True)
            )
            current_pos = pos

        elif command == "V":
            vpos = token[1]
            if relative:
                vpos += current_pos.imag
            pos = complex(current_pos.real, vpos)
            segments.append(
                pt.Line(current_pos, pos, relative=relative, vertical=True)
            )
            current_pos = pos

        elif command == "C":
            control1 = token[1]
            control2 = token[2]
            end = token[3]

            if relative:
                control1 += current_pos
                control2 += current_pos
                end += current_pos

            segments.append(
                pt.CubicBezier(
                    current_pos, control1, control2, end, relative=relative
                )
            )
            current_pos = end

        elif command == "S":
            # Smooth curve. First control point is the "reflection" of
            # the second control point in the previous path.
            control2 = token[1]
            end = token[2]

            if relative:
                control2 += current_pos
                end += current_pos

            if last_command in "CS":
                # The first control point is assumed to be the reflection of
                # the second control point on the previous command relative
                # to the current point.
                control1 = current_pos + current_pos - segments[-1].control2
            else:
                # If there is no previous command or if the previous command
                # was not an C, c, S or s, assume the first control point is
                # coincident with the current point.
                control1 = current_pos

            segments.append(
                pt.CubicBezier(
                    current_pos, control1, control2, end, relative=relative, smooth=True
                )
            )
            current_pos = end

        elif command == "Q":
            control = token[1]
            end = token[2]

            if relative:
                control += current_pos
                end += current_pos

            segments.append(
                pt.QuadraticBezier(current_pos, control, end, relative=relative)
            )
            current_pos = end

        elif command == "T":
            # Smooth curve. Control point is the "reflection" of
            # the second control point in the previous path.
            end = token[1]

            if relative:
                end += current_pos

            if last_command in "QT":
                # The control point is assumed to be the reflection of
                # the control point on the previous command relative
                # to the current point.
                control = current_pos + current_pos - segments[-1].control
            else:
                # If there is no previous command or if the previous command
                # was not an Q, q, T or t, assume the first control point is
                # coincident with the current point.
                control = current_pos

            segments.append(
                pt.QuadraticBezier(
                    current_pos, control, end, smooth=True, relative=relative
                )
            )
            current_pos = end

        elif command == "A":
            # For some reason I implemented the Arc with a complex radius.
            # That doesn't really make much sense, but... *shrugs*
            radius = complex(token[1], token[2])
            rotation = token[3]
            arc = token[4]
            sweep = token[5]
            end = token[6]

            if relative:
                end += current_pos

            segments.append(
                pt.Arc(
                    current_pos, radius, rotation, arc, sweep, end, relative=relative
                )
            )
            current_pos = end

        # Finish up the loop in preparation for next command
        last_command = command
    outpaths.append(segments)
    
    return outpaths

def tupleToComplex(intuple:tuple):

    return complex(intuple[0], intuple[1])

def complexToTuple(inComplexNumber:complex):
    return (inComplexNumber.real, inComplexNumber.imag)

def _sortPathGroups(segments, i1, i2, outCurve1, outCurve2, outCurve3, outCurve4):
    group3 = segments[:i1] + [outCurve1]
    group2 = [outCurve2] + segments[i1+1:i2-1] + [outCurve3]
    group1 = segments[i2+1:] + [outCurve4]
    outGroup1 = group3 + group1
    outGroup2 = group2
    return outGroup1, outGroup2

def sortPathGroups(segments, i1, i2, outCurve1, outCurve2, outCurve3, outCurve4):
    # pt.Line(start=complex(point[0], point[1])
    if i1<i2:
        _group1, _group2 = _sortPathGroups(segments, i1, i2, outCurve1, outCurve2, outCurve3, outCurve4)
    else:
        _group1, _group2 = _sortPathGroups(segments, i2, i1, outCurve3, outCurve4, outCurve1, outCurve2)
    if len(_group1) <= len(_group2):
        group1 = []
        for seg in _group1:
            if seg != None:
                group1.append(seg)
        group2 = []
        for seg in _group2:
            if seg != None:
                group2.append(seg)
        # group1, group2 = _group1, _group2
    else:
        group1 = []
        for seg in _group2:
            if seg != None:
                group1.append(seg)
        group2 = []
        for seg in _group1:
            if seg != None:
                group2.append(seg)
        # group1, group2 = _group2, _group1
    return group1, group2
    
def bezier_to_points(p1, p2, p3, p4, segments: int = 10):
    for t in np.linspace(0, 1, num=segments):
        x = (
            p1[0] * math.pow(1 - t, 3)
            + 3 * p2[0] * math.pow(1 - t, 2) * t
            + 3 * p3[0] * (1 - t) * math.pow(t, 2)
            + p4[0] * math.pow(t, 3)
        )
        y = (
            p1[1] * math.pow(1 - t, 3)
            + 3 * p2[1] * math.pow(1 - t, 2) * t
            + 3 * p3[1] * (1 - t) * math.pow(t, 2)
            + p4[1] * math.pow(t, 3)
        )
        yield (x, y), t

def determineMovement(point1: tuple, point2: tuple, margin = 2) -> Literal['vertical','horizontal','no movement']:
    # if point1[0] > point2[0]+margin and not  point1[1] > point2[1]+margin:
    #     return 'horizontal'
    # elif point1[1] > point2[1]+margin and not  point1[0] > point2[0]+margin:
    #     return 'vertical'
    # elif point1[1] > point2[1]+margin and point1[0] > point2[0]+margin:
    #     return 'both'
    # else:
    x_movement = point1[0] - point2[0]
    if x_movement<0:
        x_movement = x_movement*-1
    y_movement = point1[1] - point2[1]
    if y_movement<0:
        y_movement = y_movement*-1
    if x_movement > y_movement:
        return 'horizontal'
    elif x_movement < y_movement:
        return 'vertical'
    else:
        return 'no movement'

def determineMovementAsInt(point1:tuple, point2:tuple):
    x_movement = point1[0] - point2[0]
    if x_movement<0:
        x_movement = x_movement*-1
    y_movement = point1[1] - point2[1]
    if y_movement<0:
        y_movement = y_movement*-1
    total_movement = x_movement+y_movement
    total_movement = total_movement*0.5
    # if total_movement<0:
    #     total_movement=total_movement*-1
    return (x_movement, y_movement, total_movement)

def compareSingCoordinates(coordinate1: float, coordinate2: float, margin = 1):
    coordinate_sum1 = coordinate1-coordinate2
    # coordinate_sum2 = coordinate2-coordinate1
    if coordinate_sum1 < 0:
        coordinate_sum1 = coordinate_sum1*-1
    if coordinate_sum1 < margin:
        return True
    else:
        return False
    
def iterOverPoints(path: pt.Path|list, intervals = 10):
    # points = []
    if type(path) == pt.Path:
        for i, segment in enumerate(path._segments):
            movement = determineMovement((segment.start.real, segment.start.real.imag), (segment.end.real, segment.end.real.imag))
            for point in iterOverPointsinSegment(segment, intervals):
                yield point, segment, i,movement
    else:
        for i, segment in enumerate(path):
            movement = determineMovement((segment.start.real, segment.start.real.imag), (segment.end.real, segment.end.real.imag))
            for point in iterOverPointsinSegment(segment, intervals):
                yield point, segment, i, movement
    # for segment in path._segments:
    #     if type(segment) == pt.Linear:
    #         points.append(segment.start) 
    #         points.append(segment.end)
    #     elif type(segment) == pt.CubicBezier:
    #         points.append(segment.start) 
    #         points.append(segment.control1)
    #         points.append(segment.control2)
    #         points.append(segment.end)
    #     elif type(segment) == pt.QuadraticBezier:
    #         points.append(segment.start) 
    #         points.append(segment.control)
    #         points.append(segment.relative)
    #         points.append(segment.end)
    #     else:
    #         raise KeyError    
    # for point in points:
    #     yield point

def cutBezierCurve(incurve:pt.CubicBezier, tCut: complex | tuple, segments: int = 10):
    '''
    segments must be equal to segments used in bezier_to_points()
    '''
    A = complexToTuple(incurve.start)
    P = complexToTuple(incurve.control1)
    Q = complexToTuple(incurve.control2)
    G = complexToTuple(incurve.end)
    if type(tCut) == complex:
        D = complexToTuple(tCut)
    else:
        D = tCut
    # find u and v, u == t(?)
    t = tCut
    u = t
    v = 1-u
    B = (u * P[0] + v * A[0], u * P[1] + v * A[1])
    F = (u * G[0] + v * Q[0], u * G[1] + v * Q[1])
    H = (u * Q[0] + v * P[0], u * Q[1] + v * P[1])
    C = (u * H[0] + v * B[0], u * H[1] + v * B[1])
    E = (u * F[0] + v * H[0], u * F[1] + v * H[1])
    D = (u * E[0] + v * C[0], u * E[1] + v * C[1])

    outCurve1 = pt.CubicBezier(tupleToComplex(A), tupleToComplex(B), tupleToComplex(C), tupleToComplex(D))
    outCurve2 = pt.CubicBezier(tupleToComplex(D), tupleToComplex(E), tupleToComplex(F), tupleToComplex(G))

    return outCurve1, outCurve2

def iterOverPointsinSegment(segment: pt.PathSegment, intervals = 10):
    points = []
    if issubclass(type(segment), pt.Linear):
        start = (segment.start.real, segment.start.imag)
        end = (segment.end.real, segment.end.imag)
        # on a line segment, start is always t == 0 and end is always t == 1
        # add it just for compatibilities sake
        points.append((start, 0)) 
        points.append((end, 1))
    elif type(segment) == pt.CubicBezier:
        start = (segment.start.real, segment.start.imag)
        end = (segment.end.real, segment.end.imag)
        control1 = (segment.control1.real, segment.control1.imag)
        control2 = (segment.control2.real, segment.control2.imag)
        for x, t in bezier_to_points(
                        start,
                        control1,
                        control2,
                        end, intervals
                    ):
            
            points.append((x, t))
    elif type(segment) == pt.QuadraticBezier:
        raise KeyError
        points.append(segment.start) 
        points.append(segment.control)
        points.append(segment.relative)
        points.append(segment.end)
    elif type(segment) == pt.Move:
        start = (segment.start.real, segment.start.imag)
        points.append((start, 0))
    # elif type(segment) == pt.Close:
    #     points.append(segment.)
    else:
        print(type(segment))
        raise KeyError    
    for point in points:
        yield point

def filterGroups(possibleGroups):
    filteredGroups = []#[list, list]
    userGroups = {} # version which uses the groups as key and decStr as list of decstrs. Then we convert that to a list based on key, item-- no, problems with using lists as keys. So we use a string version of list as key, but since we cannot eval that back due to python wanting to convert it into a Move object (among other things), we will simply store the group, strdesc as a tuple to then turn back into a list, ignoring the stringyfied group key
    for group in possibleGroups:
        if not str(group) in list(userGroups.keys()):
            userGroups[str(group)] = group
    for key, item in userGroups.items():
        filteredGroups.append(item)
    return filteredGroups

def displayGroups(possibleGroups):
    for group in possibleGroups:
        if len(group) !=0:
            if type(group[0])!= pt.Move:
                todrop = None
                while any([type(x)== pt.Move for x in group]):
                    for i, _elememnt in enumerate(group):
                        if type(_elememnt) == pt.Move:
                            todrop = i
                            break
                    if todrop != None:
                        del group[i]
                group[:0] = [pt.Move(group[0].start)]
            topdropz = None
            for i2, _elememnt in enumerate(group):
                if type(_elememnt) == pt.Close:
                    topdropz = i2
            if topdropz!=None:
                del group[topdropz]

            displayPath = pt.Path()
            for mem in group:
                displayPath.append(mem)
            print(displayPath)
            displayGroup = SVG(f'<svg><path d = \"{displayPath.d()}z\"/></svg>') 
      