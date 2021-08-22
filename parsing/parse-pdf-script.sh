#!/bin/bash

MEDIA_NAME="$1"
pdftotext -layout ../media-scripts/$MEDIA_NAME/"$MEDIA_NAME".pdf ../media-scripts/$MEDIA_NAME/"$MEDIA_NAME".txt
python extract-quotes.py