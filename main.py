import cv2

from process_image import ImageProcessor
from server import socketServer
import keyboard

picture_flag = False
forward_flag = False
backward_flag = False
quit_flag = False

def handle_x_button():
    global picture_flag
    picture_flag = True

def handle_w_button():
    global forward_flag
    forward_flag = True

def handle_s_button():
    global backward_flag
    backward_flag = True

def handle_q_button():
    global quit_flag
    quit_flag = True

def process_frame(frame):
    if frame is not None:
        processor = ImageProcessor(frame,1,0.3)
        processor.process_image(canny_lower= 0, canny_upper=200,hough_threshold=100,
                                    m_error = 0.07, b_error=50, display=True)
        processor.get_only_door_lines(3, 3, display=True)
        for l in processor.valid_lines:
            print(f"Line: y = {l[0]}x + {l[1]}")

        return "open" if len(processor.valid_lines) > 1 else "closed"

def send_forward():
    pass


def main():
    global picture_flag
    global forward_flag
    global backward_flag
    global quit_flag
    keyboard.add_hotkey('x', handle_x_button)
    keyboard.add_hotkey('w', handle_w_button)
    keyboard.add_hotkey('s', handle_s_button)
    keyboard.add_hotkey('q', handle_q_button)

    #server = socketServer()

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    while True:
        ret, frame=cap.read()
        cv2.imshow('USB Camera', frame)
        cv2.waitKey(1)
        if picture_flag:
            print('x')
            door_state = process_frame(frame)
            print(door_state)
            picture_flag = False

        if forward_flag:
            print("w")
            forward_flag = False

        if backward_flag:
            print("s")
            backward_flag = False

        if quit_flag:
            print("q")
            break

if __name__ == "__main__":

    main()