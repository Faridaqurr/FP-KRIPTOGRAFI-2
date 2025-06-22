from PIL import Image
import random
import itertools

def _get_bw_patterns(n: int):
    """Membangkitkan pola untuk skema (n, n)-VCS."""
    base_matrices = [
        (0, 0, 255, 255), (255, 255, 0, 0),
        (0, 255, 0, 255), (255, 0, 255, 0),
        (0, 255, 255, 0), (255, 0, 0, 255)
    ]
    black_patterns = list(itertools.permutations(random.choice(base_matrices), 4))
    return base_matrices, black_patterns

def create_color_shares(image: Image.Image, n_shares: int) -> list:
    """Membuat n-jumlah shares dari sebuah gambar berwarna menggunakan dithering."""
    if n_shares < 2:
        raise ValueError("Jumlah shares harus minimal 2.")
    
    image = image.convert("RGB")
    source_channels = image.split()
    width, height = image.size
    share_width, share_height = width * 2, height * 2
    
    processed_channels = []
    
    for channel_img in source_channels:
        bw_channel = channel_img.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
        current_channel_shares = [Image.new('1', (share_width, share_height)) for _ in range(n_shares)]
        white_patterns, black_patterns_base = _get_bw_patterns(n_shares)

        for y in range(height):
            for x in range(width):
                pixel = bw_channel.getpixel((x, y))
                patterns_for_shares = (
                    [random.choice(white_patterns)] * n_shares if pixel == 255
                    else random.sample(black_patterns_base, n_shares)
                )

                for i in range(n_shares):
                    p = patterns_for_shares[i]
                    pixels_share = current_channel_shares[i].load()
                    pixels_share[x * 2, y * 2] = p[0]
                    pixels_share[x * 2 + 1, y * 2] = p[1]
                    pixels_share[x * 2, y * 2 + 1] = p[2]
                    pixels_share[x * 2 + 1, y * 2 + 1] = p[3]
        
        processed_channels.append(current_channel_shares)

    final_shares = []
    red_shares, green_shares, blue_shares = processed_channels

    for i in range(n_shares):
        final_share_img = Image.new("RGB", (share_width, share_height))
        pixels_final = final_share_img.load()
        pixels_r = red_shares[i].load()
        pixels_g = green_shares[i].load()
        pixels_b = blue_shares[i].load()

        for y in range(share_height):
            for x in range(share_width):
                r_val = pixels_r[x, y]
                g_val = pixels_g[x, y]
                b_val = pixels_b[x, y]
                pixels_final[x, y] = (r_val, g_val, b_val)
        
        final_shares.append(final_share_img)

    return final_shares

def combine_color_shares(shares: list) -> Image.Image:
    """Menggabungkan beberapa share berwarna untuk merekonstruksi gambar."""
    if not shares or len(shares) < 2:
        raise ValueError("Dibutuhkan minimal 2 shares untuk digabungkan.")
    first_share = shares[0]
    size = first_share.size
    for share in shares[1:]:
        if share.size != size:
            raise ValueError("Semua share harus memiliki ukuran yang sama.")
    result_image = Image.new("RGB", size, (255, 255, 255))
    pixels_res = result_image.load()
    shares_pixels = [share.load() for share in shares]
    for y in range(size[1]):
        for x in range(size[0]):
            final_r = min(s[x, y][0] for s in shares_pixels)
            final_g = min(s[x, y][1] for s in shares_pixels)
            final_b = min(s[x, y][2] for s in shares_pixels)
            pixels_res[x, y] = (final_r, final_g, final_b)
            
    return result_image