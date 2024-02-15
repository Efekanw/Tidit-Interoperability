import os
import cv2
from ultralytics import YOLO

########################### BOŞLUK ATILDI DEPLOY    lazım
def detect_objects(img):
    CONFIDENCE = 0.5
    # loading the YOLOv8 model with the default weight file
    model = YOLO("yolov8n.pt")
    labels = open("/app/coco.names").read().strip().split("\n")
    results = model.predict(image, conf=CONFIDENCE)[0]
    detected = []
    for data in results.boxes.data.tolist():
        data_list = []
        xmin, ymin, xmax, ymax, confidence, class_id = data
        #[{"class": "person", "x": 5, "y": 10}, {"class": "car", "x": 12, "y": 20}]
        text = f"'label': '{labels[int(class_id)]}', 'confidence': '{confidence:.2f}', 'xmin': '{xmin}', 'ymin': '{ymin}', 'xmax': '{xmax}', 'ymax': '{ymax}'" # json döndür
        detected.append(text)
    return detected


if __name__ == '__main__':
    image_dir = '/app/images'
    for filename in os.listdir(image_dir):
        if filename.endswith('.jpg'):
            image_path = os.path.join(image_dir, filename)
    image = cv2.imread(image_path)
    print(detect_objects(image))