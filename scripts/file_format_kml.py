# Methods to adjust KMLs' format to the one that querying script expects.
from glob import glob
from os.path import basename
import re


def add_kml_header_footer(filename):
    bname = basename(filename)
    crop = bname.split('.')[0].split('_')[1]
    label = bname.split('.')[0].split('_')[2]
    footer = "</Folder>\n</Document></kml>"
    header = """<?xml version="1.0" encoding="utf-8" ?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document id="root_doc">
    <Folder><name>{}{}</name>""".format(crop, label)
    print(header)

    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(header + '\n' + content + footer)
        f.flush()
        f.close()


def replace(filename: str, old: str, new: str):
    with open(filename, 'r+') as file:
        filedata = file.read()
        # Replace the target string
        filedata = filedata.replace(old, new)
        # Write the file out again
        file.write(filedata)
        file.flush()
        file.close()


def replace_regex(filename, old, new):
    with open(filename, 'r+') as file:
        content = file.read()
        content_new = re.sub(old, new, content, flags=re.M)
        file.seek(0, 0)
        file.write(content_new)
        file.truncate()
        file.flush()
        file.close()


def remove_leading_spaces(filename):
    replace_regex(filename, '^\\s*', r'')


def parse_kml():
    folder = '../../clustering/labeled_KML/'
    files = glob(folder + "*kml")
    for file in files:
        filepath = folder + file
        add_kml_header_footer(filepath)
        remove_leading_spaces(filepath)
        replace_regex(filepath, r'\r\n', r'\n')
        replace_regex(filepath, old=r'</coordinates>\n', new=r'</coordinates>')
        replace_regex(filepath, old=r'</coordinates>\s+', new=r'</coordinates>')
        replace_regex(filepath, old=r'</coordinates>.?-', new=r'</coordinates>-')
        replace_regex(filepath, old=r'\n</Placemark>', new=r'</Placemark>')
        replace_regex(filepath, old=r'\n<Placemark>', new=r'<Placemark>')
