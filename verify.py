import cv2
import random
import os

image_dir = "dataset/images"
label_dir = "dataset/labels"

# 随机选择一张图片和标签
image_files = os.listdir(image_dir)
img_name = random.choice(image_files)
img_path = os.path.join(image_dir, img_name)
txt_path = os.path.join(label_dir, os.path.splitext(img_name)[0] + ".txt")

# 读取图片和标签
img = cv2.imread(img_path)
h, w = img.shape[:2]

with open(txt_path, 'r') as f:
    for line in f.readlines():
        class_id, xc, yc, bw, bh = map(float, line.strip().split())
        # 转换为像素坐标
        x1 = int((xc - bw/2) * w)
        y1 = int((yc - bh/2) * h)
        x2 = int((xc + bw/2) * w)
        y2 = int((yc + bh/2) * h)
        # 绘制矩形框
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Check", img)
cv2.waitKey(0)