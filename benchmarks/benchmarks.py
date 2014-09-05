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

# Get data samples
from utils import get_data_samples
source_file = get_data_samples(cmd_folder)

# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.
import timeside
from timeside.core import get_processor
import urllib
import tempfile


class GstSuite:
    """
    TimeSide benchmark suite for Gstreamer based processors
    """

    def setup(self):
        self.decoder = timeside.decoder.file.FileDecoder(uri=source_file)

    def transcode_ogg(self):
        ogg_file = tempfile.NamedTemporaryFile(suffix='.ogg')
        encoder = timeside.encoder.ogg.VorbisEncoder(ogg_file.name, overwrite=True)
        return (self.decoder | encoder)

    def transcode_mp3(self):
        mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3')
        encoder = timeside.encoder.mp3.Mp3Encoder(mp3_file.name, overwrite=True)
        return (self.decoder | encoder)

    def time_transcode_ogg(self):
        pipe = self.transcode_ogg()
        pipe.run()

    def time_transcode_mp3(self):
        pipe = self.transcode_mp3()
        pipe.run()

    ## def mem_transcode_ogg(self):
    ##     pipe = self.transcode_ogg()
    ##     pipe.run()
    ##     return pipe

    ## def mem_transcode_mp3(self):
    ##     pipe = self.transcode_mp3()
    ##     pipe.run()
    ##     return pipe


class AnalyzerSuite:
    """
    TimeSide benchmark suite for Analyzer processors
    """

    def setup(self):
        self.decoder = timeside.decoder.file.FileDecoder(uri=source_file)

    def _benchmark_analyzer(self, analyzer_id, benchmark_type='time'):
        analyzer = get_processor(analyzer_id)()
        pipe = (self.decoder | analyzer)
        pipe.run()
        print pipe.results.keys()
        if benchmark_type == 'mem':
            return pipe

    # MeanDCShift
    def time_MeanDCShift(self):
        self._benchmark_analyzer('mean_dc_shift', benchmark_type='time')

    ## def mem_MeanDCShift(self):
    ##     return self._benchmark_analyzer('mean_dc_shift', benchmark_type='mem')

    #Level
    def time_Level(self):
        self._benchmark_analyzer('level', benchmark_type='time')

    ## def mem_Level(self):
    ##     return self._benchmark_analyzer('level', benchmark_type='mem')

    ## # VampSimpleHost
    ## def time_VampSimpleHost(self):
    ##     self._benchmark_analyzer('vamp_simple_host', benchmark_type='time')

    ## def mem_VampSimpleHost(self):
    ##     return self._benchmark_analyzer('vamp_simple_host',
    ##                                     benchmark_type='mem')

    ## # AubioMelEnergy
    ## def time_AubioMelEnergy(self):
    ##     self._benchmark_analyzer('aubio_melenergy', benchmark_type='time')

    ## def mem_AubioMelEnergy(self):
    ##     return self._benchmark_analyzer('aubio_melenergy', benchmark_type='mem')

    ## # AubioMfcc
    ## def time_AubioMfcc(self):
    ##     self._benchmark_analyzer('aubio_mfcc', benchmark_type='time')

    ## def mem_AubioMfcc(self):
    ##     return self._benchmark_analyzer('aubio_mfcc', benchmark_type='mem')

    ## # AubioPitch
    ## def time_AubioPitch(self):
    ##     self._benchmark_analyzer('aubio_pitch', benchmark_type='time')

    ## def mem_AubioPitch(self):
    ##     return self._benchmark_analyzer('aubio_pitch', benchmark_type='mem')

    ## # AubioSpecdesc
    ## def time_AubioSpecdesc(self):
    ##     self._benchmark_analyzer('aubio_specdesc', benchmark_type='time')

    ## def mem_AubioSpecdesc(self):
    ##     return self._benchmark_analyzer('aubio_specdesc', benchmark_type='mem')

    ## # AubioTemporal
    ## def time_AubioTemporal(self):
    ##     self._benchmark_analyzer('aubio_temporal', benchmark_type='time')

    ## def mem_AubioTemporal(self):
    ##     return self._benchmark_analyzer('aubio_temporal', benchmark_type='mem')

    ## # IRITMonopoly
    ## def time_IRITMonopoly(self):
    ##     self._benchmark_analyzer('irit_monopoly', benchmark_type='time')

    ## def mem_IRITMonopoly(self):
    ##     return self._benchmark_analyzer('irit_monopoly', benchmark_type='mem')

    ## # IRITStartSeg
    ## def time_IRITStartSeg(self):
    ##     self._benchmark_analyzer('irit_startseg', benchmark_type='time')

    ## def mem_IRITStartSeg(self):
    ##     return self._benchmark_analyzer('irit_startseg', benchmark_type='mem')

    # IRITSpeech4Hz
    def time_IRITSpeech4Hz(self):
        self._benchmark_analyzer('irit_speech_4hz', benchmark_type='time')

    ## def mem_IRITSpeech4Hz(self):
    ##     return self._benchmark_analyzer('irit_speech_4hz', benchmark_type='mem')

    # IRITSpeechEntropy
    def time_IRITSpeechEntropy(self):
        self._benchmark_analyzer('irit_speech_entropy', benchmark_type='time')

    ## def mem_IRITSpeechEntropy(self):
    ##     return self._benchmark_analyzer('irit_speech_entropy', benchmark_type='mem')

    ## # LimsiSad
    ## def time_LimsiSad(self):
    ##     self._benchmark_analyzer('limsi_sad', benchmark_type='time')

    ## def mem_LimsiSad(self):
    ##     return self._benchmark_analyzer('limsi_sad', benchmark_type='mem')

    # Spectrogram
    def time_Spectrogram(self):
        self._benchmark_analyzer('spectrogram_analyzer', benchmark_type='time')

    ## def mem_Spectrogram(self):
    ##     return self._benchmark_analyzer('spectrogram_analyzer',
    ##                                     benchmark_type='mem')

    # OnsetDetectionFunction
    def time_OnsetDetectionFunction(self):
        self._benchmark_analyzer('odf', benchmark_type='time')

    ## def mem_OnsetDetectionFunction(self):
    ##     return self._benchmark_analyzer('odf', benchmark_type='mem')

    # Waveform
    def time_Waveform(self):
        self._benchmark_analyzer('waveform_analyzer', benchmark_type='time')

    ## def mem_Waveform(self):
    ##     return self._benchmark_analyzer('waveform_analyzer',
    ##                                     benchmark_type='mem')

    ## # Yaafe
    ## def time_Yaafe(self):
    ##     self._benchmark_analyzer('yaafe', benchmark_type='time')

    ## def mem_Yaafe(self):
    ##     return self._benchmark_analyzer('yaafe', benchmark_type='mem')
