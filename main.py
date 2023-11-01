from conexao_arduino.arduino_connection import ArduinoConnection
from ROI.image_process import process_image2
import threading as th
import time


def connection_thread(conn: ArduinoConnection):
    while True:
        try:
            data = conn.receive_data()
        except TypeError:
            print()
            break
        if data is None:
            print("Got no data")
        else:
            print(f"Got data: {data}")
        time.sleep(1)


def run_camera_loop():
    import cv2

    camera = cv2.VideoCapture("/dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0")

    if not camera.isOpened():
        print("Could not open camera")
        return
    # camera = cv2.VideoCapture(0)

    height = 720
    width = int(height * 1.5)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    frame_counter = 0

    while True:
        _, frame = camera.read()
        frame_counter += 1

        # Define the coordinates of the top-left and bottom-right corners of the region you want to crop
        x1, y1 = 200, 170  # Top-left corner
        x2, y2 = 900, 360  # Bottom-right corner

        # Crop the region
        frame = frame[y1:y2, x1:x2]

        frame = process_image2(frame)

        # frame = process_image(frame)
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


if __name__ == "__main__":
    #
    # Example usage
    #
    serial_port = "/dev/ttyACM0"  # Replace with the actual port
    arduino_conn = ArduinoConnection(serial_port)
    print("Connecting...")
    arduino_conn.connect()
    print("Connected to Arduino!")

    conn_thread = th.Thread(
        target=connection_thread,
        args=[
            arduino_conn,
        ],
    )
    conn_thread.daemon = True
    conn_thread.start()

    try:
        run_camera_loop()
    except KeyboardInterrupt:
        arduino_conn.close()
        conn_thread.join()
