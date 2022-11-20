'''
MRoyale Skin Converter v3.0.2

Copyright (C) MMXXII clippy#4722 (AKA WaCopyrightInfringio)
(See https://tinyurl.com/infernopatch for an explanation of my old username.)

Having trouble running the program? Try running it online:
https://replit.com/@WaluigiRoyale/MR-Converter-3?embed=true

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program (see the file license.txt).
    If not, see <https://www.gnu.org/licenses/>.

Version 1.0 (Feb. 12, 2022): Launch

Version 1.1 (Feb. 19, 2022): “default” command now only copies from same 
    position in template vs. new; added compatibility check

Version 1.2 (Feb. 21, 2022): Adds alternate image to copy from (“alt” and
    “copyalt” commands)

Version 1.3 (Feb. 27, 2022): Rewrote each command as a separate function instead
    of having one big if statement; “base” command to start from blank image

Version 1.3.1 (Aug. 29, 2022): Fixed empty-line check in copyalt

Version 1.4 (Oct. 10, 2022):
  + rotate and flip commands
  + filter command with basic grayscale and filter commands
  * Fixed bug where base_image was a reference to open_image rather than a copy
  * Only pay attention to the first occurrence of a given header command
    (previously, only the LAST one counted)
  * Restructured logic for optional arguments so there are fewer errors

Version 2.0 (Oct. 10, 2022)
NEW FEATURES:
  + Split filter into grayscale and invert commands (because future filters
    may have multiple arguments)
  + colorfilter command to adjust RGB color levels
EASE OF USE:
  + Compatibility check now automatically fixes problems on the fly with old 
    scripts (without making permanent changes to the scripts)
  + Prints save path so user knows the file will be overwritten
  + Warning if file doesn't start with “mrconverter”
  + Better error-catching: rejects commands if user doesn't provide enough 
    arguments
UNDER THE HOOD:
  + Massive rewrite to improve code readability.

Version 2.1 (Oct. 11, 2022): 
  + Special “.INPUT” path for open and save commands
  + More instructions on scripts the user can run
  * Fixed error checking for alt and template
  - Template no longer supports wildcards (*) in path because it made no sense

Version 2.2 (Oct. 25, 2022):
  + hue, saturation, lightness filters
  + fill command to fill a rectangular area with all one color
  * Better code organization
  + Added the W
  - Removed Herobrine

Version 2.2.1 (Oct. 31, 2022):
  + Allows script writers to exclude x and y values in filters to apply the
    filter to the whole image
  * Bug fixes
  * Preparing for a major update

Version 3.0 (Nov. 18, 2022):
  + Turned converter into a GUI
  + contrast filter
  + Converter is now usable on Replit, no Python installation needed
  * Many, many bug fixes, including lots of rare crash bugs
  + Added the W
  - Removed Herobrine

Version 3.0.1 (Nov. 19, 2022 / ONLINE ONLY):
  + Better instructions for online use

Version 3.0.2 (Nov. 20, 2022):
  + ReadMe file
  * Fixed bug in R2D and L2D skin conversion scripts that replaced a frame of
    the Fire climb animation with Fire power-down
  * Fixed allowing commas in filenames
'''

import os, sys
import PIL.Image, PIL.ImageOps, PIL.ImageTk
from time import time

from tkinter import *
import tkinter.font as tkfont
import tkinter.filedialog as filedialog

###########################################################################
#### GLOBAL VARIABLES #####################################################
###########################################################################

app_version = [3,0,2]

def get_app_version():
    return str(app_version[0])+'.'+str(app_version[1])+'.'+\
        str(app_version[2])

window = Tk()
window.wm_title('Clippy’s MRoyale Skin Converter v' + get_app_version())
window.geometry('640x320')
# UNCOMMENT THIS LINE ON REPL.IT BUILDS OR TO RUN THE APP IN FULLSCREEN
window.attributes('-fullscreen', True)

app_icon = PhotoImage(file='assets/ui/icon.png')
window.iconphoto(False, app_icon)

colors = {
    'red': '#c00000',
    'green': '#008000',
    'blue': '#0080ff',
    'gray': '#808080',
    'silver': '#c0c0c0',
}

# Different platforms use different default font sizes.
# Get this system's default size to use as a base. 
# All other font sizes will be a multiple of it.
def relative_font_size(multiple):
    base_font_size = tkfont.Font(font='TkDefaultFont').cget('size')
    return int(multiple * base_font_size)

# f_italic = tkfont.Font(slant='italic')
f_bold = tkfont.Font(weight='bold', size=relative_font_size(1))
f_large = tkfont.Font(size=relative_font_size(1.5))
f_heading = tkfont.Font(weight='bold', size=relative_font_size(1.5))

side_frame = LabelFrame(window, width=160, height=320)

'''
gray = not yet reached
blue = in progress
green = completed
red = failed
'''
step_status = ['blue', 'gray', 'gray', 'gray', 'gray', 'gray']
steps = [
    Label(side_frame, text='● Select Script', fg=colors[step_status[0]], 
        justify='left'),
    Label(side_frame, text='● Load Script', fg=colors[step_status[1]], 
        justify='left'),
    Label(side_frame, text='● Compatibility Check', 
        fg=colors[step_status[2]], 
        justify='left'),
    Label(side_frame, text='● Open & Save Paths', fg=colors[step_status[3]], 
        justify='left'),
    Label(side_frame, text='● Run Script', fg=colors[step_status[4]], 
        justify='left'),
    Label(side_frame, text='● Summary', fg=colors[step_status[5]], 
        justify='left'),
]

title = Label(side_frame, text='Skin Converter v'+get_app_version(), 
        font=f_bold)
footer = Label(side_frame, text='a Clippy production', fg=colors['gray'])

main_frame = LabelFrame(window, width=480, height=320)
main_frame.grid_propagate(False)

menu_heading = Label(main_frame, text='What do you want to convert?', 
        font=f_heading)

menu_btns_p1 = [
    Button(main_frame, text='Convert a Legacy skin to Deluxe',
            font=f_large),
    Button(main_frame, text='Convert a Remake skin to Deluxe',
            font=f_large),
    Button(main_frame, text='Convert a Legacy obj mod to Deluxe',
            font=f_large),
    Label(main_frame), # filler
    Button(main_frame, text='Legacy/Custom...'),
    Label(main_frame), # filler
    Button(main_frame, text='Exit'),
]

menu_btns_p2 = [
    Button(main_frame, text='Convert a Remake skin to Legacy'),
    Button(main_frame, 
            text='Add taunt sprites to an incomplete Legacy skin'),
    Button(main_frame, 
            text='Convert a Legacy smb_map mod to Legacy smb_map_new'),
    Label(main_frame), # filler
    Button(main_frame, text='Run a custom script'),
    Button(main_frame, text='Submit your custom script'),
    Label(main_frame), # filler
    Button(main_frame, text='Back'),
]

icons = {
    'info': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('assets/ui/info.png')),
    'question': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('assets/ui/question.png')),
    'warning': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('assets/ui/warning.png')),
    'error': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('assets/ui/denied.png')),
    'done': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('assets/ui/accepted.png')),
}

# warnings is for any problem with conversion scripts that mean a command
# can’t run properly or at all, but which doesn’t require us to halt
# the conversion completely. Any warnings are displayed to the user after
# the script finishes running.
warnings = []

###########################################################################
#### BASIC COMMANDS #######################################################
###########################################################################

# DOCUMENTATION: copy,0<oldX>,0<oldY>,0<newX>,48<newY>,16[width],16[height] 
# Copy from old image to specified position in new image.
def copy(i, open_image, base_image):
    min_args = 5
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    oldX = i[1]
    oldY = i[2]
    newX = i[3]
    newY = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width = i[5]
    if len(i) == 6:
        i += [width]
    height = i[6]

    region = open_image.crop((oldX, oldY, oldX+width, oldY+height))
    base_image.paste(region, (newX, newY, newX+width, newY+height))

# DOCUMENTATION: copyalt,0<oldX>,0<oldY>,0<newX>,48<newY>,16[width],
#   16[height] 
# Copy from alt image to specified position in new image.
def copyalt(i, alt_image, base_image):
    min_args = 5
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    oldX = i[1]
    oldY = i[2]
    newX = i[3]
    newY = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width = i[5]
    if len(i) == 6:
        i += [width]
    height = i[6]

    region = alt_image.crop((oldX, oldY, oldX+width, oldY+height))
    base_image.paste(region, (newX, newY, newX+width, newY+height))

# DOCUMENTATION: default,0<x>,0<y>,16[width],16[height] 
# Copy from template image to same position in new image.
def default(i, template_image, base_image):
    min_args = 3
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    region = template_image.crop((x, y, x+width, y+height))
    base_image.paste(region, (x, y, x+width, y+height))

# DOCUMENTATION: clear,0<x>,0<y>,16[width],16[height] 
# Clear area from new image. 
# Used to be called “delete” -- this still works for compatiblity reasons.
def clear(i, base_image):
    min_args = 3
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    empty_image = PIL.Image.new('RGBA', (width, height))
    base_image.paste(empty_image, (x, y, x+width, y+height))

###########################################################################
#### TRANSFORMATION COMMANDS ##############################################
###########################################################################

# DOCUMENTATION: resize,256<newWidth>,256<newHeight> 
# Resize the new image's canvas. Does not perform any scaling. 
# Anchor top left.
def resize(i, base_image):
    min_args = 3
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    newWidth = i[1]
    newHeight = i[2]

    oldWidth, oldHeight = base_image.size
    new_image = PIL.Image.new('RGBA', (newWidth,newHeight))
    new_image.paste(base_image,
                    (0,0,oldWidth,oldHeight))
    base_image = new_image

# DOCUMENTATION: rotate,90<degreesClockwise: multiple of 90>,0<x>,0<y>,
#   16[size] 
# Rotate the area in place on the new image. Unlike copy commands, 
# only one size argument is used, as the rotated area must be square.
def rotate(i, base_image):
    min_args = 4
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    degreesClockwise = i[1]
    x = i[2]
    y = i[3]

    # If size specified, use that value. If not, use 16. 
    # Remember: squares only.
    if len(i) == 4:
        i += [16]
    size = i[4]

    if (i[1] % 90) != 0:
        log_warning('\
Rotating by a number not divisible by 90 may have unintended effects.')

    # The rotation angle is negated in the PIL call 
    # because PIL rotates counterclockwise.
    region = base_image.crop((x, y, x+size, y+size))
    region = region.rotate(-degreesClockwise, 
        PIL.Image.Resampling.NEAREST, expand=0)
    base_image.paste(region, (x, y, x+size, y+size))

# DOCUMENTATION: flip,x<direction: x or y>,0<x>,0<y>,16[width],16[height]
# Flip the area in place on the new image. Unlike rotation, width and height
# can be different here.
def flip(i, base_image):
    min_args = 4
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    degreesClockwise = i[1]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    region = base_image.crop((x, y, x+width, y+height))
    # PIL has different commands for horizontal vs. vertical flip
    if i[1] == 'x':
        region = PIL.ImageOps.mirror(region)
    elif i[1] == 'y':
        region = PIL.ImageOps.flip(region)
    # Otherwise, if direction is invalid, do nothing (the goal is to make 
    # it so the user CAN'T crash the program by mistake)
    base_image.paste(region, (x, y, x+width, y+height))

###########################################################################
#### FILTER COMMANDS ######################################################
###########################################################################

# DOCUMENTATION: grayscale,0[x],0[y],16[width],16[height] 
# Converts the area to grayscale (AKA black-and-white). For the command that
# literally makes the area only black and white (1-bit), use "threshold".
def grayscale(i, base_image):
    min_args = 1
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    region = base_image.crop((x, y, x+width, y+height)).convert('LA')
    base_image.paste(region, (x, y, x+width, y+height))

# DOCUMENTATION: invert,0[x],0[y],16[width],16[height] 
# Inverts the area. For example, black becomes white, and red becomes cyan.
def invert(i, base_image):
    min_args = 1
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]
        
    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            rgba = region.getpixel((loop_x, loop_y))
            region.putpixel((loop_x, loop_y), 
                    (255-rgba[0], 255-rgba[1], 255-rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))
    
# DOCUMENTATION: colorfilter,0<redAdjust: -255 to +255>,0<greenAdjust>,
#   0<blueAdjust>,0[x],0[y],16[width],16[height]
# Adjusts the R/G/B levels. You can use all three adjust arguments at the 
# same time to adjust brightness.
def colorfilter(i, base_image):
    min_args = 4
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    redAdjust = i[1]
    greenAdjust = i[2]
    blueAdjust = i[3]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 5:
        i = [i[0], i[1], i[2], i[3], base_image.size[0], base_image.size[1]]
    x = i[4]
    y = i[5]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 6:
        i += [16, 16]
    width = i[6]
    if len(i) == 7:
        i += [width]
    height = i[7]
        
    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            rgba = region.getpixel((loop_x, loop_y))
            region.putpixel((loop_x, loop_y), 
                    (rgba[0]+redAdjust, rgba[1]+greenAdjust, 
                    rgba[2]+blueAdjust, rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))
    
# DOCUMENTATION: opacity,0<adjust: -255 to +255>,0[x],0[y],
#   16[width],16[height]
# Adjusts the opacity (alpha) levels. 
# Negative = more transparent, positive = more opaque.
def opacity(i, base_image):
    min_args = 2
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    adjust = i[1]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]
        
    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            rgba = region.getpixel((loop_x, loop_y))
            region.putpixel((loop_x, loop_y), 
                    (rgba[0], rgba[1], rgba[2], rgba[3]+adjust))
    base_image.paste(region, (x, y, x+width, y+height))
    
# Convert RGBA to HSLA for use in filters
def rgba_to_hsla(color):
    r = color[0]
    g = color[1]
    b = color[2]
    a = color[3]

    # I'm copying this from Wikipedia and they use extra variables here
    max_color = max(r,g,b)
    min_color = min(r,g,b)
    c = max_color - min_color

    l = (0.5 * (max_color + min_color))/2.55

    s = 0
    if (l != 0 and l != 1):
        s = ((max_color - l) / (min(l, 1-l)))
        # I really don't know why my calculations are ending up wrong
        # but here's a duct-tape solution:
        s = -(s + 1.5815065763252287) * (100/2.6021668930625266)

    h = 0
    if c == 0:
        pass # hue stays at 0
    elif max_color == r:
        h = 60 * (0 + (g-b)/c)
    elif max_color == g:
        h = 60 * (2 + (b-r)/c)
    elif max_color == b:
        h = 60 * (4 + (r-g)/c)

    return [round(h, 1), round(s, 1), round(l, 1), a]

# Convert HSLA to RGBA for use in filters
def hsla_to_rgba(color):
    h = color[0]
    s = color[1]/100
    l = color[2]/100
    a = color[3]

    # Also from Wikipedia
    c = (1 - abs(2*l - 1)) * s
    h_ = h/60
    x = c * (1 - abs(h_ % 2 - 1))

    # Convert from [0.0, 1.0] scale to [0, 255] 
    c = int(c * 255)
    x = int(x * 255)

    if s == 0: # special case for grayscale
        gray = int(l*255)
        return [gray,gray,gray,a]
    if 0 <= h_ < 1:
        return [int(c),int(x),0,a]
    if 1 <= h_ < 2:
        return [int(x),int(c),0,a]
    if 2 <= h_ < 3:
        return [0,int(c),int(x),a]
    if 3 <= h_ < 4:
        return [0,int(x),int(c),a]
    if 4 <= h_ < 5:
        return [int(x),0,int(c),a]
    if 5 <= h_ < 6:
        return [int(c),0,int(x),a]

# Normalize HSLA values in place.
def format_hsla(color):
    # Hue must be from 0 to 360
    color[0] %= 360

    # Saturation must be from 0 to 100
    color[1] = clip(color[1], 0, 100)

    # Lightness must be from 0 to 100
    color[2] = clip(color[2], 0, 100)

    # And as always, we don't touch alpha
    return color

# DOCUMENTATION: hue,0<adjust: -180 to +180>,0[x],0[y],16[width],16[height] 
# Adjusts the hue.
def hue(i, base_image):
    min_args = 2
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    adjust = i[1]
    
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]
        
    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            hsla = rgba_to_hsla(region.getpixel((loop_x, loop_y)))
            hsla[0] += adjust
            format_hsla(hsla)
            rgba = hsla_to_rgba(hsla)
            region.putpixel((loop_x, loop_y), 
                    (rgba[0], rgba[1], rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))
    
# DOCUMENTATION: saturation,0<adjust: -100 to +100>,0[x],0[y],16[width],
#   16[height] 
# Adjusts the saturation (in HSLA color space). Positive adjust means 
# more colorful. Negative adjust means less colorful. -100 means grayscale.
def saturation(i, base_image):
    min_args = 2
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    adjust = i[1]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]
        
    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            hsla = rgba_to_hsla(region.getpixel((loop_x, loop_y)))
            hsla[1] += adjust
            format_hsla(hsla)
            rgba = hsla_to_rgba(hsla)
            region.putpixel((loop_x, loop_y), 
                    (rgba[0], rgba[1], rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))
    
# DOCUMENTATION: lightness,0<adjust: -100 to +100>,0[x],0[y],16[width],
#   16[height] 
# Adjusts the lightness (in HSLA color space). Positive adjust means 
# lighter. Negative adjust means darker. -100 means all black, 
# +100 means all white.
def lightness(i, base_image):
    min_args = 2
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    adjust = i[1]
    
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]
        
    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            hsla = rgba_to_hsla(region.getpixel((loop_x, loop_y)))
            hsla[2] += adjust
            format_hsla(hsla)
            rgba = hsla_to_rgba(hsla)
            region.putpixel((loop_x, loop_y), 
                    (rgba[0], rgba[1], rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))
    
# DOCUMENTATION: fill,0<red: 0 to 255>,0<green: 0 to 255>,0<blue: 0 to 255>,
#   255<alpha: 0 to 255>,0[x],0[y],16[width],16[height] 
# Fills the area with the selected color.
def fill(i, base_image):
    min_args = 5
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    red = i[1]
    green = i[2]
    blue = i[3]
    alpha = i[4]
    
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 6:
        i = [i[0], i[1], i[2], i[3], i[4], 0, 0, base_image.size[0], 
                base_image.size[1]]
    x = i[5]
    y = i[6]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[7]
    if len(i) == 5:
        i += [width]
    height = i[8]

    base_image.paste((red, green, blue, alpha), (x, y, width, height))

# Clip a number if it's below a minimum OR above a maximum
def clip(n, minimum, maximum):
    if n < minimum:
        n = minimum
    if n > maximum:
        n = maximum
    return n
    

def contrast(i, base_image):
    min_args = 2
    if len(i) < min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    adjust = clip(i[1], -128, 127.99) # Avoid dividing by 0

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16x16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]
        
    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            rgba = region.getpixel((loop_x, loop_y))

            # Temporarily convert r/g/b
            new_r = (rgba[0] - 127.5)
            new_g = (rgba[1] - 127.5)
            new_b = (rgba[2] - 127.5)

            # Adjust contrast
            if (adjust < 0):
                new_r *= (adjust + 128)/128
                new_g *= (adjust + 128)/128
                new_b *= (adjust + 128)/128
            elif (adjust > 0):
                new_r *= 128/(-adjust+128)
                new_g *= 128/(-adjust+128)
                new_b *= 128/(-adjust+128)

            # Convert back and clip
            new_r = int(clip(new_r+127.5, 0, 255))
            new_g = int(clip(new_g+127.5, 0, 255))
            new_b = int(clip(new_b+127.5, 0, 255))

            region.putpixel((loop_x, loop_y), 
                    (new_r, new_g, new_b, rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

def warning(i):
    min_args = 1
    if len(i) < min_args:
        log_warning('Unknown warning from script')
        return

    log_warning('Warning from script: '+i[1])

###########################################################################
#### COMING SOON ##########################################################
###########################################################################

def threshold(i, base_image):
    log_warning(i[0]+' is coming soon...')
    
def colorize(i, base_image):
    log_warning(i[0]+' is coming soon...')

def scale(i, base_image):
    log_warning(i[0]+' is coming soon...')

# Much further down the pipeline (requires completely new syntax)
    
def select(i, base_image):
    log_warning(i[0]+' is coming soon...')
    
def if_(i, base_image):
    log_warning(i[0]+' is coming soon...')

###########################################################################
#### HELPER FUNCTIONS #####################################################
###########################################################################

# Clear the main content frame -- remove text, buttons, etc.
def cls():
    for child in main_frame.winfo_children():
        child.place_forget()

# Redraw each step in its current color
def status_refresh():
    # Update fill color for each step, then draw it
    for index, item in enumerate(steps):
        item.config(fg=colors[step_status[index]])
        item.place(x=0, y=24+24*index)

# Update the status for each step and redraw the steps
def status_set(newStatus):
    global step_status
    step_status = newStatus
    status_refresh()

# Mark the current step as complete and move to next step
def status_complete():
    global step_status

    next_step = 0
    for i in range(len(step_status)):
        if step_status[i] == 'gray':
            next_step = i
            break
        else:
            step_status[i] = 'green'

    step_status[next_step] = 'blue'

    status_refresh()

# Mark the current step as failed
def status_fail():
    global step_status

    curr_step = 0
    for i in range(1, len(step_status)):
        if step_status[i] == 'gray':
            curr_step = i - 1
            break

    step_status[curr_step] = 'red'

    status_refresh()

# Generic function to display a dialog box in the window, 
# with text and buttons.
# icon is one of: info, question, warning, error, done, bomb
def dialog(heading_text, msg_text, bottom_text, icon_name, 
        btn1_text, btn1_event, btn2_text=None, btn2_event=None):
    cls()

    if icon_name in icons:
        icon = Label(main_frame, image=icons[icon_name])
        icon.place(x=470, y=10, anchor=NE)

    if heading_text:
        heading = Label(main_frame, text=heading_text, font=f_heading, 
                justify='left')
        heading.place(x=0, y=0)

    msg = []
    if isinstance(msg_text, str): 
        # Convert to list if message is only one line / a string
        msg_text = [msg_text]
    for index, item in enumerate(msg_text):
        if item.startswith('<b>'):
            msg.append(Label(main_frame, text=item[3:], justify='left', 
                wraplength=470, font=f_bold))
        else:
            msg.append(Label(main_frame, text=item, justify='left', 
                wraplength=470))

        if heading_text:
            msg[index].place(x=0, y=36+index*24)
        else: # Empty heading = place text at top
            msg[index].place(x=0, y=index*24)

    if bottom_text:
        bottom = Label(main_frame, text=bottom_text, justify='left')
        bottom.place(x=0, y=280, anchor=SW)

    btn1 = Button(main_frame, text=btn1_text)
    if btn2_text:
        btn2 = Button(main_frame, text=btn2_text)

    if btn2_text:
        btn1.place(x=230, y=310, anchor=SE)
        btn2.place(x=250, y=310, anchor=SW)
    else:
        btn1.place(x=240, y=310, anchor=S)

    btn1.bind('<Button-1>', lambda _: btn1_event())
    if btn2_text:
        btn2.bind('<Button-1>', lambda _: btn2_event())

def the_W():
    dialog('There’s a new bird among us', 'We will only be adding the W.',
        '', 'info', 'Clear cache', main)

def log_warning(w):
    global warnings
    if w not in warnings:
        warnings.append(w)
        
def menu_p1():
    cls()

    menu_heading.place(x=240, y=0, anchor=N)

    next_y = 0
    for i in (menu_btns_p1):
        i.place(x=240, y=40+next_y, anchor=N)
        if str(i.cget('font')) == 'TkDefaultFont':
            next_y += 30
        else: # user-defined large font
            next_y += 40

def menu_p2():
    cls()

    menu_heading.place(x=240, y=0, anchor=N)

    next_y = 0
    for i in (menu_btns_p2):
        i.place(x=240, y=40+next_y, anchor=N)
        next_y += 30

# Update the user on the progress of a large conversion task.
def update_subhead(subhead):
    global start_num, stop_num, current_num

    rounded_pct = round(current_num/(stop_num-start_num)*100, 1)

    subhead = Label(main_frame, 
        text='Now converting: image '+str(current_num)+\
            ' ('+str(rounded_pct)+'%)', 
        justify='left')
    subhead.place(x=0, y=24)

    return subhead

###########################################################################
#### MAIN FUNCTIONS #######################################################
###########################################################################

def main():
    #### INITIAL GUI SETUP ####
    # Place frames
    side_frame.place(x=0, y=0)
    main_frame.place(x=160, y=0) 

    # Place sidebar items
    title.place(x=0, y=0)
    footer.place(x=80, y=315, anchor=S)
    for index, item in enumerate(steps):
        item.place(x=0, y=24+24*index)
    # Note that the position of anything with main_frame as parent is 
    # RELATIVE (i.e. 160 will be added to x)

    #### STEP 1: SELECT SCRIPT ####
    cls()
    status_set(['blue', 'gray', 'gray', 'gray', 'gray', 'gray'])

    menu_btns_p1[0].bind('<Button-1>', 
            lambda _: open_script('scripts/DxSkin.txt'))
    menu_btns_p1[1].bind('<Button-1>', 
            lambda _: open_script('scripts/RemakeToDxSkin.txt'))
    menu_btns_p1[2].bind('<Button-1>', 
            lambda _: open_script('scripts/DxObj.txt'))

    menu_btns_p1[4].bind('<Button-1>', 
            lambda _: menu_p2())

    menu_btns_p1[6].bind('<Button-1>', 
            lambda _: exit_app())

    menu_btns_p2[0].bind('<Button-1>', 
            lambda _: open_script('scripts/swim_taunt.txt'))
    menu_btns_p2[1].bind('<Button-1>', 
            lambda _: open_script('scripts/just_taunt.txt'))
    menu_btns_p2[2].bind('<Button-1>', 
            lambda _: open_script('scripts/map_new.txt'))

    menu_btns_p2[4].bind('<Button-1>', 
            lambda _: open_script(''))
    menu_btns_p2[5].bind('<Button-1>', 
            lambda _: the_W())

    menu_btns_p2[7].bind('<Button-1>', 
            lambda _: menu_p1())

    menu_p1()

    window.update()

    window.mainloop()

def open_script(script_file):
    global data, version, version_str

    # Ask user to pick a script if they want to run a custom script
    if not script_file:
        script_file = filedialog.askopenfilename(
                title='Select a script to run',
                initialdir='./scripts/')
        # If script file path is still empty, user cancelled, back to menu
        if script_file == '':
            main()
            return

    #### STEP 2: SCRIPT INFO ####
    cls()
    status_complete()

    try:
        file_obj = open(script_file, 'r')
        raw_content = file_obj.read()
        file_obj.close()
    except FileNotFoundError: 
        # If user somehow tries to run a nonexistent file
        status_fail()
        dialog('Error', 
            'Couldn’t find a file with that name. Please try again.', 
            '', 'error', 'Back', main)
        return
    except UnicodeDecodeError: 
        # If user opens a “script” with weird characters
        status_fail()
        dialog('Error', 
            ['Couldn’t read the file with that name.',
                'Are you sure it’s a conversion script?'],
            '', 'error', 'Back', main)
        return
    except IsADirectoryError: 
        # If user opens a folder or Mac app bundle
        status_fail()
        dialog('Error', 
            '''That file is a folder or application. 
Please try again.''',
            '', 'error', 'Back', main)
        return

    if not raw_content.startswith('mrconverter'):
        dialog('Warning', 
            ['\
The file you selected may not be designed for this converter.',
'Proceed with caution.'], 
            '', 'warning', 'Okay', main)

    lines = raw_content.split('\n')
    data = []
    for l in range(len(lines)):
        # Ignore comments like this one
        lines[l] = lines[l].split('#')[0].rstrip()
        # Load the rest of the line
        data.append(lines[l].split(','))

    # Strip whitespace from lines, then if it can be an int, make it an int
    for i in range(len(data)):
        for j in range(len(data[i])):
            try:
                # Descriptions may contain commas, 
                # so keep space after those.
                # Otherwise, remove whitespace from sides of commands.
                # Ditto for file paths.
                if data[i][0] != 'description' \
                        and data[i][0] != 'open' \
                        and data[i][0] != 'save' \
                        and data[i][0] != 'alt' \
                        and data[i][0] != 'template':
                    data[i][j] = data[i][j].strip()
                data[i][j] = int(data[i][j])
            except ValueError:
                pass

    version = [0,0,0]
    version_str = '0.0.0'
    for i in data:
        if i[0] == 'version':
            # Make sure user entered enough numbers
            if len(i) < 3:
                dialog('Warning', 
['Invalid version in script. Version must take the form “x.y.z”.', 
'The converter will default to version 0.0.0.'],
                    '', 'warning', 'Okay', main)
            else:
                version = i[1:4]
                version_str = '.'.join([str(x) for x in version])
            break

    name = 'Unknown Script'
    for i in data:
        if i[0] == 'name':
            name = i[1]
            break

    author = 'Unknown Author'
    for i in data:
        if i[0] == 'author':
            author = i[1]
            break

    description = 'No description available.'
    for i in data:
        if i[0] == 'description':
            description = ','.join(i[1:])
            break

    dialog('Loaded script: '+name, ['File path: '+script_file, 
            'By: '+author, 'Description: '+description], 
            '''Do you want to run this script?

If you click “Yes”, this program will check for problems with the script.
If no problems are found, the script will run right away.''', 'question',
            'Yes', compatibility_check, 'No', main)

def compatibility_check():
    global data, version, version_str, open_path, save_path, template_path,\
            alt_path, base_blank, start_num, stop_num, current_num, multi

    #### STEP 3: COMPATIBILITY CHECK ####
    cls()
    status_complete()

    # Load header data
    open_path = ''
    for i in data:
        if i[0] == 'open':
            open_path = i[1]
            break

    alt_path = ''
    for i in data:
        if i[0] == 'alt':
            alt_path = i[1]
            break
            
    template_path = ''
    for i in data:
        if i[0] == 'template':
            template_path = i[1]
            break
            
    save_path = ''
    for i in data:
        if i[0] == 'save':
            save_path = i[1]
            break

    base_blank = False
    for i in data:
        if i[0] == 'base' and i[1] == 'blank':
            base_blank = True
            break

    start_num = None
    for i in data:
        if i[0] == 'start':
            # start number has to be an integer
            if type(i[1]) != int:
                log_warning('Start number is not an integer.')
                break
            start_num = i[1]
            break

    stop_num = None
    for i in data:
        if i[0] == 'stop':
            # stop number has to be an integer
            if type(i[1]) != int:
                log_warning('Stop number is not an integer.')
                break
            stop_num = i[1]+1
            # Unlike in Python, the “stop” is inclusive.
            # e.g. if stop is 10, it will convert #10 but not #11
            break

    current_num = start_num

    all_issues = [ 
        '“default” command had 6 arguments (instead of 4) before v1.1.', #0
        '''\
“filter” command is only supported in v1.4. Instead of “filter,grayscale,...”,
use “grayscale,...”''', #1
        '“template” no longer supports wildcards in filepath since v2.1', #2
        '“alt” no longer supports wildcards in filepath since v3.0', #3
    ]
    file_issues = []

    # Warn if the “version” field is later than the current version
    # (unless it's just a newer release version)
    # The compatibility checks are irrelevant for scripts made for newer 
    # versions, because I can't predict the future.
    # Wait, no, I can predict the future: 
    # Chat will continue to be a mistake.
    if version[0] > app_version[0] or \
            (version[0] == app_version[0] and version[1] > app_version[1]):
        dialog('Compatiblity warning', 
            ['This script was designed for a newer converter version.',
'You can try to run it if you want, but we can’t guarantee it’ll work.',
'We are not responsible for any damage to your files this may cause.'], 
            'Do you want to continue anyway?', 'warning',
            'Yes', get_paths, 'No', main)
    else:
        # Scan file for compatibility issues
        for i in data:
            # Version 1.1: “default” no longer takes newX and newY arguments
            # Automatically fixed by converter
            if i[0] == 'default' and version[0] < 1 or \
                    (version[0] == 1 and version[1] < 1):
                file_issues.append(0)
                del i[3]
                del i[4]
            # Version 1.5: “filter” command split into subcommands 
            # like “grayscale”
            # Automatically fixed by converter
            if i[0] == 'filter' and version[0] < 1 or \
                    (version[0] == 1 and version[1] < 4):
                file_issues.append(1)
                del i[0]
            # Version 2.1: “template” command no longer supports wildcards 
            # in path
            # Cannot be fixed
            if '*' in template_path and version[0] < 2 or \
                    (version[0] == 2 and version[1] < 1):
                file_issues.append(2)
            # Version 3.0: alt command no longer supports wildcards in path
            # Cannot be fixed
            if '*' in alt_path and version[0] < 3: 
                # don't need to check minor version above, 
                # as there’s no minor version less than 0
                file_issues.append(3)

        # Compatibility warnings
        if len(file_issues) > 0:
            main_text = [
                Label(main_frame, text=\
'Your script was designed for version '+version_str+' of this converter.'),
                Label(main_frame, text=\
'It contains the following compatibility issues:'),
            ]
            for i in file_issues:  
                main_text.append(Label(main_frame, text='- '+all_issues[i]))
            
            dialog('Compatibility warning', main_text, 
                [
                    Label(main_frame, text=\
'Do you wish to continue anyway, even though things may not work properly?'),
                    Label(main_frame, text=\
'We are not responsible for any damage to your files this may cause.'),
                ], 'warning', 'Yes', get_paths, 'No', main)
        else:
            get_paths()
            return

def get_paths():
    global multi, start_num, stop_num, open_path, save_path

    #### STEP 4: OPEN & SAVE PATHS ####
    cls()
    status_complete()

    # All scripts need readable open and save paths, 
    # or they won’t run at all
    if not open_path or not save_path:
        status_fail()
        dialog('Error', 
['The file you opened doesn’t specify a location to open and/or save images.',
'Are you sure it’s a conversion script?'], None, 'error', 'Back', main)
        return

    # Determine whether script is converting 1 file (single-file mode)
    # or multiple files (multi-file mode)
    multi = False
    if start_num != None and stop_num != None and \
            '*' in open_path and '*' in save_path:
        multi = True

    # Make user choose file if that's what the script wants
    if open_path.upper() == '.INPUT':
        open_path = filedialog.askopenfilename(\
                title='Select an image to open and copy from',
                initialdir='./')
        # If open_path is still empty, user cancelled — go back to step 1
        if not open_path:
            main()
            return

    # Only run the open-path existence check on single-file conversions. 
    # For multi-file conversions, existence will be checked file-by-file 
    # in the main loop.
    if not multi:
        try:
            # This part doesn't actually open the file for conversion --
            # it's just to make sure it exists
            open(open_path).close()
        except FileNotFoundError:
            status_fail()
            dialog('Error', 
['The script tried to open the following file, but it does not exist.',
'<b>'+open_path,
'Check your spelling and try again.'], '', 'error', 'Back', main)
            return
        except IsADirectoryError: 
            # If user opens a folder or Mac app bundle
            status_fail()
            dialog('Error', 
                '''The path '''+open_path+''' is a folder or application.
Please try again.''',
                '', 'error', 'Back', main)
            return

    if save_path.upper() == '.INPUT':
        save_path = filedialog.asksaveasfilename(\
                title='Select a path to save to', defaultextension='.png',
                filetypes=[('PNG image', '*.png')],
                initialdir='./')
        # If save_path is still empty, user cancelled — go back to step 1
        if save_path == '':
            main()
            return
        else: 
            # We don't need to check overwriting on our end because
            # the system dialog handles it
            run_script()
            return
    else:
        # Make sure parent directory of save_path exists, 
        # if it's saving inside a directory
        parent_dir = '/'.join(save_path.split('/')[:-1])
        # “if parent_dir” => if there’s no parent directory because you’re
        # saving to the current working directory, skip the directory check
        if parent_dir and not os.path.exists(parent_dir):
            status_fail()
            dialog('Error', 
['The script is trying to save to a folder that doesn’t exist.',
'The path that caused the error was:', '<b>'+parent_dir], 
                '', 'error', 'Back', main)
            return

        # Check if the file already exists
        files_to_overwrite = []
        main_text = ['This text shouldn’t show up for any reason.',
                'If it does, please tell Clippy so he can fix it!']
        if multi: # …then we need to check EVERY file we're saving to
            for i in range(start_num, stop_num):
                check_path = save_path.replace('*', str(i))
                if os.path.exists(check_path):
                    files_to_overwrite.append(check_path)
                    # In the future, I may add a way to display all the
                    # files that would be overwritten

            if files_to_overwrite:
                main_text = [
                    '\
This script will save to one or more paths where files already exist.',
                    '\
Please check the path %s for existing files.' % save_path,
                    '\
Running the script will overwrite existing files. You can’t undo this action.',
                    'Only run scripts from users you trust!',
                ]
            else:
                run_script() # No files to overwrite -- move on
                return
        else:
            if os.path.exists(save_path):
                main_text = [
                    '\
This script will save an image to the following path:',
                    '<b>'+save_path,
                    'A file already exists at that path.',
                    '\
Running the script will overwrite the file. You can’t undo this action.',
                    'Only run scripts from users you trust!',
                ]
            else:
                run_script() # No files to overwrite -- move on
                return

        dialog('Warning', main_text, 
            'Do you want to run this script anyway?', 'warning',
            'Yes', run_script, 'No', main)

def run_script():
    global data, open_path, save_path, template_path, alt_path, base_blank,\
            start_num, stop_num, current_num, multi

    #### STEP 5: RUN SCRIPT ####
    cls()
    status_complete()

    headingText = Label(main_frame, text='Converting image...', 
        font=f_heading)
    headingText.place(x=0, y=0)

    # Update screen differently based on how many files we're converting
    heading = Label()
    subhead = Label()
    if multi:
        heading = Label(main_frame, text='Converting all images from '+\
            str(start_num)+' to '+str(stop_num-1), font=f_heading)
        subhead = update_subhead(subhead)
    else:
        heading = Label(main_frame, text='Converting 1 image...', 
            font=f_heading)
        start_num = 0
        stop_num = 1
    heading.place(x=0, y=0)
    window.update()
    
    # Start the clock
    t1 = time()
    time_last_refresh = t1
    time_since_refresh = 0

    # Load template image only once because it doesn't allow wildcards
    template_image = None
    try:
        if template_path != '':
            # template_path doesn't support wildcards because the point is
            # for there to be just 1 template
            template_image = PIL.Image.open(template_path).convert('RGBA')
        else:
            # create a dummy image to use as “template”
            template_image = PIL.Image.new('RGBA', (1, 1))
    except FileNotFoundError:
        log_warning('Couldn’t find a template file with the path '+\
            template_path+' — skipping')
    except (AttributeError, PIL.UnidentifiedImageError): 
        # We opened something, but it's not an image
        log_warning('Couldn’t open the template file at ' + \
            template_path + '.')
        log_warning('    - Are you sure it’s an image? Skipping.')
    except IsADirectoryError: # If user opens a folder or Mac app bundle
        log_warning('The template file path '+template_path+\
            ' is a folder or application.')

    # Main file-reading loop -- a different function does the actual processing
    for i in range(start_num, stop_num):
        current_num = i

        # Update only once per second so we don't slow things down too much
        # from updating the UI
        time_since_refresh += (time() - time_last_refresh)
        if time_since_refresh > 1:
            update_subhead(subhead)
            window.update()
            time_last_refresh = time()
            time_since_refresh = 0

        open_image = None
        try:
            if multi:
                open_image = PIL.Image.open(open_path.replace('*', 
                    str(i))).convert('RGBA')
            else:
                open_image = PIL.Image.open(open_path).convert('RGBA')
        except FileNotFoundError:
            # Don't need to check for multi because in single mode,
            # invalid paths will be rejected earlier
            log_warning('Couldn’t find a file with the path ' + \
                open_path.replace('*', str(i))+\
                ' — skipping')
            continue
        except (AttributeError, PIL.UnidentifiedImageError): 
            # We opened something, but it's not an image
            log_warning('Couldn’t open the file at ' + open_path + '.')
            log_warning('    - Are you sure it’s an image? Skipping.')
            continue
        except IsADirectoryError: # If user opens a folder or Mac app bundle
            log_warning('\
                The path '+open_path+' is a folder or application.')

        alt_image = None
        try:
            if alt_path != '':
                alt_image = PIL.Image.open(alt_path).convert('RGBA')
            else:
                # create a dummy image to use as “alt”
                alt_image = PIL.Image.new('RGBA', (1, 1))
        except FileNotFoundError:
            log_warning('Couldn’t find an alternate file with the path '+\
                alt_path+' — skipping')
            continue
        except (AttributeError, PIL.UnidentifiedImageError): 
            # We opened something, but it's not an image
            log_warning('Couldn’t open the alternate file at ' + \
                alt_path + '.')
            log_warning('    - Are you sure it’s an image? Skipping.')
            continue
        except IsADirectoryError: # If user opens a folder or Mac app bundle
            log_warning('The alternate path '+alt_path+\
                ' is a folder or application.')

        if base_blank:
            # Create a blank base if the script starts with that
            if template_image: 
                # If we opened a valid template image, use its size for the
                # blank base
                w, h = template_image.size
            else:
                # Otherwise, default to the size of the image we opened
                w, h = open_image.size
            base_image = PIL.Image.new('RGBA', (w,h))
        else:
            # If no base is specified, start new image as copy of old image
            base_image = open_image.copy()

        base_image = process(open_image, template_image, 
                            alt_image, base_image)
        base_image.save(save_path.replace('*', str(i)))

    t2 = time()
    replit(t2-t1)

def replit(conv_time):
    #### STEP 6: SUMMARY ####
    cls()
    status_complete()

    # Test if we're running on replit
    if os.path.isdir("/home/runner") == True:
        # User is using repl.it, so provide extra instructions on how to
        # download images
        help_text = [
            'Looks like you’re using the online converter!',
            '<b>To download your converted image(s):',
            '1. Exit fullscreen',
            '2. Find the sidebar',
            '3. Click on the ⋮ (3 dots) next to the file you just converted',
            '4. Select “Download” from the menu that pops up',
            '<b>If converting multiple files...',
            '...the fastest option is probably to download the whole project.',
            'This will download a lot of unnecessary files but it’s faster',
            'than downloading each image one at a time.'
        ]
        dialog('Replit Help', help_text, None, 'info', 'Okay', 
            lambda: summary(conv_time))
    else:
        summary(conv_time)

def summary(conv_time, warning_page=0):
    # Roll warning page over to 0 if needed
    warn_per_page = 10
    num_warn_pages = (len(warnings)-1)//warn_per_page + 1
    if warning_page >= num_warn_pages:
        warning_page = 0

    main_text = ['Done in '+str(round(conv_time, 3))+' seconds']
    bottom_text = ''

    if warnings:
        # Add 1 to displayed warning_page because end users
        # expect counting to start at 1
        bottom_text += 'CONVERTER WARNINGS: (Page '+str(warning_page+1)+\
                    ' of '+str(num_warn_pages)+')'
        for i in range(warn_per_page*warning_page, 
                warn_per_page*warning_page+warn_per_page):
            # If we’re out of warnings, break
            if i >= len(warnings):
                break
            # Otherwise, add the next warning to the text we’ll display
            bottom_text += '\n' + warnings[i]

        if num_warn_pages > 1:
            # Display dialog with extra button to go to next warning page
            dialog('Conversion complete!', main_text,
                bottom_text, 'done', 'More warnings', 
                lambda: summary(conv_time, warning_page+1), # next page
                'Okay', main)
        else:
            # Display dialog with warnings but no extra button
            # if there's only 1 page worth of warnings
            dialog('Conversion complete!', main_text,
                bottom_text, 'done', 'Okay', main)
    else:
        dialog('Conversion complete!', main_text,
            None, 'done', 'Okay', main)

# Reads lines from one file and executes its instructions
def process(open_image, template_image=None, alt_image=None, 
        base_image=None):
    HEADER_COMMANDS = ['mrconverter', 'version', 'name', 'description', 
        'author', 'open', 'save', 'template', 'alt', 'base', 
        'start', 'stop']

    for i in data:
        try:
            if i[0].strip() == '': # Skip blank lines
                pass
            elif i[0] == 'warning':
                warning(i)
            
            # Basic commands
            elif i[0] == 'copy':
                copy(i, open_image, base_image)
            elif i[0] == 'copyalt':
                if alt_path == '':
                    log_warning('\
    Skipped all “copyalt” commands because no “alt” image was specified.')
                else:
                    copyalt(i, alt_image, base_image)
            elif i[0] == 'default':
                if template_path == '':
                    log_warning('\
    Skipped all “default” commands because no “template” image was specified.')
                else:
                    default(i, template_image, base_image)
            elif i[0] == 'clear' or i[0] == 'delete':
                clear(i, base_image)
            # Transformation commands
            elif i[0] == 'resize':
                resize(i, base_image)
            elif i[0] == 'rotate':
                rotate(i, base_image)
            elif i[0] == 'flip':
                flip(i, base_image)
            # Filter commands
            elif i[0] == 'grayscale':
                grayscale(i, base_image)
            elif i[0] == 'invert':
                invert(i, base_image)
            elif i[0] == 'colorfilter':
                colorfilter(i, base_image)
            elif i[0] == 'opacity':
                threshold(i, base_image)
            elif i[0] == 'hue':
                hue(i, base_image)
            elif i[0] == 'saturation':
                saturation(i, base_image)
            elif i[0] == 'lightness':
                lightness(i, base_image)
            elif i[0] == 'fill':
                fill(i, base_image)
            elif i[0] == 'contrast':
                contrast(i, base_image)

            # COMING SOON
            elif i[0] == 'threshold':
                threshold(i, base_image)
            elif i[0] == 'colorize':
                colorize(i, base_image)
            elif i[0] == 'scale':
                scale(i, base_image)
            elif i[0] == 'select':
                select(i, base_image)
            elif i[0] == 'if':
                if_(i, base_image)

            elif i[0] in HEADER_COMMANDS:
                pass # Just so it doesn't think header commands are unknown
            else:
                log_warning('Unknown command: '+str(i[0]))
        except Exception as e: 
            # Handle any errors in the command functions so they don’t bring
            # the whole program to a halt
            log_warning(str(i[0])+' command skipped due to error: '+str(e))
    return base_image 

def crash(exctype=None, excvalue=None, tb=None):
    import tkinter.messagebox as messagebox
    bomb = PhotoImage(file='assets/ui/bomb.png')
    window.iconphoto(False, bomb)
    messagebox.showerror(window, 
        message='An error has occurred:\n'+str(excvalue))
    exit_app()

def exit_app():
    window.destroy()
    sys.exit()

###########################################################################
#### START THE PROGRAM ####################################################
###########################################################################

try:
    window.report_callback_exception = crash
    
    # Test if we're running on replit
    if os.path.isdir("/home/runner") == True:
        import tkinter.messagebox as messagebox
        messagebox.showinfo(window, 
        message='''Looks like you’re running the online (Replit) version of the skin converter! 
Please enter fullscreen so you can click all the buttons.
Click the ⋮ on the “Output” menu bar then click “Maximize”. 
If you’re on a phone, rotate it sideways, zoom out, and hide your browser’s toolbar.''')
        main()
    else:
        main()

except Exception as e: # TODO: Uncaught exceptions
    crash()
