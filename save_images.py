def run_camera_save_loop():
    import cv2

    camera = cv2.VideoCapture("/dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0")

    if not camera.isOpened():
        print("Could not open camera")
        return

    height = 720
    width = int(height * 1.5)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    frame_counter = 0
    save_images = False
    while True:
        _, frame = camera.read()
        frame_counter += 1

        # Define the coordinates of the top-left and bottom-right corners of the region
        # you want to crop
        x1, y1 = 200, 170  # Top-left corner
        x2, y2 = 900, 360  # Bottom-right corner

        # Crop the region
        frame = frame[y1:y2, x1:x2]

        cv2.imshow("video", frame)

        if save_images:
            cv2.imwrite(f"image_{frame_counter}.png", frame)

        key = cv2.waitKey(1)
        if key == -1:
            continue
        elif key == 27:
            break
        elif key == 32:
            if save_images:
                save_images = False
            else:
                save_images = True
        else:
            print(key)

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_camera_save_loop()
