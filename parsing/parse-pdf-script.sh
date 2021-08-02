#!/bin/bash
MEDIA_NAME="$1"
PDF_SCRIPT_URL="$2"
curl -o media-scripts/$MEDIA_NAME/"$MEDIA_NAME".pdf PDF_SCRIPT_URL
pdftotext -layout media-scripts/$MEDIA_NAME/"$MEDIA_NAME".pdf media-scripts/$MEDIA_NAME/"$MEDIA_NAME".txt
python extract-quotes.py