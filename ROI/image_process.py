# Distacia linhas
import cv2
import numpy as np
from .libs.line_detector_all import LineDetectorAll
from .libs import Rectangle, Scene
from .libs import draw_line_1

# %matplotlib inline


def process_image(img):
    img_gray = img[400:800, 350:850]
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.bilateralFilter(img_gray, 5, 20, 20)

    sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=9)

    opening = np.sqrt(sobel_y**2)
    opening = (np.mean(opening, axis=0)) - np.min(np.mean(opening, axis=0))

    rois = []
    n_cont = 0
    save_it = 0
    pause_cont = 0

    for i in opening:
        if i > np.mean(opening):
            if pause_cont <= 0:
                save_it = 1

        if save_it:
            rois.append(n_cont)
            pause_cont = 100
            save_it = 0

        n_cont += 1
        pause_cont -= 1

    try:
        rect_1 = Rectangle(
            x=rois[0] - 20, y=int(img_gray.shape[0] / 4), rz=0, w=100, h=100
        )

        rect_2 = Rectangle(
            x=rois[1] - 20, y=int(img_gray.shape[0] / 3), rz=0, w=100, h=100
        )
        # rect_3 = Rectangle(x=rois[2] - 20, y=int(img_gray.shape[0] / 3), rz=0, w=100, h=100)
    except IndexError:
        return img_gray

    roi_1 = rect_1.crop_from_img(img_gray)
    roi_2 = rect_2.crop_from_img(img_gray)
    # roi_3 = rect_3.crop_from_img(img_gray)

    l_Detector_1 = LineDetectorAll(9, True, False, True)
    l_Detector_2 = LineDetectorAll(9, True, False, True)
    # l_Detector_3 = LineDetectorAll(9, True, False, True)

    line_1 = l_Detector_1.detect(roi_1)
    line_2 = l_Detector_2.detect(roi_2)
    # line_3 = l_Detector_3.detect(roi_3)

    # Scenes
    scene_1 = Scene()
    scene_1.add(rect_1, "rect_1", None)
    scene_1.add(rect_2, "rect_2", None)
    # scene_1.add(rect_3, "rect_3", None)
    scene_1.add(line_1, "line_1", "rect_1")
    scene_1.add(line_2, "line_2", "rect_2")
    # scene_1.add(line_3, "line_3", "rect_3")

    # Global lines
    line_1_global = scene_1.get_global("line_1")
    line_2_global = scene_1.get_global("line_2")
    # line_3_global = scene_1.get_global("line_3")

    img_lines = img_gray
    draw_line_1(img_lines, line_1_global, color=255, linewidth=4, transparency=0.0)
    draw_line_1(img_lines, line_2_global, color=255, linewidth=4, transparency=0.0)

    text_distance = f"{line_2_global[0] - line_1_global[0]} px"
    img_lines = cv2.putText(
        img_lines,
        text=text_distance,
        org=(10, 30),
        fontFace=cv2.FONT_HERSHEY_PLAIN,
        fontScale=2,
        color=(255, 255, 255),
        thickness=2
    )
    # draw_line_1(img_lines, line_3_global, color=255, linewidth=4, transparency=0.0)

    return img_lines


def process_image2(src):
    import math

    dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # Edge detection
    dst = cv2.Canny(dst, 50, 255, None, 3)

    # Detect lines using the Hough Line Transform
    theta = np.pi/180
    lines = cv2.HoughLines(dst, 1, theta, threshold=0, max_theta=theta, min_theta=theta)

    if lines is None or len(lines) < 2:
        return src

    rho, theta = lines[0][0]
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

    line_base = (pt1, pt2)
    ret = cv2.line(
        src,
        pt1=pt1,
        pt2=pt2,
        color=(255, 0, 0),
        thickness=2
    )
    distance = 0
    for line in lines:
        rho, theta = line[0]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        line = (pt1, pt2)

        # Calculate distance between lines (e.g., closest points)
        distance = np.linalg.norm(np.array(line_base[0]) - np.array(line[0]))

        if distance > 20:
            break
    if distance < 20:
        return src

    ret = cv2.line(
        src,
        pt1=line[0],
        pt2=line[1],
        color=(255, 0, 0),
        thickness=2
    )

    text_distance = f"{round(distance/125, 2)} cm"
    ret = cv2.putText(
        ret,
        text=text_distance,
        org=(10, 30),
        fontFace=cv2.FONT_HERSHEY_PLAIN,
        fontScale=2,
        color=(255, 255, 255),
        thickness=2
    )
    return ret


if __name__ == "__main__":
    camera = cv2.VideoCapture("/dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0")
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
