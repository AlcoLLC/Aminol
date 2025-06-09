import os
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import shutil
import cairosvg  # SVG to PNG conversion için gerekli

# Target size range in kilobytes
TARGET_MIN_KB = 800
TARGET_MAX_KB = 1200

# WebP quality settings
WEBP_QUALITY_MIN = 30
WEBP_QUALITY_MAX = 95

# Supported image formats (SVG eklendi)
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.bmp', '.tiff', '.gif')

# Source directory for original images
SOURCE_DIR = "/Aminol/mediafiles"

# Target directory for compressed images
COMPRESSED_OUTPUT_DIR = "/Aminol/medias"


def get_file_size_kb(buffer):
    """Return file size in KB from BytesIO buffer"""
    return len(buffer.getvalue()) / 1024

def compress_webp(img):
    """Iteratively compress WebP to target size"""
    last_buffer = None
    for quality in range(WEBP_QUALITY_MAX, WEBP_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality, optimize=True)
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer
    return last_buffer

def convert_svg_to_image(svg_path):
    """Convert SVG to PIL Image object"""
    try:
        # SVG'yi PNG'ye çevir
        png_data = cairosvg.svg2png(url=svg_path)
        # PNG verisini PIL Image'e yükle
        img = Image.open(BytesIO(png_data))
        return img
    except Exception as e:
        print(f"❌ SVG dönüştürme hatası {svg_path}: {e}")
        return None

def process_single_image(original_image_path, compressed_image_save_path):
    """Convert and compress a single image file to WebP format.
    If the image is too small (<10KB), it will be converted to WebP anyway."""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024
        
        # Dosya uzantısını kontrol et
        file_ext = os.path.splitext(original_image_path)[1].lower()
        
        # SVG dosyası kontrolü
        if file_ext == '.svg':
            img = convert_svg_to_image(original_image_path)
            if img is None:
                return False
            print(f"🔄 SVG dönüştürüldü: {original_image_path}")
        else:
            img = Image.open(original_image_path)

        # Çıktı dosyasının uzantısını .webp olarak değiştir
        base_name = os.path.splitext(os.path.basename(compressed_image_save_path))[0]
        dir_name = os.path.dirname(compressed_image_save_path)
        compressed_image_save_path = os.path.join(dir_name, base_name + '.webp')

        # Küçük dosyalar için özel işlem
        if original_size_kb < 10:
            try:
                # RGB moduna çevir (WebP için gerekli)
                if img.mode in ('RGBA', 'LA'):
                    # Şeffaflık varsa RGBA olarak tut
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                elif img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
                
                # Küçük dosyaları da WebP'ye çevir, yüksek kalite ile
                img.save(compressed_image_save_path, format="WEBP", quality=90, optimize=True)
                
                final_size_kb = os.path.getsize(compressed_image_save_path) / 1024
                print(f"📠 WebP'ye çevrildi (küçük dosya): {original_image_path} ({int(original_size_kb)} KB) -> {compressed_image_save_path} ({int(final_size_kb)} KB)")
                return True
            except Exception as e:
                print(f"❌ Küçük dosya {original_image_path} WebP'ye çevrilirken hata: {e}")
                return False

        # Mod dönüşümleri - WebP için optimize edildi
        if img.mode == 'P':
            if img.info.get("transparency") is not None:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
        elif img.mode == 'LA':
            img = img.convert("RGBA")
        elif img.mode not in ('RGB', 'RGBA', 'L'):
            # Diğer modları RGB'ye çevir
            img = img.convert("RGB")

        # WebP sıkıştırması
        buffer = compress_webp(img)

        if buffer is None or len(buffer.getvalue()) == 0:
            print(f"❌ WebP sıkıştırması {original_image_path} için başarısız oldu.")
            # Başarısız durumda yine de WebP olarak kaydetmeyi dene
            try:
                buffer = BytesIO()
                img.save(buffer, format="WEBP", quality=75, optimize=True)
                if len(buffer.getvalue()) == 0:
                    return False
            except:
                return False

        os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        compressed_size_kb = get_file_size_kb(buffer)
        print(f"✔ WebP'ye dönüştürüldü: {original_image_path}")
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
        print(f"❌ {original_image_path} işlenirken hata: {e} (Satır: {e.__traceback__.tb_lineno if e.__traceback__ else 'N/A'})")
        return False

def is_safe_path(path, base_dir):
    """Ensure path is within the intended base_dir to prevent directory traversal attacks."""
    try:
        abs_base = os.path.abspath(base_dir)
        abs_path = os.path.abspath(path)
        return abs_path.startswith(abs_base)
    except Exception:
        return False

def process_source_directory():
    """Recursively process all valid image files from SOURCE_DIR to COMPRESSED_OUTPUT_DIR, converting to WebP."""

    if not os.path.abspath(SOURCE_DIR).startswith(os.path.abspath("/Aminol")):
        print(f"❌ Güvenlik hatası: Kaynak yolu {SOURCE_DIR}, /Aminol içinde değil.")
        return
    if not os.path.abspath(COMPRESSED_OUTPUT_DIR).startswith(os.path.abspath("/Aminol")):
        print(f"❌ Güvenlik hatası: Hedef yolu {COMPRESSED_OUTPUT_DIR}, /Aminol içinde değil.")
        return

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Kaynak dizini mevcut değil: {SOURCE_DIR}")
        return
    if not os.path.isdir(SOURCE_DIR):
        print(f"❌ Kaynak yolu bir dizin değil: {SOURCE_DIR}")
        return

    if not os.path.exists(COMPRESSED_OUTPUT_DIR):
        try:
            os.makedirs(COMPRESSED_OUTPUT_DIR)
            print(f"📁 Hedef dizin oluşturuldu: {COMPRESSED_OUTPUT_DIR}")
        except Exception as e:
            print(f"❌ Hedef dizin {COMPRESSED_OUTPUT_DIR} oluşturulamadı: {e}")
            return

    total_source_files_found = 0
    successfully_processed_this_run = 0
    skipped_existing_count = 0
    failed_this_run = 0
    converted_small_files_count = 0
    svg_converted_count = 0

    try:
        for root, dirs, files in os.walk(SOURCE_DIR):
            if not is_safe_path(root, SOURCE_DIR):
                print(f"⏭ Gezinme sırasında güvenli olmayan yol atlanıyor: {root}")
                continue

            for file in files:
                if file.lower().endswith(IMAGE_EXTENSIONS):
                    total_source_files_found += 1
                    original_path = os.path.join(root, file)

                    if not is_safe_path(original_path, SOURCE_DIR):
                        print(f"⏭ Güvenli olmayan orijinal dosya yolu atlanıyor: {original_path}")
                        continue

                    relative_path = os.path.relpath(original_path, SOURCE_DIR)
                    
                    # Çıktı dosyasının uzantısını .webp olarak değiştir
                    base_name = os.path.splitext(relative_path)[0]
                    compressed_save_path = os.path.join(COMPRESSED_OUTPUT_DIR, base_name + '.webp')

                    if not is_safe_path(compressed_save_path, COMPRESSED_OUTPUT_DIR):
                        print(f"⏭ Güvenli olmayan hedef kayıt yolu atlanıyor: {compressed_save_path}")
                        continue

                    if os.path.exists(compressed_save_path):
                        print(f"⏭ WebP dosyası hedefte zaten mevcut: {compressed_save_path}. Atlanıyor.")
                        skipped_existing_count += 1
                        continue

                    original_size_kb_before_process = os.path.getsize(original_path) / 1024
                    is_svg = original_path.lower().endswith('.svg')
                    
                    processed_successfully = process_single_image(original_path, compressed_save_path)

                    if processed_successfully:
                        successfully_processed_this_run += 1
                        if original_size_kb_before_process < 10:
                            converted_small_files_count += 1
                        if is_svg:
                            svg_converted_count += 1
                    else:
                        failed_this_run += 1
    
    except PermissionError as e:
        print(f"❌ Dizin işlenirken izin reddedildi: {e}")
    except Exception as e:
        print(f"❌ Dizin işlenirken hata: {e}")

    print(f"\n🏁 WebP dönüştürme işlemi tamamlandı.")
    print(f"🔎 Kaynakta bulunan toplam resim dosyası: {total_source_files_found}")
    print(f"📠 WebP'ye çevrilen küçük (<10KB) dosyalar: {converted_small_files_count}")
    print(f"🔄 SVG'den WebP'ye çevrilen dosyalar: {svg_converted_count}")
    print(f"⏭ Atlanan (hedefte zaten mevcut olan): {skipped_existing_count}")
    print(f"✔ Bu çalıştırmada başarıyla WebP'ye çevrilen: {successfully_processed_this_run}")
    print(f"❌ Bu çalıştırmada işlenemeyen: {failed_this_run}")
    attempted_this_run = successfully_processed_this_run + failed_this_run
    print(f"🛠 Bu çalıştırmada işlenmeye çalışılan: {attempted_this_run}")


if __name__ == "__main__":
    print(f"🚀 WebP dönüştürme ve sıkıştırma başlatılıyor.")
    print(f"📂 Kaynak dizin: {SOURCE_DIR}")
    print(f"💾 WebP dosyaları için hedef dizin: {COMPRESSED_OUTPUT_DIR}")
    print(f"📏 Hedef boyut aralığı: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print(f"🔄 Tüm resimler (SVG dahil) WebP formatına çevrilecektir.")
    print(f"❗ Not: SVG dosyaları önce PNG'ye, sonra WebP'ye çevrilecektir.")
    print("-" * 60)

    # SVG desteği için cairosvg kontrolü
    try:
        import cairosvg
        print("✅ SVG desteği aktif.")
    except ImportError:
        print("⚠️  SVG desteği yok. SVG dosyalarını işlemek için 'pip install cairosvg' komutunu çalıştırın.")
        print("    SVG dosyaları atlanacaktır.")

    process_source_directory()