import os
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Target size range in kilobytes
TARGET_MIN_KB = 800
TARGET_MAX_KB = 1200

# JPEG/WebP quality settings
JPEG_QUALITY_MIN = 30
JPEG_QUALITY_MAX = 95

# PNG compression levels (strongest first)
PNG_COMPRESSION_LEVELS = list(range(9, -1, -1))

# Supported image formats
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')

# Source and target directories
DIRECTORIES_TO_PROCESS = [
    {
        'source': 'staticfiles/images_1',
        'target': 'staticfiles/images'
    },
    {
        'source': 'staticfiles/images_folder_1',
        'target': 'staticfiles/images_folder'
    }
]


def get_file_size_kb(buffer):
    """Return file size in KB from BytesIO buffer"""
    return len(buffer.getvalue()) / 1024

def compress_jpeg(img):
    """Iteratively compress JPEG to target size"""
    best_buffer = None
    final_buffer_to_return = None

    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size_kb = get_file_size_kb(buffer)

        if final_buffer_to_return is None:
            final_buffer_to_return = buffer

        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer

        best_buffer = buffer

    return best_buffer

def compress_png(img):
    """Iteratively compress PNG to target size"""
    last_buffer = None
    for level in PNG_COMPRESSION_LEVELS:
        buffer = BytesIO()
        img.save(buffer, format="PNG", optimize=True, compress_level=level)
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer
    return last_buffer

def compress_webp(img):
    """Iteratively compress WebP to target size"""
    last_buffer = None
    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality)
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer
    return last_buffer

def process_single_image(original_image_path, compressed_image_save_path):
    """Compress a single image file and save it to the new destination."""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024

        if original_size_kb < 10:
            print(f"⏭ İşlenemeyecek kadar küçük dosya: {original_image_path} ({int(original_size_kb)} KB)")
            return False

        img = Image.open(original_image_path)
        img_format = img.format.upper() if img.format else ''

        # Mode conversions
        if img.mode == 'P' or img.mode == 'LA':
            if 'A' in img.mode or img.info.get("transparency") is not None:
                 img = img.convert("RGBA")
            else:
                 img = img.convert("RGB")
        elif img_format != "PNG" and img.mode == "RGBA":
            img = img.convert("RGB")
        elif img_format == "PNG" and img.mode not in ["RGBA", "LA"] and 'A' not in img.mode and img.info.get("transparency") is None:
            if img.mode != "RGB":
                 img = img.convert("RGB")

        buffer = None
        if img_format in ["JPEG", "JPG"]:
            if img.mode == "RGBA":
                img = img.convert("RGB")
            buffer = compress_jpeg(img)
        elif img_format == "PNG":
            buffer = compress_png(img)
        elif img_format == "WEBP":
            buffer = compress_webp(img)
        else:
            try:
                print(f"ℹ️ Desteklenmeyen format: {img_format}. PNG olarak kaydedilmeye çalışılıyor.")
                if img.mode not in ["RGB", "RGBA"]:
                    img = img.convert("RGBA") if 'A' in img.mode or img.info.get("transparency") is not None else img.convert("RGB")

                temp_buffer = BytesIO()
                img.save(temp_buffer, format="PNG", optimize=True)
                size_kb = get_file_size_kb(temp_buffer)
                if not (TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB):
                    if img.mode == 'P':
                         img = img.convert("RGBA")
                    elif 'A' not in img.mode and img.info.get("transparency") is None and img.mode != "RGB":
                         img = img.convert("RGB")

                    buffer = compress_png(img)
                else:
                    buffer = temp_buffer
            except Exception as conv_err:
                print(f"⏭ Bilinmeyen formatı dönüştürme/kaydetme hatası {original_image_path} ({img_format}): {conv_err}")
                return False

        if buffer is None or len(buffer.getvalue()) == 0:
            print(f"❌ Sıkıştırma {original_image_path} için bir buffer döndürmedi veya boş buffer döndürdü.")
            return False

        os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        compressed_size_kb = get_file_size_kb(buffer)
        print(f"✔ Sıkıştırıldı: {original_image_path}")
        print(f"  ↳ Kaydedildi: {compressed_image_save_path}")
        print(f"  📊 {int(original_size_kb)} KB → {int(compressed_size_kb)} KB")
        return True

    except FileNotFoundError:
        print(f"❌ İşlem sırasında dosya bulunamadı: {original_image_path}")
        return False
    except UnidentifiedImageError:
        print(f"❌ Resim dosyası tanımlanamadı (bozuk veya resim değil): {original_image_path}")
        return False
    except Exception as e:
        print(f"❌ {original_image_path} işlenirken hata: {e}")
        return False

def is_safe_path(path, base_dir):
    """Ensure path is within the intended base_dir to prevent directory traversal attacks."""
    try:
        abs_base = os.path.abspath(base_dir)
        abs_path = os.path.abspath(path)
        return abs_path.startswith(abs_base)
    except Exception:
        return False

def process_directory_pair(source_dir, target_dir):
    """Process images from source_dir to target_dir."""
    
    if not os.path.exists(source_dir):
        print(f"❌ Kaynak dizini mevcut değil: {source_dir}")
        return 0, 0, 0, 0
    if not os.path.isdir(source_dir):
        print(f"❌ Kaynak yolu bir dizin değil: {source_dir}")
        return 0, 0, 0, 0

    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
            print(f"📁 Hedef dizin oluşturuldu: {target_dir}")
        except Exception as e:
            print(f"❌ Hedef dizin {target_dir} oluşturulamadı: {e}")
            return 0, 0, 0, 0

    total_source_files_found = 0
    successfully_processed_this_run = 0
    skipped_existing_count = 0
    failed_this_run = 0

    try:
        for root, dirs, files in os.walk(source_dir):
            if not is_safe_path(root, source_dir):
                print(f"⏭ Gezinme sırasında güvenli olmayan yol atlanıyor: {root}")
                continue

            for file in files:
                if file.lower().endswith(IMAGE_EXTENSIONS):
                    total_source_files_found += 1
                    original_path = os.path.join(root, file)

                    if not is_safe_path(original_path, source_dir):
                        print(f"⏭ Güvenli olmayan orijinal dosya yolu atlanıyor: {original_path}")
                        continue

                    relative_path = os.path.relpath(original_path, source_dir)
                    compressed_save_path = os.path.join(target_dir, relative_path)

                    if not is_safe_path(compressed_save_path, target_dir):
                        print(f"⏭ Güvenli olmayan hedef kayıt yolu atlanıyor: {compressed_save_path}")
                        continue

                    # Check if compressed file already exists
                    if os.path.exists(compressed_save_path):
                        print(f"⏭ Dosya hedefte zaten mevcut: {compressed_save_path}. Atlanıyor.")
                        skipped_existing_count += 1
                        continue

                    if process_single_image(original_path, compressed_save_path):
                        successfully_processed_this_run += 1
                    else:
                        failed_this_run += 1
    
    except PermissionError as e:
        print(f"❌ Dizin işlenirken izin reddedildi: {e}")
    except Exception as e:
        print(f"❌ Dizin işlenirken hata: {e}")

    return total_source_files_found, skipped_existing_count, successfully_processed_this_run, failed_this_run

def process_all_directories():
    """Process all configured directory pairs."""
    
    print(f"🚀 Staticfiles resim sıkıştırma başlatılıyor.")
    print(f"📏 Hedef boyut aralığı: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print("-" * 80)
    
    grand_total_files = 0
    grand_total_skipped = 0
    grand_total_processed = 0
    grand_total_failed = 0
    
    for dir_config in DIRECTORIES_TO_PROCESS:
        source_dir = dir_config['source']
        target_dir = dir_config['target']
        
        print(f"\n📂 İşleniyor: {source_dir} → {target_dir}")
        print("-" * 60)
        
        total_files, skipped, processed, failed = process_directory_pair(source_dir, target_dir)
        
        print(f"\n📊 {source_dir} için özet:")
        print(f"🔎 Bulunan toplam resim dosyası: {total_files}")
        print(f"⏭ Atlanan (hedefte zaten mevcut olan): {skipped}")
        print(f"✔ Başarıyla sıkıştırılan: {processed}")
        print(f"❌ İşlenemeyen: {failed}")
        
        grand_total_files += total_files
        grand_total_skipped += skipped
        grand_total_processed += processed
        grand_total_failed += failed
    
    print(f"\n" + "=" * 80)
    print(f"🏁 TÜM DİZİNLER İÇİN GENEL ÖZET:")
    print(f"🔎 Toplam bulunan resim dosyası: {grand_total_files}")
    print(f"⏭ Toplam atlanan (hedefte zaten mevcut olan): {grand_total_skipped}")
    print(f"✔ Toplam başarıyla sıkıştırılan: {grand_total_processed}")
    print(f"❌ Toplam işlenemeyen: {grand_total_failed}")
    attempted_total = grand_total_processed + grand_total_failed
    print(f"🛠 Toplam işlenmeye çalışılan: {attempted_total}")


if __name__ == "__main__":
    process_all_directories()