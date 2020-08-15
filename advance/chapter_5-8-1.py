import cv2
from PIL import Image
import matplotlib.pyplot as plt


def load_cv2_image(path):
    return cv2.imread(path)


def resize_cv2_image(image, ratio):
    return cv2.resize(image, None, fx=ratio, fy=ratio)


def cv2_to_pil_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    new_image = image.copy()
    return Image.fromarray(new_image)


image = load_cv2_image("1周目/cat.jpg")
image = resize_cv2_image(image, 0.1)
image = cv2_to_pil_image(image)
image.show()
