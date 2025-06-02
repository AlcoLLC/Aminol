import os
import shutil
from PIL import Image, UnidentifiedImageError
from io import BytesIO

TARGET_MIN_KB = 800
TARGET_MAX_KB = 1200
JPEG_QUALITY_MIN = 30
JPEG_QUALITY_MAX = 95
PNG_COMPRESSION_LEVELS = list(range(9, -1, -1))
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg')

DIRECTORIES_TO_PROCESS = [
    {'source': 'staticfiles/images_1', 'target': 'staticfiles/images'},
    {'source': 'staticfiles/images_folder_1', 'target': 'staticfiles/images_folder'}
]


def get_file_size_kb(buffer):
    return len(buffer.getvalue()) / 1024


def compress_jpeg(img):
    best_buffer = None
    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        if TARGET_MIN_KB <= get_file_size_kb(buffer) <= TARGET_MAX_KB:
            return buffer
        best_buffer = buffer
    return best_buffer


def compress_png(img):
    last_buffer = None
    for level in PNG_COMPRESSION_LEVELS:
        buffer = BytesIO()
        img.save(buffer, format="PNG", optimize=True, compress_level=level)
        if TARGET_MIN_KB <= get_file_size_kb(buffer) <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer
    return last_buffer


def compress_webp(img):
    last_buffer = None
    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality)
        if TARGET_MIN_KB <= get_file_size_kb(buffer) <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer
    return last_buffer


def copy_svg_file(original_path, target_path):
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(original_path, target_path)
        print(f"📄 SVG kopyalandı: {original_path} → {target_path}")
        return True
    except Exception as e:
        print(f"❌ SVG dosyası kopyalanamadı: {original_path} → {e}")
        return False


def move_small_file(original_path, source_root):
    try:
        relative_path = os.path.relpath(original_path, source_root)
        skipped_path = os.path.join("staticfiles", "skipped_small_images", relative_path)
        os.makedirs(os.path.dirname(skipped_path), exist_ok=True)
        os.rename(original_path, skipped_path)
        print(f"📁 Küçük dosya taşındı: {skipped_path}")
    except Exception as e:
        print(f"❌ Küçük dosya taşınamadı: {original_path} → {e}")


def process_single_image(original_image_path, compressed_image_save_path, source_root):
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024

        if original_size_kb < 10:
            print(f"⏭ İşlenemeyecek kadar küçük dosya: {original_image_path} ({int(original_size_kb)} KB)")
            move_small_file(original_image_path, source_root)
            return False

        img = Image.open(original_image_path)
        img_format = img.format.upper() if img.format else ''

        # Convert modes
        if img.mode in ['P', 'LA']:
            img = img.convert("RGBA") if 'A' in img.mode or img.info.get("transparency") else img.convert("RGB")
        elif img_format != "PNG" and img.mode == "RGBA":
            img = img.convert("RGB")
        elif img_format == "PNG":
            if img.mode not in ["RGBA", "LA"] and 'A' not in img.mode and img.info.get("transparency") is None:
                img = img.convert("RGB")

        # Compress
        buffer = None
        if img_format in ["JPEG", "JPG"]:
            img = img.convert("RGB") if img.mode == "RGBA" else img
            buffer = compress_jpeg(img)
        elif img_format == "PNG":
            buffer = compress_png(img)
        elif img_format == "WEBP":
            buffer = compress_webp(img)
        else:
            try:
                img = img.convert("RGBA") if 'A' in img.mode or img.info.get("transparency") else img.convert("RGB")
                temp_buffer = BytesIO()
                img.save(temp_buffer, format="PNG", optimize=True)
                if not (TARGET_MIN_KB <= get_file_size_kb(temp_buffer) <= TARGET_MAX_KB):
                    buffer = compress_png(img)
                else:
                    buffer = temp_buffer
            except Exception as e:
                print(f"⏭ Bilinmeyen formatı dönüştürme hatası {original_image_path}: {e}")
                return False

        if not buffer or len(buffer.getvalue()) == 0:
            print(f"❌ Sıkıştırma başarısız: {original_image_path}")
            return False

        os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        compressed_size_kb = get_file_size_kb(buffer)
        print(f"✔ Sıkıştırıldı: {original_image_path}")
        print(f"  📊 {int(original_size_kb)} KB → {int(compressed_size_kb)} KB")
        return True

    except FileNotFoundError:
        print(f"❌ Dosya bulunamadı: {original_image_path}")
        return False
    except UnidentifiedImageError:
        print(f"❌ Tanınamayan resim dosyası: {original_image_path}")
        return False
    except Exception as e:
        print(f"❌ Genel hata ({original_image_path}): {e}")
        return False


def process_directory_pair(source_dir, target_dir):
    total_files = 0
    skipped_existing = 0
    processed = 0
    failed = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                total_files += 1
                original_path = os.path.join(root, file)
                relative_path = os.path.relpath(original_path, source_dir)
                compressed_path = os.path.join(target_dir, relative_path)

                if os.path.exists(compressed_path):
                    print(f"⏭ Zaten mevcut: {compressed_path}")
                    skipped_existing += 1
                    continue

                if file.lower().endswith('.svg'):
                    if copy_svg_file(original_path, compressed_path):
                        processed += 1
                    else:
                        failed += 1
                    continue

                if process_single_image(original_path, compressed_path, source_dir):
                    processed += 1
                else:
                    failed += 1

    return total_files, skipped_existing, processed, failed


def process_all_directories():
    print(f"🚀 Sıkıştırma başlatıldı ({TARGET_MIN_KB}-{TARGET_MAX_KB} KB hedef boyut)")
    print("-" * 80)

    totals = [0, 0, 0, 0]

    for pair in DIRECTORIES_TO_PROCESS:
        source, target = pair['source'], pair['target']
        print(f"\n📂 İşleniyor: {source} → {target}")
        print("-" * 60)

        result = process_directory_pair(source, target)
        totals = [sum(x) for x in zip(totals, result)]

        print(f"\n📊 {source} özeti:")
        print(f"🔎 Toplam dosya bulundu: {result[0]}")
        print(f"⏭ Atlanan (zaten var): {result[1]}")
        print(f"✔ Sıkıştırıldı/kopyalandı: {result[2]}")
        print(f"❌ Başarısız: {result[3]}")

    print("\n" + "=" * 80)
    print("🏁 GENEL ÖZET")
    print(f"🔎 Toplam dosya bulundu: {totals[0]}")
    print(f"⏭ Toplam atlanan: {totals[1]}")
    print(f"✔ Başarılı: {totals[2]}")
    print(f"❌ Başarısız: {totals[3]}")
    print(f"🛠 İşlenmeye çalışılan toplam: {totals[2] + totals[3]}")


if __name__ == "__main__":
    process_all_directories()
