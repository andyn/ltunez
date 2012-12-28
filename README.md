S-38.3152 NMPS Assignment 1: lTunez
===================================

Overview
--------

ITunez is a program that streams audio over RTSP/RTP in 8-bit 8 kHz PCM format.

Requirements
------------

* Python 2.7 (or another version with equivalent functionality)
* The `ffmpeg` command line tool.
* VLC media player, available from the VideoLAN project.

Quick start quide
-----------------

There is a directory called mp3. Add some avconv-able files (such as MP3s) there.
Run the server. Run the client.

Usage
-----

Running the server:

    ./ltunez-server

Running the client:

    ./ltunez-client
