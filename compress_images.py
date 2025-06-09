import os
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import shutil
import warnings

# Increase PIL's image size limit and configure warnings
Image.MAX_IMAGE_PIXELS = 200000000  # Increase limit to ~200MP
warnings.filterwarnings("ignore", "Image size")  # Suppress decompression bomb warnings

# Try to import cairosvg, but make it optional
try:
    import cairosvg
    SVG_SUPPORT = True
    print("✅ SVG support available")
except ImportError:
    SVG_SUPPORT = False
    print("⚠️  SVG support not available. Install Cairo dependencies and cairosvg for SVG processing.")

# Target size range in kilobytes
TARGET_MIN_KB = 800
TARGET_MAX_KB = 1200

# WebP quality settings
WEBP_QUALITY_MIN = 30
WEBP_QUALITY_MAX = 95

# Maximum image dimensions for processing (to prevent memory issues)
MAX_IMAGE_DIMENSION = 8000

# Supported image formats (SVG only if cairosvg is available)
if SVG_SUPPORT:
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.bmp', '.tiff', '.gif')
else:
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif')

# Source directory for original images
SOURCE_DIR = "/Aminol/mediafiles"

# Target directory for compressed images
COMPRESSED_OUTPUT_DIR = "/Aminol/medias"


def get_file_size_kb(buffer):
    """Return file size in KB from BytesIO buffer"""
    return len(buffer.getvalue()) / 1024

def resize_if_too_large(img, max_dimension=MAX_IMAGE_DIMENSION):
    """Resize image if it's too large to prevent memory issues"""
    width, height = img.size
    if max(width, height) > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int((height * max_dimension) / width)
        else:
            new_height = max_dimension
            new_width = int((width * max_dimension) / height)
        
        print(f"  🔄 Resizing from {width}x{height} to {new_width}x{new_height}")
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return img

def compress_webp(img):
    """Iteratively compress WebP to target size"""
    last_buffer = None
    for quality in range(WEBP_QUALITY_MAX, WEBP_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        try:
            img.save(buffer, format="WEBP", quality=quality, optimize=True)
            size_kb = get_file_size_kb(buffer)
            if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
                return buffer
            last_buffer = buffer
        except Exception as e:
            print(f"    ⚠️ WebP compression failed at quality {quality}: {e}")
            continue
    return last_buffer

def convert_svg_to_image(svg_path):
    """Convert SVG to PIL Image object"""
    if not SVG_SUPPORT:
        print(f"❌ SVG support not available for {svg_path}")
        return None
    
    try:
        # SVG'yi PNG'ye çevir
        png_data = cairosvg.svg2png(url=svg_path)
        # PNG verisini PIL Image'e yükle
        img = Image.open(BytesIO(png_data))
        return img
    except Exception as e:
        print(f"❌ SVG dönüştürme hatası {svg_path}: {e}")
        return None

def safe_makedirs(path):
    """Safely create directories, handling conflicts with existing files"""
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                # If a file exists with the same name, remove it
                print(f"  ⚠️ Removing conflicting file: {path}")
                os.remove(path)
            elif os.path.isdir(path):
                # Directory already exists, that's fine
                return True
        
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"  ❌ Failed to create directory {path}: {e}")
        return False

def process_single_image(original_image_path, compressed_image_save_path):
    """Convert and compress a single image file to WebP format.
    If the image is too small (<10KB), it will be converted to WebP anyway."""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024
        
        # Skip extremely large files that might cause memory issues
        if original_size_kb > 50000:  # 50MB limit
            print(f"⏭ Dosya çok büyük ({int(original_size_kb)} KB), atlanıyor: {original_image_path}")
            return False
        
        # Dosya uzantısını kontrol et
        file_ext = os.path.splitext(original_image_path)[1].lower()
        
        # SVG dosyası kontrolü
        if file_ext == '.svg':
            if not SVG_SUPPORT:
                print(f"⏭ SVG support not available, skipping: {original_image_path}")
                return False
            img = convert_svg_to_image(original_image_path)
            if img is None:
                return False
            print(f"🔄 SVG dönüştürüldü: {original_image_path}")
        else:
            try:
                img = Image.open(original_image_path)
            except Exception as e:
                print(f"❌ Resim açılamadı {original_image_path}: {e}")
                return False

        # Resize if too large
        img = resize_if_too_large(img)

        # Çıktı dosyasının uzantısını .webp olarak değiştir
        base_name = os.path.splitext(os.path.basename(compressed_image_save_path))[0]
        dir_name = os.path.dirname(compressed_image_save_path)
        compressed_image_save_path = os.path.join(dir_name, base_name + '.webp')

        # Create output directory safely
        output_dir = os.path.dirname(compressed_image_save_path)
        if not safe_makedirs(output_dir):
            return False

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
                
                # Küçük dosyaları da WebP'ye çevir, yüksek kalite ile
                img.save(compressed_image_save_path, format="WEBP", quality=90, optimize=True)
                
                final_size_kb = os.path.getsize(compressed_image_save_path) / 1024
                print(f"📠 WebP'ye çevrildi (küçük dosya): {original_image_path} ({int(original_size_kb)} KB) -> {compressed_image_save_path} ({int(final_size_kb)} KB)")
                return True
            except Exception as e:
                print(f"❌ Küçük dosya {original_image_path} WebP'ye çevrilirken hata: {e}")
                return False

        # Mod dönüşümleri - WebP için optimize edildi
        try:
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
        except Exception as e:
            print(f"  ⚠️ Mode conversion issue: {e}")
            # Try to convert to RGB as fallback
            try:
                img = img.convert("RGB")
            except:
                return False

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
    except MemoryError:
        print(f"❌ Yetersiz bellek: {original_image_path} (dosya çok büyük)")
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

    # Create main output directory
    if not safe_makedirs(COMPRESSED_OUTPUT_DIR):
        print(f"❌ Ana hedef dizin {COMPRESSED_OUTPUT_DIR} oluşturulamadı")
        return
    else:
        print(f"📁 Hedef dizin hazır: {COMPRESSED_OUTPUT_DIR}")

    total_source_files_found = 0
    successfully_processed_this_run = 0
    skipped_existing_count = 0
    failed_this_run = 0
    converted_small_files_count = 0
    svg_converted_count = 0
    svg_skipped_count = 0
    large_files_skipped = 0

    try:
        for root, dirs, files in os.walk(SOURCE_DIR):
            if not is_safe_path(root, SOURCE_DIR):
                print(f"⏭ Gezinme sırasında güvenli olmayan yol atlanıyor: {root}")
                continue

            for file in files:
                file_lower = file.lower()
                if file_lower.endswith(IMAGE_EXTENSIONS):
                    total_source_files_found += 1
                    original_path = os.path.join(root, file)

                    if not is_safe_path(original_path, SOURCE_DIR):
                        print(f"⏭ Güvenli olmayan orijinal dosya yolu atlanıyor: {original_path}")
                        continue

                    # Check file size before processing
                    try:
                        file_size_kb = os.path.getsize(original_path) / 1024
                        if file_size_kb > 50000:  # 50MB limit
                            large_files_skipped += 1
                            continue
                    except:
                        continue

                    # SVG dosyası kontrolü
                    if file_lower.endswith('.svg') and not SVG_SUPPORT:
                        print(f"⏭ SVG support not available, skipping: {original_path}")
                        svg_skipped_count += 1
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

                    original_size_kb_before_process = file_size_kb
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
    if large_files_skipped > 0:
        print(f"⏭ Çok büyük olduğu için atlanan dosyalar (>50MB): {large_files_skipped}")
    print(f"📠 WebP'ye çevrilen küçük (<10KB) dosyalar: {converted_small_files_count}")
    if SVG_SUPPORT:
        print(f"🔄 SVG'den WebP'ye çevrilen dosyalar: {svg_converted_count}")
    else:
        print(f"⏭ SVG desteği olmadığı için atlanan SVG dosyalar: {svg_skipped_count}")
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
    print(f"🔄 Tüm resimler WebP formatına çevrilecektir.")
    print(f"⚠️  Büyük dosyalar (>50MB) güvenlik için atlanacaktır.")
    print(f"📐 Çok büyük resimler {MAX_IMAGE_DIMENSION}px'e yeniden boyutlandırılacaktır.")
    
    if SVG_SUPPORT:
        print(f"✅ SVG desteği aktif. SVG dosyaları önce PNG'ye, sonra WebP'ye çevrilecektir.")
    else:
        print(f"⚠️  SVG desteği yok. SVG dosyalarını işlemek için Cairo kütüphanelerini yükleyin:")
        print(f"    sudo apt install libcairo2-dev libgirepository1.0-dev pkg-config")
        print(f"    pip install cairosvg")
        print(f"    SVG dosyaları atlanacaktır.")
    
    print("-" * 60)

    process_source_directory()