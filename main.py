import glob
import os
from datetime import datetime

import click
import piexif
from PIL import Image
from tqdm import tqdm


def get_filelist(root):
    """
    Get list of file path

    :param root: root path
    :type root: str
    :return: list of file path
    :rtype: list[str]
    """
    return glob.glob(os.path.join(root, '**', '*.jpg'), recursive=True)


def parse_datetime(filepath):
    """
    Parse filepath into desired EXIF datetime string

    - Input: '/Users/yuthon/Downloads/2018030923592200-F1C11A22FAEE3B82F21B330E1B786A39.jpg'
    - Output: '2018:03:09 23:59:22'

    :param filepath:
    :type filepath:
    :return: parsed datetime string
    :rtype: str
    """
    date_str = os.path.basename(filepath).split('-')[0][:-2]
    date_time = datetime.strptime(date_str, '%Y%m%d%H%M%S')
    return date_time.strftime("%Y:%m:%d %H:%M:%S")


def modify_exif(filepath) -> None:
    """
    Modify EXIF information of given filepath

    :param filepath: given path of image file
    :type filepath: str
    """
    im = Image.open(filepath)
    exif_dict = piexif.load(im.info["exif"])
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = parse_datetime(filepath)
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filepath)


@click.command()
@click.argument('root-path')
def add_datetime_to_exif(root_path):
    filelist = get_filelist(root_path)
    for filepath in tqdm(filelist):
        modify_exif(filepath)


if __name__ == '__main__':
    add_datetime_to_exif()
