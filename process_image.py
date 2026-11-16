import numpy as np
import cv2
import matplotlib.pyplot as plt

class ImageProcessor:


    def __init__(self, image, crop_lower, crop_upper):
        self.image = image
        self.CROP_LOWER = crop_lower
        self.CROP_UPPER = crop_upper
        self.cropped = self.crop_image()
        print(f"Cropped image shape: {self.cropped.shape}")
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
                        if lines_equations[i][0] != float('inf') and lines_equations[i][1] <1000]

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

    def detect_lines_in_binary_image(self, img, m_error, b_error, threshold, minLineLength, maxLineGap) -> list((int,int)):
        '''returns a list of lines in the form of (m,b) where m is the slope and b is the y-intercept'''
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        lines_equations = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            m = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')  
            b = (y1 - m * x1)
            lines_equations.append((m, b))

        
        united_lines = self.unite_lines(lines_equations, m_error, b_error)
        
        return united_lines

    def process_image(self, m_error = 0.03, b_error = 30, threshold = 50, minLineLength = 30, maxLineGap = 10, ):
        _, black_mask = cv2.threshold(self.gray_cropped, 50, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        updated_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:
                updated_contours.append(contour)

        blank_image = np.zeros_like(self.gray_cropped)
        cv2.drawContours(blank_image, updated_contours, -1, (255, 255, 255), 1)
        cv2.imshow('Detected contours', blank_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print(f"Number of contours found in image: {len(updated_contours)}\n")
        self.lines = self.detect_lines_in_binary_image(blank_image, m_error, b_error, threshold, minLineLength, maxLineGap)
        self.disp_image(self.cropped.copy(), "Cropped Image", self.lines)


def main():
    image_path = r""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: image not found! Please check the path.")
        return

    processor = ImageProcessor(image, 0.8, 0.6)
    processor.process_image(threshold = 30)

if __name__ == "__main__":
    main()