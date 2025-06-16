
from PIL import Image, ImageDraw, ImageFont
import io

def add_watermark(image: Image.Image, text: str):
    watermark = image.convert("RGBA")
    width, height = watermark.size

    txt_layer = Image.new("RGBA", watermark.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    font_size = int(min(width, height) / 20)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Use textbbox instead of deprecated textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    textwidth = bbox[2] - bbox[0]
    textheight = bbox[3] - bbox[1]
    x, y = width - textwidth - 20, height - textheight - 20

    draw.text((x, y), text, font=font, fill=(255, 0, 0, 128))
    combined = Image.alpha_composite(watermark, txt_layer)
    return combined.convert("RGB")
