from PIL import Image

# --- Konstanta ---
DELIMITER = "11111111" + "11110000" + "00001111"  # Tanda akhir pesan
DELIMITER_LEN = len(DELIMITER)

# --- Konversi Teks <-> Bit ---
def text_to_bits(text: str) -> str:
    return "".join(f"{byte:08b}" for byte in text.encode('utf-8'))

def bits_to_text(bits: str) -> str:
    byte_chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    byte_list = [int(b, 2) for b in byte_chunks if len(b) == 8]
    try:
        return bytes(byte_list).decode('utf-8', 'ignore')
    except:
        return ""

# --- Konversi Gambar ke Bit (dan sebaliknya) ---
def image_to_bits(image: Image.Image) -> str:
    if image.mode != '1':
        image = image.convert('1')
    width, height = image.size
    width_bits = f'{width:016b}'
    height_bits = f'{height:016b}'
    pixel_bits = "".join('0' if p == 0 else '1' for p in image.getdata())
    return width_bits + height_bits + pixel_bits

def bits_to_image(bit_stream: str) -> Image.Image:
    width = int(bit_stream[0:16], 2)
    height = int(bit_stream[16:32], 2)
    pixel_data_str = bit_stream[32:]
    if len(pixel_data_str) != width * height:
        raise ValueError("Data bit tidak cocok dengan ukuran gambar.")
    img = Image.new('1', (width, height))
    img.putdata([int(p) * 255 for p in pixel_data_str])
    return img

# --- Encode Bit ke Gambar (dengan blok) ---
def _encode(cover_image: Image.Image, bits_to_hide: str, block_size: int = 1) -> Image.Image:
    cover = cover_image.copy().convert("RGB")
    width, height = cover.size
    data_with_delim = bits_to_hide + DELIMITER
    num_bits = len(data_with_delim)

    max_bits = (width // block_size) * (height // block_size) * 3
    if num_bits > max_bits:
        raise ValueError("Data terlalu besar untuk disisipkan pada ukuran blok ini.")

    pixels = cover.load()
    data_index = 0

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            if data_index >= num_bits:
                break
            r, g, b = pixels[x, y]
            if data_index < num_bits:
                r = (r & 0b11111110) | int(data_with_delim[data_index]); data_index += 1
            if data_index < num_bits:
                g = (g & 0b11111110) | int(data_with_delim[data_index]); data_index += 1
            if data_index < num_bits:
                b = (b & 0b11111110) | int(data_with_delim[data_index]); data_index += 1
            pixels[x, y] = (r, g, b)

    return cover

# --- Decode Bit dari Gambar (dengan blok) ---
def _decode(stego_image: Image.Image, block_size: int = 1) -> str:
    stego = stego_image.copy().convert("RGB")
    width, height = stego.size
    pixels = stego.load()

    message_bits = []
    buffer = ""

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            r, g, b = pixels[x, y]
            for bit in [r & 1, g & 1, b & 1]:
                message_bits.append(str(bit))
                buffer += str(bit)
                if len(buffer) > DELIMITER_LEN:
                    buffer = buffer[1:]
                if buffer == DELIMITER:
                    return "".join(message_bits[:-DELIMITER_LEN])

    raise ValueError("Delimiter tidak ditemukan.")

# --- Fungsi Publik ---
def encode_text(cover_image: Image.Image, secret_text: str, block_size: int = 1) -> Image.Image:
    return _encode(cover_image, text_to_bits(secret_text), block_size)

def decode_text(stego_image: Image.Image, block_size: int = 1) -> str:
    return bits_to_text(_decode(stego_image, block_size))

def encode_image(cover_image: Image.Image, secret_image: Image.Image, block_size: int = 1) -> Image.Image:
    return _encode(cover_image, image_to_bits(secret_image), block_size)

def decode_image(stego_image: Image.Image, block_size: int = 1) -> Image.Image:
    return bits_to_image(_decode(stego_image, block_size))
