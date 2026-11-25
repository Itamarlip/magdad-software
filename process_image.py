import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

class ImageProcessor:
    def __init__(self, image, crop_lower, crop_upper):
        self.image = image
        self.CROP_LOWER = crop_lower
        self.CROP_UPPER = crop_upper
        self.cropped = self.crop_image()
        self.gray_cropped = cv2.cvtColor(self.cropped, cv2.COLOR_BGR2GRAY)
        self.blank_with_lines = np.zeros_like(self.cropped)
        self.lines = []
    


    def crop_image(self):
        return self.image[int(self.CROP_UPPER*self.image.shape[0]):int(self.CROP_LOWER*self.image.shape[0]), :]

    def disp_image(self, img, title = "Image", lines = None):
        if lines is not None:
            for line in lines:
                m,b = line
                p1 = (0, int(b))
                p2 = (img.shape[1], int(img.shape[1]*m + b))
                cv2.line(img, p1, p2, (0,0,255), 2)

        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def unite_lines(self, lines_equations : list((int,int)), m_error, b_error) -> list((int,int)):
        if not lines_equations:
            return []

        lines_equations = [lines_equations[i] for i in range(len(lines_equations)) 
                        if lines_equations[i][0] != float('inf') and
                        lines_equations[i][1] <1000 and abs(lines_equations[i][0]) < 1]
        for i in range(len(lines_equations)):
            if lines_equations[i] is None:
                continue
            m, b = lines_equations[i]
            for j in range(i + 1, len(lines_equations)):
                if lines_equations[j] is None:
                    continue
                m2, b2 = lines_equations[j]
                if abs(m - m2) < m_error and abs(b - b2) < b_error:
                    new_m = (m + m2) / 2
                    new_b = (b + b2) / 2
                    lines_equations[i] = (new_m, new_b)
                    lines_equations[j] = None

        united_lines = [line for line in lines_equations if line is not None and abs(np.arctan(line[0]))<30]
        return united_lines

    def detect_lines_in_binary_image(self, img, m_error, b_error, hough_threshold, minLineLength, maxLineGap, canny_lower, canny_upper) -> list((int,int)):
        '''returns a list of lines in the form of (m,b) where m is the slope and b is the y-intercept'''
        edges = cv2.Canny(img, canny_lower, canny_upper, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=hough_threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        lines_equations = []
        if lines is None:
            return lines_equations
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            m = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')  
            b = (y1 - m * x1)
            lines_equations.append((m, b))

        
        united_lines = self.unite_lines(lines_equations, m_error, b_error)
        
        return united_lines

    def process_image(self, m_error = 0.03, b_error = 30, hough_threshold = 50,
                       minLineLength = 30, maxLineGap = 10, canny_lower = 50,
                        canny_upper= 150, display=False):
        _, black_mask = cv2.threshold(self.gray_cropped, 50, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        updated_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:
                updated_contours.append(contour)

        blank_image = np.zeros_like(self.gray_cropped)
        cv2.drawContours(blank_image, updated_contours, -1, (255, 255, 255), 1)
        if display:
            cv2.imshow('Detected contours', blank_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        print(f"Number of contours found in image: {len(updated_contours)}")
        self.lines = self.detect_lines_in_binary_image(blank_image, m_error, b_error, hough_threshold, minLineLength, maxLineGap, canny_lower, canny_upper)
        if display:
            self.disp_image(self.cropped.copy(), "Cropped Image", self.lines)

    def decide_open_close(self, x_ratio, y_ratio):
        size_x_axis = self.gray_cropped.shape[1]
        size_y_axis = self.gray_cropped.shape[0]

        x_axis_valid = size_x_axis*x_ratio
        y_axis_valid = size_y_axis*y_ratio

        

