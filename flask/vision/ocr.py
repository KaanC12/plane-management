import cv2
import os
import numpy as np
import pytesseract
import re


class Render:
    def __init__(self, key_words=None, img_path=None, img_bytes=None):
        self.key_words = key_words
        self.result = {}
        self.type = None
        if img_path is not None:
            self.img = cv2.imread(img_path)
        if img_bytes is not None:
            npimg = np.frombuffer(img_bytes, np.uint8)
            self.img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        h, w = self.img.shape[:2]
        if h == w:
            h += 1
        if h > w:
            self.block_size = int((w / h) * 50)
        else:
            self.block_size = int((h / w) * 50)
        
        if self.block_size % 2 == 0:
            self.block_size += 1
            

    def show_img(self, img, title="Debug"):
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def text_from_box(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, self.block_size, 8)
        horizontal_brush = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_brush = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

        h_lines = cv2.morphologyEx(th, cv2.MORPH_OPEN, horizontal_brush)
        v_lines = cv2.morphologyEx(th, cv2.MORPH_OPEN, vertical_brush)

        all_lines = cv2.add(h_lines, v_lines)
        
        cnts, hi = cv2.findContours(all_lines, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        boxes = []
        for i, c in enumerate(cnts):
            parent = hi[0][i][3]
            child = hi[0][i][2]
            
            if parent == -1 or child != -1:
                continue

            x,y,w,h = cv2.boundingRect(c)
            if w*h < 500:
                continue
            boxes.append([x,y,w,h])

        for (x,y,w,h) in boxes:
            crop = self.img[y:y+h, x:x+w]
            g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            g = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            g = cv2.resize(g, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            data = pytesseract.image_to_string(g, config="--oem 3 --psm 3", lang="deu+eng").lower()
            data = self._parse_fields(data)
            self._extract_info(data)
            
    def text_from_letter(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, self.block_size, 8)
        
        brush = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        clean = cv2.morphologyEx(th, cv2.MORPH_CLOSE, brush)
        inv = cv2.bitwise_not(clean)

        cnts, _ = cv2.findContours(inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts, key=cv2.contourArea)
        
        mask = np.zeros(self.img.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        paper = cv2.bitwise_and(self.img, self.img, mask=mask)
        
        white = np.full_like(self.img, 255)
        background = cv2.bitwise_and(white, white, mask=cv2.bitwise_not(mask))

        out = cv2.add(paper, background)
        background_gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(background_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, self.block_size, 8)
        
        g = cv2.threshold(th, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        g = cv2.resize(g, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        txt = pytesseract.image_to_string(g, config="--oem 3 --psm 11", lang="eng+deu")

        

    def _parse_fields(self, data):
        patterns = {
            "1.": r"nationality\s*and\s*registration\s*marks[:.]?",
            "2.": r"manufacturer\s*and\s*manufacturer'?s\s*designation[:.]?",
            "3.": r"serial\s*number[:.]?",
            "4.": r"name\s*of\s*owner[:.]?",
            "5.": r"address\s*of\s*owner[:.]?",
        }

        words = data.split()
        found = [w for w in words if w in self.key_words]

        for f in found:
            if f in patterns:
                data = re.sub(patterns[f], "", data, flags=re.IGNORECASE)

        return data

    def _extract_info(self, clean_data):
        clean_data = clean_data.replace("\n", " ")
        pattern = r"(\d+)\.\s*.*?:\s*(.*?)(?=\s*\d+\.|$)"
        matches = re.findall(pattern, clean_data, flags=re.S)
       
        for num, values in matches:
            value = values.strip()
            value = re.sub(r"\s+", " ", value)
            self.result[num] = value
        
    def classify_document(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 8)
        horizontal_brush = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_brush = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

        h_lines = cv2.morphologyEx(th, cv2.MORPH_OPEN, horizontal_brush)
        v_lines = cv2.morphologyEx(th, cv2.MORPH_OPEN, vertical_brush)

        all_lines = cv2.add(h_lines, v_lines)
        cnts, _ = cv2.findContours(all_lines, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        box_area = 0
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            if w*h < 500:
                continue
            box_area += w*h

        w_img, h_img = self.img.shape[:2]
        img_area = w_img * h_img
        if box_area / img_area > 0.7:
            self.type = "box_form"
        else:
            self.type = "letter_form"