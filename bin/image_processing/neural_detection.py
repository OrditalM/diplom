import re
import cv2
import tensorflow as tf
import numpy as np



def load_labels(path='labels.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        labels = {}
        for row_number, content in enumerate(lines):
            pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
            if len(pair) == 2 and pair[0].strip().isdigit():
                labels[int(pair[0])] = pair[1].strip()
            else:
                labels[row_number] = pair[0].strip()
    return labels


def load_model(model_path):
    model = tf.saved_model.load(model_path)
    return model


def preprocess_image(image):
    """Preprocess the input image."""
    image = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), (320, 320))
    image = (image * 255).astype(np.uint8)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image


def detect_objects(model, image, threshold):
    input_tensor_info = model.signatures["serving_default"].inputs
    img_uint8 = (image * 255).astype(np.uint8)
    output_dict = model.signatures["serving_default"](tf.constant(img_uint8))

    boxes = output_dict['detection_boxes'].numpy().tolist()[0]
    classes = output_dict['detection_classes'].numpy().astype(int).tolist()[0]
    scores = output_dict['detection_scores'].numpy().tolist()[0]
    count = int(output_dict['num_detections'].numpy())

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'score': scores[i]
            }
            results.append(result)
    return results

