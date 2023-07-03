'''
MR Skin Converter 
Version 6.0.0

Copyright © 2022–2023 clippy#4722

Having trouble running the program? Try running it online:
https://replit.com/@WaluigiRoyale/MR-Converter-GUI?embed=true

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

See changelog.txt for version history.
'''

from glob import glob
import os, sys, colorsys
import urllib.request
import webbrowser # for installing assets
from typing import Union
from time import time
from tkinter import *
import tkinter.font as tkfont
import tkinter.filedialog as filedialog
# Non-PSL modules
import PIL.Image, PIL.ImageOps, PIL.ImageTk

###########################################################################
#### GLOBAL VARIABLES #####################################################
###########################################################################

app_version = [6,0,0]

def app_version_str():
    return str(app_version[0])+'.'+str(app_version[1])+'.'+\
        str(app_version[2])

window = Tk()
window.wm_title('Clippy’s Skin Converter')
window.geometry('480x360')
window.resizable(False, False)
# Run in fullscreen on Replit only
if os.path.isdir("/home/runner") == True:
    window.attributes('-fullscreen', True)

app_icon = PhotoImage(file='ui/icon.png')
window.iconphoto(False, app_icon)

colors = {
    'red': '#c00000',
    'green': '#008000',
    'blue': '#0080ff',
    'gray': '#808080',
    'silver': '#c0c0c0',
    # Light-gray background color #f0f0f0
    'BG': '#f0f0f0',
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

footer_frame = LabelFrame(window, width=480, height=40, bg=colors['BG'])
footer = Label(footer_frame, 
        text='Skin Converter v%s — a Clippy production' % app_version_str(), 
        fg=colors['gray'], bg=colors['BG'])
back_btn = Button(footer_frame, text='Back to Menu', 
        highlightbackground=colors['BG'])

main_frame = LabelFrame(window, width=480, height=320, bg=colors['BG'])
main_frame.grid_propagate(False)

menu_heading = Label(main_frame, text='What do you want to convert?', 
        font=f_heading, bg=colors['BG'])

menu_btns_p1 = [
    Button(main_frame, text='Convert a Legacy skin to Deluxe',
            font=f_large, highlightbackground=colors['BG']),
    Button(main_frame, text='Convert a Remake skin to Deluxe',
            font=f_large, highlightbackground=colors['BG']),
    Button(main_frame, text='Convert a Legacy obj mod to Deluxe',
            highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Legacy/Custom...', 
            highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Exit', highlightbackground=colors['BG']),
]

menu_btns_p2 = [
    Button(main_frame, text='Convert a Remake skin to Legacy', 
            highlightbackground=colors['BG']),
    Button(main_frame, 
            text='Convert a Legacy map mod to Legacy map_new', 
            highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Run a custom script', 
            highlightbackground=colors['BG']),
    Button(main_frame, text='Submit your custom script', 
            highlightbackground=colors['BG']),
    Button(main_frame, text='Convert multiple images...', 
            highlightbackground=colors['BG']),
    Button(main_frame, text='Update game images', 
            highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Back', highlightbackground=colors['BG']),
]

icons = {
    'info': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('ui/info.png')),
    'question': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('ui/question.png')),
    'warning': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('ui/warning.png')),
    'error': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('ui/denied.png')),
    'done': \
        PIL.ImageTk.PhotoImage(PIL.Image.open('ui/accepted.png')),
}

# warnings is for any problem with conversion scripts that mean a command
# can’t run properly or at all, but which doesn’t require us to halt
# the conversion completely. Any warnings are displayed to the user after
# the script finishes running.
warnings = []
multi_open_paths = []

# Lists of commands that start and/or end blocks
block_starts_ends = [
    'else',
    'elseif',
]
block_starts = [
    'if', 
    # 'for', 'while', 'foreach' # COMING SOON
] + block_starts_ends
block_ends = ['end', 'endif'] + block_starts_ends

# List of header commands. These commands are typically located at the start
# of the file. They aren't run as instructions; they contain metadata about
# the script that is processed before running it.
header_commands = ['mrconverter', 'version', 'name', 'description', 
        'author', 'open', 'save', 'template', 'alt', 'base', 
        'start', 'stop', 'loop_limit']

###########################################################################
#### LOG/EXIT COMMANDS ####################################################
###########################################################################

# Displays a warning shown after conversion finishes. Only other i-argument is
# the text of the warning.
def warning(i):
    min_args = 1
    if len(i) <= min_args:
        log_warning('Unknown warning from script')
        return

    log_warning('Warning from script: '+i[1])

# EXIT and ERROR are handled in the main command-checking loop

###########################################################################
#### BASIC COPYING COMMANDS ###############################################
###########################################################################

# DOCUMENTATION: set,$hello<name>,"Hello world"<value> 
# Set variable "hello" to the string "Hello world". Subcommands in second 
# argument will be evaluated before setting the variable. Any value in double 
# quotes will be treated as a string no matter what. If it's not in quotes and 
# it can be parsed as an integer, the value will be an integer. Anything else 
# will be treated as a string for legacy reasons, but watch out for special 
# characters!
def set(i):
    global variables

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    # If someone tries to set a number or something
    if type(i[1]) != str:
        log_warning('set: Invalid variable name %s. Variable names must start \
with a dollar sign.' % i[1])
        return

    # Now that we know i[1] is a string...
    if not i[1].startswith('$'):
        log_warning('set: Invalid variable name %s. Variable names must start \
with a dollar sign.' % i[1])
        return
    
    # Variable names must be at least 1 character long (2 counting $)
    if len(i[1]) < 2:
        log_warning('set: Invalid variable name %s. Variable names must be at \
least 1 character long.' % i[1])
        return
    
    # Cannot set private variables (which start with _)
    # Unless the variable name is ONLY the underscore
    if i[1][1] == '_' and len(i[1]) > 2:
        log_warning('set: Cannot set variable names starting with underscores, \
like %s, as these are reserved for the converter (except for “$_”).' % i[1])
        return

    # Variable names can only contain: a-z, A-Z, 0-9, _
    for char in i[1][1:]: # [1:] to ignore $ at start
        if not char.isalnum() and char != '_':
            log_warning('set: Invalid variable name %s. Variable names can \
only contain ASCII letters, numbers, and underscores.' % i[1])
            return
    
    # If all the checks passed, set the variable
    variables[i[1]] = i[2]

# DOCUMENTATION: copy,0[oldX],0[oldY],0[newX],0[newY],16[width],16[height]
# Copy from old image to specified position in new image.
# Note: copyalt has been folded into this function because there was no
# difference except in the argument name.
def copy(i, open_image, base_image):
    # No minimum number of arguments

    # If no x or y specified, apply to whole image
    if len(i) <= 4:
        i = [i[0], 0, 0, 0, 0, base_image.size[0], base_image.size[1]]
    oldX = i[1]
    oldY = i[2]
    newX = i[3]
    newY = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width = i[5]
    if len(i) == 6:
        i += [width]
    height = i[6]

    region = open_image.crop((oldX, oldY, oldX+width, oldY+height))
    base_image.paste(region, (newX, newY, newX+width, newY+height))

# DOCUMENTATION: copy_from,old<imageName>,0[oldX],0[oldY],0[newX],0[newY],
#   16[width],16[height] 
# Copy from any image ("old", "alt", "template", or even "new") to specified 
# position in new image.
def copy_from(i):
    global images

    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if i[1] not in images:
        log_warning('copy_from: Skipped because %s is not a defined image name'\
                    % i[1])
        return
    
    copy(['copy_from']+i[2:], images[i[1]], images['new'])

# DOCUMENTATION: default,0[x],0[y],16[width],16[height] 
# Copy from template image to same position in new image.
def default(i, template_image, base_image):
    # No minimum number of arguments
    
    # COMPATIBILITY: In versions prior to 1.1, "default" took 6 arguments
    # (with the first 4 being required):
    # default,0<oldX>,0<oldY>,0<newX>,0<newY>,16[width],16[height]
    if i[0] == 'default' and len(i) > 4 and (version[0] < 1 or \
            (version[0] == 1 and version[1] < 1)):
        del i[3]
        del i[4]

    # If no x or y specified, apply to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    region = template_image.crop((x, y, x+width, y+height))
    base_image.paste(region, (x, y, x+width, y+height))

# DOCUMENTATION: default_from,template<imageName>,0[x],0[y],16[width],16[height]
# Copy from any image ("old", "alt", "template", or even "new") to same 
# position in new image.
def default_from(i):
    global images

    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if i[1] not in images:
        log_warning('default_from: Skipped because %s is not a defined image name'\
                    % i[1])
        return
    
    default(['default_from']+i[2:], images[i[1]], images['new'])

# DOCUMENTATION: clear,0[x],0[y],16[width],16[height] 
# Clear area from new image. 
# Used to be called “delete” -- this still works for compatiblity reasons.
def clear(i, base_image):
    # No minimum number of arguments

    # If no x or y specified, apply to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    empty_image = PIL.Image.new('RGBA', (width, height))
    base_image.paste(empty_image, (x, y, x+width, y+height))

# DOCUMENTATION: duplicate,0[oldX],0[oldY],0[newX],0[newY],16[width],16[height]
# Copy an area on the NEW image to another position on the same canvas.
def duplicate(i, base_image):
    # No minimum number of arguments

    # If no x or y specified, apply to whole image
    if len(i) <= 4:
        i = [i[0], 0, 0, 0, 0, base_image.size[0], base_image.size[1]]
    oldX = i[1]
    oldY = i[2]
    newX = i[3]
    newY = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width = i[5]
    if len(i) == 6:
        i += [width]
    height = i[6]

    region = base_image.crop((oldX, oldY, oldX+width, oldY+height))
    base_image.paste(region, (newX, newY, newX+width, newY+height))

###########################################################################
#### ADVANCED COPYING COMMANDS ############################################
###########################################################################

# DOCUMENTATION: tile,0<copyX>,0<copyY>,16<copyWidth>,16<copyHeight>,
#   0<pasteStartX>,0<pasteStartY>,16<pasteCountHoriz>,16<pasteCountVert>,
#   open[copySource: old, template, or alt]
# Create a tile pattern on the new image using a part of the old image. 
# This command can be very useful but it’s not for beginners.
def tile(i, open_image, alt_image, base_image):
    min_args = 8
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    copyX = i[1]; copyY = i[2]; copyWidth = i[3]; copyHeight = i[4];
    pasteStartX = i[5]; pasteStartY = i[6];
    pasteCountHoriz = i[7]; pasteCountVert = i[8];

    # Default to 'old' as copySource if none specified
    if len(i) == 9:
        i.append('old')
    copySource = i[9].lower()

    for x in range(pasteCountHoriz):
        for y in range(pasteCountVert):
            if copySource == 'open' or copySource == 'old':
                copy(['copy', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        open_image, base_image)
            elif copySource == 'alt' and alt_image:
                copy(['copyalt', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        alt_image, base_image)
            else:
                log_warning('tile: Invalid copy source — defaulting to "old"')
                copy(['copy', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        open_image, base_image)

###########################################################################
#### TRANSFORMATION COMMANDS ##############################################
###########################################################################

# DOCUMENTATION: resize,256<newWidth>,256[newHeight]
# Resize the new image's canvas. Does not perform any scaling. 
# Anchor top left. If no height given, create a square canvas.
def resize(i, base_image):
    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    newWidth = i[1]
    if len(i) == 2:
        i += [newWidth]
    newHeight = i[2]

    oldWidth, oldHeight = base_image.size
    new_image = PIL.Image.new('RGBA', (newWidth,newHeight))
    new_image.paste(base_image,
                    (0,0,oldWidth,oldHeight))
    # Return the new image because trying to set base_image here will just
    # create a new image. Python is weird.
    return new_image

# DOCUMENTATION: rotate,90<degreesClockwise: multiple of 90>,0<x>,0<y>,
#   16[size] 
# Rotate the area in place on the new image. Unlike copy commands, 
# only one size argument is used, as the rotated area must be square.
def rotate(i, base_image):
    min_args = 3
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
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

# DOCUMENTATION: flip,x<direction: x or y>,0[x],0[y],16[width],16[height]
# Flip the area in place on the new image. Unlike rotation, width and height
# can be different here.
def flip(i, base_image):
    min_args = 3
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    # If no x or y specified, apply to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    direction = i[1]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    region = base_image.crop((x, y, x+width, y+height))
    # PIL has different commands for horizontal vs. vertical flip
    if direction == 'x':
        region = PIL.ImageOps.mirror(region)
    elif direction == 'y':
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
    # No minimum number of arguments

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
    # No minimum number of arguments

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
    min_args = 3
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
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
    # If neither is specified, use 16×16.
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
    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    adjust = i[1]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
    raw = colorsys.rgb_to_hls(color[0]/255, color[1]/255, color[2]/255)
    return [raw[0]*360, raw[2]*100, raw[1]*100, color[3]]

# Convert HSLA to RGBA for use in filters
def hsla_to_rgba(color):
    raw = colorsys.hls_to_rgb(color[0]/360, color[2]/100, color[1]/100)
    return [int(raw[0]*255), int(raw[1]*255), int(raw[2]*255), color[3]]

# Normalize HSLA values in place.
def format_hsla(color):
    # Hue must be from 0 to 360
    color[0] %= 360

    # Saturation must be from 0 to 100
    color[1] = clip(color[1], 0, 100)

    # Lightness must be from 0 to 100
    color[2] = clip(color[2], 0, 100)

    # And as always, we don’t touch alpha. In fact, the user doesn’t even need
    # to pass in an alpha — the function will still run.
    return color

# DOCUMENTATION: hue,0<adjust: -180 to +180>,0[x],0[y],16[width],16[height] 
# Adjusts the hue.
def hue(i, base_image):
    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    adjust = i[1]
    
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    adjust = i[1]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    adjust = i[1]
    
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
#   255[alpha: 0 to 255],0[x],0[y],16[width],16[height] 
# Fills the area with the selected color.
def fill(i, base_image):
    min_args = 3
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    red = i[1]
    green = i[2]
    blue = i[3]

    # If no alpha given, assume 100% opaque
    if len(i) <= 4:
        i.append(255)
    alpha = i[4]
    
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 6:
        i = [i[0], i[1], i[2], i[3], i[4], 0, 0, base_image.size[0], 
                base_image.size[1]]
    x = i[5]
    y = i[6]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
    
# DOCUMENTATION: contrast,0<adjust: -128 to 128>,0[x],0[y],16[width],16[height]
# Adjusts the contrast. -128 will make all non-transparent pixels medium gray; 
# +127 will make all RGB values either 0 or 255 (8 colors).
def contrast(i, base_image):
    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    adjust = clip(i[1], -128, 127.99) # Avoid dividing by 0

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
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
    
# DOCUMENTATION: 180<hue: 0 to 360>,50<saturation: 0 to 100>,
#   50<lightness: 0 to 100>,0[x],0[y],16[width],16[height]
# Colorizes specified area in place. Converts area to B&W, treats L=127.5 as 
# the specified HSL color, and interpolates the rest from there. Ex.: if the 
# base color was coral [hsl(0,100,75)], it'll turn black->gray50->white to 
# red->coral->white.
def colorize(i, base_image):
    min_args = 3
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    formatted_hsl = format_hsla([i[1], i[2], i[3]])
    h = formatted_hsl[0]
    s = formatted_hsl[1]
    l = formatted_hsl[2]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 5:
        i = [i[0], i[1], i[2], i[3], 0, 0, 
                base_image.size[0], base_image.size[1]]
    x = i[4]
    y = i[5]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 6:
        i += [16, 16]
    width = i[6]
    if len(i) == 7:
        i += [width]
    height = i[7]
        
    # First, convert the region to grayscale. 
    # We already have a function for this, so let’s use it.
    grayscale(['grayscale', x, y, width, height], base_image)

    # Default min/max lightness values
    min_l = 0
    max_l = 100
    if l > 50:
        min_l = 100 - (2 * (100 - l))
        max_l = 100
    elif l < 50:
        min_l = 0
        max_l = 2*l

    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            hsla = rgba_to_hsla(region.getpixel((loop_x, loop_y)))
            # Set hue and saturation to the values given in the user’s command
            # (leave alpha alone)
            hsla[0] = h
            hsla[1] = s

            # Adjust lightness based on user-provided lightness
            hsla[2] = ((100-hsla[2])/100)*min_l + ((hsla[2])/100)*max_l

            format_hsla(hsla)
            rgba = hsla_to_rgba(hsla)
            region.putpixel((loop_x, loop_y), 
                    (rgba[0], rgba[1], rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

# DOCUMENTATION: sepia,0[x],0[y],16[width],16[height] 
# Simplified colorize syntax for creating sepia-toned images. 
# Based on hex code #a08060 or HSL(30,25,50)
def sepia(i, base_image):
    # No minimum number of arguments

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    colorize(['colorize', 30, 25, 50, x, y, width, height], base_image)

def threshold(i, base_image):
    min_args = 1
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    minWhite = i[1]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3:
        i = [i[0], i[1], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]
        
    # First, to get the input values, convert the region to grayscale
    grayscale(['grayscale', x, y, width, height], base_image)

    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            luma = region.getpixel((loop_x, loop_y)) # returns int (luma value)
            if luma < minWhite: # black
                region.putpixel((loop_x, loop_y), 0)
            else: # white
                region.putpixel((loop_x, loop_y), 255)
    base_image.paste(region, (x, y, x+width, y+height))

###########################################################################
#### SUBCOMMANDS ##########################################################
###########################################################################

# Evaluate a subcommand embedded in parentheses, for example, (empty,0,0,16,16).
# Return the result of the command, in whatever format is appropriate.
# Invalid or empty commands return None (and will be treated as false).
def subcmd(cmd_str, open_image, template_image, alt_image, base_image):
    # No need to access global `labels` because you can't have gotos in subcmds
    global variables

    # The command will be passed in as a string something like 
    # "(empty,0,0,16,16)". We want to get rid of the parens at the start & end
    # (but keep any that are inside).
    
    # First strip whitespace
    cmd_str = cmd_str.strip()
    # Then check for parens at start and end
    # removeprefix would be nice here but that's only in Py3.9
    if len(cmd_str) >= 2 and cmd_str[0] == '(' and cmd_str[-1] == ')':
        # ...and remove them if they're there
        cmd_str = cmd_str[1:-1]
    else:
        # Otherwise, there's something wrong with the subcommand
        log_warning('Invalid subcommand: %s' % cmd_str)
        return None

    # Parse the line to separate out the arguments
    cmd = parse_line(cmd_str)

    # Replace variable names with the variable's current value
    for arg_n in range(len(cmd)):
        if type(cmd[arg_n]) == dict and cmd[arg_n]['type'] == 'var':
            if version[0] >= 6:
                cmd[arg_n] = variables[cmd[arg_n]['content']]
            else:
                cmd[arg_n] = cmd[arg_n]['content']
                log_warning('Variable name %s ignored because \
variables are not supported in scripts written for versions older than 6.0.0.'\
                            % cmd[arg_n]['content'])

    # Now that we've broken the command into the normal list format,
    # we need to check each argument of the command for parentheses and
    # recursively call this function as needed.
    for arg_n in range(1, len(cmd)):
        if type(cmd[arg_n]) == str and \
                cmd[arg_n].startswith('(') and cmd[arg_n].endswith(')'):
            # Execute the command INSIDE the parens FIRST
            cmd[arg_n] = subcmd(cmd[arg_n], open_image, template_image, 
                                      alt_image, base_image)

    # Main dictionary of all subcommands
    if cmd[0].strip() == '': # Treat empty conditionals as false
        log_warning('Empty subcommand — treated as false')
        result = None
    elif cmd[0] == 'empty':
        result = empty(cmd, open_image)

    elif cmd[0] in ['eq', '=', '==']:
        result = eq(cmd)
    elif cmd[0] in ['ne', '≠', '!=', '<>']:
        result = ne(cmd)
    elif cmd[0] in ['lt', '<']:
        result = lt(cmd)
    elif cmd[0] in ['gt', '>']:
        result = gt(cmd)
    elif cmd[0] in ['le', '≤', '<=']:
        result = le(cmd)
    elif cmd[0] in ['ge', '≥', '>=']:
        result = ge(cmd)

    elif cmd[0] in ['or', '||']:
        result = logic_or(cmd)
    elif cmd[0] in ['and', '&&']:
        result = logic_and(cmd)
    elif cmd[0] in ['not', '!']:
        result = logic_not(cmd)
    
    elif cmd[0] in ['add', '+']:
        result = add(cmd)
    elif cmd[0] in ['sub', '-', '–', '−']:
        result = sub(cmd)
    elif cmd[0] in ['mul', '*', '×']:
        result = mul(cmd)
    # elif cmd[0] in ['truediv', '/', '÷']:
    #     result = truediv(cmd)

    elif cmd[0] == 'red':
        result = red(cmd, base_image)
    elif cmd[0] == 'green':
        result = green(cmd, base_image)
    elif cmd[0] == 'blue':
        result = blue(cmd, base_image)
    elif cmd[0] == 'alpha':
        result = alpha(cmd, base_image)

    else:
        log_warning('Invalid subcommand: %s' % cmd_str)
        return None
    
    # Uncomment this line to print command and its result, for debugging
    #p#rint(cmd, result)
    return result
    
# DOCUMENTATION: (empty,0<x>,0<y>,16[width],16[height])
# True if the area on the old image is completely empty (every pixel is
# transparent), False otherwise.
def empty(i, open_image):
    # No minimum number of arguments

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, open_image.size[0], open_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [16, 16]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    region = open_image.crop((x, y, x+width, y+height))
    
    # Loop thru each pixel in region, making sure it's transparent
    for loop_x in range(width):
        for loop_y in range(height):
            rgba = region.getpixel((loop_x, loop_y))
            # If a single pixel isn't transparent, return False
            if rgba[3] != 0:
                return False
    # If we make it here, it's empty, return True
    return True

# EQUALITY SUBCOMMANDS

def eq(i):
    '''
    Equal to (eq, =, ==)
    Use "set" to set variables, not "=".
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        return i[1] == i[2]
    # But if there are 3 or more arguments (x1, x2, x3), treat the command as
    # "if x1==x2 AND x2==x3 AND..."
    return (i[1] == i[2]) and eq([i[0]] + i[2:])

def ne(i):
    '''
    Not equal to (ne, !=, <>, ≠)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        return i[1] != i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return (i[1] != i[2]) and ne([i[0]] + i[2:])

def lt(i):
    '''
    Less than (lt, <)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        try:
            return i[1] < i[2]
        except: # if e.g. invalid type match
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] < i[2]) and lt([i[0]] + i[2:])
    except:
        return None

def gt(i):
    '''
    Greater than (gt, >)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        try:
            return i[1] > i[2]
        except: # if e.g. invalid type match
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] > i[2]) and gt([i[0]] + i[2:])
    except:
        return None

def le(i):
    '''
    Less than or equal to (le, <=, ≤)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        try:
            return i[1] <= i[2]
        except: # if e.g. invalid type match
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] <= i[2]) and le([i[0]] + i[2:])
    except:
        return None

def ge(i):
    '''
    Greater than or equal to (ge, >=, ≥)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        try:
            return i[1] >= i[2]
        except: # if e.g. invalid type match
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] >= i[2]) and ge([i[0]] + i[2:])
    except:
        return None
    
# END EQUALITY SUBCOMMANDS

# LOGICAL SUBCOMMANDS

def logic_or(i):
    '''
    Logical OR (or, ||)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    short_circuit = False
    for x in i[1:]:
        short_circuit = bool(short_circuit or x)
        if short_circuit == True:
            return True
    # If we make it to the end and none of the arguments were true (so we
    # didn't short-circuit), result must be False
    return False

def logic_and(i):
    '''
    Logical AND (and, &&)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    short_circuit = True
    for x in i[1:]:
        short_circuit = bool(short_circuit and x)
        if short_circuit == False:
            return False
    # If we make it to the end and none of the arguments were true (so we
    # didn't short-circuit), result must be False
    return True

def logic_not(i):
    '''
    Logical NOT (not, !)
    '''
    # No minimum arguments. NOT only takes 1 argument; the rest will be ignored.
    return not i[1]

# END LOGICAL SUBCOMMANDS

# MATH SUBCOMMANDS

def add(i):
    '''
    Add two or more numbers (add, +)
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        try:
            # Make sure arguments are numbers (int or float).
            # If either argument is a string, function will raise an error
            # and thus return None.
            i[1] + 0
            i[2] + 0

            return i[1] + i[2]
        except:
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        # Make sure arguments are numbers (int or float).
        # If either argument is a string, function will raise an error
        # and thus return None.
        i[1] + 0
        i[2] + 0

        return (i[1] + i[2]) and add([i[0]] + i[2:])
    except:
        return None

def sub(i):
    '''
    Subtract two or more numbers 
        (sub, - [hyphen], – [endash], − [minus sign])
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        try:
            # Make sure arguments are numbers (int or float).
            # If either argument is a string, function will raise an error
            # and thus return None.
            i[1] - 0
            i[2] - 0

            return i[1] - i[2]
        except:
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        # Make sure arguments are numbers (int or float).
        # If either argument is a string, function will raise an error
        # and thus return None.
        i[1] - 0
        i[2] - 0

        return (i[1] - i[2]) and sub([i[0]] + i[2:])
    except:
        return None

def mul(i):
    '''
    Multiply two or more numbers 
        (mul, *, × [multiplication sign, not X])
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return
    
    if len(i) == 3: # If 2 arguments
        try:
            # Make sure arguments are numbers (int or float).
            # If either argument is a string, function will raise an error
            # and thus return None.
            i[1] * i[1]
            i[2] * i[2]

            return i[1] * i[2]
        except:
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        # Make sure arguments are numbers (int or float).
        # If either argument is a string, function will raise an error
        # and thus return None.
        i[1] * i[1]
        i[2] * i[2]

        return (i[1] * i[2]) and mul([i[0]] + i[2:])
    except:
        return None

# def truediv(i):
#     '''
#     Divide two or more numbers. Do not round the result down.
#         (truediv, /, ÷)
#     '''

#     min_args = 2
#     if len(i) <= min_args:
#         log_warning('The command '+i[0]+' requires at least '+\
#                 min_args+' arguments.')
#         return
    
#     if len(i) == 3: # If 2 arguments
#         try:
#             # Make sure arguments are numbers (int or float).
#             # If either argument is a string, function will raise an error
#             # and thus return None.
#             i[1] / i[1]
#             i[2] / i[2]

#             return i[1] / i[2]
#         except:
#             return None
#     # But if there are 3 or more arguments (x1, x2, x3)...
#     try:
#         # Make sure arguments are numbers (int or float).
#         # If either argument is a string, function will raise an error
#         # and thus return None.
#         i[1] / i[1]
#         i[2] / i[2]

#         return (i[1] / i[2]) and truediv([i[0]] + i[2:])
#     except:
#         return None

# END MATH SUBCOMMANDS

# COLOR SUBCOMMANDS
    
def red(i, base_image):
    '''
    DOCUMENTATION: (red,0<x>,0<y>,1[width],1[height])

    Return the red value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average red value 
    over the given rectangle.
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [1, 1]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    if width <= 1 and height <= 1:
        rgba = base_image.getpixel((x, y))
        return rgba[0]
    else:
        avg = 0 # Average RED value of region
            
        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = base_image.getpixel((loop_x, loop_y))
                avg += rgba[0]
                
        avg = int(avg / (width * height))
        return avg
    
def green(i, base_image):
    '''
    DOCUMENTATION: (green,0<x>,0<y>,1[width],1[height])

    Return the green value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average green value 
    over the given rectangle.
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [1, 1]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    if width <= 1 and height <= 1:
        rgba = base_image.getpixel((x, y))
        return rgba[1]
    else:
        avg = 0 # Average GREEN value of region
            
        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = base_image.getpixel((loop_x, loop_y))
                avg += rgba[1]
                
        avg = int(avg / (width * height))
        return avg
    
def blue(i, base_image):
    '''
    DOCUMENTATION: (blue,0<x>,0<y>,1[width],1[height])

    Return the blue value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average blue value 
    over the given rectangle.
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [1, 1]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    if width <= 1 and height <= 1:
        rgba = base_image.getpixel((x, y))
        return rgba[2]
    else:
        avg = 0 # Average BLUE value of region
            
        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = base_image.getpixel((loop_x, loop_y))
                avg += rgba[2]
                
        avg = int(avg / (width * height))
        return avg
    
def alpha(i, base_image):
    '''
    DOCUMENTATION: (alpha,0<x>,0<y>,1[width],1[height])

    Return the alpha value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average alpha value 
    over the given rectangle.

    This is for GETTING the alpha/opacity value (from 0 to 255). 
    For applying a transparency filter, use "opacity".
    '''

    min_args = 2
    if len(i) <= min_args:
        log_warning('The command %s requires at least \
%d arguments.' % (i[0], min_args))
        return

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2:
        i = [i[0], 0, 0, base_image.size[0], base_image.size[1]]
    x = i[1]
    y = i[2]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 3:
        i += [1, 1]
    width = i[3]
    if len(i) == 4:
        i += [width]
    height = i[4]

    if width <= 1 and height <= 1:
        rgba = base_image.getpixel((x, y))
        return rgba[3]
    else:
        avg = 0 # Average ALPHA value of region
            
        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = base_image.getpixel((loop_x, loop_y))
                avg += rgba[3]
                
        avg = int(avg / (width * height))
        return avg

# END COLOR SUBCOMMANDS

###########################################################################
#### HELPER FUNCTIONS #####################################################
###########################################################################

# Clear the main content frame -- remove text, buttons, etc.
def cls():
    for child in main_frame.winfo_children():
        child.place_forget()

# Displays a dialog box with one or more buttons to the user. Holds until the
# user clicks a button. Returns the name of the button clicked.
# icon is one of: info, question, warning, error, done, bomb
def button_dialog(title:str, message:Union[str, list],
                  buttons=['Cancel', 'Okay'], *, icon:str=None):
    cls()

    button_clicked = None
    # Local function that all button event bindings point to
    # Sets the button_clicked variable one layer up so the function knows
    # it can return
    def button_event(index:int):
        nonlocal button_clicked
        button_clicked = buttons[index]

    dialog_icon = None
    if icon in icons:
        dialog_icon = Label(main_frame, image=icons[icon], bg=colors['BG'])
        dialog_icon.place(x=470, y=10, anchor=NE)

    next_y = 0
    if title:
        dialog_title = Label(main_frame, text=str(title), font=f_heading, 
                justify='left', bg=colors['BG'])
        dialog_title.place(x=0, y=0)
        # If there’s title text, leave space so msg_text doesn't cover it up
        next_y = 30

    dialog_message = []
    # Failsafe in case message is in an invalid format
    if not isinstance(message, list) and not isinstance(message, str): 
        message = str(message)
    # Convert to list if message is only one line / a string
    if isinstance(message, str): 
        message = [message]

    for index, item in enumerate(message):
        dialog_message.append(Label(main_frame, text=item, justify='left', 
                wraplength=470, bg=colors['BG']))

        # Apply bold styling as needed
        if item.startswith('<b>'):
            dialog_message[-1].config(font=f_bold, 
                                      text=item[3:]) # strip <b> tag

        # Shorten wrapping if dialog box has icon, so text doesn’t cover it
        if icon and next_y < 100:
            dialog_message[-1].config(wraplength=380)

        dialog_message[index].place(x=0, y=next_y)
        next_y += dialog_message[-1].winfo_reqheight() + 4

    # Reworked dialogs don't support bottom text 
    # (it adds unnecessary complexity).

    button_objs = []
    for index, item in enumerate(buttons):
        # Create new button object
        new_btn = Button(main_frame, text=item, 
                highlightbackground=colors['BG'],
                command=lambda c=index: button_event(c))
        # Add to button obj list
        button_objs.append(new_btn)

    # Place buttons one by one on the frame, aligned right and starting with
    # the rightmost button
    next_button_x = 470
    for i in reversed(button_objs):
        i.place(x=next_button_x, y=310, anchor=SE)
        next_button_x -= i.winfo_reqwidth()
        next_button_x -= 10 # a little extra space between buttons

    # Wait for user to click a button
    while button_clicked == None:
        window.update()
    # Once we get here, a button has been clicked, so return the button's name
    return button_clicked

# Simplified version of button_dialog() that only allows 2 buttons and returns
# a boolean value. If the user clicks the right/Okay button, return True.
# Otherwise, if the user clicks the left/Cancel button, return False.
def bool_dialog(title:str, message:Union[str, list],
                  button1='Cancel', button2='Okay', *, icon:str=None):
    button_name = button_dialog(title, message, [button1, button2], icon=icon)
    if button_name == button2:
        return True
    else:
        return False
    
# yn_dialog is like bool_dialog but the buttons' return values are reversed.
# The left/Yes button returns True, and the right/No button returns false.
def yn_dialog(title:str, message:Union[str, list],
                  button1='Yes', button2='No', *, icon:str=None):
    button_name = button_dialog(title, message, [button1, button2], icon=icon)
    if button_name == button1:
        return True
    else:
        return False

# Single-button dialog. Returns None.
def simple_dialog(title:str, message:Union[str, list], 
                  button='Okay', *, icon:str=None):
    button_dialog(title, message, [button], icon=icon)

def the_W():
    simple_dialog('There’s a new bird among us', 
                  'We will only be adding the W.',
                  'Clear cache', icon='info')
    menu()

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
        text='Now converting: file '+str(current_num)+\
            ' ('+str(rounded_pct)+'%)', 
        justify='left', bg=colors['BG'])
    subhead.place(x=0, y=36)

    return subhead

###########################################################################
#### MAIN FUNCTIONS #######################################################
###########################################################################

def setup():
    #### INITIAL GUI SETUP ####
    # setup is a separate function from menu() 
    # because we only need to do everything here once

    # Place frames
    main_frame.place(x=0, y=0) 
    footer_frame.place(x=0, y=320)
    # Note that all object positions are RELATIVE to their parent frame

    # Place footer items
    footer.place(x=5, y=15, anchor=W)
    back_btn.place(x=470, y=15, anchor=E)
    back_btn.bind('<Button-1>', lambda _: menu())

    # check message of the day
    motd()

    # check if we need to install assets
    need_assets = check_assets()
    if need_assets:
        confirm_assets = bool_dialog('Setup', 
['The program will now download the needed game images from the internet.',
'Is this okay?'],
                icon='question')
        if confirm_assets:
            install_assets()
        else:
            simple_dialog('Warning', 
['While you can use the converter without downloading the images, some \
conversions may not work properly.',
'You can download the images at any time by going to Legacy/Custom → \
Update Game Images from the main menu.'], icon='warning')
    # If no installation needed, proceed silently

    menu()

def menu():
    #### STEP 1: SELECT SCRIPT ####
    cls()

    # PAGE 1

    menu_btns_p1[0].bind('<ButtonRelease-1>', 
            lambda _: script_variant('scripts/skin_L_to_Dx32.txt',
                    'scripts/skin_L32_to_Dx32.txt'))
    menu_btns_p1[1].bind('<ButtonRelease-1>', 
            lambda _: script_variant('scripts/skin_R_to_Dx32.txt',
                    'scripts/skin_R32_to_Dx32.txt'))
    menu_btns_p1[2].bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/obj_L_to_Dx.txt'))

    menu_btns_p1[4].bind('<ButtonRelease-1>', 
            lambda _: menu_p2())

    menu_btns_p1[6].bind('<ButtonRelease-1>', 
            lambda _: exit_app())
    
    # PAGE 2

    menu_btns_p2[0].bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/skin_R_to_L.txt'))
    menu_btns_p2[1].bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/map_new.txt'))

    menu_btns_p2[3].bind('<ButtonRelease-1>', 
            lambda _: script_button(''))
    menu_btns_p2[4].bind('<ButtonRelease-1>', 
            lambda _: the_W())
    menu_btns_p2[5].bind('<ButtonRelease-1>', 
            lambda _: new_multi())
    menu_btns_p2[6].bind('<ButtonRelease-1>', 
            lambda _: install_assets())

    menu_btns_p2[8].bind('<ButtonRelease-1>', 
            lambda _: menu_p1())

    menu_p1()

    window.update()

    window.mainloop()

# EVENT HANDLER for most menu buttons
def script_button(script_file:str=None):
    open_result = open_script(script_file)
    if open_result:
        check_result = compatibility_check()
        if check_result:
            path_result = get_paths()
            if path_result:
                run_result = run_script()

                # If no files converted (legacy multi only)
                while run_result < 1: 
                    try_new_folder = yn_dialog('Warning', 
['The converter finished its task without any errors, but no files were \
converted.',
'Most likely this is because you ran a batch conversion on an \
empty or invalid folder.',
'Do you want to try converting a different folder instead?'],
icon='warning')
                    if try_new_folder:
                        path_result = get_paths(new_multi=True)
                        if path_result:
                            run_result = run_script(new_multi=True)
                        else:
                            break
                    else:
                        break
    # Go back to the menu at the end
    menu()

# SPECIAL EVENT HANDLER
# Two scripts have variants based on whether the Fire sprites are 
# 16×32 or 32×32. This allows the user to select which one they want
# without cluttering the main menu with buttons and explanatory text.
def script_variant(path16, path32):
    is_32 = bool_dialog('What size are your skin’s Fire sprites?', 
        '''If the 3rd row of sprites has noticeable empty spaces like this:
\u2003█\u2003█\u2003█\u2003█\u2003██\u2003██\u2003█ 
...it’s probably 16×32.

If the 3rd row looks more like this:
████████████████ 
...it’s probably 32×32.

If you’re not sure, try 16×32 first.''', '16×32', '32×32', icon='question')
    
    if is_32:
        script_button(path32)
    else:
        script_button(path16)

# SPECIAL EVENT HANDLER for new multi-file conversion
def new_multi():
    confirm1 = bool_dialog('Multi-File Conversion - Step 1: Select Script', 
['Want to convert an entire folder of images? You’ve come to the right place!',
 'First, you’ll need to select the script file you want to run.'], 
            'Cancel', 'Continue', icon='info')
    if confirm1:
        open_result = open_script()
        if open_result:
            check_result = compatibility_check()
            if check_result:
                confirm2 = bool_dialog(\
'Multi-File Conversion - Step 2: Select Folder',
['Next, you’ll need to select your source folder.',
 'All images in this folder will be converted.',
 'The converted images will be saved in a subfolder of the folder you select.'],
                        'Cancel', 'Continue', icon='info')
                if confirm2:
                    path_result = get_paths(new_multi=True)
                    if path_result:
                        run_result = run_script(new_multi=True)

                        # If no files converted
                        while run_result < 1: 
                            try_new_folder = yn_dialog('Warning', 
['The converter finished its task without any errors, but no files were \
converted.',
'Most likely this is because you ran a batch conversion on an \
empty or invalid folder.',
'Do you want to try converting a different folder instead?'],
icon='warning')
                            if try_new_folder:
                                path_result = get_paths(new_multi=True)
                                if path_result:
                                    run_result = run_script(new_multi=True)
                                else:
                                    break
                            else:
                                break
    # else
    menu()

# Takes 1 script line (in string format) and converts it to a program-readable
# list. Account for comments, nesting, etc.
def parse_line(line: str):
    global version
    
    # Strip whitespace from start and end of line
    line = line.lstrip().rstrip()

    # Commands where the parser should NOT treat commas as separators.
    # Note that all commands here have max 1 argument as a result.
    no_split_cmds = ['description', 'open', 'save', 'alt', 'template',
                     'warning', 'error']

    # Split line on commas
    output = ['']
    paren_depth = 0 # 0 = not inside parens, 1 = "(", 2 = "((" and so on
    in_string = False # True if inside double quotes
    for index, char in enumerate(line):
        if char == ',' and paren_depth == 0 and not in_string and \
                (len(output) == 1 or output[0] not in no_split_cmds):
            # Split on commas if not inside parens, not inside a string, 
            # and command isn't in the list of no-split commands
            output.append('')
        elif char == '#' and not in_string:
            # When a '#' character is reached, treat the rest of the line as a
            # comment and don't parse it, except if inside a string.
            break
        elif char == '$' and output[-1] == '' and in_string:
            # Temporary escape for $ at start of strings, so they don't get 
            # treated as variable names down the line
            output[-1] += '\\$'
        elif char == '"' and (index == 0 or line[index-1] != '\\'): 
            # Ignore double quotes that mark strings (unless they're escaped)
            pass
        elif char == '\\' and in_string and \
                (index == 0 or line[index-1] != '\\'):
            # Ignore backslashes unless there's two in a row
            pass
        else: # All other characters get parsed normally
            output[-1] += char

        # Separately from building the output list, 
        # update paren_depth and in_string
        if char == '(' and not in_string:
            paren_depth += 1
        elif char == ')' and not in_string:
            paren_depth -= 1
            # If paren_depth is ever negative, there are too many ")"s
            if paren_depth < 0:
                log_warning('\
Syntax error: Too many closing parentheses. Skipping line: '+line)
                return [''] # Return empty line so converter skips it
        elif char == '"' and (index == 0 or line[index-1] == '\\'): 
            # Strings are only double-quotes, in case I want to add char later
            # Flip it: If we're in a string, get out.
            # If we're not in a string, get in.
            in_string = not in_string

    # If paren_depth isn't back to 0 after exiting splitter loop, syntax error
    if paren_depth > 0:
        log_warning('\
Syntax error: Not enough closing parentheses. Skipping line: '+line)
        return [''] # Return empty line so converter skips it
    
    # If we're still in a string at the end of the line, syntax error
    if in_string:
        log_warning('\
Syntax error: Line ended before string did. Skipping line: '+line)
        return [''] # Return empty line so converter skips it

    for arg_n in range(len(output)):
        # remove whitespace from sides of commands
        output[arg_n] = output[arg_n].strip()

        # First item (i.e. command name) must be a lowercase string
        if arg_n == 0:
            # Since this is before type conversion, we can assume output[0]
            # is a string
            output[0] = output[0].lower() 
            # Go to next iteration before we would convert type
            continue

        is_var = False # whether the given argument's type is "variable name"
        # Convert variable names to custom dictionary type.
        # Conversion will NOT happen if:
        #   - The string is less than 2 characters long
        #   - It's the first argument for a "set" command
        #   - It's *any* argument for a header command
        # In these cases, the $text will be treated as a normal string.
        # If script was written for a version older than 6.0.0, the variable 
        # dict will be converted back to a string later.
        if len(output[arg_n]) >= 2 and not (output[0] == 'set' and arg_n == 1)\
                and not (output[0] in header_commands):
            # Remember, everything is still a string at this point.
            # str-to-int conversion is AFTER this
            if output[arg_n][0] == '$':
                output[arg_n] = {'type': 'var', 'content': output[arg_n]}
                is_var = True
            # Unescape dollar signs in string literals
            elif output[arg_n][0:2] == '\\$':
                output[arg_n] = output[arg_n][1:]
        
        if not is_var:
            try:
                # Convert data to int if possible
                output[arg_n] = int(output[arg_n])
            except ValueError:
                # No real use for floats yet so they're not supported
                # Just keep it as a string
                pass

    return output

# Open a script, run some validity checks on it, and display info to the user
# if it's a custom script.
# Return True if it's a valid script and the user wants to run it.
# Return False if there was an error or the user declined to run it.
def open_script(script_file=''):
    global data, version, version_str
    global loop_limit, loop_counter
    global block_depths, block_stacks

    # Ask user to pick a script if they want to run a custom script
    custom_script = False
    if not script_file:
        custom_script = True
        script_file = filedialog.askopenfilename(
                title='Select a script to run',
                initialdir='./scripts/')
        # If script file path is still empty, user cancelled, back to menu
        if script_file == '':
            return False

    #### STEP 2: SCRIPT INFO ####
    cls()

    try:
        file_obj = open(script_file, 'r')
        raw_content = file_obj.read()
        file_obj.close()
    except FileNotFoundError: 
        # If user somehow tries to run a nonexistent file
        simple_dialog('Error', 
            'Couldn’t find a file with that name. Please try again.', 
            'Back', icon='error')
        return False
    except UnicodeDecodeError: 
        # If user opens a “script” with weird characters
        simple_dialog('Error', 
            ['Couldn’t read the file with that name.',
                'Are you sure it’s a conversion script?'],
            'Back', icon='error')
        return False
    except IsADirectoryError: 
        # If user opens a folder or Mac app bundle
        simple_dialog('Error', 
            '''That file is a folder or application. 
Please try again.''',
            'Back', icon='error')
        return False

    lines = raw_content.splitlines()
    data = []
    # Add empty "line 0" to make goto more consistent
    data.append(parse_line(''))

    for l in lines:
        # First pass at parsing lines 
        # (variable values and subcommands are parsed later)
        data.append(parse_line(l))

    # The block stack is how we keep track of nested blocks.
    # Each item represents one line of code.
    # We start out empty, then if we enter a block via e.g. an if statement,
    # then "if" gets added onto the stack. When we reach an "end" command,
    # the last element is taken off the stack.
    block_stacks = [] 
    # Generate list of code lines, with "indentation" for each line
    block_depths = []
    current_depth = 0 # start
    for index, item in enumerate(data):
        # If it's the first line, start with one None item on the stack
        # so if e.g. an "if" block increases the depth to 1, "if" is item 1
        if index == 0:
            block_stacks.append([None])
        # Otherwise, copy the stack from the last line
        else:
            block_stacks.append(block_stacks[-1].copy())

        # If line is empty, skip the rest
        if len(item) < 1:
            continue
        
        # Add the current line's depth to block_depths
        block_depths.append(current_depth)

        # Decrease block depth if command is a block end
        if item[0] in block_ends:
            current_depth -= 1
            block_stacks[-1].pop()

        # If block depth is *ever* negative, that's an error
        if current_depth < 0:
            simple_dialog('Syntax error', 
                'This script’s block depth is imbalanced. Please check to make \
sure it doesn’t have one too many “end” commands.', icon='error')
            return False

        # If a header command is inside a block, remove it
        if current_depth >= 1 and item[0] in header_commands:
            data[index] = ['']
            log_warning('Syntax: ignoring header command at line %d as it is \
inside a block' % index)
                        
        # Increase block depth if command is a block start
        if item[0] in block_starts:
            current_depth += 1
            block_stacks[-1].append(item[0])

    # if depth is positive at end of code, error
    if current_depth < 0:
        simple_dialog('Syntax error', 
            'This script’s block depth is imbalanced. Please check to make \
sure each block has an associated “end” command.', icon='error')
        return False

    version = app_version.copy()
    version_str = '(UNKNOWN; defaulting to %s)' % app_version_str()
    for i in data:
        if i[0] == 'version':
            # If user entered 1 or 2 numbers for the version (e.g. "1" or
            # "4,1", assume the other numbers are 0s
            if len(i) < 2:
                log_warning('Syntax warning: Empty version')
            elif len(i) == 2:
                i.append(0)
                i.append(0)
            elif len(i) == 3:
                i.append(0)

            # Make sure version numbers are positive integers
            if type(i[1]) == int and type(i[2]) == int \
                    and type(i[3]) == int and \
                    i[1] >= 0 and i[2] >= 0 and i[3] >= 0:
                version = i[1:4]
                version_str = '.'.join([str(x) for x in version])
            else:
                log_warning('Syntax warning: Invalid version')
                version_str = '(INVALID; defaulting to %s)' % \
                        app_version_str()
            # If user didn't specify a version, assume it’s for the current
            # converter version (but display the version as unknown)
            break

    name = 'Unknown Script'
    for i in data:
        if i[0] == 'name':
            if len(i) > 1:
                name = i[1]
                break
            else:
                log_warning('Syntax error: Empty name')

    author = 'Unknown Author'
    for i in data:
        if i[0] == 'author':
            if len(i) > 1:
                author = i[1]
                break
            else:
                log_warning('Syntax error: Empty author')

    description = 'No description available.'
    for i in data:
        if i[0] == 'description':
            if len(i) > 1:
                description = ','.join(i[1:])
                break
            else:
                log_warning('Syntax error: Empty description')

    # To prevent infinite loops, keep track of how many times each line is run.
    # When a limit is reached (default 1000 times), halt the program.
    loop_limit = 1000
    loop_counter = [0] * len(data)
    for i in data:
        if i[0] == 'loop_limit':
            if len(i) > 1:
                if type(i[1]) == int and i[1] > 0:
                    loop_limit = i[1]
                    break
                else:
                    log_warning('Syntax error: Invalid loop limit \
(must be a positive integer)')
            else:
                log_warning('Syntax error: Empty loop limit')

    # Only show script info if it's a custom script, because default script
    # are assumed to work
    if custom_script:
        confirm = bool_dialog('Loaded script: %s'%name, 
                ['File path: %s'%script_file, 'By: %s'%author, 
                    'Made for converter version %s'%version_str,
                    'Description: %s'%description,
                    '',
                    '<b>Do you want to run this script?'], 
                'Cancel', 'Continue', icon='question')
        if confirm:
            return True
        else:
            return False
    else:
        return True

# Load header data from script, then perform a compatibility check.
# Return False if the user cancels, and True otherwise.
def compatibility_check():
    global data, version, version_str
    global open_path, save_path, template_path, alt_path
    global base_blank
    global start_num, stop_num, current_num
    global labels, variables, images

    #### STEP 3: COMPATIBILITY CHECK ####
    cls()

    # Load header data
    open_path = '.INPUT' # New in v4.0: Default to user input if no path given
    for i in data:
        if i[0] == 'open' and len(i) > 0:
            open_path = i[1]
            break

    alt_path = ''
    for i in data:
        if i[0] == 'alt' and len(i) > 0:
            alt_path = i[1]
            break
            
    template_path = ''
    for i in data:
        if i[0] == 'template' and len(i) > 0:
            template_path = i[1]
            break
            
    save_path = '.INPUT' # New in v4.0: Default to user input if no path given
    for i in data:
        if i[0] == 'save' and len(i) > 0:
            save_path = i[1]
            break

    base_blank = False
    for i in data:
        if i[0] == 'base' and len(i) > 0 and i[1] == 'blank':
            base_blank = True
            break

    start_num = None
    for i in data:
        if i[0] == 'start' and len(i) > 0:
            # start number has to be an integer
            if type(i[1]) != int:
                log_warning('Start number is not an integer.')
                break
            start_num = i[1]
            break

    stop_num = None
    for i in data:
        if i[0] == 'stop' and len(i) > 0:
            # stop number has to be an integer
            if type(i[1]) != int:
                log_warning('Stop number is not an integer.')
                break
            stop_num = i[1]+1
            # Unlike in Python, the “stop” is inclusive.
            # e.g. if stop is 10, it will convert #10 but not #11
            break

    # Warn if the “version” field is later than the current version
    # (unless it's just a newer release version)
    # The compatibility checks are irrelevant for scripts made for newer 
    # versions, because I can't predict the future.
    # Wait, no, I can predict the future: 
    # Chat will continue to be a mistake.
    if version[0] > app_version[0] or \
            (version[0] == app_version[0] and version[1] > app_version[1]):
        conf = yn_dialog('Compatiblity warning', 
            ['This script was designed for a newer converter version.',
'You can try to run it if you want, but we can’t guarantee it’ll work.',
'We are not responsible for any damage to your files this may cause.',
'',
'Do you want to continue anyway?'], 
            icon='warning')
        if not conf:
            return False
    # The compatibility checker used to be here, but I removed it in v6.0
    # because it caused more problems than it solved.

    # DATABASE RESETS & INITIAL SYNTAX CHECKS
    
    # Dictionary of labels and the index of `data` on which they were found.
    # Example: {'_start': 0}
    # The user-facing line number will be 1 higher, 
    # e.g. _start is actually on line 1 in this example.
    labels = {}
    for index, item in enumerate(data):
        if item[0] == 'label':
            if len(item) > 1:
                if item[1] in labels:
                    log_warning(\
'Syntax error: Duplicate label “%s” on line %d ignored' % (item[1], index))
                elif type(item[1]) != str:
                    log_warning(\
'Syntax error: Label “%s” on line %d ignored because it’s not a string' % \
(item[1], index))
                else:
                    # If the label hasn't already been used, add it to the
                    # labels dictionary
                    labels[item[1]] = index
            else:
                log_warning('Syntax error: empty label')

    # Variables will mostly be user-set but let's predefine the booleans
    variables = {'$_true': True, '$_t': True,
                 '$_false': False, '$_f': False}
    
    # Images the converter can access, 
    # including 'old' (open), 'template', 'alt', and 'new' (save/base)
    # and any user-defined images
    images = {}

    return True

# Get the paths for the IMAGES the user wants to open and save to.
# Return False if there’s an invalid path or the user cancelled.
# Return True otherwise.
def get_paths(*, new_multi=False):
    global legacy_multi, start_num, stop_num, open_path, save_path, \
        multi_open_paths, multi_save_paths

    #### STEP 4: OPEN & SAVE PATHS ####
    cls()

    # Determine whether script is converting 1 file (single-file mode)
    # or multiple files (multi-file mode)
    # For a valid legacy multi-file conversion, open_path & save_path must have 
    # wildcards, and there must be start and stop numbers provided. Otherwise,
    # the script will be treated as a single-file conversion.
    legacy_multi = False # reset in case past conversions set this global var
    if start_num != None and stop_num != None and \
            '*' in open_path and '*' in save_path:
        # Note that both open and save paths must have a * in them
        legacy_multi = True
    # If a script is not a valid legacy multi-file conversion but it has start 
    # and stop numbers, throw a warning
    # TODO: Disabled due to possible bugs
#     if not legacy_multi and (start_num != None or stop_num != None):
#         log_warning('Script has start/stop numbers but is not a valid legacy \
# multi-file conversion script')

    # Make user choose image to open if that's what the script wants
    if new_multi:
        # For new multi-file conversions, ask for a FOLDER
        # (and override any open/save header commands)
        open_path = filedialog.askdirectory(
                title='Select a folder. All images in the folder will be \
converted.',
                initialdir='./')
        # If open_path is still empty, user cancelled — go back to step 1
        if not open_path:
            return False
        # Else, generate a list of paths for the main processor to loop through
        multi_open_paths = glob(open_path+'/*')
        start_num = 0
        stop_num = len(multi_open_paths)
    else:
        if open_path.upper() == '.INPUT':
            open_path = filedialog.askopenfilename(\
                    title='Choose an image to open and copy from',
                    initialdir='./')
            # If open_path is still empty, user cancelled — go back to step 1
            if not open_path:
                return False

    # Only run the open-path existence check on single-file conversions. 
    # For legacy multi-file conversions, existence will be checked file-by-file 
    # in the main loop. 
    # For new multi-file conversions, both error types should be moot.
    if not legacy_multi and not new_multi:
        try:
            # This part doesn't actually open the file for conversion --
            # it's just to make sure it exists
            open(open_path).close()
        except FileNotFoundError:
            # This code will only be reached in legacy single-file mode because
            # the OS file selector shouldn't select a nonexistent file
            choose_new_path = yn_dialog('File warning', 
['The script tried to open the following file, but it does not exist.',
'<b>'+open_path,
'Do you want to select a different file to open?'], 'Yes', 
                    'No (back to menu)', icon='warning')
            if choose_new_path:
                open_path = filedialog.askopenfilename(\
                        title='Choose an image to open and copy from',
                        initialdir='./')
                # If open_path is still empty, user cancelled
                if not open_path:
                    return False
            else:
                return False
        except IsADirectoryError: 
            # If user opens a folder or Mac app bundle
            choose_new_path = yn_dialog('File warning', 
                    '''The path '''+open_path+''' is a folder or application.
Do you want to select a different file to open?''', 'Yes', 
                    'No (back to menu)', icon='error')
            if choose_new_path:
                open_path = filedialog.askopenfilename(\
                        title='Choose an image to open and copy from',
                        initialdir='./')
                # If open_path is still empty, user cancelled
                if not open_path:
                    return False
            else:
                return False

    # Make user choose image to save if that's what the script wants
    if new_multi:
        base_save_path = open_path + '/_converted'
        save_path = base_save_path
        
        i = 1
        while os.path.exists(save_path): 
            # If there's already a subfolder called _converted, 
            # tack a number on the end
            save_path = base_save_path + str(i)
            i += 1
        # Actually make the subfolder
        os.makedirs(save_path)

        # Generate a save path for each image
        multi_save_paths = [save_path+os.sep+(i.split(os.sep)[-1]) \
                            for i in multi_open_paths]

        return True
    elif save_path.upper() == '.INPUT': # i.e. modern single-file scripts
        save_path = filedialog.asksaveasfilename(\
                title='Choose a location to save to', defaultextension='.png',
                filetypes=[('PNG image', '*.png')],
                initialdir='./')
        # If save_path is still empty, user cancelled — go back to step 1
        if save_path == '':
            return False
        else: 
            # The rest of this function is checking if the save path
            # would overwrite any existing files, but we don't need 
            # to check this ourselves here because the system dialog 
            # handles it
            return True
    else: # Only for legacy scripts (single- and multi-file)
        # Make sure parent directory of save_path exists, 
        # if it's saving inside a directory
        parent_dir = os.sep.join(save_path.split(os.sep)[:-1])
        # “if parent_dir” => if there’s no parent directory because you’re
        # saving to the current working directory, skip the directory check
        if parent_dir and not os.path.exists(parent_dir):
            choose_new_path = yn_dialog('Error', 
['The script is trying to save to a folder that doesn’t exist.',
'The path that caused the error was:', 
'<b>'+parent_dir,
'Do you want to select a different location?'], 
                'Yes', 'Back to Menu', icon='error')
            if choose_new_path:
                save_path = filedialog.asksaveasfilename(\
                        title='Choose a location to save to', 
                        defaultextension='.png',
                        filetypes=[('PNG image', '*.png')], initialdir='./')
                # If save_path is still empty, user cancelled
                if save_path == '':
                    return False
                else: 
                    # The rest of this function is checking if the save path
                    # would overwrite any existing files, but we don't need 
                    # to check this ourselves here because the system dialog 
                    # handles it
                    return True
            else:
                return False

        # Check if the file already exists
        files_to_overwrite = []
        main_text = ['This text shouldn’t show up for any reason.',
'If it does, please tell Clippy how you got here so he can fix it!']
        if legacy_multi: # …then we need to check EVERY file we're saving to
            for i in range(start_num, stop_num):
                check_path = save_path.replace('*', str(i))
                if os.path.exists(check_path):
                    files_to_overwrite.append(check_path)
                    # TODO: add a way to display all the
                    # files that would be overwritten 
                    # (3-button box with More button)

            if files_to_overwrite:
                main_text = [
                    'This script will overwrite:',
                    '<b>%s' % files_to_overwrite[0],
                    '<b>...and %i other files.' % (len(files_to_overwrite)-1),
                    'You can’t undo this action.',
                    '\
Please check the path %s (and replace * with any number from %i to %i) to see \
what other files will be overwritten.' \
    % (save_path, start_num, stop_num),
                    'Only run scripts from users you trust!',
                ]
            else:
                # No files to overwrite -- move on
                return True
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
                # No files to overwrite -- move on
                return True

        conf = yn_dialog('Warning', main_text + [
                '', 
                'Do you want to run this script anyway?'
            ], icon='warning')

        if conf:
            return True
        else:
            return False

# Runs the selected conversion script on as many files as called for.
# Return number of files successfully converted.
def run_script(*, new_multi=False):
    global data, open_path, save_path, template_path, alt_path, base_blank,\
            start_num, stop_num, current_num, legacy_multi

    #### STEP 5: RUN SCRIPT ####
    cls()

    # Set current_num after start_num is set but before the first 
    # update_subhead call
    current_num = start_num

    heading_text = Label(main_frame, text='Converting image...', 
        font=f_heading, bg=colors['BG'])
    heading_text.place(x=0, y=0)

    # Update screen differently based on how many files we're converting
    heading = Label(bg=colors['BG'])
    subhead = Label(bg=colors['BG'])
    if new_multi:
        heading = Label(main_frame, 
            text='Converting all images in the folder %s' % \
                multi_open_paths[0].split(os.sep)[-2], 
            font=f_heading, bg=colors['BG'])
        subhead = update_subhead(subhead)
    elif legacy_multi:
        heading = Label(main_frame, text='Converting all images from '+\
            str(start_num)+' to '+str(stop_num-1), font=f_heading, 
            bg=colors['BG'])
        subhead = update_subhead(subhead)
    else:
        # For single-image conversions, set start/stop so the main loop will 
        # only run once
        heading = Label(main_frame, text='Converting 1 image...', 
            font=f_heading, bg=colors['BG'])
        start_num = 0
        stop_num = 1
    heading.place(x=0, y=0)
    window.update()
    
    # Start the clock
    t1 = time()
    time_last_refresh = t1
    time_since_refresh = 0
    conv_count = 0 # Count how many files have been converted

    # Load template image only once because it doesn't allow wildcards
    images['template'] = None
    try:
        if template_path != '':
            # template_path doesn't support wildcards because the point is
            # for there to be just 1 template
            images['template'] = PIL.Image.open(template_path).convert('RGBA')
        else:
            images['template'] = None
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

    images['alt'] = None
    try:
        if alt_path != '':
            images['alt'] = PIL.Image.open(alt_path).convert('RGBA')
        else:
            images['alt'] = None
    except FileNotFoundError:
        log_warning('Couldn’t find an alternate file with the path '+\
            alt_path+' — skipping')
    except (AttributeError, PIL.UnidentifiedImageError): 
        # We opened something, but it's not an image
        log_warning('Couldn’t open the alternate file at ' + \
            alt_path + '.')
        log_warning('    - Are you sure it’s an image? Skipping.')
    except IsADirectoryError: # If user opens a folder or Mac app bundle
        log_warning('The alternate path '+alt_path+\
            ' is a folder or application.')

    # Main file-reading loop -- a different function does the actual processing
    # - For single-file conversion, start_num=0 and stop_num=1; this loop will
    #   only run once in these cases.
    # - For new multi-file conversion, stop_num is the length of the list of 
    #   files in the selected directory, and i is the list index for the 
    #   filename currently being converted.
    # - For legacy multi-file conversion, start_num and stop_num are pulled 
    #   from the conversion script.
    for i in range(start_num, stop_num):
        current_num = i

        # Update user on conversion progress.
        # Update only once per second so we don't slow things down too much
        # from updating the UI
        time_since_refresh += (time() - time_last_refresh)
        if time_since_refresh > 1:
            update_subhead(subhead)
            window.update()
            time_last_refresh = time()
            time_since_refresh = 0

        images['old'] = None
        try:
            if new_multi:
                # New multi-image conversions change open_path and save_path
                # for every iteration of the file-reading loop
                open_path = multi_open_paths[i]
                save_path = multi_save_paths[i]
                # Read image based on the new open path
                images['old'] = PIL.Image.open(open_path).convert('RGBA')
            elif legacy_multi:
                images['old'] = PIL.Image.open(open_path.replace('*', 
                    str(i))).convert('RGBA')
            else:
                images['old'] = PIL.Image.open(open_path).convert('RGBA')
        except FileNotFoundError:
            # Don't need to check for legacy_multi because in single mode,
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
            continue

        if base_blank:
            # Create a blank base if the script starts with that
            if images['template']: 
                # If we opened a valid template image, use its size for the
                # blank base
                w, h = images['template'].size
            else:
                # Otherwise, default to the size of the image we opened
                w, h = images['old'].size
            images['new'] = PIL.Image.new('RGBA', (w,h))
        else:
            # If no base is specified, start new image as copy of old image
            images['new'] = images['old'].copy()

        images['new'] = process(data)
        images['new'].save(save_path.replace('*', str(i)))
        conv_count += 1

    t2 = time()
    return pre_summary(t2-t1, conv_count) # Return helper func's result

def process_line(line: list):
    '''
    Given a line (in list form), return it in processed form, by substituting
    variable names for their associated values, then running any subcommands.
    This function does NOT execute the line's main command.
    '''
    global images

    new_line = line.copy() 

    for arg_n in range(1, len(new_line)):
        # Replace variable names with the variable's current value
        if type(new_line[arg_n]) == dict and new_line[arg_n]['type'] == 'var':
            if version[0] >= 6:
                new_line[arg_n] = variables[new_line[arg_n]['content']]
            else:
                new_line[arg_n] = new_line[arg_n]['content']
                log_warning('Variable name %s ignored because \
variables are not supported in scripts written for versions older than 6.0.0.'\
                            % new_line[arg_n]['content'])

        # Now that we've broken the command into the normal list format,
        # we need to check each argument of the command for parens and
        # recursively call this function as needed.
        if type(new_line[arg_n]) == str and \
                new_line[arg_n].startswith('(') and \
                new_line[arg_n].endswith(')'):
            # Execute the command INSIDE the parens FIRST
            new_line[arg_n] = subcmd(new_line[arg_n], images['old'], 
                                    images['template'], images['alt'], 
                                    images['new'])

    return new_line

# Reads lines from one file and executes its instructions
def process(data: list):
    global version
    global labels, variables, images
    global loop_limit, loop_counter

    # MAIN LINE-PROCESSING LOOP
    # Remember, each line has been parsed into list format already, 
    # but the subcommands have NOT been parsed
    index = 0 # START
    jumped = False # True if running the current line interrupted normal flow
    while index < len(data): # STOP
        item = process_line(data[index]) # MANUAL ENUMERATE

        # Uncomment this to print line-by-line output
        print(index, item, block_depths[index], block_stacks[index])

        # Increment loop counter for the line
        loop_counter[index] += 1
        # If we hit the loop limit, stop the script to prevent infinite loops
        if loop_counter[index] >= loop_limit:
            simple_dialog('Conversion error', 
                    '''Conversion stopped because the loop limit of %i was \
reached on line %i.
Please check your code to make sure there isn’t an infinite loop.
If you meant to loop this many times, you can increase the loop limit using \
the “loop_limit” header command.''' % (loop_limit, index), 
                    'Back to Menu', icon='error')
            menu()

        try:
            jumped = False # Reset jumped flag for new line

            if item[0].strip() == '': # Skip blank lines
                continue
            elif item[0] == 'exit': 
                # End the conversion early, but save the target file as is 
                # and exit properly.
                break
            elif item[0] == 'error':
                # Stop conversion without saving, and optionally display a 
                # message on the screen
                if len(item) < 2: # If the script doesn't include error msg
                    item.append('The conversion script was stopped due to an \
unknown error.')
                simple_dialog('Conversion error', item[1], 'Back to Menu',
                              icon='error')
                menu()
            elif item[0] == 'warning':
                warning(item)

            # Control commands
            elif item[0] == 'goto': 
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning('goto: missing line number')
                    continue

                # OPTION 1: Go to line number
                # Line numbers start counting from 1, even internally
                if type(item[1]) == int:
                    index = item[1]
                    jumped = True
                # OPTION 2: Go to label
                # This will jump to the line on which the label was declared.
                elif type(item[1]) == str:
                    if item[1] in labels:
                        index = labels[item[1]]
                        jumped = True
                    else:
                        log_warning('goto: Unrecognized label')
                else:
                    log_warning('goto: Must go to a line number (integer)')

            # One-line variant of if
            elif item[0] == 'if1':
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning('if: missing conditional statement')
                    continue

                # Result of conditional command in the if statement
                # item[1] will already be processed by the subcmd call above
                cond_result = bool(item[1])

                # If condition is FALSE, skip the next line
                if not cond_result:
                    index += 2
                    jumped = True
                # Otherwise, do nothing and the interpreter will process the
                # next line normally

            elif item[0] == 'if':
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning('if: missing conditional statement')
                    continue

                # Save depth of if block so we can check it against the 
                # elseif/else/end lines we're parsing later
                start_depth = block_depths[index]

                # Result of conditional command in the if statement
                # item[1] will already be processed by the subcmd call above
                cond_result = bool(item[1])

                # IF first conditional is FALSE, skip until we're out of 
                # the block (either elseif, else, or end)
                while not cond_result:
                    index += 1
                    item = process_line(data[index])

                    # Skip lines that don't match the depth of the original if line
                    if block_depths[index] != start_depth:
                        continue

                    if item[0] == 'elseif':
                        # Try the condition for the elseif line
                        cond_result = bool(item[1])
                        # And if this is true, then we'll get out of the loop 
                        # and run the code inside the elseif
                    elif item[0] == 'else':
                        # If we make it down here, the code in here will 
                        # run no matter what
                        break
                        # Note we're breaking out from the inner `while` loop, 
                        # not the main `for` loop
                    elif item[0] == 'end':
                        # And we're done
                        break

                # IF we get past this point (conditional is True), 
                # there's nothing more to do here. We're in the if block. 
                # Proceed as normal until we reach an "end" command.

            elif len(block_stacks[index]) > 0 \
                    and block_stacks[index][-1] in ['if', 'elseif', 'else'] \
                    and item[0] in block_ends:
                # If we encounter elseif, else, end, etc. during the normal 
                # line-reading cycle, then we've finished a block from a 
                # condition that evaluated as true, so we're done with the 
                # whole if statement

                # Go to the if block's associated end command
                while item[0] not in ['end', 'endif']:
                    index += 1
                    item = data[index]
                    # No need to process arguments because we only need to 
                    # check arg0 (command name) right now

                # Note that the "current" line is the line that actually has the
                # elseif/else/end, but this will be incremented in the
                # "finally" block below this loop so we're past the blocks

            elif item[0] == 'while':
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning('while: missing conditional statement')
                    continue

                # Save depth of if block so we can check it against the 
                # elseif/else/end lines we're parsing later
                start_depth = block_depths[index]

                # Result of conditional command in the if statement
                # item[1] will already be processed by the subcmd call above
                cond_result = bool(item[1])

                # IF first conditional is FALSE, skip until we're out of 
                # the block (either elseif, else, or end)
                while not cond_result:
                    index += 1
                    item = data[index]
                    # No need to process arguments because we only need to 
                    # check arg0 (command name) right now

                    # Skip lines that don't match the depth of the original if line
                    if block_depths[index] != start_depth:
                        continue

                    # Search for the "end" so we can skip past the loop
                    if item[0] == 'end':
                        break

                # IF we get past this point (conditional is True), 
                # there's nothing more to do here. We're inside the loop. 
                # Proceed as normal until we reach an "end" command.

            elif len(block_stacks[index]) > 0 and \
                    block_stacks[index][-1] == 'while' and item[0] == 'end':
                # If we reach an "end" when we're in a 
                # while loop (but otherwise reading lines normally), 
                # then we've reached the end of the loop block,
                # so we need to jump back up to continue the loop

                start_depth = block_depths[index]
                # Move up the lines until we reach a "while" command with
                # depth 1 less than our current depth. 
                # That'll be the block we want to jump to.
                while not cond_result:
                    index += 1
                    item = data[index]
                    # No need to process arguments because we only need to 
                    # check arg0 (command name) right now

                    if block_depths[index] != start_depth-1:
                        continue

                    # Search for the "end" so we can skip past the loop
                    if item[0] == 'while':
                        # Next line we run will check the while condition again
                        jumped = True 
                        break

            # TODO: No continue or break yet -- just use gotos for now

            # Variable commands (ONLY in scripts for v6+)
            elif item[0] == 'set':
                if version[0] >= 6:
                    set(item)
                else:
                    log_warning('set: Variables are only supported in scripts \
written for version 6.0.0 or later')
            
            # Basic copying commands
            elif item[0] == 'copy':
                copy(item, images['old'], images['new'])
            elif item[0] == 'copy_alt' or item[0] == 'copyalt':
                if not images['alt']:
                    log_warning('\
copyalt: Skipped because no “alt” image was specified.')
                else:
                    copy(item, images['alt'], images['new'])
            elif item[0] == 'copy_from':
                # Unlike other copy commands, `copyfrom` uses global image list
                # and passes the appropriate images to `copy`
                copy_from(item)
            elif item[0] == 'default':
                if not images['template']:
                    log_warning('\
default: Skipped because no “template” image was specified.')
                else:
                    default(item, images['template'], images['new'])
            elif item[0] == 'default_from':
                # Similar to copyfrom above but copying to same x/y position
                default_from(item)
            elif item[0] == 'clear':
                clear(item, images['new'])
            elif item[0] == 'delete':
                clear(item, images['new'])
                if version[0] >= 6:
                    log_warning('delete: Deprecated alias; please use “clear”')
            elif item[0] == 'duplicate':
                duplicate(item, images['new'])

            # Advanced copying commands
            elif item[0] == 'tile':
                tile(item, images['old'], images['alt'], images['new'])

            # Transformation commands
            elif item[0] == 'resize':
                images['new'] = resize(item, images['new'])
            elif item[0] == 'rotate':
                rotate(item, images['new'])
            elif item[0] == 'flip':
                flip(item, images['new'])

            # Filter commands
            elif item[0] == 'grayscale':
                grayscale(item, images['new'])
            elif item[0] == 'invert':
                invert(item, images['new'])
            elif item[0] == 'color_filter' or item[0] == 'colorfilter':
                colorfilter(item, images['new'])
            elif item[0] == 'opacity':
                opacity(item, images['new'])
            elif item[0] == 'hue': # TODO: rename and make hue a subcmd?
                hue(item, images['new'])
            elif item[0] == 'saturation':
                saturation(item, images['new'])
            elif item[0] == 'lightness':
                lightness(item, images['new'])
            elif item[0] == 'fill':
                fill(item, images['new'])
            elif item[0] == 'contrast':
                contrast(item, images['new'])
            elif item[0] == 'colorize':
                colorize(item, images['new'])
            elif item[0] == 'sepia':
                sepia(item, images['new'])
            elif item[0] == 'threshold':
                threshold(item, images['new'])

            # Just so it doesn't think header commands are unknown
            elif item[0] in header_commands:
                # I always mess this particular command up so I'll just 
                # hardcode in a note to self
                if item[0] == 'template' and len(item) > 2:
                    log_warning('Clippy, you idiot, the command you’re looking \
for is “default”, not “template”')
                # Otherwise, just skip the line since we've presumably already
                # dealt with it
            else:
                log_warning('Unknown command on line %i: %s' % (index, item[0]))

        # except Exception as e: 
        #     # Handle any errors in the command functions so they don’t bring
        #     # the whole program to a halt
        #     log_warning(str(item[0])+' command skipped due to error: '+str(e))

        finally:
            # Note: This block *will* be reached even if "continue" is called
            # in the "try" part of the loop.
            if not jumped:
                index += 1 # STEP

    return images['new'] 

# Returns number of files successfully converted.
def pre_summary(conv_time, conv_count):
    #### STEP 6: SUMMARY ####
    cls()

    # Check if we're running on replit
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
            '...the quickest option is probably to download the whole project.',
            'This will download a lot of unnecessary files but it’s faster',
            'than downloading each image one at a time.'
        ]
        simple_dialog('Replit Help', help_text, 'Okay', icon='info')

    if conv_count == 0 and (legacy_multi or new_multi):
        # Break out before we would show summary
        return 0

    summary(conv_time, conv_count)
    return conv_count

def summary(conv_time, conv_count, warning_page=0):
    # Roll warning page over to 0 if needed
    warn_per_page = 10 # TODO: account for multiline warnings
    num_warn_pages = (len(warnings)-1)//warn_per_page + 1
    if warning_page >= num_warn_pages:
        warning_page = 0

    main_text = ['Converted %d files in %s seconds' % 
                 (conv_count, str(round(conv_time, 3)))]
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
            confirm_exit = button_dialog('Conversion complete!', 
                    main_text + ['', bottom_text], ['More warnings', 'Okay'], icon='warning')
            if confirm_exit == 'More warnings':
                summary(conv_time, conv_count, warning_page+1) # next page
            else:
                return
        else:
            # Display dialog with warnings but no extra button
            # if there's only 1 page worth of warnings
            simple_dialog('Conversion complete!', main_text + ['', bottom_text], icon='warning')
            return
    else:
        simple_dialog('Conversion complete!', main_text,
            'Okay', icon='done')
        return

# List of files to install on first run
# Only download images that a script actually uses
install_list = [
    ['https://marioroyale.com/royale/img/game/smb_obj.png', 
        'deluxe/smb_obj.png'],
    ['https://marioroyale.com/royale/img/game/smb_mario.png', 
        'deluxe/smb_mario.png'],
    ['https://github.com/mroyale/assets/raw/legacy/img/game/smb_map_new.png', 'legacy/smb_map_new.png']
]

# Check if assets need to be (re)installed
def check_assets():
    global install_list

    for i in install_list:
        if not os.path.isfile('assets/'+i[1]): 
            # If a file in the install list is missing, we need to reinstall
            return True
    
    # If all the files exist, no need to install
    return False

# Install the latest game assets
def install_assets():
    global install_list

    # Create subfolders if they don't exist
    if not os.path.isdir('./assets/deluxe'):
        os.makedirs('./assets/deluxe')
    if not os.path.isdir('assets/legacy'):
        os.makedirs('./assets/legacy')

    for i in install_list:
        try:
            urllib.request.urlretrieve(i[0], 'assets/'+i[1])
        # Deal with connection errors
        except urllib.error.URLError:
            simple_dialog('Connection error', 
'Failed to download image %s. Check your internet connection and try again.' % \
i[0], icon='error')
            menu()
        except Exception:
            simple_dialog('Connection error', 
'An unknown error occurred while downloading the image %s.' % \
i[0], icon='error')
            menu()

    simple_dialog('Success', 'The images were successfully downloaded.',
                icon='done')
    menu()

# Download and display the online Message of the Day
'''
For each line, everything before the first space is the full list versions that should show the message. The rest of the line is the message itself.
The program displays a maximum of 1 MOTD -- the first that matches its version.

EXAMPLE MOTD FORMAT:

# This line is a comment and will be ignored.
u_2.3.0 Deluxifier v3.0.0 is now available! Click the "View Update" button \
    to open Github and download the update.
2.2.1_2.2.2 WARNING: Please update your program to 2.3.0 or later. \
    The version you're currently using has a bug that could damage your files.
* We will only be adding the W.

This version of the program would display "We will only be adding the W."
because it doesn't match any of the versions specified for the warnings.
'''
def motd():
    motd_url = 'https://raw.githubusercontent.com/WaluigiRoyale/\
Deluxifier/main/motd.txt'
    try:
        # Download and read MOTD
        urllib.request.urlretrieve(motd_url, 'motd.txt')
        motd_file = open('motd.txt')
        motd_lines = motd_file.read().splitlines()
        for i in range(len(motd_lines)):
            # Split into version and message
            motd_lines[i] = motd_lines[i].split(' ', 1) 
            if (len(motd_lines[i]) == 2) and \
                    ((app_version_str() in motd_lines[i][0]) or \
                        (motd_lines[i][0] == '*')):
                motd = motd_lines[i][1]
                motd_header = 'News!'
                motd_buttons = ['Exit', 'Continue']
                # Add update button if MOTD is flagged as an update notice
                if 'u' in motd_lines[i][0].lower():
                    motd_buttons.insert(0, 'View Update')
                    motd_header = 'Update available'

                motd_continue = button_dialog(motd_header, motd, motd_buttons)
                if motd_continue == 'Exit':
                    exit_app()
                elif motd_continue == 'View Update':
                    webbrowser.open('https://github.com/WaluigiRoyale/\
MR-Converter-GUI/releases/latest')
                else: # Continue
                    return
    except:
        # If the internet isn't cooperating or the MOTD file is malformed, 
        # no big deal, just skip it
        pass

def crash(exctype=None, excvalue=None, tb=None):
    import tkinter.messagebox as messagebox
    try:
        bomb = PhotoImage(file='ui/bomb.gif')
        window.iconphoto(False, bomb)
    finally:
        # Tkinter doesn't have a "public" way to show the error dialog I want,
        # but the options are hidden under the hood. 
        # Code based on Tkinter messagebox.py
        btn = messagebox._show('Error', '''An error has occurred.
%s: %s''' % (str(exctype)[8:-2], excvalue), 
messagebox.ERROR, messagebox.ABORTRETRYIGNORE)
        # btn might be a Tcl index object, so convert it to a string
        btn = str(btn)
        if btn == 'ignore':
            return
        elif btn == 'retry':
            setup()
        else: # abort
            exit_app()

def exit_app():
    window.destroy()
    sys.exit()

###########################################################################
#### START THE PROGRAM ####################################################
###########################################################################

try:
    # Comment the next line out to print full crash messages to the console
    # window.report_callback_exception = crash
    
    # Check if we're running on replit
    if os.path.isdir("/home/runner") == True:
        import tkinter.messagebox as messagebox

        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Ask user to enter fullscreen
        messagebox.showinfo(window, 
            message='''\
Looks like you’re running the online (Replit) version of the skin converter! 
You may want to enter fullscreen so you can click all the buttons.
Click the ⋮ on the “Output” menu bar then click “Maximize”. 
If you’re on a phone, rotate it sideways, zoom out, \
and hide your browser’s toolbar.''')

        # show online instructions
        messagebox.showinfo(window, 
        message='''Before converting your first file:
1. Create a Replit account. You can use an existing Google or Github account.
2. Click “Fork Repl” and follow the instructions.
3. In your newly-forked project, drag the images you want to convert \
into the list of files in the left sidebar.''')

    # Proceed to setup on all platforms
    setup()

except Exception as e:
    ei = sys.exc_info()
    crash(None, ei[1])