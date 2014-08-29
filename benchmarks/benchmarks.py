# Link Gstreamer wrappers into conda environment
import os
import sys
from distutils.sysconfig import get_python_lib

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

# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.
import timeside
import urllib
import tempfile


class GstSuite:
    """
    TimeSide benchmark suite for Gstreamer based processors
    """

    def setup(self):
        #source_url = 'http://parisson.telemeta.org/archives/items/download/PRS_07_01_03.mp3'
        source_url = 'http://parisson.telemeta.org/archives/items/download/PRS_07_01_02.mp3'
        self.source_file = tempfile.NamedTemporaryFile(suffix='.mp3')
        urllib.urlretrieve(url=source_url, filename=self.source_file.name)

    def transcode_ogg(self):
        ogg_file = tempfile.NamedTemporaryFile(suffix='.ogg')
        dec = timeside.decoder.file.FileDecoder(uri=self.source_file.name)
        enc = timeside.encoder.ogg.VorbisEncoder(ogg_file.name, overwrite=True)
        pipe = (dec | enc)
        pipe.run()

    def time_transcode_ogg(self):
        self.transcode_ogg()

    def mem_transcode_ogg(self):
        self.transcode_ogg()
