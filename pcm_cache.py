# -*- encoding: utf-8 -*-

"""
Caches PCM audio files in a directory.
Uses the avconv command line tool to convert audio files to 8000 Hz mono PCM files.
"""

# FIXME -- The code is full of references to avconv (from libav) even though we use FFmpeg.

import os
from os import path
import subprocess

class PCMCache(object):
    """Caches PCM audio files in a directory."""

    def __init__(self,
                 cache_dir = "cache",
                 source_dir = "audio",
                 avconv_path = 'ffmpeg',
                 cache_suffix = '.wav'):
        """Create a new PCMCache.

        Keyword arguments:
        cache_dir -- the cache directory (default: current working directory)
        source_dir -- the source directory (default: current working directory)
        avconv_path -- path to the ffmpeg command (default: assumed to be in PATH)
        cache_suffix -- suffix for files in the cache directory. FIXME: currently must be .wav

        """
        # Check that the cache directory exists
        if not cache_dir:
            cache_dir = os.getcwd()
        self.cache_dir = path.abspath(cache_dir)
        if not path.isdir(self.cache_dir):
            raise RuntimeError("PCM cache directory "
                               "'{!s}' does not exist.".format(self.cache_dir))
        # Check that the audio source directory exists
        if not source_dir:
            source_dir = os.getcwd()
        self.source_dir = path.abspath(source_dir)
        if not path.isdir(self.cache_dir):
            raise RuntimeError("Audio source directory"
                               "'{!s}' does not exist.".format(self.cache_dir))
        # Set FFmpeg path
        self.avconv_path = avconv_path
        # Initialize the cache
        self.cache_suffix = cache_suffix
        self.cached_files = set()
        self.refresh()

    def get_cached_files(self):
        return list(self.cached_files)

    def refresh(self):
        self.refresh_source()
        self.refresh_cache()

    def refresh_cache(self):
        """Refresh the cache directory"""
        for root, directories, files in os.walk(self.cache_dir):
            for filename in files:
                if filename.endswith(self.cache_suffix):
                    self.cached_files.add(path.join(root, filename))

    def refresh_source(self):
        """Refresh the source audio directory"""
        for root, directories, files in os.walk(self.source_dir):
            for filename in files:
                # Do not add cached files, if case the source
                # and cache directories are the same.
                if filename.endswith(self.cache_suffix):
                    continue
                # Generate the corresponding file name that will
                # be generated to the cache directory.
                cachefilename = path.join(self.cache_dir, filename + self.cache_suffix)
                # Run the converter if the cache file does not exist
                if not path.exists(cachefilename):
                    self.add_file(path.join(root, filename), cachefilename)

    def add_file(self, source, target):
        with open(os.devnull, "wb") as null:
            # -i source.mp3 -acodec pcm_mulaw -ar 8000 -ac 1 asd_8k.wav
            subprocess.call([self.avconv,
                             '-i', source, # source file name
                             '-acodec', 'pcm_mulaw', # 8-bit µ-law
                             '-ar', '8000', # 8000 Hz
                             '-ac', '1', # mono
                             target # output file name in cache directory
                            ], stdout = null, stderr = null)
        except:
            print "Fatal: system has no /dev/null or equivalent bit bucket."



if __name__ == "__main__":
    print "Updating cache."
    p = PCMCache()
    print "Cache updated! Current files:"
    for filename in p.get_cached_files():
        print " ", filename
