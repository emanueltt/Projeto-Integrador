#!/bin/bash

v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c auto_exposure=1
v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_automatic_continuous=0

v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c exposure_time_absolute=500
v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_absolute=3
v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_absolute=4
