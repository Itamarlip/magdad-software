import os
from process_image import ImageProcessor
import cv2

def main():
    image_path = r"C:\Users\TLP\Pictures\Camera Roll\WIN_20261124_21_39_59_Pro.jpg"
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: image not found! Please check the path.")
        return
    
    processor = ImageProcessor(image,1,0.3)
    processor.process_image(canny_lower= 0, canny_upper=200,hough_threshold=100,
                                 m_error = 0.05, b_error=50, display=True)
    processor.get_only_door_lines(2, 2, display=True)
    for l in processor.valid_lines:
        print(f"Line: y = {l[0]}x + {l[1]}")


def folder_check(path):
    list_of_outputs = []
    for image_path in os.listdir(path)[1:]:
        print("---------------------")
        input_path = os.path.join(path, image_path)
        print(input_path)
        image = cv2.imread(input_path)
        
        processor = ImageProcessor(image,1,0.3)
        processor.process_image(canny_lower= 0, canny_upper=200,hough_threshold=100,
                                 m_error = 0.07, b_error=50, display=False)
        processor.get_only_door_lines(2, 2, display=False)
        list_of_outputs.append("open" if len(processor.valid_lines) > 1 else "close")
        for l in processor.valid_lines:
            print(f"Line: y = {l[0]}x + {l[1]}")
    return list_of_outputs

def test_falses(path, check, expect):
    for i in range(len(check)):
        if check[i] != expect[i]:
            print("---------------------")
            print(f"expected {expect[i]} got {check[i]}")
            input_path = os.path.join(path, os.listdir(path)[i+1])
            image = cv2.imread(input_path)
            processor = ImageProcessor(image,1,0.3)
            processor.process_image(canny_lower= 0, canny_upper=200,hough_threshold=100,
                                     m_error = 0.07, b_error=50, display=True)
            processor.get_only_door_lines(2, 2, display=True)
            print(f"found {len(processor.valid_lines)} lines in this image")
            for l in processor.valid_lines:
                print(f"Line: y = {l[0]}x + {l[1]}")

if __name__ == "__main__":
    #main()
    path = r"C:\Users\TLP\Pictures\Camera Roll"
    checked_answers = folder_check(path)
    print(checked_answers)
    expected_answers = ["open"]*70 + ["close"]*16
    test_falses(path,checked_answers,expected_answers)

