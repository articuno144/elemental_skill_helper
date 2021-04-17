import pytesseract
import cv2
from mss import mss
from PIL import Image
import numpy as np
import json
import time


class CdReader:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.sct = mss()
        with open('bbox_mona.json') as f:
            self.cd_box_mona = json.load(f)
        with open('bbox.json') as f:
            self.cd_box = json.load(f)

    def get_raw_img(self, box):
        self.sct.get_pixels(box)
        img = Image.frombytes('RGB', (self.sct.width, self.sct.height), self.sct.image).convert('RGB')
        return np.array(img)

    def read_cd(self, is_mona=False):
        if is_mona:
            img = self.get_raw_img(self.cd_box_mona)
        else:
            img = self.get_raw_img(self.cd_box)
        _, img = cv2.threshold(img, 233, 255, 0)
        img = cv2.bitwise_not(img)
        parsed = pytesseract.image_to_string(img)
        parsed = self.check(parsed)
        return parsed

    def check(self, parsed):
        dot_idx = parsed.find('.')
        if dot_idx == -1:
            return None
        else:
            try:
                return float(parsed[:dot_idx+2])
            except:
                return None


if __name__ == "__main__":
    reader = CdReader()
    while True:
        print(reader.read_cd())
