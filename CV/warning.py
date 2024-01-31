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
        #왼쪽을 보고 있으면 왼쪽 턱선을 빨간색으로 출력합니다.
        if left_jawline_length / right_jawline_length < 0.7:
            cv2.polylines(self.frame, [right_jawline], True, (0, 255, 0), 3)
            cv2.polylines(self.frame, [left_jawline], True, (255, 0, 255), 3)
        #오른쪽을 보고 있으면 오른쪽 턱선을 빨간색으로 출력합니다.
        elif right_jawline_length / left_jawline_length < 0.7:
            cv2.polylines(self.frame, [right_jawline], True, (255, 0, 255), 3)
            cv2.polylines(self.frame, [left_jawline], True, (0, 255, 0), 3)
        #정면을 보고 있으면 양쪽 턱선을 초록색으로 출력합니다.
        else:
            cv2.polylines(self.frame, [right_jawline], True, (0, 255, 0), 3)
            cv2.polylines(self.frame, [left_jawline], True, (0, 255, 0), 3)
        return

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
        face_region = np.array([(self.facial_landmark.part(0).x, self.facial_landmark.part(0).y),
                                (self.facial_landmark.part(1).x, self.facial_landmark.part(1).y),
                                (self.facial_landmark.part(2).x, self.facial_landmark.part(2).y),
                                (self.facial_landmark.part(3).x, self.facial_landmark.part(3).y),
                                (self.facial_landmark.part(4).x, self.facial_landmark.part(4).y),
                                (self.facial_landmark.part(5).x, self.facial_landmark.part(5).y),
                                (self.facial_landmark.part(6).x, self.facial_landmark.part(6).y),
                                (self.facial_landmark.part(7).x, self.facial_landmark.part(7).y),
                                (self.facial_landmark.part(8).x, self.facial_landmark.part(8).y),
                                (self.facial_landmark.part(9).x, self.facial_landmark.part(9).y),
                                (self.facial_landmark.part(10).x, self.facial_landmark.part(10).y),
                                (self.facial_landmark.part(11).x, self.facial_landmark.part(11).y),
                                (self.facial_landmark.part(12).x, self.facial_landmark.part(12).y),
                                (self.facial_landmark.part(13).x, self.facial_landmark.part(13).y),
                                (self.facial_landmark.part(14).x, self.facial_landmark.part(14).y),
                                (self.facial_landmark.part(15).x, self.facial_landmark.part(15).y),
                                (self.facial_landmark.part(16).x, self.facial_landmark.part(16).y),
                                (self.facial_landmark.part(24).x, self.facial_landmark.part(18).y),
                                (self.facial_landmark.part(19).x, self.facial_landmark.part(23).y)], np.int32)
        cv2.polylines(self.frame, [face_region], True, (0, 0, 255), 5)
        return self.frame