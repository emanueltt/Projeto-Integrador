import serial
import threading as th
import time
from modules.timer import TimerSeconds


class ArduinoConnection:
    def __init__(self, device_port: str, baud_rate=9600):
        self.device_port = device_port
        self.baud_rate = baud_rate
        self.serial_port = None

    def connect(self):
        self.serial_port = serial.Serial(self.device_port, self.baud_rate)

        # Perform handshake
        timer = TimerSeconds()
        timeout = 5
        while timer.elapsed_time() < timeout:
            self.send_data("H")
            data = self.receive_data()
            if data == "A":
                return
            time.sleep(0.2)
        else:
            raise TimeoutError()

    def receive_data(self):
        """
        The function receives data from the Arduino board and sends an acknowledgment
        back to the Arduino.
        :return: The data received from the Arduino board is being returned.
        """
        if self.serial_port is None:
            raise Exception("You need to connect to the Arduino board first!")
        if self.serial_port.in_waiting > 0:
            data = self.serial_port.readline().decode().strip()
            if data:
                return data

    def send_data(self, data: str):
        if self.serial_port is None:
            raise Exception("You need to connect to the Arduino board first!")
        self.serial_port.write(data.encode())

    def close(self):
        if self.serial_port is not None:
            self.serial_port.close()

    def __del__(self):
        self.close()


def connection_thread(conn: ArduinoConnection):
    timer = TimerSeconds()
    while True:
        try:
            data = conn.receive_data()
            print("passou")
        except TypeError:
            print()
            break
        if data is not None:
            print(f"Got data: {data}")
        if timer.elapsed_time() >= 2:
            conn.send_data("P")
            break


def run_camera_loop():
    import cv2

    camera = cv2.VideoCapture("/dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0")
    # camera = cv2.VideoCapture(0)

    height = 480
    width = int(height * 1.5)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    frame_counter = 0

    while True:
        _, frame = camera.read()
        frame_counter += 1

        cv2.imshow("video", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == -1:
            continue
        # elif key == 32:
        #     cv2.imwrite(f"image_{height}p_{frame_counter}.png", frame)
        # else:
        #     print(key)

    camera.release()
    cv2.destroyAllWindows()


def run_dummy_loop():
    timer = TimerSeconds()
    while True:
        if timer.elapsed_time() >= 5:
            break


if __name__ == "__main__":
    #
    # Example usage
    #

    serial_port = "/dev/ttyACM0"  # Replace with the actual port
    arduino_conn = ArduinoConnection(serial_port)
    print("Connecting...")
    arduino_conn.connect()
    print("Connected!")
    print("Sending start command")
    arduino_conn.send_data("P")
    arduino_conn.send_data("S")

    conn_thread = th.Thread(
        target=connection_thread,
        args=[
            arduino_conn,
        ],
    )
    conn_thread.daemon = True
    conn_thread.start()

    try:
        # run_camera_loop()
        run_dummy_loop()

    except KeyboardInterrupt:
        conn_thread.join()
        arduino_conn.close()
