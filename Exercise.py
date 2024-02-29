import cv2
import numpy as np
import PoseModule as pm

class ExerciseCounter:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"Error: Could not open video capture at {video_path}")
            return

        self.detector = pm.poseDetector()
        self.count = 0
        self.dir = 0
        self.exercise_type = None

    def set_exercise_type(self, exercise_type):
        self.exercise_type = exercise_type

    def set_callback(self, callback):
        self.callback = callback  # Set the callback function for GUI updates

    def process_video(self, callback=None):
        while True:
            success, img = self.cap.read()
            if not success:
                print("Error reading frame from video capture.")
                break

            img = cv2.resize(img, (1280, 720))
            img = self.detector.findPose(img, False)
            lmList = self.detector.findPosition(img, False)

            if len(lmList) != 0:
                if self.exercise_type == "curl":
                    self.process_curls(img)
                elif self.exercise_type == "situp":
                    self.process_situps(img)
                elif self.exercise_type == "pushup":
                    self.process_pushup(img)

            # Optional: Invoke the callback function with the processed frame
            if callback:
                callback(img)

            cv2.waitKey(10)

    def process_curls(self, img):
        angle = self.detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (210, 320), (0, 100))
        bar = np.interp(angle, (210, 320), (600, 200))

        bar_color = (255, 255, 255)
        text_color = (0, 0, 255)

        if per == 100:
            bar_color = (0, 255, 0)
            text_color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
        if per == 0:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1
        
        return (img,self.count)

        cv2.rectangle(img, (1100, int(bar)), (1150, 600), bar_color, cv2.FILLED)
        cv2.rectangle(img, (1100, 200), (1150, 600), (255, 0, 0), 3)
        cv2.putText(img, f'{int(per)}%', (1090, 175), cv2.FONT_HERSHEY_DUPLEX, 1, text_color, 1)
        cv2.putText(img, "Count : " + str(int(self.count)), (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 100), 1)
    

    def process_pushup(self, img):
        angle = max(self.detector.findAngle(img, 11, 13, 15),self.detector.findAngle(img, 12, 14, 16))
        per = np.interp(angle, (200, 270), (0, 100))
        bar = np.interp(angle, (200, 270), (600, 200))

        bar_color = (255, 255, 255)
        text_color = (0, 0, 255)

        if per == 100:
            bar_color = (0, 255, 0)
            text_color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
        if per == 0:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1

        cv2.rectangle(img, (1100, int(bar)), (1150, 600), bar_color, cv2.FILLED)
        cv2.rectangle(img, (1100, 200), (1150, 600), (255, 0, 0), 3)
        cv2.putText(img, f'{int(per)}%', (1090, 175), cv2.FONT_HERSHEY_DUPLEX, 1, text_color, 1)
        cv2.putText(img, "Count : " + str(int(self.count)), (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 100), 1)


    def process_situps(self, img):
        angle = max(self.detector.findAngle(img, 12, 24, 26), self.detector.findAngle(img, 11, 23, 25))
        leg_angle = max(self.detector.findAngle(img, 24, 26, 28), self.detector.findAngle(img, 23, 25, 27))
        hand_angle = max(self.detector.findAngle(img, 12, 14, 16, False), self.detector.findAngle(img, 11, 13, 15))
        per = np.interp(angle, (75, 120), (100, 0))
        bar = np.interp(angle, (75, 120), (200, 600))

        bar_color = (255, 255, 255)
        text_color = (0, 0, 255)

        if per == 100 and leg_angle >= 260 and hand_angle >= 35:
            bar_color = (0, 255, 0)
            text_color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
        if per == 0 and leg_angle >= 260 and hand_angle >= 35:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1

        cv2.rectangle(img, (1100, int(bar)), (1150, 600), bar_color, cv2.FILLED)
        cv2.rectangle(img, (1100, 200), (1150, 600), (255, 0, 0), 3)
        cv2.putText(img, f'{int(per)}%', (1090, 175), cv2.FONT_HERSHEY_DUPLEX, 1, text_color, 1)
        cv2.putText(img, "Count : " + str(int(self.count)), (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 100), 1)


    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_latest_frame(self):
        # Return the latest frame for GUI update
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(cv2.resize(frame, (640, 480)), cv2.COLOR_BGR2RGB)
        return None
