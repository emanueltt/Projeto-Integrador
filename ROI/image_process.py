# Distância linhas
import cv2
import numpy as np
from .libs.line_detector_all import LineDetectorAll
from .libs import Rectangle, Scene
from .libs import draw_line_1

# %matplotlib inline

def calibration_px_cm(img):
    img_gray = img[100:450, 1220:img.shape[1]].copy()
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    _, img_gray = cv2.threshold(img_gray, 45, 255, cv2.THRESH_BINARY)
    # img_gray = cv2.bilateralFilter(img_gray, 5, 20, 20)
    img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)

    sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=9)

    opening = np.sqrt(sobel_y**2)
    opening = (np.mean(opening, axis = 1)) - np.min(np.mean(opening, axis = 1))

    rois = []
    n_cont = 0
    save_it = 0
    pause_cont = 0

    for i in opening:
        if i > np.mean(opening) and n_cont > 50:
            if pause_cont <= 0:
                save_it = 1

        if save_it:
            rois.append(n_cont)
            pause_cont = 100
            save_it = 0

        n_cont += 1
        pause_cont -= 1 

    rect_1 = Rectangle(x = 0, y = rois[0]-30, rz = 0, w = img_gray.shape[1], h = 70)
    rect_2 = Rectangle(x = 0, y = rois[1]-30, rz = 0, w = img_gray.shape[1], h = 70)

    roi_1 = rect_1.crop_from_img(img_gray)
    roi_2 = rect_2.crop_from_img(img_gray)

    l_Detector_1  = LineDetectorAll(9, True, False, True)
    l_Detector_2  = LineDetectorAll(9, False, False, True)

    line_1 = l_Detector_1.detect(roi_1)
    line_2 = l_Detector_2.detect(roi_2)
    line_1[2] = 0
    line_2[2] = 0

    # Scenes
    scene_1 = Scene()
    scene_1.add(rect_1, "rect_1", None)
    scene_1.add(rect_2, "rect_2", None)
    scene_1.add(line_1, "line_1", "rect_1")
    scene_1.add(line_2, "line_2", "rect_2")

    # Global lines
    line_1_global = scene_1.get_global("line_1")
    line_2_global = scene_1.get_global("line_2")

    return((line_2_global[1] - line_1_global[1])/10), sobel_y

def process_distance(img, px_cm):
    imagem_rotacionada = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Lembrar de mudar a ROI da imagem rotacionada na img_lines tbm
    img_gray = imagem_rotacionada[100:imagem_rotacionada.shape[0], 120:350].copy()
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.bilateralFilter(img_gray, 5, 20, 20)

    sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=9)

    opening = np.sqrt(sobel_y**2)
    opening = (np.mean(opening, axis = 1)) - np.min(np.mean(opening, axis = 1))

    rois = []
    n_cont = 0
    save_it = 0
    pause_cont = 0

    for i in opening:
        if i > np.mean(opening)*7 and n_cont > 50:
            if pause_cont <= 0:
                save_it = 1

        if save_it:
            rois.append(n_cont)
            pause_cont = 100
            save_it = 0

        n_cont += 1
        pause_cont -= 1 

    rect_1 = Rectangle(x = 0, y = rois[0]-20, rz = 0, w = 200, h = 120)
    rect_2 = Rectangle(x = 0, y = rois[1]-20, rz = 0, w = 200, h = 120)

    roi_1 = rect_1.crop_from_img(img_gray)
    roi_2 = rect_2.crop_from_img(img_gray)

    l_Detector_1  = LineDetectorAll(9, True, False, False)
    l_Detector_2  = LineDetectorAll(9, False, False, False)

    line_1 = l_Detector_1.detect(roi_1)
    # line_1[2] = -7
    line_2 = l_Detector_2.detect(roi_2)
    # line_2[2] = -6

    # Scenes
    scene_1 = Scene()
    scene_1.add(rect_1, "rect_1", None)
    scene_1.add(rect_2, "rect_2", None)
    scene_1.add(line_1, "line_1", "rect_1")
    scene_1.add(line_2, "line_2", "rect_2")

    # Global lines
    line_1_global = scene_1.get_global("line_1")
    line_2_global = scene_1.get_global("line_2")

    img_lines = imagem_rotacionada[100:imagem_rotacionada.shape[0], 120:350].copy()
    draw_line_1(roi_1, line_1, color=(255, 255, 255), linewidth=4, transparency=0.0)
    draw_line_1(roi_2, line_2, color=(255, 255, 255), linewidth=4, transparency=0.0)
    draw_line_1(img_lines, line_1_global, color=(255, 255, 255), linewidth=4, transparency=0.0)
    draw_line_1(img_lines, line_2_global, color=(255, 255, 255), linewidth=4, transparency=0.0)

    # Vertical line - visualization 
    cv2.line(img_lines, (int(line_1_global[0]), int(line_1_global[1])), (int(line_2_global[0]), int(line_2_global[1])), (255, 255, 255), 4) 
    
    # Distance plot
    distance_cm = (line_2_global[1] - line_1_global[1])/px_cm
    distance_text = f" {distance_cm:.2f} cm"
    cv2.putText(img_lines, distance_text, (int(line_2_global[0]), int((int(line_1_global[1])+int(line_2_global[1]))/2)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1)


    return (distance_cm, img_lines)


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


def process_image2(src: cv2.Mat, thresh1=40, thresh2=50):
    import math
    dst = src.copy()
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    # Edge detection
    dst = cv2.Canny(dst, thresh1, thresh2, None, 3)

    # Detect lines using the Hough Line Transform
    theta = np.pi/180
    lines = cv2.HoughLines(dst, 1, theta, threshold=0, max_theta=theta, min_theta=theta)

    if lines is None or len(lines) < 2:
        print("Lines is None or len(lines) < 2")
        # return src
        return None

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

        if distance > 100:
            break
    if distance < 100:
        print("Distance < 20")
        # return src
        return None

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
    return float(distance)
    # return ret


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
        x1, y1 = 50, 200  # Top-left corner
        x2, y2 = 900, 270  # Bottom-right corner

        # Crop the region
        frame = frame[y1:y2, x1:x2]

        frame = process_image2(frame)
        cv2.imshow("video", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == -1:
            continue
        # elif key == 81:  # Esquerda
        #     th1 -= 1
        # elif key == 83:  # Direita
        #     th1 += 1
        # elif key == 84:  # Baixo
        #     th2 -= 1
        # elif key == 82:  # Cima
        #     th2 += 1
        
        # elif key == 32:
        #     cv2.imwrite(f"image_{height}p_{frame_counter}.png", frame)
        else:
            print(key)
        # print(th1, th2)

    camera.release()
    cv2.destroyAllWindows()
