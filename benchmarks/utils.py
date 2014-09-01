import os
import sys
from distutils.sysconfig import get_python_lib


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
