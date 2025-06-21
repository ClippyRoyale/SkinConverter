'''
MR Skin Converter 
Version 7.6.1

Copyright 2022–2025 ClippyRoyale

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
'''

import math
import os
import sys
import colorsys
import urllib.request
import webbrowser # for installing assets
from collections import abc
from copy import deepcopy
from glob import glob
from time import time
from typing import *
from tkinter import *
import tkinter.font as tkfont
from tkinter import filedialog # not imported with tkinter by default
from tkinter import messagebox # not imported with tkinter by default
# Non-PSL modules
# This is probably TERRIBLE coding practice, but this is the easiest way to
# make the program run "out of the box" for non-developers.
try:
    import PIL.Image
    import PIL.ImageOps
    import PIL.ImageDraw # pillow
except ModuleNotFoundError:
    os.system('pip3 install pillow')
    exit()

###########################################################################
#### GLOBAL VARIABLES #####################################################
###########################################################################

app_version = [7,6,1]

# For type hints
Num = Union[int,float]
ColorArray = abc.Sequence[Num]

# Why does Python not have this built in anymore???
def cmp(x, y):
    '''three-way comparison operator'''
    return -1 if x < y else (1 if x > y else 0)
def sign(x): 
    '''returns -1 for negative, 1 for positive, 0 for everything else
    (including invalid inputs)'''
    return cmp(x, 0)

def app_version_str():
    return f'{app_version[0]}.{app_version[1]}.{app_version[2]}'

def version_lt(major:int, minor=0, patch=0):
    '''Returns True if the script's target version is LESS THAN 
    the given number, and False otherwise.'''
    if version[0] < major:
        return True
    if version[0] == major and version[1] < minor:
        return True
    if version[0] == major and version[1] == minor and version[2] < patch:
        return True
    # else
    return False

def version_lte(major:int, minor=0, patch=0):
    '''Returns True if the script's target version is LESS THAN OR EQUAL TO
    the given number, and False otherwise.'''
    if version[0] < major:
        return True
    if version[0] == major and version[1] < minor:
        return True
    if version[0] == major and version[1] == minor and version[2] <= patch:
        return True
    # else
    return False

def version_gte(major:int, minor=0, patch=0):
    '''Returns True if the script's target version is GREATER THAN OR EQUAL TO
    the given number, and False otherwise.'''
    if version[0] > major:
        return True
    if version[0] == major and version[1] > minor:
        return True
    if version[0] == major and version[1] == minor and version[2] >= patch:
        return True
    # else
    return False

def version_gt(major:int, minor=0, patch=0):
    '''Returns True if the script's target version is GREATER THAN 
    the given number, and False otherwise.'''
    if version[0] > major:
        return True
    if version[0] == major and version[1] > minor:
        return True
    if version[0] == major and version[1] == minor and version[2] > patch:
        return True
    # else
    return False

window = Tk()
window.wm_title('Clippy’s Skin Converter')
window.geometry('480x360')
window.resizable(False, False)

app_icon = PhotoImage(file='ui/iconHD.png')
window.iconphoto(False, app_icon)

colors = {
    # 25 basic colors
    'red': '#ff0000',
    'maroon': '#800000',
    'orange': '#ff8000',
    'brown': '#804000',
    'tan': '#c08040',
    'peach': '#ffd0a0',
    'amber': '#ffc000',
    'yellow': '#ffff00',
    'olive': '#808000',
    'lime': '#00ff00',
    'green': '#008000',
    'cyan': '#00ffff',
    'teal': '#008080',
    'azure': '#0080ff',
    'blue': '#0000ff',
    'navy': '#000080',
    'violet': '#8000ff',
    'purple': '#800080',
    'magenta': '#ff00ff',
    'pink': '#ff80f0',
    'black': '#000000',
    'gray': '#808080',
    'silver': '#c0c0c0',
    'white': '#ffffff',
    'transparent': '#00000000', # 8-digit

    # NES palette colors (Using Nestopia's 15° Canonical palette)
    'n00': '#666666',
    'n01': '#002a88',
    'n02': '#1412a7',
    'n03': '#3b00a4',
    'n04': '#5c007e',
    'n05': '#6e0040',
    'n06': '#6c0700',
    'n07': '#561d00',
    'n08': '#333500',
    'n09': '#0c4800',
    'n0a': '#005200',
    'n0b': '#004f08',
    'n0c': '#00404d',
    'n0d': '#000000',
    'n0e': '#000000',
    'n0f': '#000000',

    'n10': '#adadad',
    'n11': '#155fd9',
    'n12': '#4240ff',
    'n13': '#7527fe',
    'n14': '#a01acc',
    'n15': '#b71e7b',
    'n16': '#b53120',
    'n17': '#994e00',
    'n18': '#6b6d00',
    'n19': '#388700',
    'n1a': '#0d9300',
    'n1b': '#008f32',
    'n1c': '#007c8d',
    'n1d': '#000000',
    'n1e': '#000000',
    'n1f': '#000000',

    'n20': '#ffffff',
    'n21': '#64b0ff',
    'n22': '#9290ff',
    'n23': '#c676ff',
    'n24': '#f26aff',
    'n25': '#ff6ecc',
    'n26': '#ff8170',
    'n27': '#ea9e22',
    'n28': '#bcbe00',
    'n29': '#88d800',
    'n2a': '#5ce430',
    'n2b': '#45e082',
    'n2c': '#48cdde',
    'n2d': '#4f4f4f',
    'n2e': '#000000',
    'n2f': '#000000',

    'n30': '#ffffff',
    'n31': '#c0dfff',
    'n32': '#d3d2ff',
    'n33': '#e8c8ff',
    'n34': '#fac2ff',
    'n35': '#ffc4ea',
    'n36': '#ffccc5',
    'n37': '#f7d8a5',
    'n38': '#e4e594',
    'n39': '#cfef96',
    'n3a': '#bdf4ab',
    'n3b': '#b3f3cc',
    'n3c': '#b5ebf2',
    'n3d': '#b8b8b8',
    'n3e': '#000000',
    'n3f': '#000000',

    # UI background color (light gray)
    'UI_BG': '#f0f0f0',
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

footer_frame = LabelFrame(window, width=480, height=40, bg=colors['UI_BG'])
footer = Label(footer_frame,
        text='Skin Converter v%s — a Clippy production' % app_version_str(), 
        fg=colors['gray'], bg=colors['UI_BG'])
back_btn = Button(footer_frame, text='Back to Menu', 
        highlightbackground=colors['UI_BG'])

main_frame = LabelFrame(window, width=480, height=320, bg=colors['UI_BG'])
main_frame.grid_propagate(False)

menu_heading = Label(main_frame, text='What do you want to convert?', 
        font=f_heading, bg=colors['UI_BG'])
menu_heading_adv = Label(main_frame, text='Advanced conversion options', 
        font=f_heading, bg=colors['UI_BG'])
menu_spacer = Label(main_frame, bg=colors['UI_BG'])

menu_btn_skin_l_l7 = Button(main_frame, 
        text='Convert a Legacy5 skin to Legacy7',
        font=f_large, highlightbackground=colors['UI_BG'])
menu_btn_skin_d_l7 = Button(main_frame, 
        text='Convert a Deluxe skin to Legacy7',
        font=f_large, highlightbackground=colors['UI_BG'])
menu_btn_trans_bg = Button(main_frame, 
        text='Remove a partially transparent background',
        highlightbackground=colors['UI_BG'])

menu_btn_skin_p_l7 = Button(main_frame, 
        text='Convert a Legacy3 32×32 proposal skin to Legacy7', highlightbackground=colors['UI_BG'])
menu_btn_skin_d_l = Button(main_frame, text='Convert a Deluxe skin to Legacy5',
        highlightbackground=colors['UI_BG'])
menu_btn_skin_r_l = Button(main_frame, text='Convert a Remake skin to Legacy5',
        highlightbackground=colors['UI_BG'])
menu_btn_map_l_ln = Button(main_frame, 
        text='Convert a Legacy map mod to Legacy map_new',
        highlightbackground=colors['UI_BG'])

menu_btn_custom = Button(main_frame, text='Run a custom script',
        highlightbackground=colors['UI_BG'])
menu_btn_submit = Button(main_frame, text='Submit your custom script',
        highlightbackground=colors['UI_BG'])
menu_btn_multi = Button(main_frame, text='Convert multiple images...',
        highlightbackground=colors['UI_BG'])
menu_btn_assets = Button(main_frame, text='Update game images',
        highlightbackground=colors['UI_BG'])

menu_btn_page_next = Button(main_frame, text='Advanced/Custom...', 
        highlightbackground=colors['UI_BG'])
menu_btn_page_prev = Button(main_frame, text='Back', 
        highlightbackground=colors['UI_BG'])
menu_btn_exit = Button(main_frame, text='Exit', 
        highlightbackground=colors['UI_BG'])

menu_btns_p1 = [
    menu_btn_skin_l_l7,
    menu_btn_skin_d_l7,
    menu_btn_trans_bg,
    menu_spacer,
    menu_btn_page_next,
    menu_spacer,
    menu_btn_exit,
]

menu_btns_p2 = [
    menu_btn_skin_p_l7,
    menu_btn_skin_d_l,
    menu_btn_skin_r_l,
    menu_btn_map_l_ln,
    menu_spacer,
    menu_btn_custom,
    #menu_btn_submit, # temporarily removed for space reasons
    menu_btn_multi,
    menu_btn_assets,
    # menu_spacer,
    menu_btn_page_prev,
]

icons = {
    'info': \
        PhotoImage(file='ui/info.png'),
    'question': \
        PhotoImage(file='ui/question.png'),
    'warning': \
        PhotoImage(file='ui/warning.png'),
    'error': \
        PhotoImage(file='ui/denied.png'),
    'done': \
        PhotoImage(file='ui/accepted.png'),
}

# OTHER GLOBAL VARIABLES

data : List[list] # script's lines in parsed form

version : List[int] # SCRIPT version, not app version
version_str: str    # ditto

flags : Dict[str, Any]

# Multi-file conversion
legacy_multi : bool # Enabled within a script, with start and stop headers
    # new_multi is an argument, not a global var
# Only for legacy multi:
start_num : int
stop_num : int 
current_num : int
# Only for new multi:
multi_open_paths : List[str]
multi_save_paths : List[str]

# Image file paths
open_path : str
save_path : str
alt_path : str
template_path : str

# For calculating block depths while parsing scripts
block_depths : List[int]
block_stacks : List[List[str]]
# Like above but only for breakable blocks (loops)
break_depths : List[int]
break_stacks : List[List[str]]
loop_data : List[Dict[str, Any]]

base_blank : Union[bool, Tuple[int,int]]
space_sep : bool # COMING IN 8.0

# Only used if draw commands are in script
draw_obj : Optional[PIL.ImageDraw.ImageDraw] 

# databases accessible by scripts while running them:
images : Dict[str, PIL.Image.Image]
variables : Dict[str, Any]
labels : Dict[str, int]

# warnings is for any problem with conversion scripts that mean a command
# can’t run properly or at all, but which doesn’t require us to halt
# the conversion completely. Any warnings are displayed to the user after
# the script finishes running.
warnings : List[str] = []
multi_open_paths : List[str] = []

# Lists of commands that start and/or end blocks
block_starts_ends = [
    'else',
    'elseif',
    'else_if',
]
block_starts = [
    'if', 'while', 'for', 'foreach',
    # RESERVED FOR FUTURE USE:
    'func', 
    # these probably won't be added any time soon 
    # but I might as well reserve them:
    'switch', 'struct', 'enum', 'class',
] + block_starts_ends
block_ends = [
    'end', 'endif'
] + block_starts_ends

# Blocks you can break from (loops and switches)
breakable_blocks = [
    'while', 'for', 'foreach',
]

# List of header commands. These commands are typically located at the start
# of the file. They aren't run as instructions; they contain metadata about
# the script that is processed before running it.
header_commands = ['mrconverter', 'version', 'flag', 'name', 'description', 
        'desc', 'author', 'open', 'save', 'template', 'alt', 'base', 
        'start', 'stop', 'loop_limit', 'looplimit']

# Commands used to set or change variables. The first argument of each of
# these commands should be a variable, but unlike with other commands,
# the variable will be kept as a Var class (instead of being substituted).
set_commands = ['set', 'change', 'const', 'for', 'foreach',
                'list.add', 'list.addall', 'list.clear', 'list.insert',
                'list.remove', 'list.replace', 'list.swap',
                # Augmented assignment
                'iadd', 'isub', 'imul', 'itruediv', 
                'ifloordiv', 'imod', 'ipow',
                # Augmented assignment aliases (needed because set_commands
                # may be checked before alias() is called)
                '-=', # hyphen
                '–=', # en dash
                '−=', # minus sign
                '+=',    '*=', '×=',    '/=', '÷=',    '//=', '÷÷=',
                '%=',    '^=', '**=', '××=',
                # inc/dec and aliases
                'inc', '++', 
                'dec', '--', # hyphen
                '––', # en dash
                '−−', # minus sign
                ]

###########################################################################
#### CUSTOM DATA TYPES ####################################################
###########################################################################

class Color:
    def __init__(self, red:Num, green:Num, blue:Num, alpha:Num=255):
        self.alpha = 0 if alpha<0 else (255 if alpha>255 else int(alpha))

        # If fully transparent, don't store color data
        if alpha == 0:
            self.red = 0
            self.green = 0
            self.blue = 0
        else:
            self.red = 0 if red<0 else (255 if red>255 else int(red))
            self.green = 0 if green<0 else (255 if green>255 else int(green))
            self.blue = 0 if blue<0 else (255 if blue>255 else int(blue))

        hsla = rgba_to_hsla([self.red, self.green, self.blue, self.alpha])
        self.hue = hsla[0]
        self.saturation = hsla[1]
        self.lightness = hsla[2]

    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        if self.alpha == other.alpha == 0: # if both colors fully transparent
            return True
        return self.red == other.red \
            and self.green == other.green \
            and self.blue == other.blue \
            and self.alpha == other.alpha
    
    def __repr__(self):
        return f'<Color: \
rgba({self.red}, {self.green}, {self.blue}, {self.alpha})>'

# Reference to variable –– will be substituted before executing line
class Var:
    def __init__(self, name:str):
        self.name = name
    
    def __repr__(self):
        return f'<Var: {self.name}>'

# Settable variable –– handled directly by commands that set or mutate vars
class SetVar(Var):
    # init is same
    def __repr__(self):
        return f'<SetVar: {self.name}>'

class Subcommand:
    def __init__(self, content:list):
        self.content = content
    
    def __repr__(self): # displayed in e.g. debug printouts
        return f'<Subcommand: {self.content}>'
    
    def __str__(self): # displayed in e.g. assertion error messages
        return '(' + ','.join([str(i) for i in self.content]) + ')'

###########################################################################
#### LOG/EXIT COMMANDS ####################################################
###########################################################################

# Displays a warning shown after conversion finishes. Only other i-argument is
# the text of the warning.
def warning(i: list):
    log_warning(f'warning: {i[1]}')

# EXIT and ERROR are handled in the main command-checking loop
    
# USE has been removed

###########################################################################
#### BASIC COPYING COMMANDS ###############################################
###########################################################################

def set_(i: list, internal:bool=False):
    '''
    set,$hello<name>,"Hello world"<value> 

    Set variable "hello" to the string "Hello world". Subcommands in second 
    argument will be evaluated before setting the variable. Any value in double 
    quotes will be treated as a string no matter what. If it's not in quotes 
    and it can be parsed as an integer, the value will be an integer. Anything 
    else will be treated as a string for legacy reasons, but watch out for 
    special characters! (Alias `:=`)

    If this function's "internal" argument is set to True, the normal
    restrictions against setting variables starting with an underscore will 
    be overridden. When this function is called by e.g. fillcolor, internal 
    should always be set to True. When calling this function directly from a 
    conversion script, internal should always be False.
    '''
    
    # This function accepts a SetVar or str, 
    # so we may need to convert the name to a string
    if type(i[1]) == SetVar:
        raw = i[1]
        name : str = i[1].name
    elif type(i[1]) == str:
        name : str = i[1]
        raw = SetVar(name)
    else:
        log_warning(f'{i[0]}: Invalid variable {i[1]}. \
Variable names must start with a dollar sign.')
        return

    if not var_check(raw, i[0], exists=None, internal=internal):
        # var_check will generate its own warning if it fails, so no need
        # for another one here
        return

    # If the checks passed, set the variable
    variables[name] = i[2]

def const(i: list):
    '''
    const,$TAU<name>,6.283<value>

    Set a constant value so you can refer back to it by a recognizable name 
    later. Works the same as "set" but you can't go back and change the value 
    the name refers to.
    '''
    
    # This function accepts a SetVar or str, 
    # so we may need to convert the name to a string
    if type(i[1]) == SetVar:
        raw = i[1]
        name : str = i[1].name
    elif type(i[1]) == str:
        name : str = i[1]
        raw = SetVar(name)
    else:
        log_warning(f'{i[0]}: Invalid variable {i[1]}. \
Variable names must start with a dollar sign.')
        return

    if not var_check(raw, i[0], exists=False):
        # var_check will generate its own warning if it fails, so no need
        # for another one here
        return

    set_(i)
    # Flag this variable as a constant so we can't change it in the future
    variables['$__constants'].append(name)

def change(i: list, internal=False):
    '''
    change,$x<varName>,+<subcmdName>,10[arg2],... 
    
    Change the value of varName by applying the given subcommand to it. 
    The variable will be the first argument to the command, and any argument 
    after `subcmdName` will be passed as the subcommand's second, third, (etc.) 
    arguments. 
    
    Example A: `change,$x,+,10,$y` will add (10 plus the value of $y) to $x; 
    this is equivalent to `set,$x,(+,$x,10,$y)`. 
    
    Example B: `change,$x,*,2` will multiply $x's value by 2; 
    this is equivalent to `set,$x,(*,$x,2)`. 
    
    Basically, it's nothing you can't already do with set; it just makes code 
    more readable.
    '''
    
    # This function accepts a SetVar or str, 
    # so we may need to convert the name to a string
    if type(i[1]) == SetVar:
        raw = i[1]
        varName : str = i[1].name
    elif type(i[1]) == str:
        varName : str = i[1]
        raw = SetVar(varName)
    else:
        log_warning(f'{i[0]}: Invalid variable {i[1]}. \
Variable names must start with a dollar sign.')
        return
    
    subcmdName : str = i[2]

    if not var_check(raw, i[0], exists=True, internal=internal):
        # var_check will generate its own warning if it fails, so no need
        # for another one here
        return

    # Construct subcommand to compute the value we want to set the variable to
    # Note that here we use varName as a key to access `variables` in order to
    # get the value, whereas when we call set below, we use varName itself.
    # If we make it to this part of the code, we already know that varName
    # is in variables (i.e. the variable exists).
    new_subcmd = [subcmdName, variables[varName]] + i[3:]
    value = subcmd(new_subcmd)

    # Now that we have the value, set the variable to it.
    # This ALSO relies on existing functionality.
    set_([i[0], raw, value], internal=internal)

# copy,0[oldX],0[oldY],0[newX],0[newY],16[width],16[height]
# Copy from old image to specified position in new image.
# Note: copyalt has been folded into this function because there was no
# difference except in the argument name.
def copy(i, open_image, base_image):
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

# copyfrom,old<imageName>,0[oldX],0[oldY],0[newX],0[newY],
#   16[width],16[height] 
# Copy from any image ("old", "alt", "template", or even "new") to specified 
# position in new image. (Alias: copy_from)
def copyfrom(i: list):
    if i[1] not in images:
        log_warning(
            f'{i[0]}: Skipped because {i[1]} is not a defined image name'
        )
        return

    copy([i[0]]+i[2:], images[i[1]], images['new'])

# default,0[x],0[y],16[width],16[height] 
# Copy from template image to same position in new image.
def default(i, template_image, base_image):
    # COMPATIBILITY: In version 1.0, "default" took 6 arguments
    # (with the first 4 being required):
    # default,0<oldX>,0<oldY>,0<newX>,0<newY>,16[width],16[height]
    if i[0] == 'default' and len(i) > 4 and version_lt(1,1):
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

# defaultfrom,template<imageName>,0[x],0[y],16[width],16[height]
# Copy from any image ("old", "alt", "template", or even "new") to same 
# position in new image. (Alias: default_from)
def defaultfrom(i: list):
    if i[1] not in images:
        log_warning(
            f'{i[0]}: Skipped because {i[1]} is not a defined image name'
        )
        return

    default([i[0]]+i[2:], images[i[1]], images['new'])

# clear,0[x],0[y],16[width],16[height] 
# Clear area from new image. 
# Used to be called “delete” -- this still works for compatiblity reasons.
def clear(i, base_image):
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

def duplicate(i: list, base_image: PIL.Image.Image):
    '''
    duplicate,0<oldX>,0<oldY>,0<newX>,0<newY>,16[width],16[height]

    Copy an area on the NEW image to another position on the same canvas.
    '''

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

def move(i: list, base_image: PIL.Image.Image):
    '''
    move,0<oldX>,0<oldY>,0<newX>,0<newY>,16[width],16[height] 

    Cut an area on the NEW image, and paste it in another position on the 
    same canvas.
    '''

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

    # Copy the old area to the "clipboard"
    cut = base_image.crop((oldX, oldY, oldX+width, oldY+height))

    # Clear the area on the image that was just copied, 
    # now that we've saved a copy
    empty_image = PIL.Image.new('RGBA', (width, height))
    base_image.paste(empty_image, (oldX, oldY, oldX+width, oldY+height))

    # Paste the data from the clipboard
    base_image.paste(cut, (newX, newY, newX+width, newY+height))

def swap(i: list, base_image: PIL.Image.Image):
    '''
    swap,0<x1>,0<y1>,16<x2>,0<y2>,16[width],16[height]

    Swap the pixels contained in two different areas on the new image. 
    The areas you want to swap must have the same width and height.
    '''

    x1 = i[1]
    y1 = i[2]
    x2 = i[3]
    y2 = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width = i[5]
    if len(i) == 6:
        i += [width]
    height = i[6]

    # Copy both regions
    region1 = base_image.crop((x1, y1, x1+width, y1+height))
    region2 = base_image.crop((x2, y2, x2+width, y2+height))
    # Paste both regions
    base_image.paste(region1, (x2, y2, x2+width, y2+height))
    base_image.paste(region2, (x1, y1, x1+width, y1+height))

def over(i:list, open_image:PIL.Image.Image, base_image:PIL.Image.Image):
    '''
    over 0[oldX] 0[oldY] 0[newX] 0[newY] 16[width] 16[height] "old"[imageName]
    
    Like copy, except overlay the copied area on top of the existing pixels 
    (using alpha blending), instead of clearing them.
    '''

    # If no x or y specified, apply to whole image
    if len(i) <= 4:
        i = [i[0], 0, 0, 0, 0, base_image.size[0], base_image.size[1]]
    oldX : int = i[1]
    oldY : int = i[2]
    newX : int = i[3]
    newY : int = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width : int = i[5]
    if len(i) == 6:
        i += [width]
    height : int = i[6]

    if len(i) >= 8:
        # Option to override source image
        if i[7] not in images:
            log_warning(
                f'{i[0]}: Skipped because {i[7]} is not a defined image name'
            )
            return base_image
        # else
        open_image = images[i[7]]

    region = open_image.crop((oldX, oldY, oldX+width, oldY+height))
    temp = PIL.Image.new('RGBA', (base_image.width, base_image.height))
    temp.paste(region, (newX, newY, newX+width, newY+height))

    return PIL.Image.alpha_composite(base_image, temp)

def under(i:list, open_image:PIL.Image.Image, base_image:PIL.Image.Image):
    '''
    under 0[oldX] 0[oldY] 0[newX] 0[newY] 16[width] 16[height] "old"[imageName]
    
    Like copy, except place the copied area underneath the existing pixels 
    (using alpha blending).
    '''

    # If no x or y specified, apply to whole image
    if len(i) <= 4:
        i = [i[0], 0, 0, 0, 0, base_image.size[0], base_image.size[1]]
    oldX : int = i[1]
    oldY : int = i[2]
    newX : int = i[3]
    newY : int = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width : int = i[5]
    if len(i) == 6:
        i += [width]
    height : int = i[6]

    if len(i) >= 8:
        # Option to override source image
        if i[7] not in images:
            log_warning(
                f'{i[0]}: Skipped because {i[7]} is not a defined image name'
            )
            return base_image
        # else
        open_image = images[i[7]]

    region = open_image.crop((oldX, oldY, oldX+width, oldY+height))
    temp = PIL.Image.new('RGBA', (base_image.width, base_image.height))
    temp.paste(region, (newX, newY, newX+width, newY+height))

    return PIL.Image.alpha_composite(temp, base_image)

###########################################################################
#### ADVANCED COPYING COMMANDS ############################################
###########################################################################

# tile,0<copyX>,0<copyY>,16<copyWidth>,16<copyHeight>,
#   0<pasteStartX>,0<pasteStartY>,16<pasteCountHoriz>,16<pasteCountVert>,
#   open[copySource: old, template, or alt]
# Create a tile pattern on the new image using a part of the old image. 
# This command can be very useful but it’s not for beginners.
def tile(i, base_image):
    copyX = i[1]; copyY = i[2]; copyWidth = i[3]; copyHeight = i[4]
    pasteStartX = i[5]; pasteStartY = i[6]
    pasteCountHoriz = i[7]; pasteCountVert = i[8]

    # Default to 'old' as copySource if none specified
    if len(i) == 9:
        i.append('old')
    copySource = i[9].lower()

    for x in range(pasteCountHoriz):
        for y in range(pasteCountVert):
            if copySource == 'open' or copySource == 'old':
                copy(['copy', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        images['old'], base_image)
            elif copySource in images:
                copy(['copyalt', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        images[copySource], base_image)
            else:
                log_warning('tile: Invalid copy source — defaulting to "old"')
                copy(['copy', copyX, copyY, pasteStartX+(copyWidth*x),
                        pasteStartY+(copyHeight*y), copyWidth, copyHeight],
                        images['old'], base_image)
                
def copyscale(i:list):
    '''
    copyscale 0<oldX> 0<oldY> 32<oldWidth> 32<oldHeight> 0<newX> 0<newY>
        16<newWidth> 16<newHeight> 1[algo] old[source]
    
    Copy from the old (or alternative source) image to the new image, 
    while scaling the copied area to a new width/height. 
    '''

    oldX : int = i[1]
    oldY : int = i[2]
    oldWidth : int = i[3]
    oldHeight : int = i[4]

    newX : int = i[5]
    newY : int = i[6]
    newWidth : int = i[7]
    newHeight : int = i[8]

    if len(i) == 9:
        i.append(1)
    algo : int = i[9]

    if len(i) == 10:
        i.append('old')
    source : str = i[10]

    old_region : PIL.Image.Image = images[source].crop((oldX, oldY, 
            oldX+oldWidth, oldY+oldHeight)).convert('RGBa')
    new_region = PIL.Image.new('RGBa', (newWidth, newHeight))
    # Use premultiplied alpha (RGBa) instead of standard RGBA so I don't
    # have to alpha-blend by hand 

    new_rgba : ColorArray
    # new_data is the FLATTENED (1D) sequence of RGBA values that will be
    # turned into the scaled image
    new_data : List[ColorArray]
    if algo == 0 or (isinstance(algo, str) and algo.startswith('nearest')):
        new_data = []

        for ny in range(newHeight):
            for nx in range(newWidth):
                # old x/y of *individual pixels*
                ox_raw = oldX + ((nx+0.5) * (oldWidth/newWidth))
                ox = math.floor(ox_raw)
                # Special case to maximize symmetry
                if ox_raw == int(ox_raw) and nx >= newWidth/2:
                    #p#rint('*', end=' ')
                    ox -= 1

                oy_raw = oldY + ((ny+0.5) * (oldHeight/newHeight))
                oy = math.floor(oy_raw)
                # Special case to maximize symmetry
                if oy_raw == int(oy_raw) and ny >= newHeight/2:
                    oy -= 1

                #if ny == 0 and newWidth==newHeight:
                    #p#rint('(', newWidth/2, ')', nx >= newWidth/2, end=' ')
                    #p#rint('nx', nx, 'ox', ox_raw, '->', ox, end=' -- ')
                
                # Get RGBA data at the calculated pixel
                new_rgba = safe_pil_getpixel(i[0], old_region, 
                                             (ox-oldX, oy-oldY))

                # Finally, add the RGBA list to the flattened sequence
                new_data.append(tuple(new_rgba))
        # The moment of truth: turn new_data into image
        new_region.putdata(new_data)
    elif algo in (2, 'linear', 'bilinear'):
        new_region = old_region.resize((newWidth, newHeight), 
                                  PIL.Image.Resampling.BILINEAR)
    elif algo in (3, 'cubic', 'bicubic'):
        new_region = old_region.resize((newWidth, newHeight), 
                                  PIL.Image.Resampling.BICUBIC)
    # No Lanczos -- looks terrible when scaling pixel art (too many artifacts)
    else:
        # Default scaling algorithm (basically supersampling).
        # Delivers better results for pixel art, 
        # but it's slower than the others.
        if algo not in (1, 'default', 'average') \
                and (not isinstance(algo, str) \
                or not algo.startswith('super')):
            log_warning(
f'{i[0]}: unknown scaling algorithm value (defaulting to 1)'
            )

        # scale factors
        x_sf = newWidth/oldWidth
        y_sf = newHeight/oldHeight

        # Think of the old and new regions as two grids of boxes.
        # If the new grid's values are [0, 1, 2, ..., newWidth-1, newWidth],
        # then the old grid's values are [0, 1*scale_factor_width, 
        # 2*scale_factor_width, ..., newWidth-scale_factor_width, newWidth]
        # Note that len(new_x_grid) = newWidth+1
        old_x_grid = []
        for ox in range(oldWidth+1):
            old_x_grid.append(ox*x_sf)
        old_y_grid = []
        for oy in range(oldHeight+1):
            old_y_grid.append(oy*y_sf)
        # new_x_grid = list(range(newWidth))
        # new_y_grid = list(range(newHeight))
        #p#rint(old_x_grid)

        new_data = []

        # list is just [0,1,2…] so no diff. between range and range(len) here
        for ny in range(newHeight):
            for nx in range(newWidth): 
                # old_x_grid index of the first old-pixel that's factored into 
                # the new-pixel (take new_x and round down)
                l_index = 0
                for s in range(oldWidth, -1, -1):
                    l_index = s
                    if old_x_grid[s] <= nx:
                        break
                # old_x_grid index of the first old-pixel that's NOT factored 
                # into the new-pixel (take new_x+1 and round up)
                r_index = oldWidth
                for s in range(0, oldWidth+1, +1):
                    r_index = s
                    if old_x_grid[s] >= (nx+1):
                        break

                # Same thing but for y
                t_index = 0
                for s in range(oldHeight, -1, -1):
                    t_index = s
                    if old_y_grid[s] <= ny:
                        break
                b_index = oldHeight
                for s in range(0, oldHeight+1, +1):
                    b_index = s
                    if old_y_grid[s] >= (ny+1):
                        break

                # Find all horizontal and vertical "weights" (how much 
                # of each old pixel should go into the current new pixel). 
                    
                # Only do edge weighting if axis has >1 block and the 
                # first/last block has an old boundary going thru it
                l_weight = 0.0
                r_weight = 0.0
                t_weight = 0.0
                b_weight = 0.0
                # This check only works for upscales...
                if x_sf >= 1.0 and (r_index - l_index) > 1:
                    l_weight = old_x_grid[l_index+1] - nx
                    r_weight = (nx + 1) - old_x_grid[r_index-1]
                if y_sf >= 1.0 and (b_index - t_index) > 1:
                    t_weight = old_y_grid[t_index+1] - ny
                    b_weight = (ny + 1) - old_y_grid[b_index-1]
                # Test if old_x_grid[l_index] can be losslessly converted to int
                if x_sf < 1.0 and math.ceil(old_x_grid[l_index]) != \
                        int(old_x_grid[l_index]):
                    l_weight = old_x_grid[l_index+1] - nx
                if x_sf < 1.0 and math.ceil(old_x_grid[r_index]) != \
                        int(old_x_grid[r_index]):
                    r_weight = (nx + 1) - old_x_grid[r_index-1]
                if y_sf < 1.0 and math.ceil(old_y_grid[t_index]) != \
                        int(old_y_grid[t_index]):
                    t_weight = old_y_grid[t_index+1] - ny
                if y_sf < 1.0 and math.ceil(old_y_grid[b_index]) != \
                        int(old_y_grid[b_index]):
                    b_weight = (ny + 1) - old_y_grid[b_index-1]

                # Corner weights will be (edge1 * edge2)
                # p#rint('xy', nx, ny, 'wgt', l_weight, r_weight, 
                # t_weight, b_weight)
                    
                # Build separate arrays for weights on x and y axes
                # Initially build it out with the axis's scale factor
                # (for downscales) or 1.0 (for everything else)
                x_weights = [min(x_sf, 1.0)] * (r_index-l_index)
                y_weights = [min(y_sf, 1.0)] * (b_index-t_index)

                # Apply edge weights from earlier calculations
                if l_weight > 0.0:
                    x_weights[0] = l_weight
                if r_weight > 0.0:
                    x_weights[-1] = r_weight
                if t_weight > 0.0:
                    y_weights[0] = t_weight
                if b_weight > 0.0:
                    y_weights[-1] = b_weight
                # p#rint('new w/h', newWidth, newHeight, 'indices', l_index, 
                # r_index, t_index, b_index)
                        
                # Generate the full grid of weights for this pixel
                # [0, 0] in this list corresponds to 
                # [l_index, t_index] on old_grid
                # This is a 2D array, with each element signifying a weight
                # Outer array (y) has length = b_index - t_index
                # Inner array (x) has length = r_index - l_index
                # Note that Y is on the OUTSIDE!
                weight_grid = []
                for iy in y_weights:
                    weight_grid.append([ix*iy for ix in x_weights])
                # Because we're multiplying x_weights and y_weights together, 
                # corners will be handled correctly
                # (e.g. bottom right = b_weight * r_weight)
                
                #p#rint('new w/h', newWidth, newHeight, 
                #       '1D', x_weights, y_weights, '2D', weight_grid)
                        
                # Get the pixels and do the actual weighting
                new_rgba = [0,0,0,0]
                for wy in range(len(weight_grid)):
                    for wx in range(len(weight_grid[0])):
                        old_rgba = safe_pil_getpixel(i[0], 
                                old_region, (l_index+wx,t_index+wy))
                        # Update each r/g/b/a value based on weighted old value
                        for a in range(4):
                            new_rgba[a] += old_rgba[a] * weight_grid[wy][wx]
                
                # Round each element of new_rgba so it's an integer
                for a in range(4):
                    new_rgba[a] = round(new_rgba[a])

                # Finally, add the RGBA list to the flattened sequence
                new_data.append((new_rgba[0], new_rgba[1], 
                                 new_rgba[2], new_rgba[3]))
        # End of main scaling loop
        
        # The moment of truth: turn new_data into image
        new_region.putdata(new_data)

    # Convert region back to RGBA so it displays correctly
    new_region = new_region.convert('RGBA')

    images['new'].paste(new_region, (newX, newY, newX+newWidth, newY+newHeight))

###########################################################################
#### TRANSFORMATION COMMANDS ##############################################
###########################################################################

def resize(i, base_image):
    '''
    resize,256<newWidth>,256[newHeight],0[xOffset],0[yOffset]
    
    Resize the new image's canvas. Does not perform any scaling. If no height 
    given, create a square canvas. Anchor at top left by default, or move 
    original image right by `offsetX` pixels and down by `offsetY` pixels.
    '''

    newWidth = i[1]
    if len(i) == 2:
        i += [newWidth]
    newHeight = i[2]

    if len(i) <= 4: # if no offsets given, anchor at (0, 0)
        i = i[0:3] + [0, 0]
    offsetX = i[3]
    offsetY = i[4]

    oldWidth, oldHeight = base_image.size
    new_image = PIL.Image.new('RGBA', (newWidth,newHeight))
    new_image.paste(base_image,
                    (offsetX,offsetY,oldWidth,oldHeight))
    # Return the new image because trying to set base_image here will just
    # create a new image. Python is weird.
    return new_image

def crop(i:list, base_image:PIL.Image.Image):
    '''
    crop,0<x>,0<y>,0<width>,0<height>
    
    Same functionality as resize, but in a way that makes more sense if you 
    want to make the image smaller.
    '''
    
    x : int = i[1]
    y : int = i[2]
    width : int = i[3]
    height : int = i[4]

    return resize([i[0], width, height, -x, -y], base_image)

def scale(i:list):
    '''
    scale 256<newWidth> 256<newHeight> 1[algo]
    
    Scale the main canvas to the new width and height 
    (same algorithms as copyscale)
    '''

    rawWidth : int = i[1]
    rawHeight : int = i[2]
    algo : str = i[3]

    if rawWidth is None and rawHeight is None:
        log_warning(
            f'{i[0]}: Must provide either width or height as a non-null value')
        return

    oldWidth = images['new'].width
    oldHeight = images['new'].height

    if rawWidth is None:
        # If we make it here, rawHeight is guaranteed to not be None
        # (and it'll be equal to newHeight as seen below)
        newWidth : int = round(rawHeight/oldHeight * oldWidth)
    else:
        newWidth : int = rawWidth
    if rawHeight is None:
        newHeight : int = round(rawWidth/oldWidth * oldHeight)
    else:
        newHeight : int = rawHeight

    images['new'] = resize([i[0], newWidth, newHeight], images['new'])

    copyscale([i[0], 0, 0, oldWidth, oldHeight, 0, 0, newWidth, newHeight, algo, 'new'])

def rotate(i:list, base_image:PIL.Image.Image):
    '''
    rotate 90<degCW: multiple of 90> 0<x> 0<y> 16[size]
    
    Rotate the area clockwise, in place, on the new image. Unlike copy 
    commands, only 1 size argument is used, as the rotated area must be square.
    If you want to rotate a rectangular area 180°, flip it horizontally then 
    vertically instead.

    — OR —

    rotate 90<degCW: multiple of 90> 
    
    Rotate the full canvas of the new image. This may change the image's 
    dimensions (e.g. rotating a 400×300 image by 90° will make it 300×400).
    '''
    degCW : int = i[1]

    if (degCW % 90) != 0:
        log_warning(f'{i[0]}: \
Rotating by a number not divisible by 90 may have unintended effects.')

    if len(i) == 2: 
        # Special case to rotate entire image if x/y/w/h omitted
        rotated_image = base_image.rotate(
                -degCW, # negated b/c PIL rotates counterclockwise
                PIL.Image.Resampling.NEAREST, expand=True)
        return rotated_image

    x : int = i[2]
    y : int = i[3]

    # If size specified, use that value. If not, use 16. 
    # Remember: squares only.
    if len(i) == 4:
        i += [16]
    size : int = i[4]

    region = base_image.crop((x, y, x+size, y+size))
    region = region.rotate(-degCW, # negated b/c PIL rotates counterclockwise
        PIL.Image.Resampling.NEAREST, expand=False)
    base_image.paste(region, (x, y, x+size, y+size))
    return base_image

# flip,x<direction: x or y>,0[x],0[y],16[width],16[height]
# Flip the area in place on the new image. Unlike rotation, width and height
# can be different here.
def flip(i, base_image):
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
    # New in 7.5.5: can now flip horizontally and vertically at the same time
    # (i.e. rotate an area 180° even if it's not square)
    if 'x' in direction or 'h' in direction:
        region = PIL.ImageOps.mirror(region)
    if 'y' in direction or 'v' in direction:
        region = PIL.ImageOps.flip(region)
    # Otherwise, if direction is invalid, do nothing (the goal is to make 
    # it so the user CAN'T crash the program by mistake)
    base_image.paste(region, (x, y, x+width, y+height))

###########################################################################
#### FILTER COMMANDS ######################################################
###########################################################################

# grayscale,0[x],0[y],16[width],16[height] 
# Converts the area to grayscale (AKA black-and-white). For the command that
# literally makes the area only black and white (1-bit), use "threshold".
def grayscale(i, base_image):
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2: # number on the right should be equal to the index of y
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

def invert(i, base_image):
    '''
    invert,0[x],0[y],16[width],16[height]
    
    Inverts the area. For example, black becomes white, and red becomes cyan. 
    Alpha levels will be unchanged.
    '''
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2: # number on the right should be equal to the index of y
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
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba[3] == 0:
                continue

            region.putpixel((loop_x, loop_y), 
                    (255-rgba[0], 255-rgba[1], 255-rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

def rgbfilter(i, base_image):
    '''
    rgbfilter,0<redAdjust: -255 to +255>,0<greenAdjust>,0<blueAdjust>,
        0[x],0[y],16[width],16[height] 
    
    Adjusts the R/G/B color balance. You can use all three adjust arguments 
    at the same time to adjust brightness. 
    
    (Aliases: colorfilter, color_filter)
    '''
    redAdjust = i[1]
    greenAdjust = i[2]
    blueAdjust = i[3]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 5: # number on the right should be equal to the index of y
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
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba[3] == 0:
                continue

            region.putpixel((loop_x, loop_y), 
                    (rgba[0]+redAdjust, rgba[1]+greenAdjust, 
                    rgba[2]+blueAdjust, rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

# opacity,0<adjust: -255 to +255>,0[x],0[y],
#   16[width],16[height]
# Adjusts the opacity (alpha) levels. 
# Negative = more transparent, positive = more opaque.
def opacity(i, base_image):
    adjust = i[1]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3: # number on the right should be equal to the index of y
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
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            region.putpixel((loop_x, loop_y), 
                    (rgba[0], rgba[1], rgba[2], rgba[3]+adjust))
    base_image.paste(region, (x, y, x+width, y+height))

def hslfilter(i: list, base_image: PIL.Image.Image):
    '''
    hslfilter,0<hueAdjust: -180 to +180>,
        0<saturationAdjust: -100 to 100>,0<lightnessAdjust: -100 to 100>,
        0[x],0[y],16[width],16[height] 

    Adjusts hue, saturation, and lightness at the same time.
    '''

    hueAdjust = i[1]
    saturationAdjust = i[2]
    lightnessAdjust = i[3]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 5: # number on the right should be equal to the index of y
        i = [i[0], i[1], i[2], i[3], 
             0, 0, base_image.size[0], base_image.size[1]]
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
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba[3] == 0:
                continue

            hsla = rgba_to_hsla(rgba)
            hsla[0] += hueAdjust
            hsla[1] += saturationAdjust
            hsla[2] += lightnessAdjust
            format_hsla(hsla)
            rgba = hsla_to_rgba(hsla)
            region.putpixel((loop_x, loop_y), 
                    (rgba[0], rgba[1], rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

# filter.fill,0<red: 0 to 255>,0<green: 0 to 255>,
#   0<blue: 0 to 255>,255[alpha: 0 to 255],0[x],0[y],16[width],16[height] 
# Fills the area with the selected color.
def filter_fill(i, base_image: PIL.Image.Image):
    red = i[1]
    green = i[2]
    blue = i[3]

    # If no alpha given, assume 100% opaque
    if len(i) <= 4:
        i.append(255)
    alpha = i[4]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 6: # number on the right should be equal to the index of y
        i = [i[0], i[1], i[2], i[3], i[4], 0, 0, base_image.size[0], 
                base_image.size[1]]
    x = i[5]
    y = i[6]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 7:
        i += [16, 16]
    width = i[7]
    if len(i) == 8:
        i += [width]
    height = i[8]

    base_image.paste((red, green, blue, alpha), (x, y, x+width, y+height))

# Clip a number if it's below a minimum OR above a maximum
def clip(n, minimum, maximum):
    if n < minimum:
        n = minimum
    if n > maximum:
        n = maximum
    return n

# contrast,0<adjust: -128 to 128>,0[x],0[y],16[width],16[height]
# Adjusts the contrast. -128 will make all non-transparent pixels medium gray; 
# +127 will make all RGB values either 0 or 255 (8 colors).
def contrast(i, base_image):
    adjust = clip(i[1], -128, 127.99) # Avoid dividing by 0

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3: # number on the right should be equal to the index of y
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
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba[3] == 0:
                continue

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

def colorize(i: list, base_image: PIL.Image.Image):
    '''
    180<hue: 0 to 359>,50<saturation: 0 to 100>,
        50<lightness: 0 to 100>,0[x],0[y],16[width],16[height]

    Colorizes specified area in place. Converts area to B&W, treats L=127.5 as 
    the specified HSL color, and interpolates the rest from there. Ex.: if the 
    base color was coral [hsl(0,100,75)], it'll turn black->gray50->white to 
    red->coral->white.
    '''

    formatted_hsl = format_hsla([i[1], i[2], i[3]])
    h = formatted_hsl[0]
    s = formatted_hsl[1]
    l = formatted_hsl[2]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 5: # number on the right should be equal to the index of y
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
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba[3] == 0:
                continue

            hsla = rgba_to_hsla(rgba)
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

# sepia,0[x],0[y],16[width],16[height] 
# Simplified colorize syntax for creating sepia-toned images. 
# Based on hex code #a08060 or HSL(30,25,50)
def sepia(i, base_image):
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2: # number on the right should be equal to the index of y
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
    '''
    threshold,128<minWhite: 0 to 256>,0[x],0[y],16[width],16[height]

    Converts the image to 1-bit black & white based on a numeric lightness 
    threshold, determined by grayscale (luma) value. Any number LESS THAN 
    minWhite is black, any number GREATER or EQUAL is white. Set minWhite to 0 
    to make everything white. Set minWhite to 256 to make everything black. 
    Alpha levels for each pixel will be unchanged.
    '''
    minWhite = i[1]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 3: # number on the right should be equal to the index of y
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
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba[3] == 0:
                continue
            # Otherwise, alpha will be preserved when filtering
            # r/g/b will be the same because we converted the region to 
            # grayscale earlier
            luma = rgba[0]

            if luma < minWhite: # black
                region.putpixel((loop_x, loop_y), (0, 0, 0, rgba[3]))
            else: # white
                region.putpixel((loop_x, loop_y), (255, 255, 255, rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

def selcolor(i: list, base_image: PIL.Image.Image):
    '''
    selcolor,red<color>,0<hueAdjust: -180 to +180>,
        0<saturationAdjust: -100 to 100>,0<lightnessAdjust: -100 to 100>,
        0<x>,0<y>,16<width>,16<height> 

    Selective color: selects all pixels that have hues within a given sixth of 
    the HSL color wheel (red, yellow, green, cyan, blue, magenta), and applies 
    the HSL shift filter to each of those pixels.
    '''

    color = i[1].lower()[0]

    hueAdjust = i[2]
    saturationAdjust = i[3]
    lightnessAdjust = i[4]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 6: # number on the right should be equal to the index of y
        i = [i[0], i[1], i[2], i[3], i[4],
             0, 0, base_image.size[0], base_image.size[1]]
    x = i[5]
    y = i[6]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 7:
        i += [16, 16]
    width = i[7]
    if len(i) == 8:
        i += [width]
    height = i[8]

    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba[3] == 0:
                continue
            hsla = rgba_to_hsla(rgba)

            if (color == 'r' and (hsla[0] >= 330 or hsla[0] < 30)) \
                    or (color == 'y' and (hsla[0] >= 30 and hsla[0] < 90)) \
                    or (color == 'g' and (hsla[0] >= 90 and hsla[0] < 150)) \
                    or (color == 'c' and (hsla[0] >= 150 and hsla[0] < 210)) \
                    or (color == 'b' and (hsla[0] >= 210 and hsla[0] < 270)) \
                    or (color == 'm' and (hsla[0] >= 270 and hsla[0] < 330)):
                hsla[0] += hueAdjust
                hsla[1] += saturationAdjust
                hsla[2] += lightnessAdjust

            format_hsla(hsla)
            rgba = hsla_to_rgba(hsla)

            region.putpixel((loop_x, loop_y), 
                            (rgba[0], rgba[1], rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

# Note: This command seems to be pretty slow. Any suggestions for improving
# its performance are appreciated.
def twocolor(i: list, base_image: PIL.Image.Image):
    '''
    2color,0<hue>,100<saturation>,50<lightness>,0[x],0[y],16[width],16[height] 

    Simulates the effect of a two-color print job, where one of the colors is 
    black. The hue/saturation/lightness arguments are for the second color. 
    Unlike colorize, this is not recommended for use with black-and-white 
    images, as the filter uses saturation data to determine how much color each 
    pixel should have. (Alias: twocolor)
    '''

    formatted_hsl = format_hsla([i[1], i[2], i[3]])
    h = formatted_hsl[0]
    s = formatted_hsl[1]
    l = formatted_hsl[2]

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 5: # number on the right should be equal to the index of y
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

    # Save the old saturation values before we make the region grayscale
    old_region = base_image.crop((x, y, x+width, y+height))

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

    region = old_region.copy()
    for loop_x in range(width):
        for loop_y in range(height):
            rgba_gray = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # Skip fully transparent pixels
            if rgba_gray[3] == 0:
                continue

            hsla = rgba_to_hsla(rgba_gray)
            # Set hue and saturation to the values given in the user’s command
            # (leave alpha alone)
            hsla[0] = h
            hsla[1] = s

            # Adjust lightness based on user-provided lightness
            hsla[2] = ((100-hsla[2])/100)*min_l + ((hsla[2])/100)*max_l

            format_hsla(hsla)
            rgba_color = hsla_to_rgba(hsla)

            # Old saturation percentage determines the balance between "color"
            # and "gray"
            old_sat_pct = rgba_to_hsla(
                        safe_pil_getpixel(i[0], old_region, (loop_x, loop_y))
                    )[1]/100

            rgba = [
                int(rgba_color[0]*old_sat_pct + rgba_gray[0]*(1-old_sat_pct)),
                int(rgba_color[1]*old_sat_pct + rgba_gray[1]*(1-old_sat_pct)),
                int(rgba_color[2]*old_sat_pct + rgba_gray[2]*(1-old_sat_pct)),
                rgba_color[3]
            ]

            region.putpixel((loop_x, loop_y), 
                            (rgba[0], rgba[1], rgba[2], rgba[3]))
    base_image.paste(region, (x, y, x+width, y+height))

def recolor(i:list, base_image:PIL.Image.Image):
    '''
    recolor ()<oldColor> $_fillcolor<newColor> 0[x] 0[y] 16[width] 16[height]
    
    Replace every pixel matching `oldColor` with `newColor`. If `oldColor` is 
    null, recolor all non-transparent colors.
    '''
    oldColor = i[1]
    newColor = i[2]
    if isinstance(oldColor, list) and isinstance(newColor, list) and len(oldColor) != len(newColor):
        log_warning(f'{i[0]}: list lengths don’t match')
        return None

    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 5: # number on the right should be equal to the index of y
        i = [i[0], i[1], i[2], 0, 0, base_image.size[0], base_image.size[1]]
    x : int = i[3]
    y : int = i[4]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 5:
        i += [16, 16]
    width : int = i[5]
    if len(i) == 6:
        i += [width]
    height : int = i[6]

    region = base_image.crop((x, y, x+width, y+height))
    for loop_x in range(width):
        for loop_y in range(height):
            oldRGBA : ColorArray = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            if isinstance(oldColor, list) and isinstance(newColor, list):
                for j in range(len(oldColor)):
                    if oldRGBA == (oldColor[j].red, oldColor[j].green, 
                                        oldColor[j].blue, oldColor[j].alpha):
                        region.putpixel((loop_x, loop_y), 
                                (newColor[j].red, newColor[j].green, 
                                newColor[j].blue, newColor[j].alpha))
            else:
                # If oldColor is null, recolor all non-empty pixels;
                # if not, check for color match
                if (oldColor is None and oldRGBA[3] > 0) \
                        or (oldColor is not None and \
                            oldRGBA == (oldColor.red, oldColor.green, 
                                        oldColor.blue, oldColor.alpha)):
                    region.putpixel((loop_x, loop_y), 
                                    (newColor.red, newColor.green, 
                                    newColor.blue, newColor.alpha))

    base_image.paste(region, (x, y, x+width, y+height))

###########################################################################
#### LIST COMMANDS ########################################################
###########################################################################

def list_remove(i: list):
    '''
    list.remove,$l<listVar>,0<index>
    
    Remove the item at the given index from the list; shift the items after it 
    to the left. Note that this is different from the Python method 
    `l.remove()` that removes based on value rather than index.
    '''
    if not var_check(i[1], i[0], exists=True):
        # var_check will generate its own warning if it fails, so no need
        # for another one here
        return
    
    listVar : list = i[1]
    index : int = i[2]

    l : list = subst_var(listVar, i[0], mutable=True)
    del l[index]

def list_replace(i: list):
    '''
    list.replace,$l<listVar>,0<index>,"thing"<item>
    
    Replace the contents of the given `index` of `listVar` with `item`.
    '''
    if not var_check(i[1], i[0], exists=True):
        # var_check will generate its own warning if it fails, so no need
        # for another one here
        return
    
    listVar : list = i[1]
    index : int = i[2]
    item : Any = i[3]

    l : list = subst_var(listVar, i[0], mutable=True)
    l[index] = item

def list_swap(i: list):
    '''
    list.swap $l<listVar> 0<index1> 1<index2> 
    
    Swap the positions of the items of `listVar` at `index1` and `index2`  
    (eliminating the need to create a temporary variable).
    '''
    if not var_check(i[1], i[0], exists=True):
        # var_check will generate its own warning if it fails, so no need
        # for another one here
        return
    
    listVar : list = i[1]
    index1 : int = i[2]
    index2 : int = i[3]

    l : list = subst_var(listVar, i[0], mutable=True)
    l[index1], l[index2] = l[index2], l[index1]

###########################################################################
#### DRAWING COMMANDS #####################################################
###########################################################################

def setpixel(i: list):
    '''
    setpixel,0<x>,0<y>,(color,"red")<color>
    
    Sets the color of the pixel at (x,y) on the base image.
    '''

    x : int = i[1]
    y : int = i[2]
    color : Color = i[3]

    images['new'].putpixel((x, y), 
                           (color.red, color.green, color.blue, color.alpha))

def draw_rect(i: list):
    '''
    draw.rect,0<x>,0<y>,16<width>,16<height>,
        0[outline: 0 for fill, 1 for outline, 2 for both]

    Draw a rectangle with the top left corner at the given x and y.
    (Alias: draw.rectangle)
    '''
    global draw_obj
    if draw_obj is None:
        # Initialize draw object if it doesn't exist yet
        draw_obj = PIL.ImageDraw.Draw(images['new'], 'RGBA')

    x = i[1]
    y = i[2]
    width = i[3]
    height = i[4]

    # Default to filled if no outline arg given
    if len(i) == 5:
        i.append(0)
    outline = i[5]

    fc = variables['$_fillcolor']
    lc = variables['$_linecolor']
    lw = variables['$_linewidth']

    if outline == 0:
        draw_obj.rectangle([x, y, x+width-1, y+height-1], 
                           fill=(fc.red, fc.green, fc.blue, fc.alpha),
                           outline=None,
                           width=lw)
    elif outline == 1:
        draw_obj.rectangle([x, y, x+width-1, y+height-1], 
                           fill=None,
                           outline=(lc.red, lc.green, lc.blue, lc.alpha),
                           width=lw)
    elif outline == 2:
        draw_obj.rectangle([x, y, x+width-1, y+height-1], 
                           fill=(fc.red, fc.green, fc.blue, fc.alpha),
                           outline=(lc.red, lc.green, lc.blue, lc.alpha),
                           width=lw)

def draw_ellipse(i: list):
    '''
    draw.ellipse,0<x>,0<y>,16<width>,16<height>,
        0[outline: 0 for fill, 1 for outline, 2 for both]

    Draw an ellipse with the top left "corner" at the given x and y.
    '''
    global draw_obj
    if draw_obj is None:
        # Initialize draw object if it doesn't exist yet
        draw_obj = PIL.ImageDraw.Draw(images['new'], 'RGBA')

    x = i[1]
    y = i[2]
    width = i[3]
    height = i[4]

    # Default to filled if no outline arg given
    if len(i) == 5:
        i.append(0)
    outline = i[5]

    fc = variables['$_fillcolor']
    lc = variables['$_linecolor']
    lw = variables['$_linewidth']

    if outline == 0:
        draw_obj.ellipse([x, y, x+width-1, y+height-1], 
                           fill=(fc.red, fc.green, fc.blue, fc.alpha),
                           outline=None,
                           width=lw)
    elif outline == 1:
        draw_obj.ellipse([x, y, x+width-1, y+height-1], 
                           fill=None,
                           outline=(lc.red, lc.green, lc.blue, lc.alpha),
                           width=lw)
    elif outline == 2:
        draw_obj.ellipse([x, y, x+width-1, y+height-1], 
                           fill=(fc.red, fc.green, fc.blue, fc.alpha),
                           outline=(lc.red, lc.green, lc.blue, lc.alpha),
                           width=lw)

def draw_line(i: list):
    '''
    draw.line,0<x1>,0<y1>,16<x2>,16<y2> 

    Draw a line from (x1,y1) to (x2,y2). Note that this is different from the 
    width/height system used for everything else. The example coordinates 
    would have a width and height of 17 pixels.
    '''
    global draw_obj
    if draw_obj is None:
        # Initialize draw object if it doesn't exist yet
        draw_obj = PIL.ImageDraw.Draw(images['new'], 'RGBA')

    x1 = i[1]
    y1 = i[2]
    x2 = i[3]
    y2 = i[4]

    lc = variables['$_linecolor']
    lw = variables['$_linewidth']

    draw_obj.line([x1, y1, x2, y2], 
            (lc.red, lc.green, lc.blue, lc.alpha),
            width=lw)

def draw_fillcolor(i: list):
    '''
    draw.fillcolor,(rgb,255,0,0)<color> 

    Set the fill color.
    '''

    color = i[1]

    if type(color) != Color:
        log_warning(f'{i[0]}: invalid color')
        return

    set_([i[0], '$_fillcolor', i[1]], internal=True)

def draw_linecolor(i: list):
    '''
    draw.linecolor,(rgb,255,0,0)<color> 

    Set the outline color.
    '''

    color = i[1]

    if type(color) != Color:
        log_warning(f'{i[0]}: invalid color')
        return

    set_([i[0], '$_linecolor', i[1]], internal=True)

def draw_alphablend(i: list):
    '''
    
    draw.alphablend,1<toggle> 

    Toggles alpha blending on (1) or off (0). If on, drawing partially 
    transparent shapes will merge their colors with the existing pixels 
    underneath. If off, the pixels underneath will by fully overwritten by the 
    shapes. If this command is not called, alpha blending will be turned ON by 
    default. 
    TODO: add setting "2" that also alphablends the original copying commands?
    '''

    global draw_obj

    if i[1]:
        draw_obj = PIL.ImageDraw.Draw(images['new'], 'RGBA')
    else:
        draw_obj = PIL.ImageDraw.Draw(images['new'], 'RGB')

###########################################################################
#### SUBCOMMANDS ##########################################################
###########################################################################
        
def parse_subcmd(raw_cmd: str):
    '''Strip whitespace and opening/closing parentheses from a subcommand.'''

    # COPY raw_cmd to prevent issues caused by overwriting data
    # First strip whitespace
    cmd_str = raw_cmd.strip()
    # Then check for parens at start and end
    # removeprefix would be nice here but that's only in Py3.9
    if len(cmd_str) >= 2 and cmd_str[0] == '(' and cmd_str[-1] == ')':
        # ...and remove them if they're there
        cmd_str = cmd_str[1:-1]
    else:
        # Otherwise, there's something wrong with the input
        return None
    
    # Parse the line to separate out the arguments
    cmd = parse_line(cmd_str)
    # Replace command aliases (in place)
    alias(cmd, is_subcmd=True)

    return cmd

def subcmd(raw_cmd: abc.Sequence):
    '''
    Evaluate a subcommand embedded in parentheses, e.g. (empty,0,0,16,16).
    Return the result of the command, in whatever format is appropriate.
    Invalid or empty commands return None (and will be treated as false).
    '''
    # The value we're going to return at the end
    result = None

    if type(raw_cmd) == str:
        # If we're here, the command is passed in as a string something like 
        # "(empty,0,0,16,16)". We want to get rid of the parens at the
        # start and end (but keep any that are inside).
        cmd = parse_subcmd(raw_cmd)
        if cmd is None:
            # If None is returned, raw_cmd must be invalid
            # This *shouldn't* happen, but I'll plan for it just in case
            log_warning('Invalid subcommand: %s' % raw_cmd)
            return None
    elif type(raw_cmd) == list:
        # This doesn't happen in normal parsing, but some advanced commands
        # (like change) build a subcommand in list form,
        # then pass it directly to this function. In this case,
        # our job is easy.
        cmd = raw_cmd.copy()
        # Replace command aliases (in place)
        alias(cmd, is_subcmd=True)
    else:
        # If we don't get a list or str... we have no idea what to do.
        return None
    
    # Make sure subcommand has right number of arguments, 
    # and noop it out if it doesn't
    arg_check(cmd, is_subcmd=True)
    
    # empty/noop commands can return null value before we bother to evaluate
    # variables or nested subcommands
    if cmd[0].strip() == '' or cmd[0] == 'null':
        return None

    # Replace variable names with the variable's current value 
    subst_all_vars(cmd)

    # Now that we've broken the command into the normal list format,
    # we need to check each argument of the command for subcommands and
    # recursively call this function as needed.
    if version_gte(6):
        # Call short-circuiting commands BEFORE recursively calling subcmd().
        # These commands will call subcmd() from within their own functions.
        if cmd[0] == 'or':
            result = logic_or(cmd)
        elif cmd[0] == 'and':
            result = logic_and(cmd)
        elif cmd[0] == 'iif':
            result = iif(cmd)

        # For all other subcommands, loop thru arguments, and if there are
        # any unevaluated subcommands, call subcmd() on them.
        for arg_n in range(1, len(cmd)):
            if type(cmd[arg_n]) == Subcommand:
                # Execute the command INSIDE the parens FIRST
                cmd[arg_n] = subcmd(cmd[arg_n].content)
    else:
        # Subcommands existed starting in v4.1, but you couldn't nest them
        log_warning('Nested subcommands are only supported in v6.0.0 and later')

    # Main dictionary of subcommands (except noops)
    # No aliases included because those are already accounted for above
    if cmd[0] == 'eq':
        result = eq(cmd)
    elif cmd[0] == 'ne':
        result = ne(cmd)
    elif cmd[0] == 'lt':
        result = lt(cmd)
    elif cmd[0] == 'gt':
        result = gt(cmd)
    elif cmd[0] == 'le':
        result = le(cmd)
    elif cmd[0] == 'ge':
        result = ge(cmd)
    elif cmd[0] == 'cmp':
        result = cmp(cmd[0], cmd[1])

    elif cmd[0] in ['or', 'and', 'iif']:
        # These commands are already handled above but we need to check for 
        # them here too so we don't get false invalid-command errors
        pass
    elif cmd[0] == 'not':
        result = not cmd[1]
    elif cmd[0] == 'xor':
        result = (bool(cmd[1]) != bool(cmd[2]))

    elif cmd[0] == 'add':
        result = add(cmd)
    elif cmd[0] == 'sub':
        result = sub(cmd)
    elif cmd[0] == 'mul':
        result = mul(cmd)
    elif cmd[0] == 'floordiv':
        result = floordiv(cmd)
    elif cmd[0] == 'truediv':
        result = truediv(cmd)
    elif cmd[0] == 'mod':
        result = mod(cmd)
    elif cmd[0] == 'pow':
        result = pow_(cmd)
    elif cmd[0] == 'log':
        result = log(cmd)
    elif cmd[0] == 'abs':
        result = abs(cmd[1])
    elif cmd[0] == 'floor':
        result = math.floor(cmd[1])
    elif cmd[0] in 'ceil':
        result = math.ceil(cmd[1])
    elif cmd[0] == 'min':
        result = min_(cmd)
    elif cmd[0] == 'max':
        result = max_(cmd)
    elif cmd[0] == 'round':
        result = round_(cmd)

    elif cmd[0] == 'len':
        result = len(cmd[1])
    elif cmd[0] == 'get':
        result = get(cmd)
    elif cmd[0] == 'slice':
        result = slice_(cmd)
    elif cmd[0] == 'in':
        result = cmd[2] in cmd[1]
    elif cmd[0] == 'find':
        result = find(cmd)
    elif cmd[0] == 'sum':
        result = sum(cmd[1])
    elif cmd[0] == 'count':
        result = py_method(cmd[0:3], 'count') # args: var + 1 extra
    elif cmd[0] == 'sort':
        result = sort(cmd)
    elif cmd[0] == 'reverse':
        result = cmd[1][::-1]

    elif cmd[0] == 'str_mul':
        if version_gte(7,2):
            log_warning(f'{cmd[0]} is a deprecated command; please use * for \
string repetition instead')
        result = str(cmd[1]) * cmd[2]
    elif cmd[0] == 'upper':
        result = py_method(cmd[0:2], 'upper') # args: var + 0 extra
    elif cmd[0] == 'lower':
        result = py_method(cmd[0:2], 'lower') # args: var + 0 extra
    elif cmd[0] == 'titlecase':
        result = titlecase(cmd)
    elif cmd[0] == 'sentencecase':
        result = py_method(cmd[0:2], 'capitalize') # args: var + 0 extra
    elif cmd[0] == 'startswith':
        result = py_method(cmd[0:3], 'startswith') # args: var + 1 extra
    elif cmd[0] == 'endswidth':
        result = py_method(cmd[0:3], 'endswith') # args: var + 1 extra
    elif cmd[0] == 'join':
        result = join(cmd)
    elif cmd[0] == 'split':
        result = split(cmd)

    elif cmd[0] == 'list':
        result = cmd[1:]
    elif cmd[0] == 'range':
        result = range_(cmd)

    elif cmd[0] == 'int':
        result = int_(cmd)
    elif cmd[0] == 'float':
        result = float_(cmd)
    elif cmd[0] == 'str':
        result = str_(cmd)
    elif cmd[0] == 'bool':
        result = bool_(cmd)
    elif cmd[0] == 'hex':
        result = hex_(cmd)
    elif cmd[0] == 'bin':
        result = bin_(cmd)
    elif cmd[0] == 'type':
        result = type_(cmd)

    elif cmd[0] == 'color':
        result = color_(cmd)
    elif cmd[0] == 'rgba':
        result = rgb(cmd)
    elif cmd[0] == 'hsla':
        result = hsl(cmd)
    elif cmd[0] == 'getpixel':
        result = getpixel(cmd, images['new'])
    elif cmd[0] == 'pal.get':
        result = pal_get(cmd, images['old'])

    # Before version 7, red/green/blue/alpha checked the new image.
    # In v7.0.0, this was changed to the old image because this was more useful
    # and consistent with the behavior of empty.
    # Code written for earlier versions will still use the old behavior.
    elif cmd[0] == 'red':
        if version_gte(7):
            result = red_(cmd, images['old'])
        else:
            result = red_(cmd, images['new'])
    elif cmd[0] == 'green':
        if version_gte(7):
            result = green_(cmd, images['old'])
        else:
            result = green_(cmd, images['new'])
    elif cmd[0] == 'blue':
        if version_gte(7):
            result = blue_(cmd, images['old'])
        else:
            result = blue_(cmd, images['new'])
    elif cmd[0] == 'alpha':
        if version_gte(7):
            result = alpha_(cmd, images['old'])
        else:
            result = alpha_(cmd, images['new'])

    elif cmd[0] == 'hue':
        if version_gte(7,3):
            result = hue(cmd, images['old'])
        else:
            result = hue(cmd, images['new'])
    elif cmd[0] == 'saturation':
        if version_gte(7,3):
            result = saturation(cmd, images['old'])
        else:
            result = saturation(cmd, images['new'])
    elif cmd[0] in ('lightness', 'luminosity'):
        if version_gte(7,3):
            result = lightness(cmd, images['old'])
        else:
            result = lightness(cmd, images['new'])

    elif cmd[0] == 'empty':
        result = empty(cmd, images['old'])
    elif cmd[0] == 'getrgba':
        result = getrgba(cmd, images['old'])
    elif cmd[0] == 'gethsla':
        result = gethsla(cmd, images['old'])

    elif cmd[0] == 'width':
        result = width_(cmd)
    elif cmd[0] == 'height':
        result = height_(cmd)

    else:
        log_warning('Invalid subcommand: %s' % raw_cmd)
        return None

    # Uncomment this line to print subcommand and its result, for debugging
    #p#rint(cmd, result)

    return result

def iif(i: list):
    '''
    (iif,<cond>,<ifTrue>,<ifFalse>) 
    
    Inline if, as found in functional programming. Returns `ifTrue` if 
    `cond` evaluates to true, and `ifFalse` if `cond` evaluates to false. 
    Uses short-circuiting so only one of the value branches will be evaluated.
    '''

    cond = i[1]
    ifTrue = i[2]
    ifFalse = i[3]

    if isinstance(cond, Subcommand):
        cond = subcmd(cond.content)
    cond_result = bool(cond)

    if cond_result:
        if isinstance(ifTrue, Subcommand):
            return subcmd(ifTrue.content)
        else:
            return ifTrue
    else:
        if isinstance(ifFalse, Subcommand):
            return subcmd(ifFalse.content)
        else:
            return ifFalse

# EQUALITY SUBCOMMANDS

def eq(i: list):
    '''
    Equal to (eq, =, ==)
    Use "set" to set variables, not "=".
    '''

    if len(i) == 3: # If 2 arguments
        return i[1] == i[2]
    # But if there are 3 or more arguments (x1, x2, x3), treat the command as
    # "if x1==x2 AND x2==x3 AND..."
    return (i[1] == i[2]) and eq([i[0]] + i[2:])

def ne(i: list):
    '''
    Not equal to (ne, !=, <>, ≠)
    '''

    if len(i) == 3: # If 2 arguments
        return i[1] != i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return (i[1] != i[2]) and ne([i[0]] + i[2:])

def lt(i: list):
    '''
    Less than (lt, <)
    '''

    if len(i) == 3: # If 2 arguments
        try:
            return i[1] < i[2]
        except Exception: # if e.g. invalid type match
            log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] < i[2]) and lt([i[0]] + i[2:])
    except Exception:
        log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
        return None

def gt(i: list):
    '''
    Greater than (gt, >)
    '''

    if len(i) == 3: # If 2 arguments
        try:
            return i[1] > i[2]
        except Exception: # if e.g. invalid type match
            log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] > i[2]) and gt([i[0]] + i[2:])
    except Exception:
        log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
        return None

def le(i: list):
    '''
    Less than or equal to (le, <=, ≤)
    '''

    if len(i) == 3: # If 2 arguments
        try:
            return i[1] <= i[2]
        except Exception: # if e.g. invalid type match
            log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] <= i[2]) and le([i[0]] + i[2:])
    except Exception:
        log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
        return None

def ge(i: list):
    '''
    Greater than or equal to (ge, >=, ≥)
    '''

    if len(i) == 3: # If 2 arguments
        try:
            return i[1] >= i[2]
        except Exception: # if e.g. invalid type match
            log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
            return None
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return (i[1] >= i[2]) and ge([i[0]] + i[2:])
    except Exception:
        log_warning(f'{i[0]}: couldn’t compare {i[1]} and {i[2]}')
        return None

# END EQUALITY SUBCOMMANDS

# LOGICAL SUBCOMMANDS

def logic_or(i: list):
    '''
    Logical OR (or, ||)
    '''

    short_circuit : bool = False
    for arg in i[1:]:
        if type(arg) == Subcommand:
            # Execute subcommands one at a time, then check short-circuiting
            arg_result = subcmd(arg.content)
        else:
            arg_result = arg

        short_circuit = bool(short_circuit or arg_result)
        if short_circuit == True:
            return True
    # If we make it to the end and none of the arguments were true (so we
    # didn't short-circuit), result must be False
    return False

def logic_and(i: list):
    '''
    Logical AND (and, &&)
    '''

    short_circuit : bool = True
    for arg in i[1:]:
        if type(arg) == Subcommand:
            # Execute subcommands one at a time, then check short-circuiting
            arg_result = subcmd(arg.content)
        else:
            arg_result = arg

        short_circuit = bool(short_circuit and arg_result)
        if short_circuit == False:
            return False
    # If we make it to the end and all of the arguments were true (so we
    # didn't short-circuit), result must be True
    return True

# END LOGICAL SUBCOMMANDS

# MATH SUBCOMMANDS

def add(i: list):
    '''
    (+,x1,x2,...)
    
    Add two or more numbers. 
    
    (Alias: add)
    '''

    # No unary plus, that's stupid
    if len(i) == 3: # If 2 arguments
        return i[1] + i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return i[1] + add([i[0]] + i[2:])

def sub(i: list):
    '''
    (-,x1,x2,...)

    Subtract two or more numbers. 

    — OR —

    (-,x)

    Unary minus sign, negates x. Equivalent to (*, x, -1)
    
    (Aliases: sub, − [minus sign], or – [en dash]. 
    The symbol in the example is an ASCII hyphen.)
    '''

    if len(i) == 2: # If 1 argument, make it a unary minus (opposite)
        return -i[1]
    elif len(i) == 3: # If 2 arguments
        return i[1] - i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return i[1] - sub([i[0]] + i[2:])

def mul(i: list):
    '''
    (*,x1,x2,...)
    
    Multiply two or more numbers. (Aliases: mul, × [multiplication sign, 
    not letter X])
    '''

    if len(i) == 3: # If 2 arguments
        return i[1] * i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return i[1] * mul([i[0]] + i[2:])

def truediv(i: list):
    '''
    (/,x1,x2,...)
    
    Divide two or more numbers. Do not round the result. The result will 
    always be a floating-point number. 
    
    (Aliases: truediv, ÷)
    '''

    # Check for division by 0
    for n in i[2:]:
        if n == 0:
            log_warning(f'{i[0]}: Division by zero ({'÷'.join(i[1:])})')

    if len(i) == 3: # If 2 arguments
        return i[1] / i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return i[1] / truediv([i[0]] + i[2:])

def floordiv(i: list):
    '''
    (//,x1,x2,...)
    
    Integer division: divide two or more numbers, then round the result down 
    to the nearest integer. 
    
    (Aliases: floordiv, div)
    '''

    # Check for division by 0
    for n in i[2:]:
        if n == 0:
            log_warning(f'{i[0]}: Division by zero ({'÷'.join(i[1:])})')

    if len(i) == 3: # If 2 arguments
        return i[1] // i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return i[1] // floordiv([i[0]] + i[2:])

def mod(i: list):
    '''
    (%,x1,x2,...)

    Modulo: divide two or more numbers and return the remainder. 
    
    (Alias: mod)
    '''

    # Check for division by 0
    for n in i[2:]:
        if n == 0:
            log_warning(f'{i[0]}: Modulo by zero ({' mod '.join(i[1:])})')

    if len(i) == 3: # If 2 arguments
        return i[1] % i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return i[1] % mod([i[0]] + i[2:])

def pow_(i: list):
    '''
    (^,x1,x2,...)

    Raise one number to the power of another. Technically you *can* add x3, x4, 
    etc but it'll make the program crash/freeze VERY quickly. 
    
    (Aliases: pow, **)
    '''

    if len(i) == 3: # If 2 arguments
        return i[1] ** i[2]
    # But if there are 3 or more arguments (x1, x2, x3)...
    return i[1] ** pow_([i[0]] + i[2:])
    
def log(i: list):
    '''
    (log 42<x> 10[base])
    
    Logarithm of x. Defaults to a logarithm base of 10, i.e. 10^(ans) = x.

    — OR —

    (ln 42<x>) for natural logarithms
    '''

    x = i[1]
    if x <= 0:
        log_warning(f'{i[0]}: Logarithm must be of a positive number')
        return None
    if len(i) == 2:
        if i[0] == 'ln': # special alias
            i.append(math.e)
        i.append(10)
    base = i[2]
    if base <= 1:
        log_warning(f'{i[0]}: Logarithm base must be greater than 1')
        return None

    if base == 10:
        return math.log10(x)
    elif base == 2:
        return math.log2(x)
    elif base == math.e:
        return math.log(x) # python's log defaults to ln
    else:
        return math.log(x, base)

def min_(i: list):
    '''
    Return the smallest item passed to the subcommand.
    '''

    if isinstance(i[1], abc.Sequence):
        return min(i[1])
    else:
        return min(i[1:])

def max_(i: list):
    '''
    Return the largest item passed to the subcommand.
    '''

    if isinstance(i[1], abc.Sequence):
        return max(i[1])
    else:
        return max(i[1:])
    
def round_(i: list):
    '''
    (round,1.2<x>,$_false[decPlaces]) 
    
    Round using standard mathematical rules. This is a wrapper around Python's 
    built-in function of the same name, so there may be some weird edge cases. 
    If an int is given for decPlaces, return a float rounded to that many 
    decimal places. (Negative integers allow you to round to higher place 
    values; e.g. -1 = round to tens place). If decPlaces is not given or is 
    set to a non-integer value, return an int.
    '''

    decPlaces = i[2]
    # Turn all non-int values for decPlaces into "None" 
    # so Python processes it correctly
    if not isinstance(decPlaces, int):
        decPlaces = None
    
    return round(i[1], decPlaces)

# END MATH SUBCOMMANDS

# SEQUENCE SUBCOMMANDS

def get(i: list):
    '''
    (get,$x<seq>,0<index>)

    Returns the item at index 0 of the given list/string. The first item has 
    index 0, second item has index 1, etc., unless you change the index_from 
    flag. In addition, index -1 is the last item, -2 is the second-to-last 
    item, etc.
    '''
    
    seq = i[1]
    index = i[2]

    if index < 0:
        if abs(index) > len(seq):
            log_warning(
                f'{i[0]}: index {index} is out of range for sequence {seq}'
            )
            return None
        # else
        return seq[index]
    # elif index >= 0
    # Adjust index based on index_from flag 
    # so it follows Python's index-from-0 rules
    normalized_index = index - flags['index_from']
    if normalized_index < 0 or normalized_index >= len(seq):
        log_warning(
            f'{i[0]}: index {index} is out of range for list {seq}'
        )
        return None
    # else
    return seq[normalized_index]

def slice_(i: list):
    '''
    (slice,$s<seq>,0<start>,2[stop],1[step])
    
    Returns a sublist of the given list. Omitting the stop value 
    means slice the entire rest of the list. Entering a step value 
    greater than 1 means only include every Xth item of the list.
    '''
    seq : abc.Sequence = i[0]

    start : int = i[1]
    if not isinstance(start, int):
        start = flags['index_from']

    if len(i) == 2:
        seq.append(None)
    stop : Optional[int] = i[2]
    if not isinstance(stop, int):
        stop = None

    if len(i) == 3:
        seq.append(1)
    step : int = i[3]

    # Normalize start
    if start >= 0:
        start -= flags['index_from']
    # Negative start values stay as is
        
    # Normalize stop
    if stop is not None:
        if flags['closed_ranges']:
            # Have to special-case stop==-1 because if closed_ranges==1,
            # then -1 means go to the end of the list
            stop = (stop+sign(step) if (stop != -1) else None)
            # if step>0 then stop+=1
            # else if step<0 then stop-=1

    if stop is None:
        return seq[start::step]
    else:
        return seq[start:stop:step]

def find(i: list):
    '''
    (find "Hello"<seq> "l"<item> 0[start] ()[stop])
    
    Return the index of the first occurrence of item/substring `item` in the 
    list/string `seq`. Return -1 if `item` couldn't be found anywhere in `seq`.
    Use `start` and `stop` arguments to only search a subset of the sequence.
    '''
    seq : abc.Sequence = i[1]
    item : Any = i[2]

    try:
        if len(i) >= 5:
            start : int = i[3]
            stop : int = i[4]
            return seq.index(item, start, stop)
        elif len(i) == 4:
            start : int = i[3]
            return seq.index(item, start)
        else: # minimum 2 args (len==3)
            return seq.index(item)
    except ValueError: # if not in list
        if version_gte(8):
            return None
        else:
            return -1

def sort(i: list):
    '''
    (sort $l<list> ""[key] [keyArg2] [keyArg3]...)
    
    Returns a sorted version of the list l, in ascending order according to Python's built-in Timsort algorithm. The function will return a new list, and will not modify the contents of the last you pass in. 

    The optional `key` argument lets you specify a subcommand to apply some 
    operation to values before sorting them. For example, if key="lower" when 
    sorting a list of strings, then the converter will sort alphabetically and 
    ignore case (otherwise, it'll sort by Unicode codepoint, which may lead to 
    unexpected results). And if key="lightness" for a list of colors, it'll 
    sort from darkest to lightest.

    The key function can even have multiple arguments; for example, if $l is a 
    list of lists, (sort $l get 0) will sort by the first item of each sub-list.
    '''
    if version_gte(7,6) and isinstance(i[1], str):
        log_warning('sort: Sorting strings is deprecated')

    if len(i) >= 3 and i[2]: # 2 or more args + key arg doesn't eval to false
        return sorted(i[1], key = lambda a: subcmd([i[2], a] + i[3:]))
    else: # 1 arg
        return sorted(i[1])

# END SEQUENCE SUBCOMMANDS

# LIST SUBCOMMANDS

def range_(i: list):
    '''
    (range,0[start],10<stop>,1[step])
    
    Returns a list consisting of a sequence of numbers counting from `start` 
    to `stop`, and counting up by `step` every time. Unlike Python's range 
    function, any of the arguments can be floats too.
    '''
    if len(i) == 2:
        i.insert(1, flags['index_from']) # start: 0 (default) or 1
    if len(i) == 3: # fallthru -- not elif on purpose
        i.append(1) # step

    start : Num = i[1]
    stop : Num = i[2]
    step : Num = i[3]
    
    # If start or step are floats, make every element of the returned list be 
    # a float for consistency
    # (Don't care if stop is a float because it's just used in conditionals)
    if isinstance(start,float) or isinstance(step,float):
        # float_mode = True
        start = float(start)
        step = float(step)

    # Make sure stop is actually reachable.
    # If the signs of (stop - start) and step are DIFFERENT, 
    # then stop is unreachable and we throw a warning.
    if (stop - start) * step < 0:
        log_warning('f{i[0]}: unreachable stop condition')
        return []
        
    # Build out the list
    n = start
    l = []
    # Conditions vary depending on step's sign and closed_range flag
    if step > 0:
        while (n <= stop if flags['closed_ranges'] else n < stop):
            l.append(n)
            n += step
    elif step < 0:
        while (n >= stop if flags['closed_ranges'] else n > stop):
            l.append(n)
            n += step
    else: # step == 0
        log_warning(f'{i[0]}: step argument must be nonzero')

    return l

# END LIST SUBCOMMANDS

# STRING SUBCOMMANDS

def titlecase(i: list):
    '''
    (titlecase,"hello world"<str>)
    
    Convert string to title case (first letter of each word capitalized; 
    rest of word lowercase). This isn't a "true" title case, because short 
    words like "a", "of", or "the" are still capitalized. Python has a similar 
    function, but it's buggy so I made my own.
    '''
    str__ = i[1]
    result = ''
    cap_next_letter = True
    for c in str__:
        if cap_next_letter and c.isalpha():
            # use title(), not upper() -- for edge cases like ǅ
            result += c.title()
            cap_next_letter = False
        else:
            result += c.lower()
        if c.isspace():
            cap_next_letter = True
    return result

def join(i: list):
    '''
    (join (list "Hello" "World" 123)<list> ""[sep]) 
    
    Combine the contents of `list` into one string, with each item 
    separated by `sep` (or nothing if no separator given, as in the example).
    '''
    strList : list = [str(j) for j in i[1]]
    if len(i) == 2:
        i.append('')
    sep : str = i[2]
    return sep.join(strList)

def split(i: list):
    '''
    (split,"Hello World"<str>,""[sep],-1[maxSplit]) 
    
    Split the string `str` into a list of substrings. By default (or if `sep` 
    is an empty string), the interpreter will split at every sequence of 
    whitespace; otherwise, it will split every time the substring `sep` is 
    reached. `maxSplit` is the maximum number of splits that will be done 
    (i.e. the length of the resulting list will always be ≤ (maxSplit+1)); 
    the default value -1 means no limit.
    '''
    string : str = i[1]
    if len(i) == 2:
        i.append('')
    sep : str = i[2]
    if len(i) == 3:
        i.append(-1)
    maxSplit : int = i[3]
    return string.split(sep, maxSplit)

# END STRING SUBCOMMANDS

# TYPE SUBCOMMANDS

def int_(i: list):
    '''
    (int,1.5)
    
    Convert a value to integer format, if possible.

    — OR —

    (int,"0f"<value>,16[base])
    
    Only for string values: you can specify the base the string is in 
    (from 2-36), and it'll convert it correctly.
    '''

    try:
        # Special case: convert string in different base
        if len(i) >= 2 and type(i[1]) == str:
            return int(i[1], i[2])
        else:
            return int(i[1])
    except Exception:
        log_warning(f'{i[0]}: couldn’t convert {i[1]} to int type')
        return 0

def float_(i: list):
    '''
    (float,1)

    Convert a value to floating-point format, if possible.
    '''

    try:
        return float(i[1])
    except Exception:
        log_warning(f'{i[0]}: couldn’t convert {i[1]} to float type')
        return 0.0

def str_(i: list): 
    '''
    (str,1)

    — OR —

    (str,"Hello"<x1>,"World"[x2],1[x3],...)

    Convert the argument(s) to a string. If more than one argument is passed 
    in, they will each be converted to strings, then concatenated together.
    The result of the example will be "HelloWorld1" (with no spaces in between 
    because neither string had a space in it). (aliases: string, str+, str_add)

    This used to be two separate commands, str/string (for 1 arg) and
    str_add/str+ (for 2+ args); all aliases are kept for compatibility.
    '''

    if len(i) == 2: # If 1 argument
        try:
            return str(i[1])
        except Exception:
            log_warning(f'{i[0]}: couldn’t convert {i[1]} to str type')
            return ''
    # Everything below this line was previously part of str+
    elif len(i) == 3: # If 2 arguments
        try:
            return str(i[1]) + str(i[2])
        except Exception:
            log_warning(f'{i[0]}: couldn’t concatenate {i[1]} and {i[2]}')
            return ''
    # But if there are 3 or more arguments (x1, x2, x3)...
    try:
        return str(i[1]) + str_([i[0]] + i[2:])
    except Exception:
        log_warning(f'{i[0]}: couldn’t concatenate {i[1]} and {i[2]}')
        return ''

def bool_(i: list):
    '''
    (bool,1)

    Convert a value to boolean format, if possible. (alias: boolean)
    '''

    try:
        return bool(i[1])
    except Exception:
        log_warning(f'{i[0]}: couldn’t convert {i[1]} to bool type')
        return False

def hex_(i: list):
    '''
    (hex 17<x> #_t[prefix])
    
    Return hexadecimal string representation of x. `prefix` determines whether 
    to include the "0x" prefix at the start of the string. You can also set 
    `prefix` to a string to add a custom prefix. 
    Ex: (hex 17) => "0x11", (hex 255 "#") => "#0000ff"
    '''

    x = i[1]
    if len(i) == 2:
        prefix = True
    hex_str = hex(x)

    if type(i[2]) == str:
        prefix = i[2]
        return prefix+hex_str
    else:
        prefix = bool(i[2])
        return ('0x' if prefix else '')+hex_str

def bin_(i: list):
    '''
    (bin 7<x> #_t[prefix])
    
    Return binary string representation of x. `prefix` determines whether to 
    include the "0b" prefix at the start of the string. You can also set 
    `prefix` to a string to add a custom prefix. 
    Ex: (bin 7) => "0b111"
    '''

    x = i[1]
    if len(i) == 2:
        prefix = True
    bin_str = bin(x)

    if type(i[2]) == str:
        prefix = i[2]
        return prefix+bin_str
    else:
        prefix = bool(i[2])
        return ('0b' if prefix else '')+bin_str

def type_(i: list):
    '''
    (type,$x<data>) 

    Returns the data type of the given variable (or literal), as a string. 
    Possible types: "int", "float", "str", "bool", "list", "color", "null"
    '''

    t = type(i[1])

    if i[1] is None:
        return 'null'
    elif t == str:
        return 'str'
    elif t == int:
        return 'int'
    elif t == float:
        return 'float'
    elif t == bool:
        return 'bool'
    elif t == list:
        return 'list'
    elif t == Color:
        return 'color'
    else:
        # Failsafe if we somehow get a different type
        return t.__name__.lower()

# END TYPE SUBCOMMANDS

# COLOR TYPE SUBCOMMANDS

def color_(i: list):
    '''
    (color,"#ff0000"<hex>)

    Define a color based on a *string* consisting of a "#" followed by 6 or 8 
    hexademical numbers. Hex codes can be in the format #RRGGBB or #AARRGGBB 
    (e.g. "#80ffff00" will be a 50% transparent yellow).

    — OR —

    (color,"red"<name>)

    Define a color based on list of 24 named colors.

    — OR —

    (color,n00) 
    
    Define a color from the NES palette (Nestopia's 15° Canonical palette to
    be exact). Colors are numbered in hexadecimal from n00 to n3f.
    '''

    raw_color = str(i[1]).lower()

    # Hex color
    if raw_color.startswith('#'):
        rgba = hex_to_rgb(raw_color)
        return Color(rgba[0], rgba[1], rgba[2], rgba[3])
    # Named color
    else:
        if raw_color in colors:
            rgba = hex_to_rgb(colors[raw_color])
            return Color(rgba[0], rgba[1], rgba[2], rgba[3])
        else:
            log_warning(f'{i[0]}: unknown color name {raw_color}')

def rgb(i: list):
    '''
    (rgba,0<red: 0 to 255>,0<green: 0 to 255>,0<blue: 0 to 255>,
        255[alpha: 0 to 255])

    — OR —

    (rgba,(list,255,128,0[,255])<list>)

    Returns a Color based on red, green, blue, and (optional) alpha values. 
    (alias: rgb)
    '''

    # Special case: first (and presumably only) argument has `list` type
    if type(i[1]) == list:
        if len(i[1]) == 3: # no alpha included
            return Color(i[1][0], i[1][1], i[1][2], 255)
        elif len(i[1]) >= 4:
            return Color(i[1][0], i[1][1], i[1][2], i[1][3])
        else:
            log_warning(f'{i[0]}: command requires 3 arguments or a list with \
3 or more items')
            return

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires 3 arguments or a list with 3 or \
more items')
        return

    r : int = i[1]
    g : int = i[2]
    b : int = i[3]

    if len(i) == 4:
        i.append(255) # If no alpha given, default to 255 (fully opaque)
    a : int = i[4]

    return Color(r, g, b, a)

def hsl(i: list):
    '''
    (hsla,0<hue: 0 to 359>,100<saturation: 0 to 100>,50<lightness: 0 to 100>,
        255[alpha: 0 to 255]) 

    — OR —

    (hsla,(list,255,128,0[,255])<list>)

    Define a color based on the hue/saturation/lightness (or luminosity) model, 
    plus optional alpha. (Alias: hsl)
    '''

    # Special case: first (and presumably only) argument has `list` type
    if type(i[1]) == list:
        if len(i[1]) == 3: # no alpha included
            rgba = hsla_to_rgba([i[1][0], i[1][1], i[1][2], 255])
            return Color(rgba[0], rgba[1], rgba[2], rgba[3])
        elif len(i[1]) >= 4:
            rgba = hsla_to_rgba([i[1][0], i[1][1], i[1][2], i[1][3]])
            return Color(rgba[0], rgba[1], rgba[2], rgba[3])
        else:
            log_warning(f'{i[0]}: command requires 3 arguments or a list with \
3 or more items')
            return

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires 3 arguments or a list with 3 or \
more items')
        return

    h : int = i[1]
    s : int = i[2]
    l : int = i[3]

    if len(i) == 4:
        i.append(255) # If no alpha given, default to 255 (fully opaque)
    a : int = i[4]

    rgba = hsla_to_rgba([h,s,l,a])
    return Color(rgba[0], rgba[1], rgba[2], rgba[3])

def getpixel(i: list, base_image: PIL.Image.Image):
    '''
    getpixel,new[image],0<x>,0<y>
    
    Returns Color object of the color at the given (x,y) position 
    on the given image.
    '''

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}')
    else:
        i.insert(1, 'new')
        # Default to `new` if no image specified.
        # In most other commands, we just insert a blank, but here we need
        # the image name to be right because we pass it to `getrgba` later

    x : int = i[2]
    y : int = i[3]

    rgba_list = getrgba([i[0], i[1], x, y], base_image)
    return Color(rgba_list[0], rgba_list[1], rgba_list[2], 
                 rgba_list[3]) # create color type from that RGBA list

def pal_get(i: list, base_image: PIL.Image.Image):
    '''
    pal.get 0[x] 0[y] 0[width] 0[height]
    
    Return a list of all colors in the area/image. Follows filter rules for 
    omitted arguments.
    '''
    # For filters, if no x or y specified, apply filter to whole image
    if len(i) <= 2: # number on the right should be equal to the index of y
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
    # Set maxcolors to total num. of pixels in area so it's impossible for it
    # to return None
    all_colors : List[Tuple[int,ColorArray]] \
            = region.getcolors(maxcolors=width*height) # type:ignore
    rgba_list = [i[1] for i in all_colors]
    return [Color(rgba_list[i][0], rgba_list[i][1], rgba_list[i][2], 
                  rgba_list[i][3]) for i in range(len(rgba_list))]

# END COLOR TYPE SUBCOMMANDS

# COLOR INFO SUBCOMMANDS

def empty(i: list, open_image: PIL.Image.Image):
    '''
    (empty old[image] 0<x> 0<y> 16[width] 16[height]) 

    — OR —

    (empty (rgb 255 128 0)<color>)
    
    True if the area on the given image (by default "old") is completely empty 
    (every pixel is transparent), False otherwise.

    Note that unlike the Color Info Subcommands, this defaults to the old 
    image, not the new one.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].alpha == 0

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: Command requires either a value of type “color” \
or x & y values')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            open_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name “{i[1]}”')
    else:
        i.insert(1, '')

    x : int = i[2]
    y : int = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 16×16.
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [16, 16]
    width : int = i[4]
    if len(i) == 5:
        i += [width]
    height : int = i[5]

    region = open_image.crop((x, y, x+width, y+height))

    # Loop thru each pixel in region, making sure it's transparent
    for loop_x in range(width):
        for loop_y in range(height):
            rgba = safe_pil_getpixel(i[0], region, (loop_x, loop_y))
            # If a single pixel isn't transparent, return False
            if rgba[3] != 0:
                return False
    # If we make it here, it's empty, return True
    return True

def getrgba(i: list, base_image: PIL.Image.Image):
    '''
    (getrgba,new[image],0<x>,0<y>,1[width],1[height])

    — OR —

    (getrgba,(rgb,255,128,0)<color>)
    
    Return a list consisting of the [red, green, blue, alpha] values of a
    Color object, pixel, or area of pixels.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return [i[1].red, i[1].green, i[1].blue, i[1].alpha]

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return [0,0,0,0]

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}')
            return [0,0,0,0]
    else:
        i.insert(1, '')

    x : int = i[2]
    y : int = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width : int = i[4]
    if len(i) == 5:
        i += [width]
    height : int = i[5]

    if width <= 1 and height <= 1:
        rgba = safe_pil_getpixel(i[0], base_image, (x, y))
        return list(rgba)
    else:
        avgR = 0
        avgG = 0
        avgB = 0
        avgA = 0

        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
                avgR += rgba[0]
                avgG += rgba[1]
                avgB += rgba[2]
                avgA += rgba[3]

        avgR = int(avgR / (width * height))
        avgG = int(avgG / (width * height))
        avgB = int(avgB / (width * height))
        avgA = int(avgA / (width * height))

        return [avgR, avgG, avgB, avgA]

def gethsla(i: list, base_image: PIL.Image.Image):
    '''
    (gethsla,new[image],0<x>,0<y>)

    — OR —

    (gethsla,(rgb,255,128,0)<color>)
    
    Return a list consisting of the [hue, saturation, lightness, alpha] values 
    of a Color object or pixel. Does NOT support averaging an area of pixels
    because that concept simply doesn't make sense given that hue is a circle.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return [i[1].hue, i[1].saturation, i[1].lightness, i[1].alpha]

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}')
    else:
        i.insert(1, '')

    x : int = i[2]
    y : int = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width : int = i[4]
    if len(i) == 5:
        i += [width]
    height : int = i[5]

    if width <= 1 and height <= 1:
        rgba : ColorArray = safe_pil_getpixel(i[0], base_image, (x, y))
        return rgba_to_hsla(rgba)
    else:
        log_warning('gethsla: Take a minute to think about why the concept of \
“average hue” doesn’t make sense. (Hint: Hue is a circle; what’s the average \
of 0 + 359?')
        return None

def red_(i: list, base_image: PIL.Image.Image):
    '''
    (red,old[image],0<x>,0<y>,1[width],1[height])

    Return the red value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average red value 
    over the given rectangle.
    If a Color object is given, return its "red" attribute.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].red

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}. \
Defaulting to “old”.')
    else:
        i.insert(1, '')

    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    if width <= 1 and height <= 1:
        rgba = safe_pil_getpixel(i[0], base_image, (x, y))
        return rgba[0]
    else:
        avg = 0 # Average RED value of region

        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
                avg += rgba[0]

        avg = int(avg / (width * height))
        return avg

def green_(i: list, base_image: PIL.Image.Image):
    '''
    (green,old[image],0<x>,0<y>,1[width],1[height])

    Return the green value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average green value 
    over the given rectangle.
    If a Color object is given, return its "green" attribute.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].green

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}. \
Defaulting to “old”.')
    else:
        i.insert(1, '')

    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    if width <= 1 and height <= 1:
        rgba = safe_pil_getpixel(i[0], base_image, (x, y))
        return rgba[1]
    else:
        avg = 0 # Average GREEN value of region

        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
                avg += rgba[1]

        avg = int(avg / (width * height))
        return avg

def blue_(i: list, base_image: PIL.Image.Image):
    '''
    (blue,old[image],0<x>,0<y>,1[width],1[height])

    Return the blue value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average blue value 
    over the given rectangle.
    If a Color object is given, return its "blue" attribute.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].blue

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}. \
Defaulting to “old”.')
    else:
        i.insert(1, '')

    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    if width <= 1 and height <= 1:
        rgba = safe_pil_getpixel(i[0], base_image, (x, y))
        return rgba[2]
    
    # else
    avg = 0 # Average BLUE value of region

    for loop_x in range(x, x+width):
        for loop_y in range(y, y+height):
            rgba = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
            avg += rgba[2]

    avg = int(avg / (width * height))
    return avg

def alpha_(i: list, base_image: PIL.Image.Image):
    '''
    (alpha,old[image],0<x>,0<y>,1[width],1[height])

    Return the alpha value (from 0 to 255) of a single pixel. 
    If width and height are given, take the average alpha value 
    over the given rectangle.
    If a Color object is given, return its "alpha" attribute.

    This is for GETTING the alpha/opacity value (from 0 to 255). 
    For applying a transparency filter, use "opacity".
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].alpha

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}. \
Defaulting to “old”.')
    else:
        i.insert(1, '')

    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    if width <= 1 and height <= 1:
        rgba = safe_pil_getpixel(i[0], base_image, (x, y))
        return rgba[3]
    else:
        avg = 0 # Average ALPHA value of region

        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                rgba = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
                avg += rgba[3]

        avg = int(avg / (width * height))
        return avg


def hue(i: list, base_image: PIL.Image.Image):
    '''
    (hue,old[image],0<x>,0<y>,1[width],1[height])

    Return the hue value (from 0 to 359) of a single pixel. 
    If width and height are given, take the average value 
    over the given rectangle.
    If a Color object is given, return its "hue" attribute.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].hue

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}. \
Defaulting to “old”.')
    else:
        i.insert(1, '')

    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    if width <= 1 and height <= 1:
        hsla = rgba_to_hsla(safe_pil_getpixel(i[0], base_image, (x, y)))
        return hsla[0]
    else:
        avg = 0 # Average HUE value of region

        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                hsla = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
                avg += hsla[0]

        avg = int(avg / (width * height))
        return avg


def saturation(i: list, base_image: PIL.Image.Image):
    '''
    (saturation,old[image],0<x>,0<y>,1[width],1[height])

    Return the HSL saturation value (from 0 to 100) of a single pixel. 
    If width and height are given, take the average value 
    over the given rectangle.
    If a Color object is given, return its "saturation" attribute.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].saturation

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}. \
Defaulting to “old”.')
    else:
        i.insert(1, '')

    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    if width <= 1 and height <= 1:
        hsla = rgba_to_hsla(safe_pil_getpixel(i[0], base_image, (x, y)))
        return hsla[1]
    else:
        avg = 0 # Average SATURATION value of region

        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                hsla = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
                avg += hsla[1]

        avg = int(avg / (width * height))
        return avg


def lightness(i: list, base_image: PIL.Image.Image):
    '''
    (lightness,old[image],0<x>,0<y>,1[width],1[height])

    Return the HSL lightness (luminosity) value (from 0 to 100) 
    of a single pixel. If width and height are given, 
    take the average value over the given rectangle.
    If a Color object is given, return its "lightness" attribute.
    '''

    # Special case: first (and presumably only) argument has color type
    if type(i[1]) == Color:
        return i[1].lightness

    # If not special case, check arg count *again*
    if len(i) <= 2:
        log_warning(f'{i[0]}: command requires either a value of type “color” \
or x & y values.')
        return

    # If image name is given at arg1, set base_image to that. 
    # Otherwise, keep base_image as is and insert an empty string so the
    # remaining arguments are in a consistent position.
    if type(i[1]) == str:
        if i[1] in images:
            base_image = images[i[1]]
        else:
            log_warning(f'{i[0]}: Unrecognized image name {i[1]}. \
Defaulting to “old”.')
    else:
        i.insert(1, '')

    x = i[2]
    y = i[3]

    # If width/height specified, use those values.
    # If neither is specified, use 1×1 (single pixel).
    # If only width is specified, use that value for height too.
    if len(i) == 4:
        i += [1, 1]
    width = i[4]
    if len(i) == 5:
        i += [width]
    height = i[5]

    if width <= 1 and height <= 1:
        hsla = rgba_to_hsla(safe_pil_getpixel(i[0], base_image, (x, y)))
        return hsla[2]
    else:
        avg = 0 # Average LIGHTNESS value of region

        for loop_x in range(x, x+width):
            for loop_y in range(y, y+height):
                hsla = safe_pil_getpixel(i[0], base_image, (loop_x, loop_y))
                avg += hsla[2]

        avg = int(avg / (width * height))
        return avg

# END COLOR INFO SUBCOMMANDS

# IMAGE INFO SUBCOMMANDS

def width_(i: list) -> int:
    '''
    Return the width of the image with the specified name.
    '''
    img_name = i[1]
    return images[img_name].width

def height_(i: list) -> int:
    '''
    Return the height of the image with the specified name.
    '''
    img_name = i[1]
    return images[img_name].height

# END IMAGE INFO SUBCOMMANDS

###########################################################################
#### LANGUAGE HELPER FUNCTIONS ############################################
###########################################################################
    
def subst_all_vars(cmd: list):
    '''
    Substitute all variable names with their values, in a given command
    or subcommand. If a variable is not defined, log a warning and treat its
    value as None.
    '''

    for arg_n in range(1, len(cmd)):
        cmd[arg_n] = subst_var(cmd[arg_n], cmd[0])

def subst_var(ref:Any, cmd_name='', mutable=False) -> Any:
    '''
    Given a variable reference, return its value. If there is no 
    variable with that name, log a warning and treat its value as `None`.

    The `cmd` argument is only used for error messages if the variable
    is not defined.

    By default, this function returns a COPY of lists, which is always the
    intended behavior in `$var` calls in scripts. 

    However, certain list commands need an editable version of the list,
    so you can set the `mutable` argument to `True` to get that.
    In fact, this function will silently refuse to substitute SetVar objects
    unless you do that.
    '''
    if type(ref) == Var or (type(ref) == SetVar and mutable):
        var_name : str = ref.name
        if var_check(ref, cmd_name, exists=True):
            if (isinstance(variables[var_name], list) and not mutable) \
                    or isinstance(variables[var_name], Color):
                # Deep-copy reference types (e.g. lists, colors).
                # This may cause a performance hit but it fixes a lot
                # of bugs because the whole lists-are-references thing
                # goes against common sense sometimes.
                return deepcopy(variables[var_name])
            else:
                return variables[var_name]
        else:
            log_warning(f'{cmd_name}: variable “{var_name}” is not defined')
            # if variable not defined, make default value be None
            return None
    # if it's not a variable reference, just return the value passed in
    return ref

def var_check(v: Union[Var, SetVar], cmd_name='Variable error', *, 
              exists:Optional[bool]=None, internal=False):
    '''
    Variable name validity check for all commands that set or change variables.
    
    Takes in a Var or SetVar. For Var, "valid" = "can access the variable".
    For SetVar, "valid" = "can access or set", unless internal is True,
    in which case "valid" = "can access".

    The parameter "exists" determines how we should check for the variable's
    existence. If True, the variable must already exist (ex.: change, list.add,
    $var). If False, the variable must NOT already exist (ex.: const).
    If None (ex.: set), we don't care either way.

    Also takes in a command name, but that's just for reporting errors.

    Return True if variable name is valid, and False if it's not.
    '''

    read_write = None
    if type(v) is Var:
        read_write = False
        var_name = v.name
    elif type(v) is SetVar:
        read_write = True
        var_name = v.name
    elif type(v) is str:
        var_name = v
    else:
        # If someone tries to set a number or something
        log_warning(f'{cmd_name}: Invalid variable {v}. \
Variable names must start with a dollar sign.')
        return None

    # Now that we have var_name as a string...
    if not var_name.startswith('$'):
        log_warning(f'{cmd_name}: Invalid variable name {var_name}. \
Variable names must start with a dollar sign.')
        return False

    # Variable names must be at least 1 character long (2 counting $)
    if len(var_name) < 2:
        log_warning(f'{cmd_name}: Invalid variable name {var_name}. \
Variable names must be at least 1 character long.')
        return False
    
    # Cannot set constants (not even internally)
    if read_write and var_name in variables['$__constants']:
        log_warning(f'{cmd_name}: Cannot set {var_name}, as it has \
already been declared as a constant')
        return False

    # Cannot set system variables (which start with _) unless internal == True
    # Unless the variable name is ONLY the underscore
    if var_name[1] == '_' and len(var_name) > 2 \
            and read_write and not internal:
        log_warning(f'{cmd_name}: Cannot set variable names starting with \
underscores, like {var_name}, as these are reserved for the converter \
(except for “$_”).')
        return False

    # Block access of private variables (start with __).
    # foreach may insert private variables later,
    # but we want to block any that were typed into the script
    if var_name[1:3] == '__' and not internal:
        log_warning(f'{cmd_name}: variables starting with “$__” \
are private and cannot be accessed by scripts.')

    # Variable names can only contain: a-z, A-Z, 0-9, _
    for char in var_name[1:]: # [1:] to ignore $ at start
        if not char.isalnum() and char != '_':
            log_warning(f'{cmd_name}: Invalid variable name {var_name}. \
Variable names can only contain ASCII letters, numbers, and underscores.')
            return False
        
    # Existence check as appropriate
    if exists is True:
        return var_name in variables
    elif exists is False:
        return var_name not in variables
    # else, if it's None, and we made it here, the name is valid
    return True

def arg_check(cmd: list, is_subcmd: bool):
    '''Check that a (sub)command has the right number of arguments.
    If it doesn't, log a warning and neutralize the command.'''

    # This database no longer includes aliases! Those are listed separately.
    v7_cmd_min_args = {
        # blanks, headers, end, noop, and label are excluded from this database
        'exit': 0,
        'skip': 0,
        'error': 0,
        'warning': 1,
        'assert': 1,
        # 'use': 1, # unnecessary in v7.2

        'goto': 1,
        'gosub': 1,
        'retsub': 0,
        'if1': 1,
        'if': 1,
        'elseif': 1,
        'else': 0,
        'while': 1,
        'next': 0,
        'break': 0,
        'for': 2, # see also special case in initialization
        'foreach': 2,

        'set': 2,
        'const': 2,
        'change': 2,

        'iadd': 2,
        'isub': 2,
        'imul': 2,
        'itruediv': 2,
        'ifloordiv': 2,
        'imod': 2,
        'ipow': 2,
        'inc': 1,
        'dec': 1,

        'copy': 0,
        'copyalt': 0, # this just calls copy now
        'copyfrom': 1,
        'default': 0,
        'defaultfrom': 1,
        'clear': 0,
        'duplicate': 4,
        'move': 4,
        'swap': 4,
        'over': 0,
        'under': 0,

        'tile': 8,
        'copyscale': 8,

        'resize': 1,
        'crop': 4,
        'scale': 2,
        'rotate': 1,
        'flip': 1,

        'grayscale': 0,
        'invert': 0,
        'rgbfilter': 3,
        'opacity': 1,
        'filter.hue': 1,
        'filter.saturation': 1,
        'filter.lightness': 1,
        'filter.fill': 3, # deprecated in v7.2
        'contrast': 1,
        'colorize': 3,
        'sepia': 0,
        'threshold': 1,
        'hslfilter': 3,
        'selcolor': 4,
        'twocolor': 3,
        'recolor': 2,

        'list.add': 2,
        'list.addall': 2,
        'list.clear': 1,
        'list.insert': 3,
        'list.remove': 2,
        'list.replace': 3,
        'list.swap': 3,

        'setpixel': 3,
        'draw.rect': 4,
        'draw.ellipse': 4,
        'draw.line': 4,
        'draw.fillcolor': 1,
        'draw.linecolor': 1,
        'draw.alphablend': 1,
    }

    v7_subcmd_min_args = {
        'eq': 2,
        'ne': 2,
        'lt': 2,
        'gt': 2,
        'le': 2,
        'ge': 2,
        'cmp': 2,

        'or': 2,
        'and': 2,
        'not': 1,
        'xor': 2,

        'add': 2,
        'sub': 1, # different from other math operators because of unary syntax
        'mul': 2,
        'truediv': 2,
        'floordiv': 2,
        'mod': 2,
        'pow': 2,

        'log': 1,
        'abs': 1,
        'floor': 1,
        'ceil': 1,
        'min': 1,
        'max': 1,
        'round': 1,

        'len': 1,
        'get': 2,
        'slice': 3,
        'in': 2,
        'find': 2,
        'sum': 1,
        'count': 2,
        'sort': 1,
        'reverse': 1,

        'str_mul': 2, # DEPRECATED since 7.2
        'upper': 1,
        'lower': 1,
        'titlecase': 1,
        'sentencecase': 1,
        'startswith': 2,
        'endswith': 2,
        'join': 1,
        'split': 1,

        'list': 0,
        'range': 1,

        'int': 1,
        'float': 1,
        'str': 1,
        'bool': 1,
        'hex': 1,
        'bin': 1,
        'type': 1,

        'color': 1,
        'rgba': 3,
        'hsla': 3,
        'getpixel': 2,
        'pal.get': 0,

        'empty': 2,
        'getrgba': 1,
        'gethsla': 1,

        'red': 1,
        'green': 1,
        'blue': 1,

        'alpha': 1,

        'hue': 1,
        'saturation': 1,
        'lightness': 1,

        'width': 1,
        'height': 1,
    }

    if is_subcmd and cmd[0] in v7_subcmd_min_args:
        min_args = v7_subcmd_min_args[cmd[0]]
    elif not is_subcmd and cmd[0] in v7_cmd_min_args:
        min_args = v7_cmd_min_args[cmd[0]]
    else:
        # If we don't have data for a command, assume it's okay
        return

    # Same check for commands and subcommands
    if len(cmd) <= min_args:
        log_warning('%s: command requires at least \
%d arguments' % (cmd[0], min_args))
        if is_subcmd:
            cmd = ['null'] + cmd
        elif cmd[0] in block_starts:
            cmd = ['if', 0] + cmd
        else:
            cmd = ['noop'] + cmd
        return
    # If we make it down here, the command passed the check.

def py_method(i: list, method: str):
    '''
    Higher-order function that handles any command that's just a wrapper
    around some Python method, especially a method to mutate objects in place.
    
    Note that the `method` argument must be a string. Only include the name
    of the method, not the object. The method will be called on i[1]. 
    If i[2] and i[3] exist, they will be passed as arguments to the method.
    (Examples: "append", "__iadd__" [i.e. +=])

    Unlike commands, i must have the exact number of arguments you want to use
    (no more, no less), because Python doesn't like extra arguments.

    Returns whatever the Python method (that was passed in) returns.
    '''
    # This function gets its own arg check because it's not a proper command
    if len(i) <= 1: # empty command, or command with 0 arguments
        log_warning(f'{i[0]}: Need at least 1 argument (a variable) \
to call a method on it')
        return
    
    # else
    varRef = i[1]
    # Normally a SetVar but not always (`count` cmd is an exception)
    if isinstance(varRef, SetVar) and not var_check(varRef, i[0], exists=True):
        # var_check will generate its own warning if it fails, so no need
        # for another one here
        return
    varData : Any = subst_var(varRef, i[0], mutable=True)

    if len(i) == 2: # 1 arguments: just the variable
        return getattr(varData, method)()
    elif len(i) == 3: # 2 arguments: the variable + 1 extra arg
        return getattr(varData, method)(i[2])
    elif len(i) == 4: # 3 arguments: the variable + 2 extra args
        return getattr(varData, method)(i[2], i[3])

def hex_to_rgb(hex_str: str) -> Tuple[int, int, int, int]:
    '''
    Convert a hex color to an RGBA tuple.
    '''
    if len(hex_str) == 7: # hash + 6 digits = RGB
        try:
            r = int(hex_str[1:3], 16)
            g = int(hex_str[3:5], 16)
            b = int(hex_str[5:7], 16)
            a = 0xff
            return (r,g,b,a)
        except ValueError:
            log_warning('color: invalid hex color')
            return (0,0,0,0)
    elif len(hex_str) == 9: # hash + 8 digits = RGBA
        try:
            r = int(hex_str[1:3], 16)
            g = int(hex_str[3:5], 16)
            b = int(hex_str[5:7], 16)
            a = int(hex_str[7:9], 16)
            return (r,g,b,a)
        except ValueError:
            log_warning('color: invalid hex color')
            return (0,0,0,0)
    else:
        log_warning('color: invalid hex color (must be “#” followed by \
6 or 8 digits')
        return (0,0,0,0)

def rgba_to_hsla(color: ColorArray) -> List[Num]:
    """Convert RGBA to HSLA for use in filters.
    Takes in a list with 4 items [r,g,b,a]"""
    raw = colorsys.rgb_to_hls(color[0]/255, color[1]/255, color[2]/255)
    return [raw[0]*360, raw[2]*100, raw[1]*100, int(color[3])]

def hsla_to_rgba(color: ColorArray) -> List[int]:
    """Convert HSLA to RGBA for use in filters.
    Takes in a list with 4 items [h,s,l,a]"""
    # Note that colorsys uses the unusual HLS, not HSL
    raw = colorsys.hls_to_rgb(color[0]/360, color[2]/100, color[1]/100)
    return [int(raw[0]*255), int(raw[1]*255), int(raw[2]*255), int(color[3])]

# Normalize HSLA values in place.
def format_hsla(color: List[Num]):
    # Convert everything to int
    color[0] = int(color[0])
    color[1] = int(color[1])
    color[2] = int(color[2])
    if len(color) > 3:
        color[3] = int(color[3])

    # Hue must be from 0 to 360
    color[0] %= 360

    # Saturation must be from 0 to 100
    color[1] = clip(color[1], 0, 100)

    # Lightness must be from 0 to 100
    color[2] = clip(color[2], 0, 100)

    # And as always, we don’t touch alpha. In fact, the user doesn’t even need
    # to pass in an alpha — the function will still run.
    return color

def safe_pil_getpixel(cmd_name:str, img:PIL.Image.Image, 
                      xy_tuple:Tuple[int,int]) -> ColorArray:
    """
    Basically calls PIL's getpixel and then does some type-checking, before
    returning a guaranteed RGBA tuple.

    Takes in:
    * A command name, just for error checking
    * An image or region of an image
    * A x/y coordinate tuple
    """
    raw_pixel = img.getpixel(xy_tuple)
    if isinstance(raw_pixel, tuple) and len(raw_pixel) == 4:
        return raw_pixel
    else:
        log_warning(f'{cmd_name[0]}: Image is corrupted')
        return (0,0,0,0) # transparent

def set_ln(index:int):
    set_(['set', '$_ln', index], internal=True)
    set_(['set', '$_linenumber', index], internal=True)

###########################################################################
#### GUI FUNCTIONS ########################################################
###########################################################################

# Clear the main content frame -- remove text, buttons, etc.
def cls():
    for child in main_frame.winfo_children():
        child.place_forget()

def button_dialog(title:str, message:Union[str, List[str]],
                  buttons:Tuple[str, ...]=('Cancel', 'Okay'), *, 
                  icon:Optional[str]=None):
    '''
    Displays a dialog box with one or more buttons to the user. Holds until the
    user clicks a button. Returns the name of the button clicked.

    icon is one of: info, question, warning, error, done, bomb
    '''

    cls()

    button_clicked = None
    # Nested function that all button event bindings point to
    # Sets the button_clicked variable one layer up so the function knows
    # it can return
    def button_event(index:int):
        nonlocal button_clicked
        button_clicked = buttons[index]

    dialog_icon = None
    if icon in icons:
        dialog_icon = Label(main_frame, image=icons[icon], bg=colors['UI_BG'])
        dialog_icon.place(x=470, y=10, anchor=NE)

    next_y = 0
    if title:
        dialog_title = Label(main_frame, text=str(title), font=f_heading, 
                justify='left', bg=colors['UI_BG'])
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
                wraplength=470, bg=colors['UI_BG']))

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
                highlightbackground=colors['UI_BG'],
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

def bool_dialog(title:str, message:Union[str, List[str]],
                  button1='Cancel', button2='Okay', *, 
                  icon:Optional[str]=None):
    '''
    Simplified version of button_dialog() that only allows 2 buttons and returns
    a boolean value. If the user clicks the right/Okay button, return True.
    Otherwise, if the user clicks the left/Cancel button, return False.
    '''
    button_name = button_dialog(title, message, (button1, button2), icon=icon)
    if button_name == button2:
        return True
    else:
        return False

def yn_dialog(title:str, message:Union[str, List[str]],
                  button1='Yes', button2='No', *, icon:Optional[str]=None):
    '''
    yn_dialog is like bool_dialog but the buttons' return values are reversed.
    The left/Yes button returns True, and the right/No button returns false.
    '''
    button_name = button_dialog(title, message, (button1, button2), icon=icon)
    if button_name == button1:
        return True
    else:
        return False

def simple_dialog(title:str, message:Union[str, List[str]], 
                  button='Okay', *, icon:Optional[str]=None):
    '''
    Single-button dialog. Returns None.
    '''
    button_dialog(title, message, (button,), icon=icon)
    
def the_W():
    simple_dialog('There’s a new bird among us', 
                  'We will only be adding the W.',
                  'Clear cache', icon='info')
    menu()

def log_warning(warn:str):
    ln = variables['$_linenumber']
    warn_with_ln = f'[Line {ln}] {warn}'
    if warn_with_ln not in warnings:
        warnings.append(warn_with_ln)

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

    main_frame.update_idletasks()

def menu_p2():
    cls()

    menu_heading_adv.place(x=240, y=0, anchor=N)

    next_y = 0
    for i in (menu_btns_p2):
        i.place(x=240, y=40+next_y, anchor=N)
        next_y += 30

    main_frame.update_idletasks()

# Update the user on the progress of a large conversion task.
def update_subhead(subhead):
    rounded_pct = round(current_num/(stop_num-start_num)*100, 1)

    subhead = Label(main_frame, 
        text=f'Now converting: file {current_num} ({rounded_pct}%)', 
        justify='left', bg=colors['UI_BG'])
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
'You can download the images at any time by going to Advanced/Custom → \
Update Game Images from the main menu.'], icon='warning')
    # If no installation needed, proceed silently

    menu()

def menu():
    #### STEP 1: SELECT SCRIPT ####
    cls()

    # PAGE 1

    menu_btn_skin_l_l7.bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/skin_L_to_L7.s.txt'))
    menu_btn_skin_d_l7.bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/skin_Dx32_to_L7.s.txt'))

    menu_btn_page_next.bind('<ButtonRelease-1>', 
            lambda _: menu_p2())

    menu_btn_exit.bind('<ButtonRelease-1>', 
            lambda _: exit_app())

    # PAGE 2

    menu_btn_skin_p_l7.bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/skin_P32_to_L7.s.txt'))
    menu_btn_skin_d_l.bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/skin_Dx32_to_L.txt'))
    menu_btn_skin_r_l.bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/skin_R_to_L.txt'))
    menu_btn_map_l_ln.bind('<ButtonRelease-1>', 
            lambda _: script_button('scripts/map_new.txt'))

    menu_btn_custom.bind('<ButtonRelease-1>', 
            lambda _: script_button(''))
    menu_btn_submit.bind('<ButtonRelease-1>', 
            lambda _: the_W())
    menu_btn_multi.bind('<ButtonRelease-1>', 
            lambda _: new_multi_event())
    menu_btn_assets.bind('<ButtonRelease-1>', 
            lambda _: install_assets())

    menu_btn_page_prev.bind('<ButtonRelease-1>', 
            lambda _: menu_p1())

    menu_p1()

    window.update()

    window.mainloop()

# EVENT HANDLER for most menu buttons
def script_button(script_file:str=''):
    open_result = open_script(script_file)
    if open_result:
        path_result = get_paths()
        if path_result:
            run_result = run_script()

            # If no files converted (legacy multi only)
            while legacy_multi and run_result < 1: 
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

# SPECIAL EVENT HANDLER for new batch conversion
def new_multi_event():
    confirm1 = bool_dialog('Batch Conversion - Step 1: Select Script', 
['Want to convert an entire folder of images? You’ve come to the right place!',
 'First, you’ll need to select the script file you want to run.'], 
            'Cancel', 'Continue', icon='info')
    if confirm1:
        open_result = open_script()
        if open_result:
            confirm2 = bool_dialog(\
'Batch Conversion - Step 2: Select Folder',
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

def alias(cmd: list, is_subcmd: bool):
    ''' 
    Takes in a command (in list form). If the command name is in the alias
    database, change it to the standard name (e.g. else_if to elseif, 
    ceiling to ceil, < to lt)

    Changes the command in place and returns nothing.

    This only covers pure command aliases, i.e. where the only difference
    is the name. It doesn't cover e.g. copyAlt now being equivalent to 
    copyFrom,alt under the hood.
    ''' 

    # So we only have to check length once
    if len(cmd) < 1:
        return

    v7_cmd_aliases = {
            'goback': 'retsub',
            'else_if': 'elseif',
            ':=': 'set',

            '+=': 'iadd',
            '-=': 'isub', # hyphen
            '–=': 'isub', # en dash
            '−=': 'isub', # minus sign
            '*=': 'imul',
            '×=': 'imul',
            '/=': 'itruediv',
            '÷=': 'itruediv',
            '//=': 'ifloordiv',
            '÷÷=': 'ifloordiv',
            '%=': 'imod',
            '^=': 'ipow',
            '**=': 'ipow',
            '××=': 'ipow',

            '++': 'inc',
            '--': 'dec', # hyphen
            '––': 'dec', # en dash
            '−−': 'dec', # minus sign

            'copy_alt': 'copyalt',
            'copy_from': 'copyfrom',
            'default_from': 'defaultfrom',
            'delete': 'clear', # deprecated in v6.0
            'dup': 'duplicate',
            
            'filter.grayscale': 'grayscale',
            'filter.invert': 'invert',
            'colorfilter': 'rgbfilter',
            'color_filter': 'rgbfilter',
            'filter.rgb': 'rgbfilter',
            'filter.opacity': 'opacity',
            'filter.contrast': 'contrast',
            'filter.colorize': 'colorize',
            'filter.sepia': 'sepia',
            'filter.threshold': 'threshold',
            'filter.hsl': 'hslfilter',
            'filter.selcolor': 'selcolor',
            '2color': 'twocolor',
            'filter.twocolor': 'twocolor',
            'filter.2color': 'twocolor',

            'hue': 'filter.hue', # deprecated in v7.0
            'saturation': 'filter.saturation', # deprecated in v7.0
            'lightness': 'filter.lightness', # deprecated in v7.0
            'fill': 'filter.fill', # deprecated in v7.0

            'draw.rectangle': 'draw.rect',
    }

    v7_subcmd_aliases = {
            'length': 'len',

            '=': 'eq',
            '==': 'eq',
            '≠': 'ne',
            '!=': 'ne',
            '<>': 'ne',
            '<': 'lt',
            '>': 'gt',
            '≤': 'le',
            '<=': 'le',
            '≥': 'ge',
            '>=': 'ge',
            '<=>': 'cmp',

            '||': 'or',
            '&&': 'and',
            '!': 'not',

            '+': 'add',
            '-': 'sub', # hyphen
            '–': 'sub', # en dash
            '−': 'sub', # minus sign
            '*': 'mul',
            '×': 'mul',
            '/': 'truediv',
            '÷': 'truediv',
            'div': 'floordiv',
            '//': 'floordiv',
            '÷÷': 'floordiv',
            '%': 'mod',
            '^': 'pow',
            '**': 'pow',
            '××': 'pow',

            'ceiling': 'ceil',

            'str*': 'str_mul',
            'uppercase': 'upper',
            'lowercase': 'lower',
            
            'string': 'str',
            'str_add': 'str',
            'str+': 'str',
            'boolean': 'bool',
            
            'rgb': 'rgba',
            'hsl': 'hsla',

            'getrgb': 'getrgba',
            'gethsl': 'gethsla',
    }

    if is_subcmd and cmd[0] in v7_subcmd_aliases:
        new_name = v7_subcmd_aliases[cmd[0]]

        # Warn about deprecated aliases
        if version_gte(7,2) and cmd[0] in ('str_add', 'str+'):
            log_warning(\
                f'{cmd[0]}: Deprecated alias; please use {new_name} instead')
            
        cmd[0] = new_name
    elif (not is_subcmd) and cmd[0] in v7_cmd_aliases:
        new_name = v7_cmd_aliases[cmd[0]]

        # Warn about deprecated aliases
        if version_gte(6) and cmd[0] == 'delete':
            log_warning(\
                f'{cmd[0]}: Deprecated alias; please use {new_name} instead')
        if version_gte(7) and cmd[0] in ('hue', 'saturation', 
                                         'lightness', 'fill'):
            log_warning(\
                f'{cmd[0]}: Deprecated alias; please use {new_name} instead')

        cmd[0] = new_name
    # Not an alias -> no change
    # Command is changed in place — no list return needed

# Takes 1 script line (in string format) and converts it to a program-readable
# list. Account for comments, nesting, etc.
def parse_line(line: str) -> list:
    # Strip whitespace from start and end of line
    line = line.lstrip().rstrip()

    # Commands where the parser should NOT treat commas as separators.
    # Note that all commands here have max 1 argument as a result.
    no_split_cmds = ['description', 'desc', 'open', 'save', 'alt', 'template',
                     'warning', 'error']
    # No-Split Commands are only a thing in comma-separated mode, where they
    # are supported for compatibility reasons (they were necessary before
    # quoted strings were added if you wanted to include commas in filenames,
    # descriptions, etc.) Space-separated mode requires all strings to be 
    # quoted, so there's no need for the concept.

    # Split line on commas
    output : list = ['']
    paren_depth = 0 # 0 = not inside parens, 1 = "(", 2 = "((" and so on
    in_string = False # True if inside double quotes
    in_comment = False # True if inside /* multiline comment */
    for index, char in enumerate(line):
        if in_comment:
            if char == '/' and index >= 1 and line[index-1] == '*':
                # End of multiline comment -- Syntax: */
                in_comment = False
            # Else, still in comment, continue ignoring everything
            # Even if we're leaving the comment, don't want to read last "/"
            continue

        if not space_sep and char == ',' and paren_depth == 0 \
                and not in_string and \
                (len(output) == 1 or output[0] not in no_split_cmds):
            # Split on commas if not inside parens, not inside a string, 
            # and command isn't in the list of no-split commands
            output.append('')
        elif space_sep and char.isspace() and paren_depth == 0 \
                and not in_string:
            # If in space-separated mode, split on any whitespace character
            # (besides newlines of course)
            if output[-1] != '':
                # ^ this makes it so you only split once for each sequence of 
                # whitespace characters
                output.append('')
        elif char == '#' and not in_string:
            # When a '#' character is reached, treat the rest of the line as a
            # comment and don't parse it, except if inside a string.
            break
        elif char == '/' and index+1 < len(line) and \
                line[index+1] == '*' and not in_string and version_gte(7,2,1):
            # Start of multiline comment -- Syntax: /*
            in_comment = True
            continue
        elif char == '\\' and in_string and \
                (index == 0 or line[index-1] != '\\') and version_gte(6):
            # Version 6.0.0 and later only:
            # Ignore backslashes unless there's two in a row
            pass
        elif char == 'n' and in_string and \
                index >= 1 and line[index-1] == '\\': 
            # \n -> newline
            output[-1] += '\n'
        elif char == 't' and in_string and \
                index >= 1 and line[index-1] == '\\': 
            # \t -> tab
            output[-1] += '\t'
        else: # All other characters get parsed normally
            output[-1] += char

        # Separately from building the output list, 
        # update paren_depth and in_string
        if char == '(' and not in_string:
            paren_depth += 1
        elif char == ')' and not in_string:
            paren_depth -= 1
            # v4.1.0 AND LATER ONLY:
            # If paren_depth is ever negative, there are too many ")"s
            if paren_depth < 0 and version_gte(4,1):
                log_warning(f'\
Syntax error: Too many closing parentheses. Skipping line: {line}')
                return [''] # Return empty line so converter skips it
        elif char == '"' and (index == 0 or line[index-1] != '\\'): 
            # Strings are only double-quotes, in case I want to add char later.
            # Even if I don't, it's easier if I only have one quote character
            # to worry about.
            # Flip it: If we're in a string, get out.
            # If we're not in a string, get in.
            in_string = not in_string

    # If file is space-separated, the loop we just exited may leave an empty 
    # string at the end of a list if there's whitespace at the end of the line.
    # (For example, if there's a comment at the end of the line) 
    # We should remove this extra space because it can cause errors later.
    if space_sep and len(output) >= 2 and output[-1] == '':
        output.pop()

    # v4.1.0 AND LATER ONLY:
    # If paren_depth isn't back to 0 after exiting splitter loop, syntax error
    if paren_depth > 0 and version_gte(4,1):
        log_warning(f'\
Syntax error: Not enough closing parentheses. Skipping line: {line}')
        return [''] # Return empty line so converter skips it

    # v6.0.0 AND LATER ONLY:
    # If we're still in a string at the end of the line, syntax error
    if in_string and version_gte(6):
        log_warning(f'\
Syntax error: Line ended before string did. Skipping line: {line}')
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

        # If data is explicitly specified to be a string (with quotation marks),
        # leave it as a string and remove its quotation marks.
        # No need to worry about escaped quotation marks because they've 
        # already been dealt with.
        if version_gte(6) and output[arg_n].startswith('"') \
                and output[arg_n].endswith('"') and len(output[arg_n]) >= 2:
            output[arg_n] = output[arg_n][1:-1]
        # Separate out subcommands
        elif version_gte(4,1) and output[arg_n].startswith('(') \
                and output[arg_n].endswith(')'):
            cmd = parse_subcmd(output[arg_n])
            if cmd is None:
                log_warning(f'Invalid subcommand: {output[arg_n]}')
                output[arg_n] = None
            else:
                output[arg_n] = Subcommand(cmd)
        # In certain positions, variable strings should be turned into
        # SetVar instead of Var, so they won't be substituted before
        # running a line.
        elif version_gte(6) and len(output[arg_n]) >= 2 \
                and output[arg_n].startswith('$') \
                and ((output[0] in set_commands \
                        and arg_n == 1) \
                    or (output[0] == 'foreach' and len(output) > 3 \
                        and arg_n == 2)) \
                and var_check(output[arg_n]):
            #   ^ this means we're doing var_check twice (2nd time when
            #   we're executing the line) but this ensures that invalid
            #   variable names will be turned into strings
            output[arg_n] = SetVar(output[arg_n])
        # Convert variable names to Var object.
        # Conversion will NOT happen if:
        #   - We already converted this argument to SetVar
        #   - The string is less than 2 characters long
        #   - It's *any* argument for a header command
        #   - The script was written for a converter version BELOW 6.0.0
        # In these cases, the $text will be treated as a normal string.
        elif version_gte(6) and len(output[arg_n]) >= 2 \
                and output[arg_n].startswith('$') \
                and (output[0] not in header_commands)  \
                and var_check(output[arg_n]):
            output[arg_n] = Var(output[arg_n])
        # Try to convert to numeric types (int or float), or leave it as a 
        # string if that doesn't work
        else:
            try:
                # Convert data to (decimal) int if possible
                # Note that leading zeroes ARE allowed
                output[arg_n] = int(output[arg_n])
            except ValueError:
                if output[arg_n].startswith('0x'): # hexadecimal int
                    try:
                        output[arg_n] = int(output[arg_n][2:], 16)
                    except ValueError:
                        # Can't be a float if it starts with 0x,
                        # so only remaining option is keeping it as string
                        pass
                elif output[arg_n].startswith('0b'): # binary int
                    try:
                        output[arg_n] = int(output[arg_n][2:], 2)
                    except ValueError:
                        # Can't be a float if it starts with 0x,
                        # so only remaining option is keeping it as string
                        pass
                # No octal support because nobody uses octal anymore
                else:
                    try:
                        # Okay then, how about a float? (v6.1.0 and later)
                        # First, convert to lowercase 
                        processed_arg = output[arg_n].lower().strip()
                        # Don't convert words (inf, infinity, nan) to float.
                        # You can still force these to be read as float by
                        # using (float,inf) or (float,"nan") or similar.
                        if version_gte(6,1) and \
                                processed_arg not in (
                                    'inf', '-inf', '+inf', 
                                    'infinity', '-infinity', '+infinity', 
                                    'nan', '-nan', '+nan', 
                                ):
                            output[arg_n] = float(processed_arg)
                    except ValueError:
                        # Just keep it as a string
                        pass

    return output

# Open a script, run some validity checks on it, and display info to the user
# if it's a custom script.
# Return True if it's a valid script and the user wants to run it.
# Return False if there was an error or the user declined to run it.
def open_script(script_file=''):
    global data, version, version_str
    global flags, space_sep, draw_obj
    global warnings, variables, images

    cls()

    # Ask user to pick a script if they want to run a custom script
    custom_script = False
    if not script_file:
        custom_script = True
        script_file = filedialog.askopenfilename(
                title='Select a script to run', defaultextension='.txt',
                filetypes=[('Plain text', '*.txt')],
                initialdir='./scripts/')
        # If script file path is still empty, user cancelled, back to menu
        if script_file == '':
            return False

    #### STEP 2: SCRIPT INFO ####
    try:
        file_obj = open(script_file, 'r', encoding='utf-8')
        # Read script file line-by-line to reduce chance of memory issues
        lines = file_obj.readlines()
        # readlines() will put a '\n' at the end of each line but this'll be 
        # dealt with when rstrip() is called on each line
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
    
    # Determine whether file is comma-separated or space-separated
    space_sep = False
    if script_file.lower().endswith('.s.txt'):
        space_sep = True

    # Merge lines if the first line ends in a backslash
    # Start at len-2 and move up. This allows more than 2 lines to be merged.
    # len-1 is the actual last line, but that shouldn't do anything if it ends 
    # with a backslash because there's no next line to merge with.
    for i in range(len(lines)-2, -1, -1):
        if lines[i].rstrip().endswith('\\'):
            # Remove the actual backslash character
            # Add a space in between so words can't get smashed together
            lines[i] = lines[i].rstrip()[:-1] + ' ' + lines[i+1].lstrip()
            # Blank out the line after instead of deleting it entirely, 
            # to preserve original line numbering for goto
            lines[i+1] = '' 

    # Add empty "line 0" to make goto more consistent
    lines.insert(0, '')

    # DATABASE RESETS & INITIAL SYNTAX CHECKS

    # Reset warnings
    warnings = []

    # Variables will mostly be user-set but let's predefine some stuff...
    variables = {
        # booleans + null
        '$_true': True, '$_t': True,
        '$_false': False, '$_f': False,
        '$_null': None, '$_0': None,
        # mathematical constants
        '$_pi': math.pi, '$_e': math.e,
        # system variables (can be accessed by scripts but not set directly)
        '$_linenumber': 0, '$_ln': 0, # this one gets an alias
        '$_linecount': len(lines)-1, # subtract 1 because of the extra line 0
        '$_fillcolor': Color(255, 255, 255),
        '$_linecolor': Color(0, 0, 0),
        '$_linewidth': 1,
        # private variables (can't be accessed by scripts; internal use only;
        # subject to change at any time)
        '$__constants': [], # List of all constants in the variables dict.
                            # These should be strings, e.g. ['$PI', '$DEBUG']
    }

    # Images the converter can access, 
    # including 'old' (open), 'template', 'alt', and 'new' (save/base)
    # and any user-defined images
    images = {}

    # Before we begin, we need to determine the script's target version 
    # and flags because they'll influence some aspects of how we parse code.
    # This is actually going to be pretty close to how the parser worked in 
    # very early versions, because the version command follows a simple,
    # predictable format.

    version = app_version.copy() # default if no version given in script
    version_str = '(UNKNOWN; defaulting to %s)' % app_version_str()

    # SCRIPT FLAGS
    flags = {}
    # To prevent infinite loops, keep track of how many times each line is run.
    # When a limit is reached (default 100,000 times), halt the program.
    flags['loop_limit'] = None
    # Optionally deviate from Python's standard handling of loop/list ranges
    flags['index_from'] = None
    flags['closed_ranges'] = None
    
    # Reset the draw object so it won't point to an image that no longer exists
    # This was a bug before 7.3
    draw_obj = None
    
    for raw_line in lines:
        line_no_cmt = raw_line.split('#')[0].rstrip()
        cmd : List[Any]
        if space_sep:
            cmd = line_no_cmt.split() # Nice and easy!
        else:
            cmd = line_no_cmt.split(',')
        # Having a completely empty line causes problems, so add an empty
        # string to cmd if necessary
        if len(cmd) < 1:
            cmd.append('')

        # Strip whitespace from line, and if it can be an int, make it an int
        for j in range(len(cmd)):
            try:
                cmd[j] = cmd[j].strip()
                cmd[j] = int(cmd[j])
            except Exception:
                pass

        if cmd[0] == 'version':
            # If user entered 1 or 2 numbers for the version (e.g. "1" or
            # "4,1", assume the other numbers are 0s
            if len(cmd) < 2:
                log_warning('Syntax warning: Empty version')
            elif len(cmd) == 2:
                cmd.append(0)
                cmd.append(0)
            elif len(cmd) == 3:
                cmd.append(0)

            # Make sure version numbers are positive integers
            if type(cmd[1]) == int and type(cmd[2]) == int \
                    and type(cmd[3]) == int and \
                    cmd[1] >= 0 and cmd[2] >= 0 and cmd[3] >= 0:
                version = cmd[1:4]
                version_str = '.'.join([str(x) for x in version])
            else:
                log_warning('Syntax warning: Invalid version')
                version_str = '(INVALID; defaulting to %s)' % \
                        app_version_str()
            # If user didn't specify a version, assume it’s for the current
            # converter version (but display the version as unknown)

        # The rest of this loop is for flags
        if flags['loop_limit'] is None and \
                (cmd[0] in ('looplimit', 'loop_limit')):
            if len(cmd) > 1:
                if type(cmd[1]) == int and cmd[1] > 1:
                    flags['loop_limit'] = cmd[1]
                else:
                    log_warning(f'{cmd[0]}: Invalid loop limit value \
(must be a positive integer)')
            else:
                log_warning(f'{cmd[0]}: Missing loop limit value')
        if cmd[0] == 'flag' and len(cmd) > 1 and cmd[1] == 'loop_limit':
            if len(cmd) > 2:
                if type(cmd[2]) == int and cmd[2] > 1:
                    flags['loop_limit'] = cmd[2]
                else:
                    log_warning('flag: Invalid loop_limit value \
(must be a positive integer)')
            else:
                log_warning('flag: Missing loop_limit value')
        if flags['index_from'] is None \
                and len(cmd) > 1 and cmd[1] == 'index_from':
            if len(cmd) > 2:
                if cmd[2] in (0, 1):
                    flags['index_from'] = cmd[2]
                else:
                    log_warning('flag: Invalid index_from value \
(must be 0 or 1)')
            else:
                log_warning('flag: Missing index_from value')
        if flags['closed_ranges'] is None \
                and len(cmd) > 1 and cmd[1] == 'closed_ranges':
            if len(cmd) > 2:
                if cmd[2] in (0, 1):
                    flags['closed_ranges'] = cmd[2]
                else:
                    log_warning('flag: Invalid closed_ranges value \
(must be 0 or 1)')
            else:
                log_warning('flag: Missing closed_ranges value')

    # Default flags if not set by script
    if flags['loop_limit'] is None:
        flags['loop_limit'] = 100000
    if flags['index_from'] is None:
        flags['index_from'] = 0
    if flags['closed_ranges'] is None:
        flags['closed_ranges'] = 0

    data = []

    for line_str in lines:
        # Initial parsing of lines 
        # (variable values and subcommands are parsed later)
        line_list : list = parse_line(line_str)
        # Replace command aliases (in place)
        alias(line_list, is_subcmd=False)
        data.append(line_list)

    name = 'Unknown Script'
    for cmd in data:
        if cmd[0] == 'name':
            if len(cmd) > 1:
                name = cmd[1]
                break
            else:
                log_warning('Syntax error: Empty name')

    author = 'Unknown Author'
    for cmd in data:
        if cmd[0] == 'author':
            if len(cmd) > 1:
                author = cmd[1]
                break
            else:
                log_warning('Syntax error: Empty author')

    description = 'No description available.'
    for cmd in data:
        if cmd[0] in ['description', 'desc']:
            if len(cmd) > 1:
                description = cmd[1]
                break
            else:
                log_warning('description: command requires at least 1 argument')

    # Warn if the “version” field is later than the current version
    # (unless it's just a newer release version)
    # The compatibility checks are irrelevant for scripts made for newer 
    # versions, because I can't predict the future.
    # Wait, no, I can predict the future: Chat will continue to be a mistake.
    if version_gt(app_version[0], app_version[1], app_version[2]):
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
        return confirm # True if Continue clicked, False if Cancel clicked
    else:
        return True

# Get the paths for the IMAGES the user wants to open and save to.
# Return False if there’s an invalid path or the user cancelled.
# Return True otherwise.
def get_paths(*, new_multi=False):
    global legacy_multi, open_path, save_path, alt_path, template_path
    global base_blank, start_num, stop_num, multi_open_paths, multi_save_paths
    global labels

    #### STEP 3: OPEN & SAVE PATHS ####
    cls()

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
'label: Duplicate label “%s” on line %d ignored' % (item[1], index))
                elif type(item[1]) != str:
                    log_warning(\
'label: Label “%s” on line %d ignored because it’s not a string' % \
(item[1], index))
                else:
                    # If the label hasn't already been used, add it to the
                    # labels dictionary
                    labels[item[1]] = index
            else:
                log_warning('label: empty label on line %d' % index)

    # Load rest of header data
    # Remember, you can use int, float, and string literals here but NOT
    # variables (including bools and math constants) or subcommands.

    # IMAGE PATHS

    # New in v4.0: Default to user input if no path given
    open_path = '.INPUT' 
    for cmd in data:
        if cmd[0] == 'open' and len(cmd) > 1:
            if isinstance(cmd[1], str):
                open_path = cmd[1]
                break
            elif cmd[1] == 0:
                # "//NONE" uses double slashes because that should always be an
                # illegal path (and thus will never conflict with any file
                # selected by the user).
                open_path = '//NONE'
                break
            elif cmd[1] == 1:
                # alias for .INPUT
                break
            else:
                log_warning('open: Invalid path. Defaulting to user input.')
                break

    alt_path = ''
    for cmd in data:
        if cmd[0] == 'alt' and len(cmd) > 1:
            if isinstance(cmd[1], str):
                alt_path = cmd[1]
                break
            else:
                log_warning('alt: Invalid path. No alternate image loaded.')
                break

    template_path = ''
    for cmd in data:
        if cmd[0] == 'template' and len(cmd) > 1:
            if isinstance(cmd[1], str):
                template_path = cmd[1]
                break
            else:
                log_warning('template: Invalid path. No template image loaded.')
                break

    # New in v4.0: Default to user input if no path given
    save_path = '.INPUT'
    for cmd in data:
        if cmd[0] == 'save' and len(cmd) > 1:
            if isinstance(cmd[1], str):
                save_path = cmd[1]
                break
            elif cmd[1] == 0:
                # "//NONE" uses double slashes because that should always be an
                # illegal path (and thus will never conflict with any file
                # selected by the user).
                save_path = '//NONE'
                break
            elif cmd[1] == 1:
                # alias for .INPUT
                break
            else:
                log_warning('save: Invalid path. Defaulting to user input.')
                break

    base_blank = False
    for cmd in data:
        if cmd[0] == 'base' and len(cmd) > 1 and cmd[1] == 'blank':
            base_blank = True
            break
        elif cmd[0] == 'base' and len(cmd) > 2 \
                and type(cmd[1]) == int and type(cmd[2]) == int:
            # User-specified size for blank base
            base_blank = (cmd[1], cmd[2])

    has_start_num = False # replacing prev start_num=None which fails typecheck
    start_num = 0
    for cmd in data:
        if cmd[0] == 'start' and len(cmd) > 1:
            # start number has to be an integer
            if type(cmd[1]) != int:
                log_warning('start: must be an integer')
                break
            has_start_num = True
            start_num = cmd[1]
            break

    has_stop_num = False
    stop_num = 1
    for cmd in data:
        if cmd[0] == 'stop' and len(cmd) > 1:
            # stop number has to be an integer
            if type(cmd[1]) != int:
                log_warning('stop: must be an integer')
                break
            has_stop_num = True
            stop_num = cmd[1]+1
            # Unlike in Python, the “stop” is inclusive.
            # e.g. if stop is 10, it will convert #10 but not #11
            break

    # Determine whether script is converting 1 file (single-file mode)
    # or multiple files (multi-file mode)
    # For a valid legacy multi-file conversion, open_path & save_path must have 
    # wildcards, and there must be start and stop numbers provided. Otherwise,
    # the script will be treated as a single-file conversion.
    legacy_multi = False # reset in case past conversions set this global var
    if has_start_num and has_stop_num and \
            '*' in open_path and '*' in save_path:
        # Note that both open and save paths must have a * in them
        legacy_multi = True
    # If a script is not a valid legacy multi-file conversion but it has start 
    # and stop numbers, throw a warning
    if (not legacy_multi) and (has_start_num or has_stop_num):
        log_warning('Script has start/stop numbers but is not a valid legacy \
multi-file conversion script')

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
            if open_path != '//NONE':
                open(open_path, encoding='utf-8').close()
        except FileNotFoundError:
            # This code will only be reached in legacy single-file mode because
            # the OS file selector shouldn't select a nonexistent file
            choose_new_path = yn_dialog('File warning', 
['The script tried to open the following file, but it does not exist.',
f'<b>{open_path}',
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
                    f'''The path {open_path} is a folder or application.
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
        base_save_path = f'{open_path}/_converted'
        save_path = base_save_path

        n = 1
        while os.path.exists(save_path): 
            # If there's already a subfolder called _converted, 
            # tack a number on the end
            save_path = base_save_path + str(n)
            n += 1
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
f'<b>{parent_dir}',
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
                    f'<b>{save_path}',
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

        return bool(conf)

# Runs the selected conversion script on as many files as called for.
# Return number of files successfully converted.
def run_script(*, new_multi=False):
    global open_path, save_path
    global start_num, stop_num, current_num
    global block_depths, block_stacks
    global break_depths, break_stacks, loop_data

    #### STEP 4: RUN SCRIPT ####
    cls()

    # Set current_num after start_num is set but before the first 
    # update_subhead call
    current_num = start_num

    heading_text = Label(main_frame, text='Converting image...', 
        font=f_heading, bg=colors['UI_BG'])
    heading_text.place(x=0, y=0)

    # Update screen differently based on how many files we're converting
    heading = Label(bg=colors['UI_BG'])
    subhead = Label(bg=colors['UI_BG'])
    if new_multi:
        heading = Label(main_frame, 
            text='Converting all images in the folder %s' % \
                multi_open_paths[0].split(os.sep)[-2], 
            font=f_heading, bg=colors['UI_BG'])
        subhead = update_subhead(subhead)
    elif legacy_multi:
        heading = Label(main_frame, 
            text=f'Converting all images from {start_num} to {stop_num-1}', font=f_heading, 
            bg=colors['UI_BG'])
        subhead = update_subhead(subhead)
    else:
        # For single-image conversions, set start/stop so the main loop will 
        # only run once
        heading = Label(main_frame, text='Converting 1 image...', 
            font=f_heading, bg=colors['UI_BG'])
        start_num = 0
        stop_num = 1
    heading.place(x=0, y=0)
    window.update()

    # Start the clock
    t1 = time()
    time_last_refresh = t1
    time_since_refresh = 0
    conv_count = 0 # Count how many files have been converted

    #### BEGIN SCRIPT INITIALIZATION ####

    # The block stack is how we keep track of nested blocks.
    # Each item represents one line of code.
    # We start out empty, then if we enter a block via e.g. an if statement,
    # then "if" gets added onto the stack. When we reach an "end" command,
    # the last element is taken off the stack.
    block_stacks = []
    block_depths = [] # "indentation" of each line

    break_stacks = [] # block_stacks but only blocks you can break from
    break_depths = []

    loop_data = [] # Additional data associated with each block of code 
    # Each line gets its own dictionary in loop_data
    for _ in range(len(data)):
        loop_data.append({})
    # Each line will have the following associated keys: 
    # start_lines, end_lines, for_vars, for_stops, for_steps
    # Note that start_lines and end_lines only concern loops (not if blocks)

    current_stack = []
    # Generate list of code lines, with "indentation" for each line
    current_depth = 0 # start

    current_break_depth = 0
    current_break_stack = []

    current_start_lines = []
    current_end_lines = []
    current_for_vars = [] # None = this block is a while loop
    # Don't need to save a "for_start" because we only need to check that 
    # variable once (i.e. in the first iteration of the loop)
    current_for_stops = []
    current_for_steps = []
    need_reverse_search = False

    for index, item in enumerate(data):
        # len(item) will never be 0 because parse_line() returns [''] for
        # empty lines
        
        # Check that the command has enough arguments (may change its contents)
        arg_check(item, is_subcmd=True)

        # Pre-process for loops (expand arguments) so we can build up loop_data
        # Make sure the command has enough arguments
        if item[0] == 'for':
            if len(item) < 3: 
                log_warning(f'{item[0]}: not enough arguments — need at least \
a loop variable and a number to stop at')
                # Neutralize block by making it always evaluate to false
                item = ['if', None] + item
            elif not var_check(item[1], item[0], exists=None):
                # var_check will generate warning
                # Neutralize block by making it always evaluate to false
                item = ['if', None] + item
            else:
                # If some arguments are omitted, fill them in.
                # If we go back to this loop, the values will stay filled in,
                # but that's fine because the defaults won't change.
                if len(item) == 3: # for,var,stop -> insert start before stop
                    item.insert(2, flags['index_from']) # 0 (default), or 1
                # No elif so the len==3 block can fall through into this
                if len(item) == 4: # for,var,start,stop -> append step
                    item.append(1)

                # These don't get used right away but they will show up later 
                # in this function
                # If we're here, item[1] must be SetVar, as it passed var_check
                loopVar : SetVar = item[1]
                # start : int = item[2]
                stop : int = item[3]
                step : int = item[4]
        elif item[0] == 'foreach':
            if len(item) < 3: 
                log_warning(f'{item[0]}: not enough arguments — need at least \
a loop variable and a list to iterate on')
                # Neutralize block by making it always evaluate to false
                item = ['if', None] + item
            elif not var_check(item[1], item[0], exists=None):
                # var_check will generate warning
                # Neutralize block by making it always evaluate to false
                item = ['if', None] + item
            elif len(item) > 3 and not var_check(item[2], item[0], exists=None):
                # If both index and item variable names are given,
                # we need to var_check on arg2 as well
                # Neutralize block by making it always evaluate to false
                item = ['if', None] + item
            else:
                if len(item) == 3:
                    # If no index variable specified, insert one
                    item.insert(1, SetVar(f'$__index{current_depth}'))
                    # Example: a foreach loop that starts unindented will have
                    # a default index variable of $__index0
                indexVar : SetVar = item[1]
                itemVar : SetVar = item[2]
                seq : abc.Sequence = item[3]

        # Decrease block depth if command is a block end
        if item[0] in block_ends:
            current_depth -= 1

            # If block depth is *ever* negative, that's an error
            if current_depth < 0:
                simple_dialog('Syntax error', 
                    'This script’s block depth is imbalanced. Please check \
to make sure it doesn’t have too many “end” commands.', icon='error')
                return False
        
            if current_stack[-1] in breakable_blocks:
                current_break_depth -= 1

        # Add new block onto stack
        # Excludes block_starts_ends so e.g. "else" doesn't add an extra "if"
        # on the end and mess up calculations
        if item[0] in block_starts and item[0] not in block_starts_ends:
            if item[0] in ('elseif', 'else_if', 'else'):
                # Special case: elseif/else get added to the stack as "if" since
                # it's really all part of one big statement
                current_stack.append('if')
            else:
                # Everything else gets added under the actual command name
                current_stack.append(item[0])
        
        if item[0] == 'for':
            need_reverse_search = True
            # Now that the loop has all its arguments, build up loop_data
            # (except loop_ends because that'll need to search in reverse)
            current_start_lines.append(index)
            # loopVar,stop,step are guaranteed to be assigned in pre-processing
            # if they aren't assigned, the block will be neutralized to if,()
            # so this part will never be reached
            current_for_vars.append(loopVar)
            current_for_stops.append(stop)
            current_for_steps.append(step)
        elif item[0] == 'foreach':
            need_reverse_search = True
            current_start_lines.append(index)
            current_for_vars.append((indexVar, itemVar, seq))
            current_for_stops.append(None)
            current_for_steps.append(None)
        elif item[0] in breakable_blocks:
            need_reverse_search = True
            current_start_lines.append(index)
            current_for_vars.append(None)
            current_for_stops.append(None)
            current_for_steps.append(None)

        # Update break_stacks if necessary (i.e. if block_stacks is changing)
        # [-1] is still prev line because we haven't saved the stacks yet
        if len(block_stacks) == 0 or current_stack != block_stacks[-1]:
            current_break_stack = [i for i in current_stack.copy() if \
                             ((i is None) or (i in breakable_blocks))]

        # Add the current line's depth to block_depths
        block_depths.append(current_depth)
        # and its stack to block_stacks
        block_stacks.append(current_stack.copy()) 
        # .copy() is important as otherwise every item of block_stacks would
        # point to the same list

        break_depths.append(current_break_depth)
        # Only add breakable blocks from the current block stack,
        # PLUS the None at the start
        break_stacks.append(current_break_stack)

        loop_data[index]['start_lines'] = current_start_lines.copy()
        loop_data[index]['for_vars'] = current_for_vars.copy()
        loop_data[index]['for_stops'] = current_for_stops.copy()
        loop_data[index]['for_steps'] = current_for_steps.copy()

        # Remove last block from stack AFTER saving the stack, so "end" commands
        # will still be inside the stack
        # Excludes block_starts_ends so e.g. "else" doesn't remove an extra "if"
        # from the end and mess up calculations
        if item[0] in block_ends and item[0] not in block_starts_ends:
            popped = current_stack.pop()
            if popped in breakable_blocks:
                need_reverse_search = True
                current_start_lines.pop()
                current_for_vars.pop()
                current_for_stops.pop()
                current_for_steps.pop()

        # Increase block depth if command is a block start
        if item[0] in block_starts:
            current_depth += 1
            if item[0] in breakable_blocks:
                current_break_depth += 1

        # Uncomment to print all the lines out upon initial parse
        #p#rint(index, item, block_depths[index], block_stacks[index])

    # if depth is positive at end of code, error
    if current_depth > 0:
        simple_dialog('Syntax error', 
            'This script’s block depth is imbalanced. Please check to make \
sure each block has an associated “end” command.', icon='error')
        return False

    # Only if the code has loops, search through the code in reverse
    # (reverse makes the code take linear time instead of quadratic)
    if need_reverse_search:
        for index in range(len(data)-1, -1, -1):
            item = data[index] # MANUAL ENUMERATE

            if item[0] in block_ends and block_stacks[index][-1] != 'if':
                current_end_lines.append(index)

            loop_data[index]['end_lines'] = current_end_lines.copy()

            if item[0] in block_starts and block_stacks[index][-1] != 'if':
                current_end_lines.pop()

    #### END SCRIPT INITIALIZATION ####

    # Load template image only once because it doesn't allow wildcards
    try:
        if template_path != '':
            # template_path doesn't support wildcards because the point is
            # for there to be just 1 template
            images['template'] = PIL.Image.open(template_path).convert('RGBA')
    except FileNotFoundError:
        log_warning('Couldn’t find a template file with the path '+\
            template_path+' — skipping')
    except (AttributeError, PIL.UnidentifiedImageError): 
        # We opened something, but it's not an image
        log_warning('Couldn’t open the template file at ' + \
            template_path + '. Are you sure it’s an image? Skipping.')
    except IsADirectoryError: # If user opens a folder or Mac app bundle
        log_warning('The template file path '+template_path+\
            ' is a folder or application.')

    try:
        if alt_path != '':
            images['alt'] = PIL.Image.open(alt_path).convert('RGBA')
    except FileNotFoundError:
        log_warning('Couldn’t find an alternate file with the path '+\
            alt_path+' — skipping')
    except (AttributeError, PIL.UnidentifiedImageError): 
        # We opened something, but it's not an image
        log_warning('Couldn’t open the alternate file at ' + \
            alt_path + '. Are you sure it’s an image? Skipping.')
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

        # images['old'] guaranteed to be defined below
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
                if open_path == '//NONE':
                    # We need to have SOMETHING as the old image, so let's make
                    # a blank 1×1 image
                    images['old'] = PIL.Image.new('RGBA', (1,1))
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
            log_warning(f'Couldn’t open the file at {open_path}. Are you sure \
it’s an image? Skipping.')
            continue
        except IsADirectoryError: # If user opens a folder or Mac app bundle
            log_warning(f'The path {open_path} is a folder or application.')
            continue

        if base_blank:
            # Create a blank base if the script starts from that
            if type(base_blank) == tuple and len(base_blank) >= 2: 
                # If base command contains a 2-tuple, make that the
                # new image's width and height
                w, h = base_blank
            elif 'template' in images:
                # If we opened a valid template image, use its size for the
                # blank base
                w, h = images['template'].size
            elif open_path == '//NONE':
                # If we aren't opening any image, default to 256×256
                w = 256; h = 256
            else:
                # Otherwise, default to the size of the image we opened
                w, h = images['old'].size
            images['new'] = PIL.Image.new('RGBA', (w,h))
        else:
            # If no base is specified, start new image as copy of old image
            images['new'] = images['old'].copy()

        # THE IMPORTANT LINE:
        final_img : Optional[PIL.Image.Image] = process()
        # process() returns None if it reads a "skip" command

        if final_img is not None and save_path != '//NONE':
            final_img.save(save_path.replace('*', str(i)))
        conv_count += 1

    t2 = time()
    return pre_summary(t2-t1, conv_count, new_multi) # Return helper func's result

def process_line(line: list):
    '''
    Given a line (in list form), return it in processed form, by substituting
    variable names for their associated values, then running any subcommands.
    This function does NOT execute the line's main command.
    '''
    cmd = line.copy() 

    subst_all_vars(cmd)

    for arg_n in range(1, len(cmd)):
        # Now that we've broken the command into the normal list format,
        # we need to check each argument of the command for parens and
        # recursively call this function as needed.
        if type(cmd[arg_n]) == Subcommand:
            # Execute the command INSIDE the parens FIRST
            cmd[arg_n] = subcmd(cmd[arg_n].content)

    return cmd

def process():
    '''
    Reads lines from one file and executes its instructions.
    Returns the image that will be saved.
    '''
    # To prevent infinite loops, keep track of how many times each line is run.
    # When a limit is reached (default 10000 times), halt the program.
    # New in v7.2.1: Reset the loop counter for every file.
    loop_counter = [0] * len(data)

    # Stack of line numbers saved when entering subroutines.
    # Note that numbers here are the line that has the gosub command,
    # so execution will resume from the *next* line.
    substack = []

    # MAIN LINE-PROCESSING LOOP
    # Remember, each line has been parsed into list format already, 
    # but the subcommands have NOT been parsed
    index = 0 # START
    jumped = False # True if running the current line interrupted normal flow
    while index < len(data): # STOP
        item = data[index] # MANUAL ENUMERATE

        # Uncomment this to print line-by-line output
        # p#rint(index, item, block_depths[index], block_stacks[index], 
        #     break_depths[index], break_stacks[index])

        # Increment loop counter for the line
        loop_counter[index] += 1
        # If we hit the loop limit, stop the script to prevent infinite loops
        if loop_counter[index] >= flags['loop_limit']:
            simple_dialog('Conversion error', 
                    [f'''Conversion stopped because the loop limit of \
{flags['loop_limit']} was reached on line {index}.''',
'Please check your code to make sure there isn’t an infinite loop.',
'''If you meant to loop this many times, you can increase the loop limit \
using the header command “flags,loop_limit,<NUMBER>”.'''], 
                    'Back to Menu', icon='error')
            menu()

        try:
            # Wait until we're in the error-catching area to run subcommands
            item = process_line(item)

            jumped = False # Reset jumped flag for new line

            if item[0].strip() == '' or item[0] in ('noop', 'label'): 
                # Skip blank lines, noops, and labels
                continue
            elif item[0] == 'exit': 
                # End the conversion early, but save the target file as is 
                # and exit properly.
                break
            elif item[0] == 'skip':
                # End the conversion early, without saving or displaying an 
                # error message. Intended for use in batch conversion where
                # you want to flag only files that meet specific criteria.
                return None
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
            elif item[0] == 'assert':
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning(f'{item[0]}: missing assertion')
                    continue

                assertion_result = bool(item[1])
                if not assertion_result:
                    log_warning(f'{item[0]}: FAIL {data[index][1]}')
                    # Use the unevaluated argument because otherwise it'll
                    # just show up as "True" or "False"
            elif item[0] == 'use':
                log_warning(f'{item[0]}: command is no longer needed in \
scripts with draw commands. Simply call the draw commands on their own \
*without* putting “use,draw” first.')
            elif item[0] == 'ai':
                # from __future__ import braces
                log_warning(f'{item[0]}: not a chance')

            # Control commands
            elif item[0] == 'goto': 
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning('goto: missing line number or label')
                    continue

                # OPTION 1: Go to line number
                # Line numbers start counting from 1, even internally
                if type(item[1]) == int:
                    index = item[1]
                    set_ln(index)
                    jumped = True
                # OPTION 2: Go to label
                # This will jump to the line on which the label was declared.
                elif type(item[1]) == str:
                    if item[1] in labels:
                        index = labels[item[1]]
                        set_ln(index)
                        jumped = True
                    else:
                        log_warning(
                            f'{item[0]}: Unrecognized label “{item[1]}”'
                        )
                else:
                    log_warning('goto: Must go to a line number (integer) \
or label (string)')

            elif item[0] == 'gosub':
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning('gosub: missing line number or label')
                    continue

                # This is literally just goto but you add the line number
                # onto a stack
                substack.append(index)

                # OPTION 1: Go to line number
                # Line numbers start counting from 1, even internally
                if type(item[1]) == int:
                    index = item[1]
                    set_ln(index)
                    jumped = True
                # OPTION 2: Go to label
                # This will jump to the line on which the label was declared.
                elif type(item[1]) == str:
                    if item[1] in labels:
                        index = labels[item[1]]
                        set_ln(index)
                        jumped = True
                    else:
                        log_warning(
                            f'{item[0]}: Unrecognized label “{item[1]}”'
                        )
                else:
                    log_warning('gosub: Must go to a line number (integer) \
or label (string)')

            elif item[0] == 'retsub':
                if len(substack) >= 1:
                    index = substack.pop()
                    set_ln(index)
                else:
                    log_warning(f'{item[0]}: Stack is empty')

            # One-line variant of if
            elif item[0] == 'if1':
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning(f'{item[0]}: missing conditional statement')
                    continue

                if version_gte(7,1):
                    log_warning(f'{item[0]}: This command is deprecated. \
Please use “if” instead.')

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
                    log_warning(f'{item[0]}: missing conditional statement')
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
                    set_ln(index)
                    # Initially, we only want to get out the command name.
                    # We'll come back to evaluate variables and subcommands
                    # later if needed. If we processed them all at once,
                    # that'd run the risk of e.g. getting variable-not-defined
                    # errors because we haven't executed the line that defines
                    # the variable yet. This bug was fixed in 7.6.0.
                    item = data[index]

                    # Skip lines that don't match depth of original if line
                    if block_depths[index] != start_depth:
                        continue

                    if item[0] in ('elseif', 'else_if'):
                        # Reprocess line with variables this time (see above)
                        item = process_line(data[index])
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
                    elif item[0] in ('end', 'endif'):
                        # And we're done
                        break

                # IF we get past this point (conditional is True), 
                # there's nothing more to do here. We're in the if block. 
                # Proceed as normal until we reach an "end" command.

            # Excluding "end"/"endif" here because if we reach there naturally,
            # we're already at the end of the if statement so there's nothing
            # left to do
            elif item[0] in ('elseif', 'else_if', 'else') \
                    and len(block_stacks[index]) > 0 \
                    and block_stacks[index][-1] == 'if':
                # if, elseif, and else are all added to block_stacks as "if".
                # If we encounter elseif, else, end, etc. during the normal 
                # line-reading cycle, then we've finished a block from a 
                # condition that evaluated as true, so we're done with the 
                # whole if statement

                # Jump down the lines until we reach an "end" command at the
                # appropriate depth
                start_depth = block_depths[index]
                while True:
                    index += 1
                    if index >= len(data):
                        # This should be impossible because if we end up at 
                        # the end of the file while scanning, the blocks must
                        # be imbalanced. But this should eliminate any chance
                        # of crashes.
                        break
                    item = data[index]
                    # No need to process arguments because we only need to 
                    # check arg0 (command name) right now
                    if item[0] in ('end', 'endif') \
                            and block_depths[index] == start_depth:
                        break

                # Note that the "current" line is the line that actually has the
                # elseif/else/end, but this will be incremented in the
                # "finally" block below this loop so we're past the blocks

            elif item[0] == 'while':
                # Make sure the command has enough arguments
                if len(item) < 2: 
                    log_warning(f'{item[0]}: missing conditional statement')
                    continue

                # Fill in "do" argument with 0 if it's not present
                if len(item) == 2:
                    item.append(0)
                do = isinstance(item[2], int) and bool(item[2])

                # Save depth of if block so we can check it against the 
                # elseif/else/end lines we're parsing later
                start_depth = block_depths[index]

                # Result of conditional command in the if statement
                # item[1] will already be processed by the subcmd call above
                cond_result = True
                if not do:
                    cond_result = bool(item[1])

                # IF condition is FALSE, skip until we're out of 
                # the block (either elseif, else, or end)
                while not cond_result:
                    index += 1
                    item = data[index]
                    # No need to process arguments because we only need to 
                    # check arg0 (command name) right now

                    # Skip lines that don't match the depth of the original
                    # while line
                    if block_depths[index] != start_depth:
                        continue

                    # Search for the "end" so we can skip past the loop
                    if item[0] == 'end':
                        break

                # IF we get past this point (condition is True), 
                # there's nothing more to do here. We're inside the loop. 
                # Proceed as normal until we reach an "end" command.

            elif (item[0] == 'end' and len(block_stacks[index]) > 0 and \
                    block_stacks[index][-1] == 'while'):
                # If we reach an "end" when we're in a 
                # while loop (but otherwise reading lines normally), 
                # then we've reached the end of the loop block,
                # so we need to jump back up to continue the loop

                start_line = index
                start_depth = block_depths[index]
                # Move up the lines until we reach a "while" command with
                # depth equal to our current depth. 
                # That'll be the line we want to jump to.

                # Must move up at least 1 line so that the following while loop
                # doesn't break right away from being on the same line
                index -= 1
                # item = data[index]

                # Move up the lines until we get to the start
                while block_depths[index] != start_depth:
                    index -= 1
                    # item = data[index]

                # Check condition separately here, because if the "do" argument
                # equals 1, then we don't check on the while line so the
                # loop would be infinite
                cond_result = bool(item[1])

                if cond_result:
                    # If condition is true, enter the loop
                    index += 1
                    jumped = True
                else:
                    # Otherwise, jump back out
                    index = start_line
                    set_ln(index)
                    # We're back to the "end" line now, and we'll proceed to
                    # the next line normally

            elif item[0] == 'next':
                # Skip to the next iteration of the loop.
                # Practically speaking, this is the same as a "goto" that goes
                # to the loop's "end" line.

                # Can only use command inside a loop
                if len(break_stacks[index]) == 0:
                    log_warning(
                        'next: This command can only be used inside a loop')
                    continue

                index = loop_data[index]['end_lines'][-1]
                set_ln(index)
                jumped = True

            elif item[0] == 'break':
                # Exit the current loop (or loops, if you add an integer
                # argument after the keyword).
                # Practically speaking, this is the same as a "goto" that goes
                # to the loop's "end" line PLUS 1.

                # Can only use command inside a loop
                if len(break_stacks[index]) == 0:
                    log_warning(
                        'break: This command can only be used inside a loop')
                    continue

                # If no multi-break specified, default to single break
                if len(item) <= 2:
                    item.append(1)
                break_count = item[1]

                # Make sure we aren't breaking too far out
                max_breaks = len(loop_data[index]['end_lines'])
                if break_count > max_breaks:
                    log_warning(f'break: tried to break {break_count} times \
from a stack of {max_breaks} loops')
                    # End the program early due to error
                    index = len(data) # jump to one line after last
                    set_ln(index)
                    continue

                # Jump to the appropriate end line based on break count
                index = loop_data[index]['end_lines'][-break_count] + 1
                set_ln(index)
                jumped = True

            elif item[0] == 'for':
                # Loop will always have ≥4 args (len≥5) after initialization
                loopVar : SetVar = item[1]
                start : int = item[2]
                stop : int = item[3]
                step : int = item[4]

                # Initial setting of loop variable
                set_([item[0], loopVar, start], internal=False)

                # First test of whether to break out of loop
                time2stop = False
                if step < 0:
                    time2stop = (variables[loopVar.name] <= stop \
                            and not flags['closed_ranges']) \
                        or (variables[loopVar.name] < stop \
                            and flags['closed_ranges'])
                else:
                    time2stop = (variables[loopVar.name] >= stop \
                            and not flags['closed_ranges']) \
                        or (variables[loopVar.name] > stop \
                            and flags['closed_ranges'])
                if time2stop:
                    index = loop_data[index]['end_lines'][-1] + 1
                    set_ln(index)
                    jumped = True

                # If we make it here, we're in the loop.
                # Note: If you goto somewhere inside the loop and that means 
                # the loop variable is undefined, I can't help you with that.
                # My brain hurts.
                # Why did I add goto again?

            elif (item[0] == 'end' and len(block_stacks[index]) > 0 and \
                    block_stacks[index][-1] == 'for'):
                # Yes, this will be str, not SetVar. The string is extracted
                # during initialization.
                loopVar : SetVar = loop_data[index]['for_vars'][-1]
                stopRaw = loop_data[index]['for_stops'][-1]
                stepRaw = loop_data[index]['for_steps'][-1]
                # Compute subcommands and variables for stop and step
                # by passing a fake command to process_line
                # This is only necessary because the items loop_data won't
                # get automatically processed
                processed = process_line(['noop', stopRaw, stepRaw])
                stop : int = processed[1]
                step : int = processed[2]

                # Step the loop variable
                # If code executes in a normal structured-programming way,
                # it shouldn't be a problem to assume variables[loopVar]
                # already exists. If the script misuses gotos, we could have
                # a problem, but if you use goto, you're on your own.
                change([item[0], loopVar, '+', step])

                # Check if it's time to stop
                time2stop = False
                if step < 0:
                    time2stop = (variables[loopVar.name] <= stop \
                            and not flags['closed_ranges']) \
                        or (variables[loopVar.name] < stop \
                            and flags['closed_ranges'])
                else:
                    time2stop = (variables[loopVar.name] >= stop \
                            and not flags['closed_ranges']) \
                        or (variables[loopVar.name] > stop \
                            and flags['closed_ranges'])
                if time2stop:
                    index = loop_data[index]['end_lines'][-1] + 1
                    set_ln(index)
                    jumped = True
                # Otherwise, jump to first line inside loop
                else:
                    index = loop_data[index]['start_lines'][-1]
                    set_ln(index)
                    jumped = False
                    # ...and we're off to another iteration of the loop

            elif item[0] == 'foreach':
                # Yes, these will be str, not SetVar. The strings are extracted
                # during initialization.
                indexVar : SetVar = item[1]
                itemVar : SetVar = item[2]
                seq : abc.Sequence = item[3]

                # Initial setting of both loop variables
                start : int = flags['index_from']
                # Only use internal override if indexVar is __indexN
                set_(
                    [item[0], indexVar, start], 
                    internal=(indexVar.name==f'$__index{block_depths[index]}')
                )
                set_([item[0], itemVar, seq[start]], internal=False)

                # First test of whether to break out of loop
                if (variables[indexVar.name] >= len(seq) \
                            and not flags['closed_ranges']) \
                        or (variables[indexVar.name] > len(seq) \
                            and flags['closed_ranges']):
                    index = loop_data[index]['end_lines'][-1] + 1
                    set_ln(index)
                    jumped = True

                # If we make it here, we're in the loop.
                    
            elif (item[0] == 'end' and len(block_stacks[index]) > 0 and \
                    block_stacks[index][-1] == 'foreach'):
                # Unlike for, everything we want is simply stored in for_vars
                indexVar : SetVar = loop_data[index]['for_vars'][-1][0]
                itemVar : SetVar = loop_data[index]['for_vars'][-1][1]
                seqRaw = loop_data[index]['for_vars'][-1][2]

                # Compute subcommands and variables for seq
                # by passing a fake command to process_line
                # This is only necessary because the items loop_data won't
                # get automatically processed
                processed = process_line(['noop', seqRaw])
                seq : abc.Sequence = processed[1]

                # Check if it's time to stop
                if (variables[indexVar.name] >= len(seq)-1 \
                            and not flags['closed_ranges']) \
                        or (variables[indexVar.name] > len(seq)-1 \
                            and flags['closed_ranges']):
                    index = loop_data[index]['end_lines'][-1] + 1
                    set_ln(index)
                    jumped = True
                else:
                    # Step the index variable
                    change([item[0], indexVar, '+', 1], internal=True)
                    # Update item variable
                    set_([item[0], itemVar, seq[variables[indexVar.name]]])

                    # Jump to first line inside loop
                    index = loop_data[index]['start_lines'][-1] + 1
                    set_ln(index)
                    jumped = True
                    # ...and we're off to another iteration of the loop

            # Variable commands (ONLY in scripts for v6+)
            elif item[0] in ('set', ':='):
                set_(item)
            elif item[0] == 'const':
                const(item)
            elif item[0] == 'change':
                change(item)
            elif item[0] == 'iadd':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'add'] + item[2:])
            elif item[0] == 'isub':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'sub'] + item[2:])
            elif item[0] == 'imul':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'mul'] + item[2:])
            elif item[0] == 'itruediv':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'truediv'] + item[2:])
            elif item[0] == 'ifloordiv':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'floordiv'] + item[2:])
            elif item[0] == 'imod':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'mod'] + item[2:])
            elif item[0] == 'ipow':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'pow'] + item[2:])
            elif item[0] == 'inc':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'add', 1])
            elif item[0] == 'dec':
                change([item[0], # cmd name
                        item[1], # variable identifier
                        'sub', 1])

            # Basic copying commands
            elif item[0] == 'copy':
                copy(item, images['old'], images['new'])
            elif item[0] in ('copy_alt', 'copyalt'):
                if 'alt' in images:
                    copy(item, images['alt'], images['new'])
                else:
                    log_warning('\
copyalt: Skipped because no “alt” image was specified.')
            elif item[0] in ('copyfrom', 'copy_from'):
                # Unlike other copy commands, `copyfrom` uses global image list
                # and passes the appropriate images to `copy`
                copyfrom(item)
            elif item[0] == 'default':
                if 'template' in images:
                    default(item, images['template'], images['new'])
                else:
                    log_warning('\
default: Skipped because no “template” image was specified.')
            elif item[0] in ('defaultfrom', 'default_from'):
                # Similar to copyfrom above but copying to same x/y position
                defaultfrom(item)
            elif item[0] == 'clear':
                clear(item, images['new'])
            elif item[0] == 'delete':
                clear(item, images['new'])
                if version_gte(6):
                    log_warning('delete: Deprecated alias; please use “clear”')
            elif item[0] == 'duplicate':
                duplicate(item, images['new'])
            elif item[0] == 'move':
                move(item, images['new'])
            elif item[0] == 'swap':
                swap(item, images['new'])
            elif item[0] == 'over':
                images['new'] = over(item, images['old'], images['new'])
            elif item[0] == 'under':
                images['new'] = under(item, images['old'], images['new'])

            # Advanced copying commands
            elif item[0] == 'tile':
                tile(item, images['new'])
            elif item[0] == 'copyscale':
                copyscale(item)

            # Transformation commands
            elif item[0] == 'resize':
                images['new'] = resize(item, images['new'])
            elif item[0] == 'crop':
                images['new'] = crop(item, images['new'])
            elif item[0] == 'scale':
                images['new'] = scale(item, images['new'])
            elif item[0] == 'rotate':
                images['new'] = rotate(item, images['new'])
            elif item[0] == 'flip':
                flip(item, images['new'])

            # Filter commands
            elif item[0] in ('grayscale', 'filter.grayscale'):
                grayscale(item, images['new'])
            elif item[0] in ('invert', 'filter.invert'):
                invert(item, images['new'])
            elif item[0] in ('rgbfilter', 'color_filter', 
                             'colorfilter', 'filter.rgb'):
                rgbfilter(item, images['new'])
            elif item[0] in ('opacity', 'filter.opacity'):
                opacity(item, images['new'])
            elif item[0] in ('contrast', 'filter.contrast'):
                contrast(item, images['new'])
            elif item[0] in ('colorize', 'filter.colorize'):
                colorize(item, images['new'])
            elif item[0] in ('sepia', 'filter.sepia'):
                sepia(item, images['new'])
            elif item[0] in ('threshold', 'filter.threshold'):
                threshold(item, images['new'])
            elif item[0] in ('hslfilter', 'filter.hsl'):
                hslfilter(item, images['new'])
            elif item[0] in ('selcolor', 'filter.selcolor'):
                selcolor(item, images['new'])
            elif item[0] in ('2color', 'twocolor', 
                             'filter.2color', 'filter.twocolor'):
                twocolor(item, images['new'])
            elif item[0] == 'recolor':
                recolor(item, images['new'])
            # Prefix-only filters
            elif item[0] == 'filter.hue':
                hslfilter([item[0], item[1], 0, 0] + item[2:], images['new'])
            elif item[0] == 'filter.saturation':
                hslfilter([item[0], 0, item[1], 0] + item[2:], images['new'])
            elif item[0] == 'filter.lightness':
                hslfilter([item[0], 0, 0, item[1]] + item[2:], images['new'])
            elif item[0] == 'filter.fill': 
                if version_gte(7,2):
                    log_warning('fill: This command is deprecated. \
Please use “draw.rect” instead.')
                filter_fill(item, images['new'])
            # Deprecated filters
            elif item[0] == 'hue':
                if version_gte(7):
                    log_warning('hue: The prefixless version of this command \
is deprecated. Please use “filter.hue” instead.')
                hslfilter([item[0], item[1], 0, 0] + item[2:], images['new'])
            elif item[0] == 'saturation':
                if version_gte(7):
                    log_warning('saturation: The prefixless version of this \
command is deprecated. Please use “filter.saturation” instead.')
                hslfilter([item[0], 0, item[1], 0] + item[2:], images['new'])
            elif item[0] == 'lightness':
                if version_gte(7):
                    log_warning('lightness: The prefixless version of this \
command is deprecated. Please use “filter.lightness” instead.')
                hslfilter([item[0], 0, 0, item[1]] + item[2:], images['new'])
            elif item[0] == 'fill':
                if version_gte(7):
                    log_warning('fill: The prefixless version of this command \
is deprecated. Please use “filter.fill” instead.')
                filter_fill(item, images['new'])

            # List commands
            elif item[0] == 'list.add':
                py_method(item[0:3], 'append') # args: var + 1 extra

            elif item[0] == 'list.addall':
                py_method(item[0:3], 'extend') # args: var + 1 extra
            elif item[0] == 'list.clear':
                py_method(item[0:2], 'clear') # args: var + 0 extra
            elif item[0] == 'list.insert':
                py_method(item[0:4], 'insert') # args: var + 2 extra
            elif item[0] == 'list.remove':
                list_remove(item)
            elif item[0] == 'list.replace':
                list_replace(item)
            elif item[0] == 'list.swap':
                list_swap(item)

            # Drawing commands
            elif item[0] == 'setpixel':
                setpixel(item)
            elif item[0] in ('draw.rect', 'draw.rectangle'):
                draw_rect(item) # uses global draw_obj instead of img param
            elif item[0] == 'draw.ellipse':
                draw_ellipse(item) # uses global draw_obj instead of img param
            elif item[0] == 'draw.line':
                draw_line(item) # uses global draw_obj instead of img param
            elif item[0] == 'draw.fillcolor':
                draw_fillcolor(item)
            elif item[0] == 'draw.linecolor':
                draw_linecolor(item)

            # So "end" doesn't get flagged as unknown if we make it to here
            elif item[0] == 'end':
                pass

            # If a block-start command is used in an invalid context
            # (e.g. "else" without an "if"), or the command is unimplemented
            # but reserved for future use, skip to the end of the block
            elif item[0] in block_starts:
                start_depth = block_depths[index]
                while block_depths[index] != start_depth:
                    index += 1
            # At this point, we're at the "end" line but we want to SKIP
            # that so we don't jump back up. Therefore, jumped=False

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

        except Exception as e: 
            # Handle any errors in the command functions so they don’t bring
            # the whole program to a halt
            log_warning(f'{item[0]} command on line {index} \
skipped due to error: {e}')
            
            # If error occurs at start of a block, skip to outside block. 
            # Do this manually (like break,1 in 7.0) because loop_data 
            # doesn't include end lines for if statements
            if item[0] in block_starts:
                start_depth = block_depths[index]
                while block_depths[index] != start_depth:
                    index += 1
            # At this point, we're at the "end" line but we want to SKIP
            # that so we don't jump back up. Therefore, jumped=False

        finally:
            # Note: This block *will* be reached even if "continue" is called
            # in the "try" part of the loop.
            if not jumped:
                index += 1 # STEP
                set_ln(index)
    return images['new'] 

# Returns number of files successfully converted.
def pre_summary(conv_time:float, conv_count:int, new_multi:bool):
    #### STEP 5: SUMMARY ####
    cls()

    if conv_count == 0 and (legacy_multi or new_multi):
        # Break out before we would show summary
        return 0

    summary(conv_time, conv_count)
    return conv_count

def summary(conv_time:float, conv_count:int, warning_page:int=0):
    # Roll warning page over to 0 if needed
    warn_per_page = 6 # TODO: account for multiline warnings
    num_warn_pages = (len(warnings)-1)//warn_per_page + 1
    if warning_page >= num_warn_pages:
        warning_page = 0

    main_text = ['Converted %d file(s) in %s seconds' % 
                 (conv_count, str(round(conv_time, 3)))]
    bottom_text = ''

    if warnings:
        # Add 1 to displayed warning_page because end users
        # expect counting to start at 1
        bottom_text += f'CONVERTER WARNINGS: \
(Page {warning_page+1} of {num_warn_pages})'
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
                    main_text + ['', bottom_text], ('More warnings', 'Okay'), 
                    icon='warning')
            if confirm_exit == 'More warnings':
                summary(conv_time, conv_count, warning_page+1) # next page
            else:
                return
        else:
            # Display dialog with warnings but no extra button
            # if there's only 1 page worth of warnings
            simple_dialog('Conversion complete!', 
                          main_text + ['', bottom_text], icon='warning')
            return
    else:
        simple_dialog('Conversion complete!', main_text,
            'Okay', icon='done')
        return

# List of files to install on first run
# Only download images that a script actually uses
install_list = [
    ['https://raw.githubusercontent.com/mroyale/assets-dx/main/img/game/\
smb_obj.png', 
        'deluxe/smb_obj.png'],
    ['https://raw.githubusercontent.com/mroyale/assets-dx/main/img/game/\
smb_mario.png', 
        'deluxe/smb_mario.png'],
    ['https://raw.githubusercontent.com/mroyale/assets/legacy/img/game/\
smb_map_new.png', 
        'legacy/smb_map_new.png'],
    ['https://raw.githubusercontent.com/mroyale/assets/v7/img/skins/\
smb_skin0.png',
        'legacy7/smb_skin0.png'],
]

# Check if assets need to be (re)installed
def check_assets():
    for i in install_list:
        if not os.path.isfile(f'assets/{i[1]}'): 
            # If a file in the install list is missing, we need to reinstall
            return True

    # If all the files exist, no need to install
    return False

# Install the latest game assets
def install_assets():
    # Create subfolders if they don't exist
    if not os.path.isdir('./assets/deluxe'):
        os.makedirs('./assets/deluxe')
    if not os.path.isdir('assets/legacy'):
        os.makedirs('./assets/legacy')
    if not os.path.isdir('assets/legacy7'):
        os.makedirs('./assets/legacy7')

    for i in install_list:
        try:
            urllib.request.urlretrieve(i[0], f'assets/{i[1]}')
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

    simple_dialog('Success!', 'The images were successfully downloaded.',
                icon='done')
    menu()

# Download and display the online Message of the Day
'''
For each line, everything before the first space is the full list versions 
that should show the message. The rest of the line is the message itself.
The program displays a maximum of 1 MOTD -- the first that matches its version.

EXAMPLE MOTD FORMAT:

# This line is a comment and will be ignored.
u_2.3.0 Deluxifier v3.0.0 is now available!^Click the "View Update" button \
    to open Github and download the update.
# Use caret (^) for newlines.
2.2.1_2.2.2 WARNING: Please update your program to 2.3.0 or later. \
    The version you're currently using has a bug that could damage your files.
* We will only be adding the W.

This version of the program would display "We will only be adding the W."
because it doesn't match any of the versions specified for the warnings.
'''
def motd():
    motd_url = 'https://raw.githubusercontent.com/ClippyRoyale/\
SkinConverter/main/motd.txt'
    try:
        # Download and read MOTD
        urllib.request.urlretrieve(motd_url, 'motd.txt')
        motd_file = open('motd.txt', encoding='utf-8')
        motd_lines = motd_file.read().splitlines()
        motd_data : List[List[str]] = []
        motd_file.close()
        for i in range(len(motd_lines)):
            # Split into version and message
            motd_data[i] = motd_lines[i].split(' ', 1)
            if (len(motd_lines[i]) >= 2) and \
                    ((app_version_str() in motd_data[i][0]) or \
                        (motd_data[i][0] == '*')):
                motd_text = motd_data[i][1].replace('^','\n')
                motd_header = 'News!'
                motd_buttons = ['Exit', 'Continue']
                # Add update button if MOTD is flagged as an update notice
                if 'u' in motd_data[i][0].lower():
                    motd_buttons.insert(0, 'View Update')
                    motd_header = 'Update available'

                motd_continue = button_dialog(motd_header, motd_text, 
                                              tuple(motd_buttons))
                if motd_continue == 'Exit':
                    exit_app()
                elif motd_continue == 'View Update':
                    webbrowser.open('https://github.com/ClippyRoyale/\
SkinConverter/releases/latest')
                    exit_app()
                else: # Continue
                    return
    except Exception:
        # If the internet isn't cooperating or the MOTD file is malformed, 
        # no big deal, just skip it
        pass

def crash(exctype=None, excvalue=None, _=None):
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
        if btn == 'abort':
            exit_app()
        elif btn == 'retry':
            setup()
        # else ignore

def exit_app():
    window.destroy()
    sys.exit()

###########################################################################
#### START THE PROGRAM ####################################################
###########################################################################

try:
    # Comment the next line out to print full crash messages to the console
    # Uncomment this line before releasing updates to the public
    window.report_callback_exception = crash

    setup()

except Exception:
    ei = sys.exc_info()
    crash(None, ei[1])
