import os
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import shutil # shutil kütüphanesi eklendi

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


def get_file_size_kb(buffer_or_path):
    """Return file size in KB from BytesIO buffer or file path"""
    if isinstance(buffer_or_path, BytesIO):
        return len(buffer_or_path.getvalue()) / 1024
    elif isinstance(buffer_or_path, str):
        if os.path.exists(buffer_or_path):
            return os.path.getsize(buffer_or_path) / 1024
    return 0

def compress_jpeg(img):
    """Iteratively compress JPEG to target size"""
    best_buffer = None
    # En iyi sonucu saklamak için (hedefe en yakın olanı)
    # closest_size_diff = float('inf') # Bu örnekte kullanılmıyor ama mantık eklenebilir
    final_buffer_to_return = None

    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size_kb = get_file_size_kb(buffer)

        if final_buffer_to_return is None:
            final_buffer_to_return = buffer

        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer

        best_buffer = buffer # Hedef aralığa ulaşılamazsa en son (en düşük kaliteli) buffer

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
        img.save(buffer, format="WEBP", quality=quality) # WebP için optimize=True Pillow'da doğrudan yok
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
        last_buffer = buffer
    return last_buffer

def process_single_image(original_image_path, compressed_image_save_path):
    """Compress a single image file and save it to the new destination, or copy if too small."""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan veya bulunamayan kaynak dosya: {original_image_path}")
            return False

        original_size_kb = get_file_size_kb(original_image_path)

        # --- KÜÇÜK DOSYALARI KOPYALAMA ---
        if original_size_kb < 10:  # 10KB altındaki dosyalar için
            os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
            # Eğer hedefte aynı boyutta dosya zaten varsa kopyalamayı atla
            if os.path.exists(compressed_image_save_path) and get_file_size_kb(compressed_image_save_path) == original_size_kb:
                print(f"📠 Zaten hedefte ve aynı boyutta (çok küçük): {original_image_path} ({int(original_size_kb)} KB). Atlanıyor.")
            else:
                shutil.copy2(original_image_path, compressed_image_save_path)
                print(f"📠 Kopyalandı (çok küçük): {original_image_path} ({int(original_size_kb)} KB) -> {compressed_image_save_path}")
            return True # Başarıyla işlendi (kopyalandı veya doğrulandı)

        # --- SIKIŞTIRMA İŞLEMİ (10KB ve üzeri dosyalar için) ---
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
        else: # Desteklenmeyen formatlar PNG olarak denenir
            try:
                print(f"ℹ️ Desteklenmeyen format: {img_format} ({original_image_path}). PNG olarak kaydedilmeye çalışılıyor.")
                # PNG için güvenli moda dönüştür
                if img.mode == 'P':
                     img = img.convert("RGBA") # Paletliyse direkt RGBA'ya çevir, PNG sıkıştırması daha iyi çalışır
                elif 'A' not in img.mode and img.info.get("transparency") is None and img.mode != "RGB":
                     img = img.convert("RGB")
                elif img.mode not in ["RGB", "RGBA"]: # Genel fallback
                     img = img.convert("RGBA") if 'A' in img.mode or img.info.get("transparency") is not None else img.convert("RGB")

                # Önce hedef aralıkta mı diye bakmadan direkt compress_png çağır
                buffer = compress_png(img)
            except Exception as conv_err:
                print(f"⏭ Bilinmeyen formatı PNG'ye dönüştürme/kaydetme hatası {original_image_path} ({img_format}): {conv_err}")
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
        print(f"  📊 {int(original_size_kb)} KB → {int(compressed_size_kb)} KB (Hedef: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB)")
        return True

    except FileNotFoundError:
        print(f"❌ İşlem sırasında dosya bulunamadı (FileNotFoundError): {original_image_path}")
        return False
    except UnidentifiedImageError:
        print(f"❌ Resim dosyası tanımlanamadı (bozuk veya resim değil): {original_image_path}")
        return False
    except Exception as e:
        print(f"❌ {original_image_path} işlenirken genel hata: {e} (Tip: {type(e).__name__})")
        return False

def is_safe_path(path, base_dir):
    try:
        abs_base = os.path.abspath(base_dir)
        abs_path = os.path.abspath(path)
        return abs_path.startswith(abs_base)
    except Exception:
        return False

def process_source_directory():
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
    skipped_existing_in_target_range = 0
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

                    # --- YENİ KONTROL MANTIĞI ---
                    original_path_size_kb = get_file_size_kb(original_path)

                    if os.path.exists(compressed_save_path):
                        # Eğer orijinal dosya zaten küçükse (<10KB), process_single_image kopyalama/doğrulama yapsın.
                        # Eğer orijinal dosya büyükse (>10KB) ve hedefteki sıkıştırılmış dosya zaten hedef aralıktaysa, atla.
                        if original_path_size_kb >= 10: # Sıkıştırılması gereken bir dosya
                            try:
                                existing_compressed_size_kb = get_file_size_kb(compressed_save_path)
                                if TARGET_MIN_KB <= existing_compressed_size_kb <= TARGET_MAX_KB:
                                    print(f"⏭ Zaten işlenmiş ve hedef aralıkta (büyük dosya): {compressed_save_path} ({int(existing_compressed_size_kb)} KB). Atlanıyor.")
                                    skipped_existing_in_target_range += 1
                                    continue
                                else:
                                    # Hedefte var ama boyutu yanlış (örn. backend orijinali koydu), yeniden işlenecek.
                                    print(f"ℹ️ Hedefteki dosya {compressed_save_path} ({int(existing_compressed_size_kb)} KB) hedef aralıkta değil. Kaynaktan yeniden işlenecek.")
                            except OSError: # Dosya okuma hatası olursa yeniden işlemeye çalış
                                print(f"⚠️ Hedefteki {compressed_save_path} okunamadı. Kaynaktan yeniden işlenecek.")
                        # else: Orijinal dosya küçükse (<10KB), process_single_image karar verecek (kopyala veya zaten kopyalanmışsa atla).
                        # Bu durumda özel bir mesaj gerekmiyor, process_single_image loglayacak.

                    # Yukarıdaki continue çalışmadıysa (dosya hedefte yok, veya var ama yeniden işlenmesi gerekiyor,
                    # veya orijinal dosya küçük ve process_single_image tarafından ele alınacaksa)
                    # process_single_image çağrılır.
                    if process_single_image(original_path, compressed_save_path):
                        successfully_processed_this_run += 1
                    else:
                        failed_this_run +=1
    except PermissionError as e:
        print(f"❌ Dizin işlenirken izin reddedildi: {e}")
    except Exception as e:
        print(f"❌ Dizin işlenirken genel hata: {e}")

    print(f"\n🏁 İşlem tamamlandı.")
    print(f"🔎 Kaynakta bulunan toplam resim dosyası: {total_source_files_found}")
    print(f"⏭ Atlanan (önceden sıkıştırılmış ve hedef aralıkta olan büyük dosyalar): {skipped_existing_in_target_range}")
    print(f"✔ Bu çalıştırmada başarıyla işlenen (sıkıştırılan/kopyalanan): {successfully_processed_this_run}")
    print(f"❌ Bu çalıştırmada işlenemeyen: {failed_this_run}")
    attempted_this_run = successfully_processed_this_run + failed_this_run + skipped_existing_in_target_range
    # Not: attempted_this_run, tüm bulunan dosyalarla eşleşmeyebilir eğer güvenlik atlamaları olduysa.
    # Daha doğru bir ifade: Bu çalıştırmada aktif olarak değerlendirilen: successfully_processed + failed_this_run
    print(f"🛠 Bu çalıştırmada işlenmeye çalışılan veya (uygunsa) atlanan: {successfully_processed_this_run + failed_this_run + skipped_existing_in_target_range}")


if __name__ == "__main__":
    print(f"🚀 Resim sıkıştırma/kopyalama başlatılıyor.")
    print(f"📂 Kaynak dizin: {SOURCE_DIR}")
    print(f"💾 Hedef dizin: {COMPRESSED_OUTPUT_DIR}")
    print(f"📏 Hedef boyut aralığı (sıkıştırma için): {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print(f"📦 Küçük dosyalar (<10KB) sıkıştırılmadan kopyalanacak.")
    print("-" * 70)

    process_source_directory()