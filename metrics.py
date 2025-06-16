# metrics.py

import numpy as np
from skimage.metrics import peak_signal_noise_ratio

def calculate_psnr(original_image, stego_image):
    """
    Menghitung nilai PSNR antara gambar asli dan gambar stego.
    
    Args:
        original_image (PIL.Image.Image): Gambar sampul asli.
        stego_image (PIL.Image.Image): Gambar setelah disisipi data.
        
    Returns:
        float: Nilai PSNR dalam desibel (dB).
    """
    # Pastikan kedua gambar memiliki ukuran yang sama dan format RGB
    if original_image.size != stego_image.size or original_image.mode != 'RGB' or stego_image.mode != 'RGB':
        # Coba konversi jika mode berbeda tapi ukuran sama
        if original_image.size == stego_image.size:
            original_image = original_image.convert('RGB')
            stego_image = stego_image.convert('RGB')
        else:
            raise ValueError("Ukuran atau mode gambar tidak cocok untuk perhitungan PSNR.")

    # Ubah gambar PIL menjadi array NumPy
    original_array = np.array(original_image)
    stego_array = np.array(stego_image)
    
    # Hitung PSNR menggunakan scikit-image
    # Data range adalah 255 karena ini adalah gambar 8-bit
    psnr_value = peak_signal_noise_ratio(original_array, stego_array, data_range=255)
    
    return psnr_value
