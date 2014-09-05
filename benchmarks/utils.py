import os
import sys
from distutils.sysconfig import get_python_lib
import urllib

def link_gst_wrapper():

    dest_dir = get_python_lib()

    gst_packages = ['gobject', 'glib', 'pygst', 'pygst.pyc', 'pygst.pth',
                    'gst-0.10', 'pygtk.pth', 'pygtk.py', 'pygtk.pyc']

    python_version = sys.version[:3]
    global_path = os.path.join('/usr/lib', 'python' + python_version)
    global_sitepackages = [os.path.join(global_path,
                                        'dist-packages'),  # for Debian-based
                           os.path.join(global_path,
                                        'site-packages')]  # for others

    for package in gst_packages:
        for pack_dir in global_sitepackages:
            src = os.path.join(pack_dir, package)
            dest = os.path.join(dest_dir, package)
            if not os.path.exists(dest) and os.path.exists(src):
                os.symlink(src, dest)


def get_data_samples(folder):
    source_url = 'http://parisson.telemeta.org/archives/items/download/PRS_07_01_02.mp3'
    source_file = os.path.join(folder, os.path.basename(source_url))
    if not os.path.exists(source_file):
        urllib.urlretrieve(url=source_url, filename=source_file)
    return source_file
