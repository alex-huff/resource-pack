import os
import math
import sys
from functools import lru_cache
from PIL import Image
from palette import mochaPalette as palette

@lru_cache
def getClosestColorInLinearGradient(gradientSegments, color, strength):
    closest = math.inf
    closestColor = closest
    for gradientSegment in gradientSegments:
        closestColorInSegment = getClosestColorInSegment(gradientSegment, color)
        distance = squaredDistance(closestColorInSegment, color)
        if (distance < closest):
            closest = distance
            closestColor = closestColorInSegment
    return linearlyInterpolate(color, closestColor, strength)

def squaredDistance(colorOne, colorTwo):
    return \
        (colorOne[0] - colorTwo[0]) ** 2 + \
        (colorOne[1] - colorTwo[1]) ** 2 + \
        (colorOne[2] - colorTwo[2]) ** 2

def dotProduct(pointOne, pointTwo):
    return \
        (pointOne[0] * pointTwo[0]) + \
        (pointOne[1] * pointTwo[1]) + \
        (pointOne[2] * pointTwo[2])

def linearlyInterpolate(pointOne, pointTwo, factor):
    result = [math.nan, math.nan, math.nan]
    for i in range(3):
        result[i] = \
            pointOne[i] + \
            round((pointTwo[i] - pointOne[i]) * factor)
    return tuple(result)

'''
On a 3d line-segment between two colors, find
the closest point on that line-segment to a given
color. This is effectively projecting a color on
to a linear gradient between two colors.

https://math.stackexchange.com/a/2193733/1063870
Where t represents an interpolation [0, 1], the t 
representing the closest point on the infinite line
crossing the two colors in the segment to the given 
color is:

t = - (v ⋅ u) / (v ⋅ v)
where:
A is the start of the segment
B is the end of the segment
v = B - A
u = A - P

If t is in [0, 1], that is the closest point in the
segment. Otherwise, we calculate the distance between
the two colors in the gradient segment and the given
color and return the color in the gradient segment
that is closest.
'''
def getClosestColorInSegment(gradientSegment, color):
    a, b = gradientSegment
    p = color
    v = [math.nan, math.nan, math.nan]
    u = [math.nan, math.nan, math.nan]
    for i in range(3):
        v[i] = b[i] - a[i] # v = B - A
        u[i] = a[i] - p[i] # u = A - P
    t = -1 * dotProduct(v, u) / dotProduct(v, v)
    if t > 0 and t < 1:
        return linearlyInterpolate(a, b, t)
    return a if t <= 0 else b

directoryPath = sys.argv[1]
strength = .8
gradientSegments = tuple([(palette[i], palette[i + 1]) for i in range(len(palette) - 1)])

def recurseThroughFiles(path):
    for dirEntry in os.scandir(path):
        if dirEntry.is_dir():
            recurseThroughFiles(dirEntry.path)
            continue
        filePath = os.path.abspath(dirEntry.path)
        if filePath.endswith('.png'):
            originalImage = Image.open(filePath, 'r').convert('RGBA')
            dimensions = originalImage.size
            width, height = dimensions
            newImage = Image.new(originalImage.mode, dimensions)
            for x in range(width):
                for y in range(height):
                    pos = (x, y)
                    oldColor = originalImage.getpixel(pos)
                    newColor = getClosestColorInLinearGradient(gradientSegments, oldColor, strength)
                    if (len(oldColor) == 4):
                        newImage.putpixel(pos, (newColor[0], newColor[1], newColor[2], oldColor[3]))
                    else:
                        newImage.putpixel(pos, newColor)
            newImage.save(filePath)
            print(f'Saved image at {filePath}.')

recurseThroughFiles(directoryPath)
