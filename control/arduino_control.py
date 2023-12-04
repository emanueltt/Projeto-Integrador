from conexao_arduino.arduino_connection import ArduinoConnection

import threading as th
import queue


class ArduinoControl:
    THREAD_TIMEOUT = 5  # in seconds
    QUEUE_SIZE = 3
    
    def __init__(self):
        self._arduino_conn = None
        self._read_data = queue.Queue(self.QUEUE_SIZE)
        self._running = False

        self.connect()

    def connect(self):
        if self._arduino_conn is not None:
            # Already connected
            return
        self._arduino_conn = ArduinoConnection("/dev/ttyACM0")
        self._arduino_conn.connect()

    def disconnect(self):
        self._running = False
        try:
            self._read_data.get_nowait()
        except queue.Empty:
            pass
        self._arduino_conn.close()
        self._arduino_conn = None

    def read_sensor(self):
        try:
            data = self._read_data.get_nowait()
            return data
        except queue.Empty:
            return None

    def start_motor(self):
        self._arduino_conn.send_data("S")
        if not self._running:
            self._running = True
            self._reader_thread = th.Thread(target=self._sensor_reader)
            self._reader_thread.daemon = True
            self._reader_thread.start()

    def stop_motor(self):
        self._arduino_conn.send_data("P")
        if self._running:
            self._running = False
            self._reader_thread.join(self.THREAD_TIMEOUT)
    
    def _sensor_reader(self):
        while self._running:
            try:
                self._read_data.put_nowait(self._arduino_conn.receive_data())
            except queue.Full:
                continue

    def __del__(self):
        self.disconnect()
