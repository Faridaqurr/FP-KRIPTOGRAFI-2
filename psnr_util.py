from PIL import Image
import numpy as np
import math

def calculate_psnr(img1: Image.Image, img2: Image.Image) -> float:
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB").resize(img1.size)

    arr1 = np.array(img1).astype(np.float64)
    arr2 = np.array(img2).astype(np.float64)
    mse = np.mean((arr1 - arr2) ** 2)
    if mse == 0:
        return float("inf")
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
