#!/bin/sh

mjpg_streamer \
    -i "input_file.so \
        -f /home/pi/opencv-mazesolver/src/httpdocs \
        -n img.png -d 0.024" \
    -o "output_http.so \
        -p 9001 \
        -l 127.0.0.1"
