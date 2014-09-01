# Put Benchmark directory in sys.path to import `utils` module
# source: http://stackoverflow.com/a/6098238/3985889
import os
import sys
import inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(
    inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# Link Gstreamer wrappers into conda environment
from utils import link_gst_wrapper
link_gst_wrapper()


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

    def transcode_mp3(self):
        mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3')
        dec = timeside.decoder.file.FileDecoder(uri=self.source_file.name)
        enc = timeside.encoder.mp3.Mp3Encoder(mp3_file.name, overwrite=True)
        pipe = (dec | enc)
        pipe.run()

    def time_transcode_ogg(self):
        self.transcode_ogg()

    def time_transcode_mp3(self):
        self.transcode_mp3()

    def mem_transcode_ogg(self):
        self.transcode_ogg()


class AnalyzerSuite:
    """
    TimeSide benchmark suite for Analyzer processors
    """

    def setup(self):
        #source_url = 'http://parisson.telemeta.org/archives/items/download/PRS_07_01_03.mp3'
        source_url = 'http://parisson.telemeta.org/archives/items/download/PRS_07_01_02.mp3'
        self.source_file = tempfile.NamedTemporaryFile(suffix='.mp3')
        urllib.urlretrieve(url=source_url, filename=self.source_file.name)

    def _benchmark_analyzer(self, analyzer_cls):
        dec = timeside.decoder.file.FileDecoder(uri=self.source_file.name)
        analyzer = analyzer_cls()
        pipe = (dec | analyzer)
        pipe.run()


list_analyzers = timeside.core.processors(timeside.api.IAnalyzer)
for analyzer_cls in list_analyzers:
    #if analyzer_cls in ['vamp-simple-host']:
    #    continue
    test_func = lambda self: self._benchmark_analyzer(analyzer_cls)
    setattr(AnalyzerSuite, 'time_'+analyzer_cls.id(),  test_func)
