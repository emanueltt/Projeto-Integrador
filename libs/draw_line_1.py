import cv2
import numpy as np

def draw_line_1(view, line, color=(255, 255, 255), linewidth=2, transparency=0.0):
    """
    Draws a line into an image from with a specific color, linewidth and transparency.
    """
    start, end = line.end_points
    start = (int(round(start.x)),int(round(start.y)))
    end = (int(round(end.x)),int(round(end.y)))

    if transparency == 0.0:
        cv2.line(view, start, end, color, linewidth)
    else:
        overlay = view.copy()
        cv2.line(overlay, start, end, color, linewidth)
        cv2.addWeighted(overlay, 1 - transparency, view, transparency, 0, view)