S-38.3152 NMPS Assignment 1: lTunez
===================================

Overview
--------

ITunez (spelled with Ell, not Eye) is a program that streams audio over RTSP/RTP in 8-bit 8 kHz PCM format.

Requirements
------------

* Python 2.7 (or another version with equivalent functionality)
* The `ffmpeg` command line tool.
* VLC media player, available from the VideoLAN project.

Quick start quide
-----------------

run `python rtp_stream.py`. It will stream sample audio to localhost:6000 over RTP. Make sure you have VLC or
a similar player listening on that port

Hit ^C twice within one second to quit. 

