from .draw_line_1 import draw_line_1

def draw_rectangle_1(view, rect, color=(255, 255, 255), linewidth=2, transparency=0.0):
    """
    Draws a rectangle with a specific color, linewidth and transparency.
    """
    lines = rect.edge_lines
    for line in lines:
        draw_line_1(view,line,color,linewidth,transparency)

