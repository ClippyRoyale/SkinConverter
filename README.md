# MRoyale Skin Converter

Source code and documentation copyright (C) 2022–2025 ClippyRoyale

## What is this?

This is a GUI-based program for converting skins or other sprite sheets for different versions of the browser game MRoyale. You can convert:
* Legacy v5 (16×32) skins to Legacy v7 (32×32) format
* Deluxe skins to Legacy format (v5 or v7)
* Remake skins to Legacy format
* Legacy smb_map to smb_map_new
* You can also remove the semi-transparent template background from your skins, if you saved your skin image with the template left in by mistake.

While this program is not designed for maximum efficiency (it is written in Python after all), it’s still pretty fast. For example, I tested v5.2.1 and it was able to convert 69 skins per second from Legacy to Deluxe. (That functionality is now deprecated since MR Deluxe is dead.)

## Why is this useful?

Let’s say you made a skin that was in MR Remake or MR Deluxe and you want to use it in MR Legacy, but you don’t want to spend half an hour remaking all your skins manually because you’d just be doing the same thing over and over.

Or let’s say you’re the owner of MR Legacy and you want to add swimming and taunt sprites to the game but it feels like an impossible task because you’d have to add them to every existing skin. What do you do?

Simple: use the skin converter! It’ll convert your old skins into files you can use with the latest version of the game!

## How do I use it?

1. Install the latest version of Python at https://python.org if you don’t have it already.
2. Download the source code at https://github.com/ClippyRoyale/SkinConverter/releases/latest (click on “Source code (zip)” in the Assets section).
3. Unzip the file you just downloaded.
4. Double-click “converter.py” to open the code in IDLE.
5. Go to the Run menu and click Run Module.
6. Enjoy!

If you’re unable to install Python or download the source code (e.g. because you’re on a school computer), there is also a deprecated online version (based on v7.6.3) hosted on Replit. This version will not receive updates past v7.x, but I’ve kept it online as a last-resort option. This program is provided AS IS. Please do not expect me to provide any troubleshooting or bug fixes. Link: https://replit.com/@WaluigiRoyale/MR-Converter-GUI (You’ll need to create a Replit account and click the Fork button. From there, follow the instructions that pop up when you run the program.)

## System Requirements
This program doesn't have a very attractive interface. This is because I'd rather spend my time making the program *work*. In fact, it'll work on basically any operating system released in the last 15 years.

It should theoretically run on any operating system that can run Python 3.6 (though I've only ever tested it as far back as Python 3.7):
* MacOS 10.6 or later
* Windows Vista or later, if you're using the official Python installation
  * If you're *really* crazy, there are various unofficial Python 3.7 releases for Windows XP — or you can use the deprecated online version via the Supermium browser.

You should also be able to use it on Linux as well, but there are too many variations of that for me to provide any guarantees.

## Troubleshooting

### I can’t get it to run! All I see is a blank screen!

Try clicking “Stop” then clicking “Run” again. If that doesn’t work, clear your cache ( ͡° ͜ʖ ͡°)

### I downloaded the code, and when I run the program, it's in fullscreen!

You have a really old version of this app. Please download the newest version from the "Releases" section in the sidebar.
