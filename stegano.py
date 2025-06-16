# stegano.py (PERBAIKAN FINAL v2 dengan Buffer)

from PIL import Image

# Tanda akhir pesan yang unik untuk memastikan kita berhenti di tempat yang tepat
DELIMITER = "11111111" + "11110000" + "00001111"  # 3 byte unik: 255, 240, 15
DELIMITER_LEN = len(DELIMITER)

def text_to_bits(text: str) -> str:
    """Mengubah string teks menjadi string bit menggunakan UTF-8."""
    return "".join(f"{byte:08b}" for byte in text.encode('utf-8'))

def bits_to_text(bits: str) -> str:
    """Mengubah string bit kembali menjadi teks."""
    byte_chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    # Filter out chunks that are not 8 bits long
    valid_chunks = [b for b in byte_chunks if len(b) == 8]
    byte_list = [int(b, 2) for b in valid_chunks]
    
    try:
        return bytes(byte_list).decode('utf-8', 'ignore')
    except (ValueError, TypeError):
        return "" # Return empty string on error

def image_to_bits(image: Image.Image) -> str:
    """Mengubah gambar (mode '1') menjadi string bit, termasuk ukurannya."""
    if image.mode != '1':
        image = image.convert('1')
    
    width, height = image.size
    width_bits = f'{width:016b}'
    height_bits = f'{height:016b}'
    
    pixel_bits = "".join('0' if p == 0 else '1' for p in image.getdata())
    return width_bits + height_bits + pixel_bits

def bits_to_image(bit_stream: str) -> Image.Image:
    """Mengubah string bit kembali menjadi gambar."""
    try:
        width = int(bit_stream[0:16], 2)
        height = int(bit_stream[16:32], 2)
        pixel_data_str = bit_stream[32:]
        
        if len(pixel_data_str) != width * height:
            raise ValueError("Data bit tidak cocok dengan ukuran gambar.")
            
        img = Image.new('1', (width, height))
        img.putdata([int(p) * 255 for p in pixel_data_str])
        return img
    except (ValueError, IndexError):
        raise ValueError("Gagal merekonstruksi gambar dari data bit.")

def _encode(cover_image: Image.Image, bits_to_hide: str) -> Image.Image:
    """Fungsi inti untuk menyembunyikan bit ke dalam gambar."""
    cover = cover_image.copy().convert("RGB")
    
    data_with_delimiter = bits_to_hide + DELIMITER
    num_bits = len(data_with_delimiter)
    
    max_bits = cover.width * cover.height * 3
    if num_bits > max_bits:
        raise ValueError("Data terlalu besar untuk disembunyikan di dalam gambar sampul.")

    data_index = 0
    pixels = cover.load()
    
    for y in range(cover.height):
        for x in range(cover.width):
            r, g, b = pixels[x, y]
            
            if data_index < num_bits:
                r = (r & 0b11111110) | int(data_with_delimiter[data_index]); data_index += 1
            if data_index < num_bits:
                g = (g & 0b11111110) | int(data_with_delimiter[data_index]); data_index += 1
            if data_index < num_bits:
                b = (b & 0b11111110) | int(data_with_delimiter[data_index]); data_index += 1
            
            pixels[x, y] = (r, g, b)
            if data_index >= num_bits:
                return cover
    return cover

def _decode(stego_image: Image.Image) -> str:
    """Fungsi inti untuk mengekstrak bit dari gambar (dengan metode buffer)."""
    stego = stego_image.copy().convert("RGB")
    
    message_bits = []
    buffer = ""
    
    pixels = stego.getdata()
    for r, g, b in pixels:
        # Ekstrak 3 bit dari piksel
        bits = str(r & 1) + str(g & 1) + str(b & 1)
        
        for bit in bits:
            message_bits.append(bit)
            buffer += bit
            
            # Jika buffer lebih panjang dari delimiter, buang bit pertama
            if len(buffer) > DELIMITER_LEN:
                buffer = buffer[1:]
            
            # Cek jika buffer sama dengan delimiter
            if buffer == DELIMITER:
                # Delimiter ditemukan. Kembalikan semua bit SEBELUM delimiter.
                # Panjang pesan asli adalah total bit yang dibaca dikurangi panjang delimiter.
                final_message_len = len(message_bits) - DELIMITER_LEN
                return "".join(message_bits[:final_message_len])
                
    raise ValueError("Delimiter tidak ditemukan. Data mungkin rusak atau tidak ada.")


# --- Fungsi Publik (Tidak ada perubahan di sini) ---
def encode_text(cover_image: Image.Image, secret_text: str) -> Image.Image:
    bits = text_to_bits(secret_text)
    return _encode(cover_image, bits)

def decode_text(stego_image: Image.Image) -> str:
    bits = _decode(stego_image)
    return bits_to_text(bits)

def encode_image(cover_image: Image.Image, secret_image: Image.Image) -> Image.Image:
    bits = image_to_bits(secret_image)
    return _encode(cover_image, bits)

def decode_image(stego_image: Image.Image) -> Image.Image:
    bits = _decode(stego_image)
    return bits_to_image(bits)