# metrics.py

import numpy as np
from skimage.metrics import peak_signal_noise_ratio, mean_squared_error

def calculate_metrics(original_image, stego_image):
    """
    Menghitung metrik kualitas gambar: PSNR (standar), MSE, dan Skor Kemiripan (0-100%).
    
    Fungsi ini efisien karena menghitung semua metrik yang dibutuhkan 
    dalam satu kali pemanggilan.
    
    Args:
        original_image (PIL.Image.Image): Gambar sampul asli.
        stego_image (PIL.Image.Image): Gambar setelah disisipi data.
        
    Returns:
        dict: Sebuah dictionary berisi nilai 'psnr', 'mse', dan 'similarity_score'.
    """
    # 1. Validasi Ukuran Gambar
    if original_image.size != stego_image.size:
        raise ValueError("Ukuran gambar harus sama untuk perhitungan metrik.")
    
    # 2. Persiapan Data: Ubah gambar ke format yang konsisten (RGB) dan array NumPy
    original_array = np.array(original_image.convert('RGB'), dtype=np.float64)
    stego_array = np.array(stego_image.convert('RGB'), dtype=np.float64)
    mse_value = mean_squared_error(original_array, stego_array)
    
    # 3. Tangani kasus khusus: gambar identik
    # Menghindari pembagian dengan nol.
    if mse_value == 0:
        return {
            'psnr': float('inf'),       # PSNR tak terhingga jika tidak ada error
            'mse': 0.0,                 # MSE adalah 0
            'similarity_score': 100.0   # Skor kemiripan 100%
        }
    
    # 4. Hitung PSNR standar
    # Hanya dihitung jika MSE tidak nol.
    psnr_value = peak_signal_noise_ratio(original_array, stego_array, data_range=255)
    
    # 5. Hitung skor kemiripan (0-100%)
    max_mse = 255**2  # Error maksimum yang mungkin terjadi
    similarity_score = max(0, 100 * (1 - (mse_value / max_mse)))
    
    # 6. Kembalikan semua metrik dalam satu dictionary yang terstruktur
    return {
        'psnr': psnr_value,
        'mse': mse_value,
        'similarity_score': similarity_score
    }