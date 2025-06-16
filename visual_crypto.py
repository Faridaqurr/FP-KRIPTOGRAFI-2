# visual_crypto.py

from PIL import Image
import random

# Pola 2x2 untuk piksel hitam dan putih
# Masing-masing memiliki 6 kemungkinan pola untuk kerandoman
PATTERNS = {
    'white': [
        ((255, 255, 0, 0), (255, 255, 0, 0)),
        ((0, 0, 255, 255), (0, 0, 255, 255)),
        ((255, 0, 255, 0), (255, 0, 255, 0)),
        ((0, 255, 0, 255), (0, 255, 0, 255)),
        ((255, 0, 0, 255), (255, 0, 0, 255)),
        ((0, 255, 255, 0), (0, 255, 255, 0)),
    ],
    'black': [
        ((255, 255, 0, 0), (0, 0, 255, 255)),
        ((0, 0, 255, 255), (255, 255, 0, 0)),
        ((255, 0, 255, 0), (0, 255, 0, 255)),
        ((0, 255, 0, 255), (255, 0, 255, 0)),
        ((255, 0, 0, 255), (0, 255, 255, 0)),
        ((0, 255, 255, 0), (255, 0, 0, 255)),
    ]
}

def create_shares(image: Image.Image) -> (Image.Image, Image.Image):
    """
    Membuat dua share dari sebuah gambar hitam-putih.
    Setiap piksel dari gambar asli diperluas menjadi blok 2x2 piksel di setiap share.
    """
    if image.mode != '1':
        image = image.convert('1')

    width, height = image.size
    share1 = Image.new('1', (width * 2, height * 2))
    share2 = Image.new('1', (width * 2, height * 2))
    
    pixels1 = share1.load()
    pixels2 = share2.load()

    for x in range(width):
        for y in range(height):
            # Dapatkan warna piksel asli (0 untuk hitam, 255 untuk putih)
            pixel_color = image.getpixel((x, y))
            
            # Pilih pola berdasarkan warna piksel
            if pixel_color == 255:  # Putih
                p1, p2 = random.choice(PATTERNS['white'])
            else:  # Hitam
                p1, p2 = random.choice(PATTERNS['black'])

            # Terapkan pola 2x2 ke shares
            # (kiri-atas, kanan-atas, kiri-bawah, kanan-bawah)
            pixels1[x * 2, y * 2] = p1[0]
            pixels1[x * 2 + 1, y * 2] = p1[1]
            pixels1[x * 2, y * 2 + 1] = p1[2]
            pixels1[x * 2 + 1, y * 2 + 1] = p1[3]
            
            pixels2[x * 2, y * 2] = p2[0]
            pixels2[x * 2 + 1, y * 2] = p2[1]
            pixels2[x * 2, y * 2 + 1] = p2[2]
            pixels2[x * 2 + 1, y * 2 + 1] = p2[3]

    return share1, share2

def combine_shares(share1: Image.Image, share2: Image.Image) -> Image.Image:
    """
    Menggabungkan dua share untuk merekonstruksi gambar.
    Ini mensimulasikan penumpukan dua transparansi.
    Piksel hasil akan hitam jika salah satu piksel di share adalah hitam.
    """
    if share1.size != share2.size:
        raise ValueError("Ukuran kedua share harus sama.")
    
    if share1.mode != '1':
        share1 = share1.convert('1')
    if share2.mode != '1':
        share2 = share2.convert('1')

    result_image = Image.new('1', share1.size)
    pixels_res = result_image.load()
    
    pixels1 = share1.load()
    pixels2 = share2.load()

    width, height = share1.size
    for x in range(width):
        for y in range(height):
            # Logika AND (jika salah satu 0/hitam, hasilnya 0/hitam)
            pixels_res[x, y] = min(pixels1[x, y], pixels2[x, y])
            
    return result_image