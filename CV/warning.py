import numpy as np
import cv2

class Warning:
    def __init__(self):
        self.frame = None
        self.face = None
        self.facial_landmark = None

    def refresh(self, frame, face, facial_landmark):
        self.frame = frame
        self.face = face
        self.facial_landmark = facial_landmark

    def distance(self, point1, point2):
        return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    
    def print_jawline(self, right_jawline, left_jawline):
        right_jawline_length = self.distance(right_jawline[0], right_jawline[1])
        left_jawline_length = self.distance(left_jawline[0], left_jawline[1])
        #왼쪽 또는 오른쪽 보고 있으면 왼쪽 턱선을 빨간색으로 출력합니다.
        if left_jawline_length / right_jawline_length < 0.7 or right_jawline_length / left_jawline_length < 0.7:
            height, width = self.frame.shape[:2]
            self.frame = cv2.rectangle(self.frame, (0, 0), (width-1, height-1), (0, 0, 255), 5)

    def jawline_warning(self):
        ## 턱선
        # right_jawline = np.array([(self.facial_landmark.part(1).x, self.facial_landmark.part(2).y),
        #                         (self.facial_landmark.part(7).x, self.facial_landmark.part(6).y)], np.int32)
        # left_jawline = np.array([(self.facial_landmark.part(15).x, self.facial_landmark.part(2).y),
        #                         (self.facial_landmark.part(9).x, self.facial_landmark.part(6).y)], np.int32)
        ## 코 기준 좌우 가로선
        right_jawline = np.array([(self.facial_landmark.part(33).x, self.facial_landmark.part(33).y),
                                (self.facial_landmark.part(2).x, self.facial_landmark.part(2).y)], np.int32)
        left_jawline = np.array([(self.facial_landmark.part(33).x, self.facial_landmark.part(33).y),
                                (self.facial_landmark.part(14).x, self.facial_landmark.part(14).y)], np.int32)
        self.print_jawline(right_jawline, left_jawline)
        return self.frame
    
    def eyetracking_warning(self):
        height, width = self.frame.shape[:2]
        self.frame = cv2.rectangle(self.frame, (5, 5), (width-6, height-6), (255, 0, 0), 3)
        return self.frame
    