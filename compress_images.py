import os
from PIL import Image, UnidentifiedImageError # UnidentifiedImageError import edildi
from io import BytesIO
# shutil'e gerek kalmadı, çünkü sadece var olan dosyaları kontrol ediyoruz, kopyalamıyoruz.

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
    closest_size_diff = float('inf')
    final_buffer_to_return = None # Hedef aralıkta bulunamazsa kullanılacak son geçerli buffer

    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size_kb = get_file_size_kb(buffer)

        if final_buffer_to_return is None: # İlk denemede bir buffer ata
            final_buffer_to_return = buffer

        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer # Hedef aralıkta bulundu

        # Hedef aralığa en yakın olanı bulma mantığı (isteğe bağlı iyileştirme)
        # Bu örnekte, hedef aralığa ulaşılamazsa en son denenen (en düşük kaliteli) buffer'ı döndürmek yerine,
        # biraz daha gelişmiş bir mantık eklenebilir. Şimdilik basit tutalım.
        # Mevcut mantık, hedef aralığa ulaşılamazsa en son denenen (JPEG_QUALITY_MIN'e en yakın) buffer'ı döndürür.
        best_buffer = buffer # Her döngüde güncellenir, böylece en sonuncusu olur

    return best_buffer # Hedef aralığa ulaşılamazsa en son denenen buffer (veya en düşük kaliteli)

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
    """Compress a single image file and save it to the new destination."""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024

        if original_size_kb < 10:  # Çok küçük dosyaları atla (örn. 10KB altı)
            print(f"⏭ İşlenemeyecek kadar küçük dosya: {original_image_path} ({int(original_size_kb)} KB)")
            # İsteğe bağlı: küçük dosyaları olduğu gibi kopyala
            # os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
            # shutil.copy2(original_image_path, compressed_image_save_path) # shutil'i tekrar import etmeniz gerekir
            # print(f"📠 Kopyalandı (çok küçük): {original_image_path} -> {compressed_image_save_path}")
            return False # Veya kopyalandıysa True

        img = Image.open(original_image_path)
        img_format = img.format.upper() if img.format else ''

        # Mod dönüşümleri (önceki kodunuzdaki gibi)
        if img.mode == 'P' or img.mode == 'LA':
            if 'A' in img.mode or img.info.get("transparency") is not None: # Paletli PNG'ler için transparency kontrolü
                 img = img.convert("RGBA")
            else:
                 img = img.convert("RGB")
        elif img_format != "PNG" and img.mode == "RGBA":
            img = img.convert("RGB")
        elif img_format == "PNG" and img.mode not in ["RGBA", "LA"] and 'A' not in img.mode and img.info.get("transparency") is None:
             # Basit PNG'ler için (alfa kanalı yoksa)
            if img.mode != "RGB":
                 img = img.convert("RGB")


        buffer = None
        if img_format in ["JPEG", "JPG"]:
            if img.mode == "RGBA": # JPEG RGBA'yı desteklemez
                img = img.convert("RGB")
            buffer = compress_jpeg(img)
        elif img_format == "PNG":
            buffer = compress_png(img)
        elif img_format == "WEBP":
            buffer = compress_webp(img)
        else:
            try:
                print(f"ℹ️ Desteklenmeyen format: {img_format}. PNG olarak kaydedilmeye çalışılıyor.")
                if img.mode not in ["RGB", "RGBA"]: # PNG için güvenli bir moda dönüştür
                    img = img.convert("RGBA") if 'A' in img.mode or img.info.get("transparency") is not None else img.convert("RGB")

                temp_buffer = BytesIO()
                img.save(temp_buffer, format="PNG", optimize=True)
                size_kb = get_file_size_kb(temp_buffer)
                if not (TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB):
                    # img'nin PNG sıkıştırması için doğru modda olduğundan emin ol
                    if img.mode == 'P': # Paletli ise ve sıkıştırma gerekiyorsa RGBA'ya dönüştür
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
    except UnidentifiedImageError: # Pillow'dan bu hatayı import edin
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

def process_source_directory():
    """Recursively process all valid image files from SOURCE_DIR to COMPRESSED_OUTPUT_DIR."""

    # Güvenlik kontrolleri (önceki kodunuzdaki gibi)
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

                    # --- YENİ KONTROL ---
                    # Sıkıştırılmış dosyanın hedefte zaten var olup olmadığını kontrol et
                    if os.path.exists(compressed_save_path):
                        # İsteğe bağlı: Mevcut dosyanın boyutunu da kontrol edebilirsiniz.
                        # try:
                        #     existing_size_kb = os.path.getsize(compressed_save_path) / 1024
                        #     if TARGET_MIN_KB <= existing_size_kb <= TARGET_MAX_KB:
                        #         print(f"⏭ Zaten işlenmiş ve hedef aralıkta: {compressed_save_path} ({int(existing_size_kb)} KB). Atlanıyor.")
                        #         skipped_existing_count += 1
                        #         continue
                        #     else:
                        #         # Eğer boyut aralığı dışındaysa ve yeniden işlenmesini istiyorsanız bu kısmı aktif edin.
                        #         # print(f"ℹ️ Mevcut dosya {compressed_save_path} ({int(existing_size_kb)} KB) hedef aralıkta değil. Yeniden işleniyor.")
                        #         pass # Yeniden işlemek için devam et
                        # except OSError: # Dosya silinmiş veya erişilemez olabilir
                        #     pass # Yeniden işlemek için devam et
                        
                        # Basit kontrol: Eğer dosya varsa, daha önce işlendiğini varsay ve atla.
                        print(f"⏭ Dosya hedefte zaten mevcut: {compressed_save_path}. Atlanıyor.")
                        skipped_existing_count += 1
                        continue # Bir sonraki dosyaya geç
                    # --- KONTROL SONU ---

                    if process_single_image(original_path, compressed_save_path):
                        successfully_processed_this_run += 1
                    else:
                        failed_this_run +=1
    
    except PermissionError as e:
        print(f"❌ Dizin işlenirken izin reddedildi: {e}")
    except Exception as e:
        print(f"❌ Dizin işlenirken hata: {e}")

    print(f"\n🏁 İşlem tamamlandı.")
    print(f"🔎 Kaynakta bulunan toplam resim dosyası: {total_source_files_found}")
    print(f"⏭ Atlanan (hedefte zaten mevcut olan): {skipped_existing_count}")
    print(f"✔ Bu çalıştırmada başarıyla sıkıştırılan: {successfully_processed_this_run}")
    print(f"❌ Bu çalıştırmada işlenemeyen: {failed_this_run}")
    attempted_this_run = successfully_processed_this_run + failed_this_run
    print(f"🛠 Bu çalıştırmada işlenmeye çalışılan: {attempted_this_run}")


if __name__ == "__main__":
    # Pillow'dan UnidentifiedImageError'ı import ettiğinizden emin olun
    # from PIL import UnidentifiedImageError (script'in başında zaten var)
    
    print(f"🚀 Resim sıkıştırma başlatılıyor.")
    print(f"📂 Kaynak dizin: {SOURCE_DIR}")
    print(f"💾 Sıkıştırılmış dosyalar için hedef dizin: {COMPRESSED_OUTPUT_DIR}")
    print(f"📏 Hedef boyut aralığı: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print("-" * 60)

    process_source_directory()