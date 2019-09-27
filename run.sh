#!/bin/bash
cd /dados/dev/tensorface-venv/ && source bin/activate
export PYTHONPATH=/Dropbox/py/tensorFace
cd /Dropbox/py/tensorFace && python ./src/gui/tensorFace.py
