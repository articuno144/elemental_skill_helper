import time
import sys
import json
import numpy as np
import pytesseract
import cv2
from mss import mss
from PIL import Image
from read_cd import CdReader


class CdRecorder:
    def __init__(self):
        self.cd = 0.0
        self.time_last_update = time.time()
    
    def update(self, cd=None):
        if cd is None:
            self.cd -= time.time() - self.time_last_update
            self.cd = max(0.0, self.cd)
        else:
            self.cd = cd
        self.time_last_update  = time.time()

class SkillHelper:
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)
        self.is_mona = [False, False, False, False]
        if self.config["mona"] > 0:
            self.is_mona[self.config["mona"]-1] = True
        self.recorders = [CdRecorder() for _ in range(4)]
        self.cd_reader = CdReader()
        self.tag_positions = []
        cv2.namedWindow("countdown")

    def tick(self):
        for recorder in self.recorders:
            recorder.update()
        current_character = self.get_current_character()
        new_cd = self.cd_reader.read_cd(self.is_mona[current_character])
        if new_cd is not None:
            self.recorders[current_character].update(new_cd)

    def get_current_character(self):
        self.cd_reader.sct.get_pixels(self.config["bbox"])
        img = Image.frombytes('RGB', (self.cd_reader.sct.width, self.cd_reader.sct.height), self.cd_reader.sct.image).convert('RGB')
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        brightness = [img[self.config["char1"],10],
                      img[self.config["char2"],10],
                      img[self.config["char3"],10],
                      img[self.config["char4"],10]]
        return np.argmin(brightness)
    
    def print(self):
        print()
        for i, recorder in enumerate(self.recorders):
            progress_bar = "#" * int(recorder.cd/0.2)
            print(progress_bar)
            print(progress_bar)
            print()
    
    def draw(self):
        img = np.ones([800, 1200]) * 255
        for i, recorder in enumerate(self.recorders):
            progress = min(int(recorder.cd/0.02), 1200)
            img[i*200:(i+1)*200,:progress] *= 0
        cv2.imshow("countdown", img)
        cv2.waitKey(20)


if __name__ == "__main__":
    helper = SkillHelper()
    while True:
        helper.tick()
        helper.draw()