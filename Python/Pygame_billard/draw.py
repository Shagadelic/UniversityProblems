"""
draw.py

The draw module defines functions that allow the user to create a
drawing.  A drawing appears on the canvas.  The canvas appears
in the window.  As a convenience, the module also imports the
commonly used Color objects defined in the color module.
"""

import time
import os
import sys
import pygame
import pygame.gfxdraw
import pygame.font
import color #praktikum.color as 

if (sys.hexversion < 0x03000000):
    import Tkinter
    import tkMessageBox
    import tkFileDialog
else:
	import tkinter as Tkinter
	import tkinter.messagebox as tkMessageBox
	import tkinter.filedialog as tkFileDialog
	
#-----------------------------------------------------------------------

# Default Sizes and Values

_BORDER = 0.0
#_BORDER = 0.05
_DEFAULT_XMIN = 0.0
_DEFAULT_XMAX = 1.0
_DEFAULT_YMIN = 0.0
_DEFAULT_YMAX = 1.0
_DEFAULT_CANVAS_SIZE = 512
_DEFAULT_PEN_RADIUS = .005  # Maybe change this to 0.0 in the future.
_DEFAULT_PEN_COLOR = color.BLACK

_DEFAULT_FONT_FAMILY = 'Helvetica'
_DEFAULT_FONT_SIZE = 12

_xmin = None
_ymin = None
_xmax = None
_ymax = None

_fontFamily = _DEFAULT_FONT_FAMILY
_fontSize = _DEFAULT_FONT_SIZE

_canvasWidth = float(_DEFAULT_CANVAS_SIZE)
_canvasHeight = float(_DEFAULT_CANVAS_SIZE)
_penRadius = None
_penColor = _DEFAULT_PEN_COLOR
_keysTyped = []

# Has the window been created?
_windowCreated = False

#-----------------------------------------------------------------------
# Begin added by Alan J. Broder
#-----------------------------------------------------------------------

# Keep track of mouse status

# Has the mouse been left-clicked since the last time we checked?
_mousePressed = False

# The position of the mouse as of the most recent mouse click
_mousePos = None
 
#-----------------------------------------------------------------------
# End added by Alan J. Broder
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def _pygameColor(c):
    """
    Convert c, an object of type color.Color, to an equivalent object
    of type pygame.Color.  Return the result.
    """
    r = c.getRed()
    g = c.getGreen()
    b = c.getBlue()
    return pygame.Color(r, g, b)

#-----------------------------------------------------------------------

# Private functions to scale and factor X and Y values.

def _scaleX(x):
    return _canvasWidth * (x - _xmin) / (_xmax - _xmin)

def _scaleY(y):
    return _canvasHeight * (_ymax - y) / (_ymax - _ymin)

def _factorX(w):
    return w * _canvasWidth / abs(_xmax - _xmin)

def _factorY(h):
    return h * _canvasHeight / abs(_ymax - _ymin)

#-----------------------------------------------------------------------
# Begin added by Alan J. Broder
#-----------------------------------------------------------------------

def _userX(x):
    return _xmin + x * (_xmax - _xmin) / _canvasWidth

def _userY(y):
    return _ymax - y * (_ymax - _ymin) / _canvasHeight

#-----------------------------------------------------------------------
# End added by Alan J. Broder
#-----------------------------------------------------------------------
    
#-----------------------------------------------------------------------

def setCanvasSize(w=_DEFAULT_CANVAS_SIZE, h=_DEFAULT_CANVAS_SIZE):
    """
    Set the size of the canvas to w pixels wide and h pixels high.
    Calling this function is optional. If you call it, you must do
    so before calling any drawing function.
    """
    global _background
    global _surface
    global _canvasWidth
    global _canvasHeight
    global _windowCreated

    if _windowCreated:
        raise Exception('The stddraw window already was created')

    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')

    _canvasWidth = w
    _canvasHeight = h
    _background = pygame.display.set_mode([w, h])
    pygame.display.set_caption('stddraw window (r-click to save)')
    _surface = pygame.Surface((w, h))
    _surface.fill(_pygameColor(color.WHITE))
    _windowCreated = True

def setXscale(min=_DEFAULT_XMIN, max=_DEFAULT_XMAX):
    """
    Set the x-scale of the canvas such that the minimum x value
    is min and the maximum x value is max.
    """
    global _xmin
    global _xmax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception('min must be less than max')
    size = max - min
    _xmin = min - _BORDER * size
    _xmax = max + _BORDER * size

def setYscale(min=_DEFAULT_YMIN, max=_DEFAULT_YMAX):
    """
    Set the y-scale of the canvas such that the minimum y value
    is min and the maximum y value is max.
    """
    global _ymin
    global _ymax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception('min must be less than max')
    size = max - min
    _ymin = min - _BORDER * size
    _ymax = max + _BORDER * size

def setPenRadius(r=_DEFAULT_PEN_RADIUS):
    """
    Set the pen radius to r, thus affecting the subsequent drawing
    of points and lines. If r is 0.0, then points will be drawn with
    the minimum possible radius and lines with the minimum possible
    width.
    """
    global _penRadius
    r = float(r)
    if r < 0.0:
        raise Exception('Argument to setPenRadius() must be non-neg')
    _penRadius = r * float(_DEFAULT_CANVAS_SIZE)

def setPenColor(c=_DEFAULT_PEN_COLOR):
    """
    Set the pen color to c, where c is an object of class color.Color.
    c defaults to stddraw.BLACK.
    """
    global _penColor
    _penColor = c

def setFontFamily(f=_DEFAULT_FONT_FAMILY):
    """
    Set the font family to f (e.g. 'Helvetica' or 'Courier').
    """
    global _fontFamily
    _fontFamily = f

def setFontSize(s=_DEFAULT_FONT_SIZE):
    """
    Set the font size to s (e.g. 12 or 16).
    """
    global _fontSize
    _fontSize = s

#-----------------------------------------------------------------------

def _makeSureWindowCreated():
    global _windowCreated
    if not _windowCreated:
        setCanvasSize()
        _windowCreated = True

#-----------------------------------------------------------------------

# Functions to draw shapes, text, and images on the background canvas.

def _pixel(x, y):
    """
    Draw on the background canvas a pixel at (x, y).
    """
    _makeSureWindowCreated()
    xs = _scaleX(x)
    xy = _scaleY(y)
    pygame.gfxdraw.pixel(
        _surface,
        int(round(xs)),
        int(round(xy)),
        _pygameColor(_penColor))

def point(x, y):
    """
    Draw on the background canvas a point at (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    # If the radius is too small, then simply draw a pixel.
    if _penRadius <= 1.0:
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(
                xs-_penRadius,
                ys-_penRadius,
                _penRadius*2.0,
                _penRadius*2.0),
            0)

def _thickLine(x0, y0, x1, y1, r):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    Draw the line with a pen whose radius is r.
    """
    xs0 = _scaleX(x0)
    ys0 = _scaleY(y0)
    xs1 = _scaleX(x1)
    ys1 = _scaleY(y1)
    if (abs(xs0-xs1) < 1.0) and (abs(ys0-ys1) < 1.0):
        filledCircle(x0, y0, r)
        return
    xMid = (x0+x1)/2
    yMid = (y0+y1)/2
    _thickLine(x0, y0, xMid, yMid, r)
    _thickLine(xMid, yMid, x1, y1, r)

def line(x0, y0, x1, y1):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    """

    THICK_LINE_CUTOFF = 3 # pixels

    _makeSureWindowCreated()

    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)

    lineWidth = _penRadius * 2.0
    if lineWidth == 0.0: lineWidth = 1.0
    if lineWidth < THICK_LINE_CUTOFF:
        x0s = _scaleX(x0)
        y0s = _scaleY(y0)
        x1s = _scaleX(x1)
        y1s = _scaleY(y1)
        pygame.draw.line(
            _surface,
            _pygameColor(_penColor),
            (x0s, y0s),
            (x1s, y1s),
            int(round(lineWidth)))
    else:
        _thickLine(x0, y0, x1, y1, _penRadius/_DEFAULT_CANVAS_SIZE)

def circle(x, y, r):
    """
    Draw on the background canvas a circle of radius r centered on
    (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0*r)
    hs = _factorY(2.0*r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs-ws/2.0, ys-hs/2.0, ws, hs),
            int(round(_penRadius)))

def filledCircle(x, y, r):
    """
    Draw on the background canvas a filled circle of radius r
    centered on (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0*r)
    hs = _factorY(2.0*r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs-ws/2.0, ys-hs/2.0, ws, hs),
            0)

def rectangle(x, y, w, h):
    """
    Draw on the background canvas a rectangle of width w and height h
    whose lower left point is (x, y).
    """
    global _surface
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factorX(w)
    hs = _factorY(h)
    # If the rectangle is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs, ys-hs, ws, hs),
            int(round(_penRadius)))

def filledRectangle(x, y, w, h):
    """
    Draw on the background canvas a filled rectangle of width w and
    height h whose lower left point is (x, y).
    """
    global _surface
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factorX(w)
    hs = _factorY(h)
    # If the rectangle is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs, ys-hs, ws, hs),
            0)

def square(x, y, r):
    """
    Draw on the background canvas a square whose sides are of length
    2r, centered on (x, y).
    """
    _makeSureWindowCreated()
    rectangle(x-r, y-r, 2.0*r, 2.0*r)

def filledSquare(x, y, r):
    """
    Draw on the background canvas a filled square whose sides are of
    length 2r, centered on (x, y).
    """
    _makeSureWindowCreated()
    filledRectangle(x-r, y-r, 2.0*r, 2.0*r)

def polygon(x, y):
    """
    Draw on the background canvas a polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _makeSureWindowCreated()
    # Scale X and Y values.
    xScaled = []
    for xi in x:
        xScaled.append(_scaleX(float(xi)))
    yScaled = []
    for yi in y:
        yScaled.append(_scaleY(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((xScaled[i], yScaled[i]))
    points.append((xScaled[0], yScaled[0]))
    pygame.draw.polygon(
        _surface,
        _pygameColor(_penColor),
        points,
        int(round(_penRadius)))

def filledPolygon(x, y):
    """
    Draw on the background canvas a filled polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _makeSureWindowCreated()
    # Scale X and Y values.
    xScaled = []
    for xi in x:
        xScaled.append(_scaleX(float(xi)))
    yScaled = []
    for yi in y:
        yScaled.append(_scaleY(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((xScaled[i], yScaled[i]))
    points.append((xScaled[0], yScaled[0]))
    pygame.draw.polygon(_surface, _pygameColor(_penColor), points, 0)

def filledRaute(x, y, breite):
    haelfte = breite/2
    x = [x, x-haelfte, x, x+haelfte]
    y = [y-haelfte, y, y+haelfte, y]
    filledPolygon(x, y)

def text(x, y, s):
    """
    Draw string s on the background canvas centered at (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    xs = _scaleX(x)
    ys = _scaleY(y)
    font = pygame.font.SysFont(_fontFamily, _fontSize)
    text = font.render(s, 1, _pygameColor(_penColor))
    textpos = text.get_rect(center=(xs, ys))
    _surface.blit(text, textpos)

def picture(pic, x=None, y=None):
    """
    Draw pic on the background canvas centered at (x, y).  pic is an
    object of class picture.Picture. x and y default to the midpoint
    of the background canvas.
    """
    global _surface
    _makeSureWindowCreated()
    # By default, draw pic at the middle of the surface.
    if x is None:
        x = (_xmax + _xmin) / 2.0
    if y is None:
        y = (_ymax + _ymin) / 2.0
    x = float(x)
    y = float(y)
    xs = _scaleX(x)
    ys = _scaleY(y)
    ws = pic.width()
    hs = pic.height()
    picSurface = pic._surface # violates encapsulation
    _surface.blit(picSurface, [xs-ws/2.0, ys-hs/2.0, ws, hs])

def clear(c=color.WHITE):
    """
    Clear the background canvas to color c, where c is an
    object of class color.Color. c defaults to stddraw.WHITE.
    """
    _makeSureWindowCreated()
    _surface.fill(_pygameColor(c))

def save(f):
    """
    Save the window canvas to file f.
    """
    _makeSureWindowCreated()

    #if sys.hexversion >= 0x03000000:
    #    # Hack because Pygame without full image support
    #    # can handle only .bmp files.
    #    bmpFileName = f + '.bmp'
    #    pygame.image.save(_surface, bmpFileName)
    #    os.system('convert ' + bmpFileName + ' ' + f)
    #    os.system('rm ' + bmpFileName)
    #else:
    #    pygame.image.save(_surface, f)

    pygame.image.save(_surface, f)

#-----------------------------------------------------------------------

def _show():
    """
    Copy the background canvas to the window canvas.
    """
    _background.blit(_surface, (0, 0))
    pygame.display.flip()
    _checkForEvents()

def _showAndWaitForever():
    """
    Copy the background canvas to the window canvas. Then wait
    forever, that is, until the user closes the stddraw window.
    """
    _makeSureWindowCreated()
    _show()
    QUANTUM = .1
    while True:
        time.sleep(QUANTUM)
        _checkForEvents()

def show(msec=float('inf')):
    """
    Copy the background canvas to the window canvas, and
    then wait for msec milliseconds. msec defaults to infinity.
    """
    if msec == float('inf'):
        _showAndWaitForever()

    _makeSureWindowCreated()
    _show()
    _checkForEvents()

    # Sleep for the required time, but check for events every
    # QUANTUM seconds.
    QUANTUM = .1
    sec = msec / 1000.0
    if sec < QUANTUM:
        time.sleep(sec)
        return
    secondsWaited = 0.0
    while secondsWaited < sec:
        time.sleep(QUANTUM)
        secondsWaited += QUANTUM
        _checkForEvents()

#-----------------------------------------------------------------------

def _saveToFile():
    """
    Display a dialog box that asks the user for a file name.  Save the
    drawing to the specified file.  Display a confirmation dialog box
    if successful, and an error dialog box otherwise.  The dialog boxes
    are displayed using Tkinter, which (on some computers) is
    incompatible with Pygame. So the dialog boxes must be displayed
    from child processes.
    """
    import subprocess
    _makeSureWindowCreated()

    stddrawPath = os.path.realpath(__file__)

    childProcess = subprocess.Popen(
        [sys.executable, stddrawPath, 'getFileName'],
        stdout=subprocess.PIPE)
    so, se = childProcess.communicate()
    fileName = so.strip()

    if sys.hexversion >= 0x03000000:
        fileName = fileName.decode('utf-8')

    if fileName == '':
        return

    if not fileName.endswith(('.jpg', '.png')):
        childProcess = subprocess.Popen(
            [sys.executable, stddrawPath, 'reportFileSaveError',
            'File name must end with ".jpg" or ".png".'])
        return

    try:
        save(fileName)
        childProcess = subprocess.Popen(
            [sys.executable, stddrawPath, 'confirmFileSave'])
    except (pygame.error) as e:
        childProcess = subprocess.Popen(
            [sys.executable, stddrawPath, 'reportFileSaveError', str(e)])

def _checkForEvents():
    """
    Check if any new event has occured (such as a key typed or button
    pressed).  If a key has been typed, then put that key in a queue.
    """
    global _surface
    global _keysTyped
    
    #-------------------------------------------------------------------
    # Begin added by Alan J. Broder
    #-------------------------------------------------------------------
    global _mousePos
    global _mousePressed
    #-------------------------------------------------------------------
    # End added by Alan J. Broder
    #-------------------------------------------------------------------
    
    _makeSureWindowCreated()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            _keysTyped = [event.unicode] + _keysTyped
            if event.key == pygame.K_x:
               pygame.quit()
               sys.exit()
        elif (event.type == pygame.MOUSEBUTTONUP) and \
            (event.button == 3):
            _saveToFile()
        
            
        #---------------------------------------------------------------
        # Begin added by Alan J. Broder
        #---------------------------------------------------------------
        # Every time the mouse button is pressed, remember
        # the mouse position as of that press.
        elif (event.type == pygame.MOUSEBUTTONDOWN) and \
            (event.button == 1): 
            _mousePressed = True
            _mousePos = event.pos                      
        #---------------------------------------------------------------
        # End added by Alan J. Broder
        #---------------------------------------------------------------

#-----------------------------------------------------------------------

# Functions for retrieving keys

def hasNextKeyTyped():
    """
    Return True if the queue of keys the user typed is not empty.
    Otherwise return False.
    """
    global _keysTyped
    return _keysTyped != []

def nextKeyTyped():
    """
    Remove the first key from the queue of keys that the the user typed,
    and return that key.
    """
    global _keysTyped
    return _keysTyped.pop()

#-----------------------------------------------------------------------
# Begin added by Alan J. Broder
#-----------------------------------------------------------------------

# Functions for dealing with mouse clicks 

def mousePressed():
    """
    Return True if the mouse has been left-clicked since the 
    last time mousePressed was called, and False otherwise.
    """
    global _mousePressed
    if _mousePressed:
        _mousePressed = False
        return True
    return False

def mousePosition():
    """
    Return the x and y coordinate in user space of the location at
    which the mouse is positioned at the moment.
    """
    xMouse, yMouse = pygame.mouse.get_pos()
    xMouse /= _canvasWidth
    yMouse /= _canvasHeight
    yMouse = 1 - yMouse
    return (xMouse, yMouse)
    
#-----------------------------------------------------------------------
# End added by Alan J. Broder
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

# Initialize the x scale, the y scale, and the pen radius.

setXscale()
setYscale()
setPenRadius()
pygame.font.init()

#-----------------------------------------------------------------------

# Functions for displaying Tkinter dialog boxes in child processes.

def _getFileName():
    """
    Display a dialog box that asks the user for a file name.
    """
    root = Tkinter.Tk()
    root.withdraw()
    reply = tkFileDialog.asksaveasfilename(initialdir='.')
    sys.stdout.write(reply)
    sys.stdout.flush()
    sys.exit()

def _confirmFileSave():
    """
    Display a dialog box that confirms a file save operation.
    """
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showinfo(title='File Save Confirmation',
        message='The drawing was saved to the file.')
    sys.exit()

def _reportFileSaveError(msg):
    """
    Display a dialog box that reports a msg.  msg is a string which
    describes an error in a file save operation.
    """
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showerror(title='File Save Error', message=msg)
    sys.exit()