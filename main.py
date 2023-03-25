'''
MR Skin Converter 
Version 5.1.0

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

import os, sys, colorsys
import urllib.request # for installing assets
import PIL.Image, PIL.ImageOps, PIL.ImageTk
from typing import Union
from time import time
from tkinter import *
import tkinter.font as tkfont
import tkinter.filedialog as filedialog

###########################################################################
#### GLOBAL VARIABLES #####################################################
###########################################################################

app_version = [5,1,0]

def app_version_str():
    return str(app_version[0])+'.'+str(app_version[1])+'.'+\
        str(app_version[2])

window = Tk()
window.wm_title('Clippy’s Skin Converter v' + app_version_str())
window.geometry('640x320')
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

side_frame = LabelFrame(window, width=160, height=320, bg=colors['BG'])

'''
gray = not yet reached
blue = in progress
green = completed
red = failed
'''
step_status = ['blue', 'gray', 'gray', 'gray', 'gray', 'gray']
steps = [
    Label(side_frame, text='● Select Script', fg=colors[step_status[0]], 
        justify='left', bg=colors['BG']),
    Label(side_frame, text='● Load Script', fg=colors[step_status[1]], 
        justify='left', bg=colors['BG']),
    Label(side_frame, text='● Compatibility Check', 
        fg=colors[step_status[2]], 
        justify='left', bg=colors['BG']),
    Label(side_frame, text='● Open & Save Paths', fg=colors[step_status[3]], 
        justify='left', bg=colors['BG']),
    Label(side_frame, text='● Run Script', fg=colors[step_status[4]], 
        justify='left', bg=colors['BG']),
    Label(side_frame, text='● Summary', fg=colors[step_status[5]], 
        justify='left', bg=colors['BG']),
]

title = Label(side_frame, text='Skin Converter v'+app_version_str(), 
        font=f_bold, bg=colors['BG'])
footer = Label(side_frame, text='a Clippy production', 
        fg=colors['gray'], bg=colors['BG'])

main_frame = LabelFrame(window, width=480, height=320, bg=colors['BG'])
main_frame.grid_propagate(False)

menu_heading = Label(main_frame, text='What do you want to convert?', 
        font=f_heading, bg=colors['BG'])

menu_btns_p1 = [
    Button(main_frame, text='Convert a Legacy skin to Deluxe',
            font=f_large, highlightbackground=colors['BG']),
    Button(main_frame, text='Convert a Remake skin to Deluxe',
            font=f_large, highlightbackground=colors['BG']),
    Button(main_frame, text='Convert ANY obj mod to Deluxe',
            font=f_large, highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Legacy/Custom...', 
            highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Exit', highlightbackground=colors['BG']),
]

menu_btns_p2 = [
    Button(main_frame, text='Convert a Remake skin to Legacy', 
            highlightbackground=colors['BG']),
    Button(main_frame, text='Convert a Remake obj to Deluxe', 
            highlightbackground=colors['BG']),
    Button(main_frame, 
            text='Convert a Legacy map mod to Legacy map_new', 
            highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Run a custom script', 
            highlightbackground=colors['BG']),
    Button(main_frame, text='Submit your custom script', 
            highlightbackground=colors['BG']),
    Button(main_frame, text='Update game images', 
            highlightbackground=colors['BG']),
    Label(main_frame, bg=colors['BG']), # filler
    Button(main_frame, text='Back', highlightbackground=colors['BG']),
]

back_btn = Button(side_frame, text='Back to Menu', 
                  highlightbackground=colors['BG'])

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

# Lists of commands that start and/or end blocks
block_starts = ['if', 'for', 'while']
block_ends = ['end', 'endif']
block_starts_ends = ['elseif', 'else']

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

# DOCUMENTATION: copy,0[oldX],0[oldY],0[newX],0[newY],16[width],16[height]
# Copy from old image to specified position in new image.
def copy(i, open_image, base_image):
    min_args = 4
    if len(i) <= min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

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

# DOCUMENTATION: copyalt,0[oldX],0[oldY],0[newX],0[newY],16[width],16[height]
# Copy from alt image to specified position in new image.
# TODO: Fold this into “copy” and give that command a “source” argument,
# and allow users to set an arbitrary number of variables with custom paths.
def copyalt(i, alt_image, base_image):
    min_args = 4
    if len(i) <= min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

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

    region = alt_image.crop((oldX, oldY, oldX+width, oldY+height))
    base_image.paste(region, (newX, newY, newX+width, newY+height))

# DOCUMENTATION: default,0[x],0[y],16[width],16[height] 
# Copy from template image to same position in new image.
def default(i, template_image, base_image):
    min_args = 2
    if len(i) <= min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return


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

# DOCUMENTATION: clear,0[x],0[y],16[width],16[height] 
# Clear area from new image. 
# Used to be called “delete” -- this still works for compatiblity reasons.
def clear(i, base_image):
    min_args = 2
    if len(i) <= min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

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
    min_args = 4
    if len(i) <= min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

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
#   open[copySource: open, template, or alt]
# Create a tile pattern on the new image using a part of the old image. 
# This command can be very useful but it’s not for the faint of heart.
def tile(i, open_image, alt_image, base_image):
    min_args = 8
    if len(i) <= min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
        return

    copyX = i[1]; copyY = i[2]; copyWidth = i[3]; copyHeight = i[4];
    pasteStartX = i[5]; pasteStartY = i[6];
    pasteCountHoriz = i[7]; pasteCountVert = i[8];

    # Default to 'open' as copySource if none specified
    if len(i) == 9:
        i.append('open')
    copySource = i[9].lower()

    for x in range(pasteCountHoriz):
        for y in range(pasteCountVert):
            if copySource == 'open':
                copy(['copy', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        open_image, base_image)
            elif copySource == 'alt' and alt_image:
                copyalt(['copyalt', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        alt_image, base_image)
            else:
                log_warning('tile: Invalid copy source — defaulting to "open"')
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
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
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

# DOCUMENTATION: flip,x<direction: x or y>,0[x],0[y],16[width],16[height]
# Flip the area in place on the new image. Unlike rotation, width and height
# can be different here.
def flip(i, base_image):
    min_args = 3
    if len(i) <= min_args:
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
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
#   255<alpha: 0 to 255>,0[x],0[y],16[width],16[height] 
# Fills the area with the selected color.
def fill(i, base_image):
    min_args = 4
    if len(i) <= min_args:
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
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
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
        log_warning('The command '+i[0]+' requires at least '+\
                min_args+' arguments.')
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

# Evaluate a boolean operator command, for example, (empty,0,0,16,16).
# Return True or False based on how the command evaluates.
# Invalid commands return False.
def oper_bool(cmd, base_image, open_image):
    # TODO: add support for nested conditionals
    i = parse_line(cmd.lstrip('(').rstrip(')'))
    if i[0].strip() == '': # Treat empty conditionals as false
        log_warning('Empty conditional command')
        return False
    elif i[0] == 'empty':
        return empty(i, open_image)
    else:
        log_warning('Invalid conditional command: ' + str(i))
        return False
    
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
    # If we make it here, it's empty, return True\
    return True

###########################################################################
#### COMING SOON ##########################################################
###########################################################################

def scale(i, base_image):
    log_warning(i[0]+' is coming soon...')

# Much further down the pipeline (requires completely new syntax)
    
def select(i, base_image):
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
        if step_status[i] == 'blue':
            curr_step = i
            break

    step_status[curr_step] = 'red'

    status_refresh()

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
        dialog_title = Label(main_frame, text=title, font=f_heading, 
                justify='left', bg=colors['BG'])
        dialog_title.place(x=0, y=0)
        # If there’s title text, leave space so msg_text doesn't cover it up
        next_y = 30

    dialog_message = []
    if isinstance(message, str): 
        # Convert to list if message is only one line / a string
        message = [message]

    for index, item in enumerate(message): # TODO: Scroll if not enough space
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

    # Reworked dialogs won't support bottom text 
    # (it adds unnecessary complexity).

    dialog_buttons = []
    for i in buttons:
        dialog_buttons.append(Button(main_frame, text=i, 
                                     highlightbackground=colors['BG']))

    # Place buttons one by one on the frame, aligned right and starting with
    # the rightmost button
    next_button_x = 470
    for i in reversed(dialog_buttons):
        i.place(x=next_button_x, y=310, anchor=SE)
        next_button_x -= i.winfo_reqwidth()
        next_button_x -= 10 # a little extra space between buttons

    # Set event bindings for all buttons
    for index, item in enumerate(dialog_buttons):
        item.bind('<ButtonRelease-1>', lambda _: button_event(index))

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
    side_frame.place(x=0, y=0)
    main_frame.place(x=160, y=0) 

    # Place sidebar items
    title.place(x=0, y=0)
    footer.place(x=80, y=315, anchor=S)
    for index, item in enumerate(steps):
        item.place(x=0, y=24+24*index)
    back_btn.place(x=80, y=295, anchor=S)
    back_btn.bind('<ButtonRelease-1>', lambda _: menu())
    # Note that the position of anything with main_frame as parent is 
    # RELATIVE (i.e. 160 will be added to x)

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
    status_set(['blue', 'gray', 'gray', 'gray', 'gray', 'gray'])

    menu_btns_p1[0].bind('<ButtonRelease-1>', 
            lambda _: script_variant('scripts/skin_L_to_Dx32.txt',
                                    'scripts/skin_L32_to_Dx32.txt'))
    menu_btns_p1[1].bind('<ButtonRelease-1>', 
            lambda _: script_variant('scripts/skin_R_to_Dx32.txt',
                                    'scripts/skin_R32_to_Dx32.txt'))
    menu_btns_p1[2].bind('<ButtonRelease-1>', 
            lambda _: open_script('scripts/obj_L_to_Dx.txt'))

    menu_btns_p1[4].bind('<ButtonRelease-1>', 
            lambda _: menu_p2())

    menu_btns_p1[6].bind('<ButtonRelease-1>', 
            lambda _: exit_app())

    menu_btns_p2[0].bind('<ButtonRelease-1>', 
            lambda _: open_script('scripts/skin_R_to_L.txt'))
    menu_btns_p2[1].bind('<ButtonRelease-1>', 
            lambda _: open_script('scripts/obj_R_to_Dx.txt'))
    menu_btns_p2[2].bind('<ButtonRelease-1>', 
            lambda _: open_script('scripts/map_new.txt'))

    menu_btns_p2[4].bind('<ButtonRelease-1>', 
            lambda _: open_script(''))
    menu_btns_p2[5].bind('<ButtonRelease-1>', 
            lambda _: the_W())
    menu_btns_p2[6].bind('<ButtonRelease-1>', 
            lambda _: install_assets())

    menu_btns_p2[8].bind('<ButtonRelease-1>', 
            lambda _: menu_p1())

    menu_p1()

    window.update()

    window.mainloop()

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
        open_script(path32)
    else:
        open_script(path16)

# Takes 1 script line (in string format) and converts it to a program-readable
# list. Account for comments, nesting, etc.
def parse_line(line: str):
    # Strip whitespace from start and end of line
    line = line.lstrip().rstrip()

    # Remove comments (like this one)
    # Note: This applies to filenames too if they're hardcoded into the script,
    # but I'm not fixing this because it's an edge case.
    line = line.split('#')[0].rstrip()

    # Commands where the parser should NOT treat commas as separators.
    # Note that all commands here have max 1 argument as a result.
    no_split_cmds = ['description', 'open', 'save', 'alt', 'template',
                     'warning', 'error']

    # Split line on commas
    output = ['']
    paren_depth = 0 # 0 = not inside parens, 1 = "(", 2 = "((" and so on
    for char in line:
        if char == ',' and paren_depth == 0 and \
                (len(output) == 1 or output[0] not in no_split_cmds):
            # Split on commas if not in parens and not in the 
            # list of no-split commands
            output.append('')
        else:
            output[-1] += char

        # Separately from building the output list, update paren_depth
        if char == '(':
            paren_depth += 1
        elif char == ')':
            paren_depth -= 1
            # If paren_depth is ever negative, there are too many ")"s
            if paren_depth < 0:
                log_warning('\
Too many closing parentheses. Skipping line: '+line)
                return [''] # Return empty line so converter skips it

    # If paren_depth isn't back to 0 after exiting splitter loop, syntax error
    if paren_depth > 0:
        log_warning('\
Not enough closing parentheses. Skipping line: '+line)
        return [''] # Return empty line so converter skips it

    for i in range(len(output)):
        # Descriptions may contain commas, so keep space after those.
        # Otherwise, remove whitespace from sides of commands. 
        # Ditto for file paths.
        if output[0] not in no_split_cmds:
            output[i] = output[i].strip()

        try:
            # Convert data to int if possible
            output[i] = int(output[i])
        except ValueError:
            pass

    return output

def open_script(script_file):
    global data, version, version_str

    # Ask user to pick a script if they want to run a custom script
    custom_script = False
    if not script_file:
        custom_script = True
        script_file = filedialog.askopenfilename(
                title='Select a script to run',
                initialdir='./scripts/')
        # If script file path is still empty, user cancelled, back to menu
        if script_file == '':
            menu()
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
        simple_dialog('Error', 
            'Couldn’t find a file with that name. Please try again.', 
            'Back', icon='error')
        menu()
    except UnicodeDecodeError: 
        # If user opens a “script” with weird characters
        status_fail()
        simple_dialog('Error', 
            ['Couldn’t read the file with that name.',
                'Are you sure it’s a conversion script?'],
            'Back', icon='error')
        menu()
    except IsADirectoryError: 
        # If user opens a folder or Mac app bundle
        status_fail()
        simple_dialog('Error', 
            '''That file is a folder or application. 
Please try again.''',
            'Back', icon='error')
        menu()

    lines = raw_content.split('\n')
    data = []
    for l in lines:
        data.append(parse_line(l))

    version = app_version.copy()
    version_str = '(UNKNOWN; defaulting to %s)' % app_version_str
    for i in data:
        if i[0] == 'version':
            # If user entered 1 or 2 numbers for the version (e.g. "1" or
            # "4,1", assume the other numbers are 0s
            if len(i) == 1:
                version.append(0)
                version.append(0)
            if len(i) == 2:
                version.append(0)
            elif len(i) >= 3:
                version = i[1:4]
                version_str = '.'.join([str(x) for x in version])
            # If user didn't specify a version, assume it’s for the current
            # converter version (but display the version as unknown)
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

    # Only show script info if it's a custom script, because default script
    # are assumed to work
    if custom_script:
        confirm = bool_dialog('Loaded script: %s'%name, 
                ['File path: %s'%script_file, 'By: %s'%author, 
                    'Made for converter version %s'%version_str,
                    'Description: %s'%description,
                    '',
                    '<b>Do you want to run this script?', '''\
If you click “Continue”, this program will check for problems with the script.
If no problems are found, the script will run right away.'''], 
                'Cancel', 'Continue', icon='question')
        if confirm:
            compatibility_check()
        else:
            menu()
    else:
        compatibility_check()

def compatibility_check():
    global data, version, version_str, open_path, save_path, template_path,\
            alt_path, base_blank, start_num, stop_num, current_num, multi

    #### STEP 3: COMPATIBILITY CHECK ####
    cls()
    status_complete()

    # Load header data
    open_path = '.INPUT' # New in v3.1: Default to user input if no path given
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
            
    save_path = '.INPUT' # New in v3.1: Default to user input if no path given
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
        conf = yn_dialog('Compatiblity warning', 
            ['This script was designed for a newer converter version.',
'You can try to run it if you want, but we can’t guarantee it’ll work.',
'We are not responsible for any damage to your files this may cause.',
'',
'Do you want to continue anyway?'], 
            icon='warning')
        if conf:
            get_paths()
        else:
            menu()
    else:
        try:
            # Scan file for compatibility issues
            for i in data:
                # Version 1.1: “default” no longer takes newX and newY arguments
                # Automatically fixed by converter
                if i[0] == 'default' and len(i) > 4 and (version[0] < 1 or \
                        (version[0] == 1 and version[1] < 1)):
                    file_issues.append(0)
                    del i[3]
                    del i[4]
                # Version 1.5: “filter” command split into subcommands 
                # like “grayscale”
                # Automatically fixed by converter
                if i[0] == 'filter' and (version[0] < 1 or \
                        (version[0] == 1 and version[1] < 4)):
                    file_issues.append(1)
                    del i[0]
                # Version 2.1: “template” command no longer supports wildcards 
                # in path
                # Cannot be fixed
                if '*' in template_path and (version[0] < 2 or \
                        (version[0] == 2 and version[1] < 1)):
                    file_issues.append(2)
                # Version 3.0: alt command no longer supports wildcards in path
                # Cannot be fixed
                if '*' in alt_path and (version[0] < 3): 
                    # don't need to check minor version above, 
                    # as there’s no minor version less than 0
                    file_issues.append(3)

            # Compatibility warnings
            if len(file_issues) > 0:
                main_text = [
'Your script was designed for version %s of this converter.' % version_str, 
'It contains the following compatibility issues:', 
                ]
                for i in file_issues:  
                    main_text.append(Label(main_frame, text='- '+all_issues[i]))
                
                conf = yn_dialog('Compatibility warning', main_text.extend([
'',
'Do you wish to continue anyway, even though things may not work properly?',
'We are not responsible for any damage to your files this may cause.', 
                    ]), icon='warning')
                if conf:
                    get_paths()
                else:
                    menu()
            else:
                get_paths()
                return
        except:
            # If we find an error while compatibility checking, just skip it
            # and get right to converting
            simple_dialog('Compatibility checker error', 
                    ['Skipping compatibility check due to an error.',
                    'Please tell Clippy how you got here so he can fix it.'],
                    icon='warning')

def get_paths():
    global multi, start_num, stop_num, open_path, save_path

    #### STEP 4: OPEN & SAVE PATHS ####
    cls()
    status_complete()

    # Determine whether script is converting 1 file (single-file mode)
    # or multiple files (multi-file mode)
    multi = False
    if start_num != None and stop_num != None and \
            '*' in open_path and '*' in save_path:
        multi = True

    # Make user choose file if that's what the script wants
    if open_path.upper() == '.INPUT':
        open_path = filedialog.askopenfilename(\
                title='Choose an image to open and copy from',
                initialdir='./')
        # If open_path is still empty, user cancelled — go back to step 1
        if not open_path:
            menu()
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
            simple_dialog('Error', 
['The script tried to open the following file, but it does not exist.',
'<b>'+open_path,
'Check your spelling and try again.'], 'Back', icon='error')
            menu()
        except IsADirectoryError: 
            # If user opens a folder or Mac app bundle
            status_fail()
            simple_dialog('Error', 
                '''The path '''+open_path+''' is a folder or application.
Please try again.''',
                'Back', icon='error')
            menu()

    if save_path.upper() == '.INPUT':
        save_path = filedialog.asksaveasfilename(\
                title='Choose a location to save to', defaultextension='.png',
                filetypes=[('PNG image', '*.png')],
                initialdir='./')
        # If save_path is still empty, user cancelled — go back to step 1
        if save_path == '':
            menu()
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
            simple_dialog('Error', 
['The script is trying to save to a folder that doesn’t exist.',
'The path that caused the error was:', '<b>'+parent_dir], 
                'Back to Menu', icon='error')
            menu()

        # Check if the file already exists
        files_to_overwrite = []
        main_text = ['This text shouldn’t show up for any reason.',
                'If it does, please tell Clippy so he can fix it!']
        if multi: # …then we need to check EVERY file we're saving to
            for i in range(start_num, stop_num):
                check_path = save_path.replace('*', str(i))
                if os.path.exists(check_path):
                    files_to_overwrite.append(check_path)
                    # TODO: add a way to display all the
                    # files that would be overwritten 
                    # (3-button box with More button)

            if files_to_overwrite:
                main_text = [
                    '\
This script will overwrite one or more existing files. \
You can’t undo this action.',
                    '\
Please check the path %s (where * is any number) for existing files.' \
    % save_path,
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

        conf = yn_dialog('Warning', main_text.extend([
                '', 
                'Do you want to run this script anyway?'
            ]), icon='warning')
        if conf:
            run_script()
        else:
            menu()

def run_script():
    global data, open_path, save_path, template_path, alt_path, base_blank,\
            start_num, stop_num, current_num, multi

    #### STEP 5: RUN SCRIPT ####
    cls()
    status_complete()

    heading_text = Label(main_frame, text='Converting image...', 
        font=f_heading, bg=colors['BG'])
    heading_text.place(x=0, y=0)

    # Update screen differently based on how many files we're converting
    heading = Label(bg=colors['BG'])
    subhead = Label(bg=colors['BG'])
    if multi:
        heading = Label(main_frame, text='Converting all images from '+\
            str(start_num)+' to '+str(stop_num-1), font=f_heading, 
            bg=colors['BG'])
        subhead = update_subhead(subhead)
    else:
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

    # Load template image only once because it doesn't allow wildcards
    template_image = None
    try:
        if template_path != '':
            # template_path doesn't support wildcards because the point is
            # for there to be just 1 template
            template_image = PIL.Image.open(template_path).convert('RGBA')
        else:
            template_image = None
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

    alt_image = None
    try:
        if alt_path != '':
            alt_image = PIL.Image.open(alt_path).convert('RGBA')
        else:
            alt_image = None
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

        base_image = process(data, open_image, template_image, 
                            alt_image, base_image)
        base_image.save(save_path.replace('*', str(i)))

    t2 = time()
    replit(t2-t1)

def replit(conv_time):
    #### STEP 6: SUMMARY ####
    cls()
    status_complete()

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
    summary(conv_time)

def summary(conv_time, warning_page=0):
    # Roll warning page over to 0 if needed
    warn_per_page = 10 # TODO: turn this into a scrolling thing (maybe popup?)
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
            confirm_exit = button_dialog('Conversion complete!', 
                    main_text + ['', bottom_text], 
                    'More warnings', 'Okay', icon='warning')
            if confirm_exit == 'More warnings':
                summary(conv_time, warning_page+1) # next page
            else:
                menu()
        else:
            # Display dialog with warnings but no extra button
            # if there's only 1 page worth of warnings
            simple_dialog('Conversion complete!', main_text + ['', bottom_text], icon='warning')
            menu()
    else:
        simple_dialog('Conversion complete!', main_text,
            'Okay', icon='done')
        menu()

# Reads lines from one file and executes its instructions
def process(data: list, open_image, template_image=None, alt_image=None, 
        base_image=None):
    header_commands = ['mrconverter', 'version', 'name', 'description', 
        'author', 'open', 'save', 'template', 'alt', 'base', 
        'start', 'stop']

    skip_index = -1 # Variable used to skip lines
    for index, item in enumerate(data):
        # Skip line if it's in a block
        if index <= skip_index:
            continue

        # Uncomment this to print line-by-line output
        #p#rint(index+1, item) # +1 to get correct line number

        try:
            if item[0].strip() == '': # Skip blank lines
                pass

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
            elif item[0] == 'if':
                # Make sure the if statement is properly constructed
                if len(item) < 2: 
                    log_warning('if: missing conditional statement')
                    continue

                # Result of conditional command in the if statement
                cond_result = oper_bool(item[1], base_image, open_image)
                
                # Bundle together the code inside the block
                block_depth = 1
                if_block_data = []
                reached_else = False
                skip_to_end = False
                for j in range(index+1, len(data)):
                                # ^ index+1 means we skip "if" line
                    # Check if we've reached end of the whole thing
                    if data[j][0] in ['end', 'endif']: 
                        # endif retained for compatibility
                        block_depth -= 1
                        if block_depth == 0:
                            break

                    # Skip to end if that's on
                    if skip_to_end:
                        continue

                    # Check if we've reached else
                    if not reached_else and block_depth == 1 and \
                            data[j][0] in ['else']:
                        reached_else = True
                        continue
                    
                    # If condition is false and we're not at else yet,
                    # skip until we are
                    if block_depth == 1 and \
                            not cond_result and not reached_else:
                        continue
                    # If condition is true and we're at else, start 
                    # skipping to end so we don't fall through to the else code
                    elif block_depth == 1 and \
                            cond_result and reached_else:
                        skip_to_end = True
                        continue

                    if data[j][0] in ['if']:
                        block_depth += 1

                    # If we're still here, add line to block_data
                    if_block_data.append(data[j])

                # If it still thinks we're in a block when we leave the loop, 
                # that's an error
                if block_depth != 0:
                    log_warning('Reached end of code while still in a block')

                # Recursively call this function on the block.
                # This *should* work for nested blocks.
                # This will be given the code in the "if" part OR the "else"
                # part depending on the conditional and the loop above.
                base_image = process(if_block_data, open_image, template_image, 
                        alt_image, base_image)

                # Skip the lines inside the block by setting main loop 
                # index variable to j
                skip_index = j
            
            # Basic copying commands
            elif item[0] == 'copy':
                copy(item, open_image, base_image)
            elif item[0] == 'copyalt':
                if not alt_image:
                    log_warning('\
    Skipped all “copyalt” commands since no “alt” image was specified.')
                else:
                    copyalt(item, alt_image, base_image)
            elif item[0] == 'default':
                if not template_image:
                    log_warning('\
    Skipped all “default” commands since no “template” image was specified.')
                else:
                    default(item, template_image, base_image)
            elif item[0] == 'clear' or item[0] == 'delete':
                clear(item, base_image)
            elif item[0] == 'duplicate':
                duplicate(item, base_image)

            # Advanced copying commands
            elif item[0] == 'tile':
                tile(item, open_image, alt_image, base_image)

            # Transformation commands
            elif item[0] == 'resize':
                base_image = resize(item, base_image)
            elif item[0] == 'rotate':
                rotate(item, base_image)
            elif item[0] == 'flip':
                flip(item, base_image)

            # Filter commands
            elif item[0] == 'grayscale':
                grayscale(item, base_image)
            elif item[0] == 'invert':
                invert(item, base_image)
            elif item[0] == 'colorfilter':
                colorfilter(item, base_image)
            elif item[0] == 'opacity':
                opacity(item, base_image)
            elif item[0] == 'hue':
                hue(item, base_image)
            elif item[0] == 'saturation':
                saturation(item, base_image)
            elif item[0] == 'lightness':
                lightness(item, base_image)
            elif item[0] == 'fill':
                fill(item, base_image)
            elif item[0] == 'contrast':
                contrast(item, base_image)
            elif item[0] == 'colorize':
                colorize(item, base_image)
            elif item[0] == 'sepia':
                sepia(item, base_image)
            elif item[0] == 'threshold':
                threshold(item, base_image)

            # COMING SOON
            elif item[0] == 'scale':
                scale(item, base_image)
            elif item[0] == 'select':
                select(item, base_image)

            # Just so it doesn't think header commands are unknown
            elif item[0] in header_commands:
                # I always mess this particular command up so I'll just 
                # put in a note to self
                if item[0] == 'template' and len(item) > 2:
                    log_warning('Clippy, you idiot, the command you’re looking \
for is “default”, not “template”')
            else:
                log_warning('Unknown command: '+str(item[0]))

        except Exception as e: 
            # Handle any errors in the command functions so they don’t bring
            # the whole program to a halt
            log_warning(str(item[0])+' command skipped due to error: '+str(e))
    return base_image 

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
            menu()
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

        # Check screen size and if it's too small, ask user to enter fullscreen
        if screen_width < 640 or screen_height < 320:
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

# TODO: Add batch skin conversion without needing to know the scripting language
# TODO: Add "source,NAME,PATH" command to replace alt/copyalt
#       (or maybe call the command "load"?)