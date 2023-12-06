from conexao_arduino.arduino_connection import ArduinoConnection

import threading as th
import time
import queue


class ArduinoControl:
    THREAD_TIMEOUT = 5  # in seconds
    QUEUE_SIZE = 1
    
    def __init__(self):
        self._arduino_conn = None
        self._read_data_queue = queue.Queue(self.QUEUE_SIZE)
        self._running = False

        self.connect()

    def connect(self):
        if self._arduino_conn is not None:
            # Already connected
            return
        try:
            self._arduino_conn = ArduinoConnection("/dev/ttyACM0")
            self._arduino_conn.connect()
        except Exception as e:
            print(f"[ArduinoControl] {e}")

    def disconnect(self):
        self._running = False
        try:
            self._read_data_queue.get_nowait()
        except queue.Empty:
            pass
        self._arduino_conn.close()
        self._arduino_conn = None

    def read_sensor(self):
        try:
            data = self._read_data_queue.get()
            return data
        except queue.Empty:
            return None
        
    def spin_motor_clockwise(self):
        self._arduino_conn.send_data("A")

    def spin_motor_anticlockwise(self):
        self._arduino_conn.send_data("D")

    def start_motor(self):
        self._arduino_conn.send_data("S")
        if not self._running:
            self._running = True
            self._reader_thread = th.Thread(target=self._sensor_reader)
            self._reader_thread.start()

    def stop_motor(self):
        self._arduino_conn.send_data("P")
        if self._running:
            self._running = False
            self._clear_queue()
            self._reader_thread.join()

    def _clear_queue(self):
        while True:
            try:
                self._read_data_queue.get_nowait()
            except queue.Empty:
                break

    def _sensor_reader(self):
        while self._running:
            try:
                reading = self._arduino_conn.receive_data()
                if reading is not None:
                    reading = round(float(reading)/9.81, 2)
                    self._read_data_queue.put_nowait(reading)
            except queue.Full:
                pass
            time.sleep(0.1)

    def __del__(self):
        self.disconnect()
