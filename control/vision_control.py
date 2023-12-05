import cv2
import os
import threading as th
import time
import queue

from ROI.image_process import process_image, process_image2


class VisionControl:
    THREAD_TIMEOUT = 5  # in seconds
    QUEUE_SIZE = 1
    
    def __init__(self):
        self._camera = None
        self._measurement_data_queue = queue.Queue(self.QUEUE_SIZE)
        self._image_queue = queue.Queue(self.QUEUE_SIZE)
        self._running = False

        self.connect()

    def connect(self):
        if self._camera is not None:
            # Already connected
            return
        
        try:
            self._camera = cv2.VideoCapture("/dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0")

            if not self._camera.isOpened():
                raise ConnectionError("Could not connect to the camera!")

            self._configure_camera()
        except Exception as e:
            print(f"[VisionControl] {e}")

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
            self._measurement_data_queue.get_nowait()
        except queue.Empty:
            pass
        self._camera.release()
        self._camera = None

    def adjust_camera_focus(self, focus_value: int):
        if focus_value < 0 or focus_value > 10:
            raise ValueError(f"[VisionControl] Invalid focus_value. Valid value range is between 0 and 10.")
        os.system(f"v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_absolute={focus_value}")

    def calibrate_camera(self):
        raise NotImplementedError

    def get_measurement(self):
        try:
            data = self._measurement_data_queue.get_nowait()
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

            process_image = frame.copy()

            # Define the coordinates of the top-left and bottom-right corners of the region you want to crop
            x1, y1 = 50, 200  # Top-left corner
            x2, y2 = 900, 270  # Bottom-right corner

            # Crop the region
            process_image = process_image[y1:y2, x1:x2]

            # Process image
            process_result = process_image2(process_image)

            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            self._try_add_image_to_queue(frame)
            if process_result is None:
                continue

            # Put result into the queue
            try:
                self._measurement_data_queue.put_nowait(process_result)
            except queue.Full:
                pass

    def _try_add_image_to_queue(self, image):
        try:
            self._image_queue.put_nowait(image)
        except queue.Full:
            return

    def __del__(self):
        self.disconnect()
