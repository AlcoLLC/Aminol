import os
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import shutil
import warnings

# Image limits
Image.MAX_IMAGE_PIXELS = 200000000
warnings.filterwarnings("ignore", "Image size")

# SVG desteği
try:
    import cairosvg
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False

# Hedef boyut aralığı (KB)
TARGET_MIN_KB = 20
TARGET_MAX_KB = 50

# WebP kalite aralığı
WEBP_QUALITY_MIN = 30
WEBP_QUALITY_MAX = 95

# Maksimum görsel boyutu (200px sabit)
MAX_IMAGE_DIMENSION = 200

# Desteklenen uzantılar
if SVG_SUPPORT:
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.bmp', '.tiff', '.gif')
else:
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif')

# Kaynak ve hedef dizinler
SOURCE_DIR = "/Aminol/gallery"
COMPRESSED_OUTPUT_DIR = "/Aminol/mediafile/gallery"

def get_file_size_kb(buffer):
    return len(buffer.getvalue()) / 1024

def resize_to_max(img, max_dimension=MAX_IMAGE_DIMENSION):
    width, height = img.size
    if max(width, height) <= max_dimension:
        return img

    if width > height:
        new_width = max_dimension
        new_height = int(height * max_dimension / width)
    else:
        new_height = max_dimension
        new_width = int(width * max_dimension / height)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img

def compress_webp(img):
    last_buffer = None
    for quality in range(WEBP_QUALITY_MAX, WEBP_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        try:
            img.save(buffer, format="WEBP", quality=quality, optimize=True)
            size_kb = get_file_size_kb(buffer)
            if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
                return buffer
            last_buffer = buffer
        except:
            continue
    return last_buffer

def convert_svg_to_image(svg_path):
    if not SVG_SUPPORT:
        return None
    try:
        png_data = cairosvg.svg2png(url=svg_path)
        img = Image.open(BytesIO(png_data))
        return img
    except:
        return None

def safe_makedirs(path):
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
        os.makedirs(path, exist_ok=True)
        return True
    except:
        return False

def process_single_image(original_image_path, compressed_image_save_path):
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            return False

        file_ext = os.path.splitext(original_image_path)[1].lower()

        if file_ext == '.svg':
            img = convert_svg_to_image(original_image_path)
            if img is None:
                return False
        else:
            try:
                img = Image.open(original_image_path)
            except:
                return False

        img = resize_to_max(img)

        # Mode dönüşümü
        try:
            if img.mode in ['P', 'LA']:
                img = img.convert("RGBA")
            elif img.mode not in ['RGB', 'RGBA', 'L']:
                img = img.convert("RGB")
        except:
            try:
                img = img.convert("RGB")
            except:
                return False

        base_name = os.path.splitext(os.path.basename(compressed_image_save_path))[0]
        dir_name = os.path.dirname(compressed_image_save_path)
        compressed_image_save_path = os.path.join(dir_name, base_name + '.webp')

        if not safe_makedirs(dir_name):
            return False

        buffer = compress_webp(img)
        if buffer is None or len(buffer.getvalue()) == 0:
            return False

        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        return True

    except:
        return False

def is_safe_path(path, base_dir):
    try:
        abs_base = os.path.abspath(base_dir)
        abs_path = os.path.abspath(path)
        return abs_path.startswith(abs_base)
    except:
        return False

def process_source_directory():
    if not os.path.exists(SOURCE_DIR) or not os.path.isdir(SOURCE_DIR):
        print("❌ Geçerli kaynak dizini bulunamadı.")
        return

    if not safe_makedirs(COMPRESSED_OUTPUT_DIR):
        print("❌ Hedef dizin oluşturulamadı.")
        return

    for root, _, files in os.walk(SOURCE_DIR):
        if not is_safe_path(root, SOURCE_DIR):
            continue

        for file in files:
            if not file.lower().endswith(IMAGE_EXTENSIONS):
                continue

            original_path = os.path.join(root, file)
            if not is_safe_path(original_path, SOURCE_DIR):
                continue

            relative_path = os.path.relpath(original_path, SOURCE_DIR)
            base_name = os.path.splitext(relative_path)[0]
            compressed_save_path = os.path.join(COMPRESSED_OUTPUT_DIR, base_name + '.webp')

            if os.path.exists(compressed_save_path):
                continue

            process_single_image(original_path, compressed_save_path)

if __name__ == "__main__":
    print("🚀 200px WebP Dönüştürme Başladı...")
    process_source_directory()
    print("✅ İşlem Tamamlandı.")
