import fitz
import cv2
import numpy as np
import matplotlib.pyplot as plt

def document_to_images(path):
    doc = fitz.open(path)
    page_num = doc.page_count
    images = []
    for i in range(page_num):
        # print(f"Processing page {i + 1}/{page_num}")
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=fitz.Matrix(400/72, 400/72))
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        images.append(img)
    return images

def show_images_grid(images):
    plt.figure(figsize=(20, 20))
    for i, image in enumerate(images):
        plt.subplot(len(images) // 2 + 1, 2, i + 1)
        plt.imshow(image, cmap='gray')
    plt.show()