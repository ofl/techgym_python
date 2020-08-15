import cv2
from PIL import Image
import matplotlib.pyplot as plt


def load_pil_image(path):
    return Image.open(path)


def resize_pil_image(image, ratio):
    w, h = image.size
    return image.resize((int(float(w)*ratio), int(float(h)*ratio)), Image.LANCZOS)


image = load_pil_image("1周目/cat.jpg")
image = resize_pil_image(image, 0.1)
image.show()
