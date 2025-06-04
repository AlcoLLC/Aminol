import os
from PIL import Image, UnidentifiedImageError # UnidentifiedImageError import edildi
from io import BytesIO
import shutil # Kopyalama işlemi için shutil import edildi

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

# Source directory for original images
SOURCE_DIR = "/Aminol/media"

# Target directory for compressed images
COMPRESSED_OUTPUT_DIR = "/Aminol/mediafiles"


def get_file_size_kb(buffer):
    """Return file size in KB from BytesIO buffer"""
    return len(buffer.getvalue()) / 1024

def compress_jpeg(img):
    """Iteratively compress JPEG to target size"""
    best_buffer = None
    # En iyi sonucu saklamak için (hedefe en yakın olanı)
    # closest_size_diff = float('inf') # Bu satır kullanılmıyor, kaldırılabilir
    # final_buffer_to_return = None # Bu satır kullanılmıyor, kaldırılabilir

    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size_kb = get_file_size_kb(buffer)

        # final_buffer_to_return is None: # İlk denemede bir buffer ata # Bu mantık artık best_buffer ile yönetiliyor
        #     final_buffer_to_return = buffer

        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer # Hedef aralıkta bulundu

        best_buffer = buffer # Her döngüde güncellenir, böylece en sonuncusu (en düşük kaliteye en yakın) olur

    return best_buffer # Hedef aralığa ulaşılamazsa en son denenen buffer

def compress_png(img):
    """Iteratively compress PNG to target size"""
    last_buffer = None
    for level in PNG_COMPRESSION_LEVELS:
        buffer = BytesIO()
        img.save(buffer, format="PNG", optimize=True, compress_level=level)
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer # Son denenen buffer'ı sakla
    return last_buffer # Hedef aralığa ulaşılamazsa son denenen (en düşük sıkıştırma seviyeli) buffer'ı döndür

def compress_webp(img):
    """Iteratively compress WebP to target size"""
    last_buffer = None
    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality)
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer # Son denenen buffer'ı sakla
    return last_buffer # Hedef aralığa ulaşılamazsa son denenen (en düşük kaliteli) buffer'ı döndür

def process_single_image(original_image_path, compressed_image_save_path):
    """Compress a single image file and save it to the new destination.
    If the image is too small (<10KB), it will be copied directly."""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024

        # --- DEĞİŞİKLİK BAŞLANGICI ---
        if original_size_kb < 10:  # Çok küçük dosyaları atla (örn. 10KB altı)
            try:
                # Hedef dizinin var olduğundan emin ol
                os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
                # Dosyayı olduğu gibi kopyala
                shutil.copy2(original_image_path, compressed_image_save_path)
                print(f"📠 Kopyalandı (çok küçük, <10KB): {original_image_path} ({int(original_size_kb)} KB) -> {compressed_image_save_path}")
                return True # Kopyalama başarılı olduğu için True dön
            except Exception as e:
                print(f"❌ Küçük dosya {original_image_path} kopyalanırken hata: {e}")
                return False # Kopyalama sırasında hata oluşursa False dön
        # --- DEĞİŞİKLİK SONU ---

        img = Image.open(original_image_path)
        img_format = img.format.upper() if img.format else ''

        # Mod dönüşümleri
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
                # PNG için güvenli bir moda dönüştür
                if img.mode == 'P': # Eğer paletli ise ve alfa kanalı olabilirse RGBA'ya dönüştür
                    img = img.convert("RGBA")
                elif 'A' not in img.mode and img.info.get("transparency") is None and img.mode != "RGB":
                     img = img.convert("RGB") # Alfa yoksa ve RGB değilse RGB'ye
                elif 'A' in img.mode and img.mode != "RGBA":
                    img = img.convert("RGBA") # Alfa varsa ve RGBA değilse RGBA'ya
                elif img.mode not in ["RGB", "RGBA", "L", "LA"]: # Bilinmeyen diğer modlar için güvenli liman
                    print(f"⚠️ {original_image_path} için bilinmeyen mod {img.mode}, RGBA'ya dönüştürülüyor.")
                    img = img.convert("RGBA")


                temp_buffer = BytesIO()
                img.save(temp_buffer, format="PNG", optimize=True) # compress_level olmadan ilk deneme
                size_kb = get_file_size_kb(temp_buffer)

                if not (TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB):
                    # Eğer ilk deneme hedef aralıkta değilse, compress_png ile yeniden dene
                    # compress_png zaten doğru mod dönüşümünü (RGBA/RGB) kendi içinde yapmaya çalışacak.
                    buffer = compress_png(img)
                else:
                    buffer = temp_buffer
            except Exception as conv_err:
                print(f"⏭ Bilinmeyen formatı dönüştürme/kaydetme hatası {original_image_path} ({img_format}): {conv_err}")
                return False

        if buffer is None or len(buffer.getvalue()) == 0:
            print(f"❌ Sıkıştırma {original_image_path} için bir buffer döndürmedi veya boş buffer döndürdü.")
            # Eğer orijinal dosya boyutu hedef aralığın altındaysa ve sıkıştırma sonucu boş/yok ise,
            # belki orijinal dosyayı kopyalamak bir seçenek olabilir. Ancak şu an için başarısız sayıyoruz.
            if original_size_kb < TARGET_MAX_KB : # Eğer orijinal zaten hedeften küçükse
                print(f"ℹ️ {original_image_path} orijinal boyutu ({int(original_size_kb)}KB) zaten hedef aralığın altında/yakınında, ama sıkıştırma başarısız oldu.")
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
    """Recursively process all valid image files from SOURCE_DIR to COMPRESSED_OUTPUT_DIR."""

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
    copied_small_files_count = 0 # Küçük dosyaları saymak için yeni sayaç

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
                    compressed_save_path = os.path.join(COMPRESSED_OUTPUT_DIR, relative_path)

                    if not is_safe_path(compressed_save_path, COMPRESSED_OUTPUT_DIR):
                        print(f"⏭ Güvenli olmayan hedef kayıt yolu atlanıyor: {compressed_save_path}")
                        continue

                    if os.path.exists(compressed_save_path):
                        # İsteğe bağlı boyut kontrolü burada da yapılabilir, ancak basitlik adına sadece varlık kontrolü
                        print(f"⏭ Dosya hedefte zaten mevcut: {compressed_save_path}. Atlanıyor.")
                        skipped_existing_count += 1
                        continue

                    # process_single_image artık küçük dosyalar için True döndürecek
                    # ve kopyalama işlemini kendi içinde yapacak.
                    original_size_kb_before_process = os.path.getsize(original_path) / 1024 # Kopyalananları saymak için
                    
                    processed_successfully = process_single_image(original_path, compressed_save_path)

                    if processed_successfully:
                        successfully_processed_this_run += 1
                        if original_size_kb_before_process < 10: # Eğer dosya kopyalandıysa
                             copied_small_files_count +=1
                    else:
                        failed_this_run +=1
    
    except PermissionError as e:
        print(f"❌ Dizin işlenirken izin reddedildi: {e}")
    except Exception as e:
        print(f"❌ Dizin işlenirken hata: {e}")

    print(f"\n🏁 İşlem tamamlandı.")
    print(f"🔎 Kaynakta bulunan toplam resim dosyası: {total_source_files_found}")
    print(f"📠 Kopyalanan küçük (<10KB) dosyalar: {copied_small_files_count}") # Yeni bilgi
    print(f"⏭ Atlanan (hedefte zaten mevcut olan): {skipped_existing_count}")
    # successfully_processed_this_run artık kopyalanan küçük dosyaları da içeriyor.
    # Eğer sıkıştırılan ve kopyalananları ayrı görmek isterseniz:
    print(f"✔ Bu çalıştırmada başarıyla işlenen (sıkıştırılan veya küçük olduğu için kopyalanan): {successfully_processed_this_run}")
    print(f"❌ Bu çalıştırmada işlenemeyen: {failed_this_run}")
    attempted_this_run = successfully_processed_this_run + failed_this_run # Bu artık kopyalananları da doğru sayar
    print(f"🛠 Bu çalıştırmada işlenmeye çalışılan: {attempted_this_run}")


if __name__ == "__main__":
    print(f"🚀 Resim sıkıştırma başlatılıyor.")
    print(f"📂 Kaynak dizin: {SOURCE_DIR}")
    print(f"💾 Sıkıştırılmış dosyalar için hedef dizin: {COMPRESSED_OUTPUT_DIR}")
    print(f"📏 Hedef boyut aralığı: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print(f"❗ Not: 10KB'den küçük dosyalar sıkıştırılmadan hedef dizine kopyalanacaktır.") # Ek bilgi
    print("-" * 60)

    process_source_directory()