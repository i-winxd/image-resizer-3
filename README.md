# Image Resizer 3

Quick Python module to resize images using nearest neighbors interpolation, which prevents messing up pixel art

By default, images will be exported in `./export/`. The folder will be created if not already.

Required modules: `Pillow` (`pip install pillow`)

Works on Python 3.9 onwards. Use `python resize.py` with arguments. This program is intended for those with experience using and running Python applications; if you dedicate two hours to being able to run a simple "hello world" program in your command line, you should be able to run this.

```
usage: resize.py [-h] [-r] [-d] [-s SCALE] [-e EXPORT] file_name

Resizes images using nearest neighbors interpolation

positional arguments:
  file_name             Path to an image file or a directory. 
                        Image: process that image. 
                        Directory: Process all images in that directory.

options:
  -h, --help            show this help message and exit
  -r, --recursive       If a folder is passed, process all subdirectories (but not subdirectories within)
  -d, --debug           Prints out when I'm exporting an image
  -s SCALE, --scale SCALE
                        Scale factor (default 10, integers only)
  -e EXPORT, --export EXPORT
                        Path to export directory (default: export)
```

How command arguments work:

- Positional arguments are mandatory. You can put it right after the program name or at the end of the command.
- Optional arguments are in `[SQUARE BRACKETS]` as seen in `usage`. The ALL CAPS words are to be substituted. For example, `python resize.py -r -d -s 10 -e export file_name`
