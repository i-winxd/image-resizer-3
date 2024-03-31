# REQUIRED PYTHON PACKAGES: Pillow
# pip install pillow
# Run: python [this file] -h
# where -h is for "help"

import argparse
import os
from pathlib import Path
from PIL import Image
from PIL.Image import Resampling

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tga", ".heic"}
EXPORT_FOLDER_PATH = "export"
DEFAULT_SCALE = 10


def create_folder(fp: str) -> None:
    if not os.path.exists(fp):
        os.makedirs(fp)


def resize_image(image: Image.Image, scale: int):
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height), Resampling.NEAREST)
    return resized_image


def process_image(path_to_image: str, save_to: str, scale_factor: int) -> None:
    """Attempt to process path_to_image, exporting it to save_to if possible"""
    _, ext = os.path.splitext(path_to_image)
    if ext not in IMG_EXTS:
        return
    img = Image.open(path_to_image)
    resized: Image.Image = resize_image(img, scale_factor)
    resized.save(save_to)


def process_many_files(all_files: list[str], save_to: str, scale_factor: int, debug_mode: bool) -> None:
    """Attempt to process a directory, saving all images in save_to"""
    for img_path in all_files:
        name_full, _ = os.path.splitext(img_path)
        name_condensed = os.path.basename(name_full)
        if debug_mode:
            print(f"Processing {name_condensed}")
        process_image(img_path, os.path.join(save_to, name_condensed + ".png"), scale_factor)


def main() -> None:
    parser = argparse.ArgumentParser(description="Resizes images using nearest neighbors interpolation")
    parser.add_argument("file_name", type=str, help="Path to an image file or a directory.\n"
                                                    "Image: process that image. "
                                                    "Directory: Process all images in that directory.")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="If a folder is passed, process all subdirectories (but not subdirectories within)")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Prints out when I'm exporting an image")
    parser.add_argument("-s", "--scale", type=int, help="Scale factor (default 10, integers only)")
    parser.add_argument("-e", "--export", type=str, help="Path to export directory (default: export)")

    args = parser.parse_args()
    fp = args.file_name
    recursive = args.recursive
    debug_mode = args.debug
    scale_factor = args.scale if args.scale is not None else DEFAULT_SCALE
    export_directory = args.export if args.export else EXPORT_FOLDER_PATH

    if debug_mode:
        print(f"{fp=}, {recursive=}, {debug_mode=}, {scale_factor=}, {export_directory=}")

    create_folder(export_directory)
    cur_path = Path(fp)

    if not cur_path.exists():
        print("File does not exist.")
        return

    if cur_path.is_dir():
        folder_name = cur_path.name
        save_to_path = os.path.join(export_directory, folder_name)
        create_folder(os.path.join(export_directory, folder_name))
        files_in_dir = [str(file.resolve()) for file in cur_path.iterdir() if file.is_file()]
        process_many_files(files_in_dir, save_to_path, scale_factor, debug_mode)
        if recursive:
            directories_in_dir = [inner_dir for inner_dir in cur_path.iterdir() if inner_dir.is_dir()]
            for directory in directories_in_dir:
                folder_to_make = os.path.join(export_directory, folder_name, os.path.basename(str(directory)))
                create_folder(folder_to_make)
                files_in_subdir = [str(file.resolve()) for file in directory.iterdir() if file.is_file()]
                process_many_files(files_in_subdir, folder_to_make, scale_factor, debug_mode)
    else:
        current_path_str = str(cur_path)
        name, ext = os.path.splitext(current_path_str)
        name_condensed = os.path.basename(name)
        process_image(current_path_str, os.path.join(export_directory, name_condensed + ".png"), scale_factor)


if __name__ == '__main__':
    main()
