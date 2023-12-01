import cv2
import os
import threading as th
import time
import queue


class VisionControl:
    THREAD_TIMEOUT = 5  # in seconds
    
    def __init__(self):
        self._camera = None
        self._measurement_data = queue.Queue(1)
        self._running = False

        self.connect()

    def connect(self):
        if self._camera is not None:
            # Already connected
            return
        self._camera = cv2.VideoCapture("/dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0")

        if not self._camera.isOpened():
            raise ConnectionError("Could not connect to the camera!")

        self._configure_camera()

    def _configure_camera(self):
        height = 720
        width = int(height * 1.777)  # Keep aspect ratio

        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        os.system('v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c auto_exposure=1')
        time.sleep(0.2)
        os.system('v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_automatic_continuous=0')
        time.sleep(0.2)
        os.system("v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c exposure_time_absolute=500")

    def disconnect(self):
        self._running = False
        try:
            self._measurement_data.get_nowait()
        except queue.Empty:
            pass
        self._camera.release()
        self._camera = None

    def adjust_camera_focus(self, focus_value: int):
        if focus_value < 0 or focus_value > 10:
            raise ValueError(f"Invalid focus_value. Valid value range is between 0 and 10.")
        os.system(f"v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_absolute={focus_value}")

    def calibrate_camera(self):
        raise NotImplementedError

    def get_measurement(self):
        try:
            data = self._measurement_data.get_nowait()
            return data
        except queue.Empty:
            return None

    def start_processing(self):
        if not self._running:
            self._running = True
            self._processing_thread = th.Thread(target=self._image_processor)
            self._processing_thread.daemon = True
            self._processing_thread.start()

    def stop_processing(self):
        if self._running:
            self._running = False
            self._processing_thread.join(self.THREAD_TIMEOUT)

    def _image_processor(self):
        while self._running:
            # Read image
            _, frame = self._camera.read()
            if frame is None:
                continue

            # Process image

            # Put result into the queue
            process_result = "resultado distancia"
            self._measurement_data.put(process_result)

    def __del__(self):
        self.disconnect()