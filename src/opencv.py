import cv2
import numpy as np

import linecalc


class OpenCV:
    def __init__(self, maze, w, h):
        self.lines_last_frames = []
        self.w = w
        self.h = h
        self.maze = maze
        self.np_camera_matrix = np.array([[57., 0., 59.], [0., 57., 46.], [0., 0., 1.]])
        self.np_distortion_coefficients = np.array([-3.0048e-01, 8.4940e-02, -3.5780e-03, -2.08614e-03, -1.0185e-02])
        self.linecalc = linecalc.LineCalc(w, h)

    def modify_image(self, frame, total_processed_frames):
        img = frame.array
        img = cv2.rotate(img, 1)
        img = cv2.undistort(img, self.np_camera_matrix, self.np_distortion_coefficients)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_blurred = cv2.GaussianBlur(img_gray, (15, 15), 0)
        img_sharpened = cv2.addWeighted(img_gray, 1.5, img_blurred, -0.5, 0)

        img_canny = cv2.Canny(img_sharpened, 130, 190)

        lines = cv2.HoughLinesP(image=img_canny,
                                rho=1,
                                theta=np.pi / 180,
                                threshold=20,
                                minLineLength=30,
                                maxLineGap=10)

        img_black_thres = cv2.inRange(img_sharpened, 0, 50)

        num_black_pixels = cv2.countNonZero(img_black_thres)

        return cv2.cvtColor(img_sharpened, cv2.COLOR_GRAY2BGR), lines, num_black_pixels

    def find_lines(self, img_canny, x1, y1, x2, y2, tmp_turns_seen_rn):

        if not self.linecalc.is_line_horizontal(x1, y1, x2, y2):
            if self.linecalc.contains_line_bottom(x1, y1, x2, y2):
                tmp_turns_seen_rn[self.maze.backward] = True
                # purple
                cv2.line(img_canny, (x1, y1), (x2, y2), (85, 26, 139), 2)

            if self.linecalc.contains_line_top(x1, y1, x2, y2):
                tmp_turns_seen_rn[self.maze.forward] = True
                # green
                cv2.line(img_canny, (x1, y1), (x2, y2), (0, 255, 0), 2)

        else:
            cv2.line(img_canny, (x1, y1), (x2, y2), (255, 0, 255), 2)
            if self.linecalc.contains_line_left_area(x1, y1, x2, y2):
                tmp_turns_seen_rn[self.maze.left] = True
                # red
                cv2.line(img_canny, (x1, y1), (x2, y2), (255, 0, 0), 2)

            if self.linecalc.contains_line_side_area(x1, y1, x2, y2):
                tmp_turns_seen_rn[self.maze.right] = True
                # blue
                cv2.line(img_canny, (x1, y1), (x2, y2), (0, 0, 255), 2)
