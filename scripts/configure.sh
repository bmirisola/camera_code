deviceId="0"
v4l2-ctl -d /dev/video$deviceId --set-ctrl=brightness=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=saturation=255
v4l2-ctl -d /dev/video$deviceId --set-ctrl=contrast=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=gain=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=sharpness=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=backlight_compensation=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=white_balance_temperature_auto=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=white_balance_temperature=6500
v4l2-ctl -d /dev/video$deviceId --set-ctrl=exposure_auto=1
v4l2-ctl -d /dev/video$deviceId --set-ctrl=exposure_auto_priority=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=exposure_absolute=1
v4l2-ctl -d /dev/video$deviceId --set-ctrl=focus_auto=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=focus_absolute=0
v4l2-ctl -d /dev/video$deviceId --set-ctrl=led1_mode=0


