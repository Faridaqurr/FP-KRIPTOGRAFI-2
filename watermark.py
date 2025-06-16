# watermark.py (VERSI BARU DENGAN WATERMARK TEKS)

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def add_image_watermark(base_image, watermark_logo, position=('bottom-right'), opacity=0.5, scale=0.1):
    """Menambahkan watermark logo ke gambar dasar."""
    base = base_image.copy().convert("RGBA")
    
    # Buat layer watermark dari logo, pastikan mode RGBA
    watermark = watermark_logo.copy().convert("RGBA")

    # Atur opacity (alpha channel) dari watermark
    if opacity < 1.0:
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    
    # Ubah ukuran watermark
    base_width, base_height = base.size
    watermark_width_target = int(base_width * scale)
    
    # Menjaga aspek rasio logo
    ratio = watermark_width_target / float(watermark.size[0])
    watermark_height_target = int(float(watermark.size[1]) * float(ratio))
    watermark = watermark.resize((watermark_width_target, watermark_height_target), Image.Resampling.LANCZOS)
    
    wm_width, wm_height = watermark.size
    
    # Tentukan posisi
    margin = 10
    if position == 'center':
        pos_x = (base_width - wm_width) // 2
        pos_y = (base_height - wm_height) // 2
    elif position == 'top-left':
        pos_x = margin
        pos_y = margin
    elif position == 'top-right':
        pos_x = base_width - wm_width - margin
        pos_y = margin
    elif position == 'bottom-left':
        pos_x = margin
        pos_y = base_height - wm_height - margin
    else: # Default ke bottom-right
        pos_x = base_width - wm_width - margin
        pos_y = base_height - wm_height - margin
        
    # Buat layer transparan untuk menempelkan watermark
    transparent_layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    transparent_layer.paste(watermark, (pos_x, pos_y), mask=watermark) # Gunakan mask untuk transparansi yg benar
    
    # Gabungkan gambar dasar dengan layer watermark
    watermarked_image = Image.alpha_composite(base, transparent_layer)
    
    return watermarked_image.convert("RGB")


def add_text_watermark(base_image, text, position=('bottom-right'), opacity=0.5, font_size=50, font_color=(255, 255, 255)):
    """Menambahkan watermark teks ke gambar dasar."""
    base = base_image.copy().convert("RGBA")
    
    # Buat layer transparan untuk menggambar teks
    txt_layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    
    # Coba muat font, jika gagal gunakan font default
    try:
        # Font 'arial.ttf' umum di Windows. Untuk sistem lain mungkin perlu 'DejaVuSans.ttf'
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    draw = ImageDraw.Draw(txt_layer)
    
    base_width, base_height = base.size
    
    # Hitung ukuran bounding box teks
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Atur warna dengan opacity
    r, g, b = font_color
    alpha = int(255 * opacity)
    final_color = (r, g, b, alpha)
    
    # Tentukan posisi
    margin = 10
    if position == 'center':
        pos_x = (base_width - text_width) // 2
        pos_y = (base_height - text_height) // 2
    elif position == 'top-left':
        pos_x = margin
        pos_y = margin
    elif position == 'top-right':
        pos_x = base_width - text_width - margin
        pos_y = margin
    elif position == 'bottom-left':
        pos_x = margin
        pos_y = base_height - text_height - margin
    else: # Default ke bottom-right
        pos_x = base_width - text_width - margin
        pos_y = base_height - text_height - margin

    # Gambar teks ke layer transparan
    draw.text((pos_x, pos_y), text, font=font, fill=final_color)
    
    # Gabungkan gambar dasar dengan layer teks
    watermarked_image = Image.alpha_composite(base, txt_layer)
    
    return watermarked_image.convert("RGB")