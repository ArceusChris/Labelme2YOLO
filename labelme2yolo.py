import os
import json
import numpy as np
from pathlib import Path
import cv2

def convert_labelme_to_yolo(json_dir, output_dir, class_list):
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 遍历所有JSON文件
    for json_file in Path(json_dir).glob("*.json"):
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # 获取图像尺寸（优先从JSON中读取，否则从图片读取）
        img_width = data['imageWidth']
        img_height = data['imageHeight']
        image_path = os.path.join(image_dir, data['imagePath'])
        if not os.path.exists(image_path):
            img = cv2.imread(image_path)
            if img is not None:
                img_height, img_width = img.shape[:2]
            else:
                print(f"Warning: Image {image_path} not found, skip {json_file}")
                continue
        
        # 生成YOLO标签文件路径
        txt_path = os.path.join(output_dir, Path(json_file.stem).with_suffix('.txt'))
        
        # 写入YOLO格式标签
        with open(txt_path, 'w') as f_txt:
            for shape in data['shapes']:
                label = shape['label']
                if label not in class_list:
                    print(f"Warning: Label '{label}' not in class list, skip.")
                    continue
                class_id = class_list.index(label)
                
                # 提取坐标点并转换为矩形框
                points = np.array(shape['points'])
                x_min, y_min = np.min(points, axis=0)
                x_max, y_max = np.max(points, axis=0)
                
                # 计算YOLO格式的归一化坐标
                x_center = (x_min + x_max) / 2 / img_width
                y_center = (y_min + y_max) / 2 / img_height
                width = (x_max - x_min) / img_width
                height = (y_max - y_min) / img_height
                
                # 确保坐标在[0,1]范围内
                x_center = np.clip(x_center, 0.0, 1.0)
                y_center = np.clip(y_center, 0.0, 1.0)
                width = np.clip(width, 0.0, 1.0)
                height = np.clip(height, 0.0, 1.0)
                
                # 写入文件
                f_txt.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

if __name__ == "__main__":
    # 配置参数
    image_dir = "dataset/images"         # 图片目录
    json_dir = "dataset/labelme_jsons"    # Labelme JSON文件目录
    output_dir = "dataset/labels"         # 输出YOLO标签目录
    class_list = ["car"] # 按实际类别顺序填写
    
    # 执行转换
    convert_labelme_to_yolo(json_dir, output_dir, class_list)