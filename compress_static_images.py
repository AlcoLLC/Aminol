import os
import shutil
from PIL import Image, UnidentifiedImageError
from io import BytesIO

TARGET_MIN_KB = 800
TARGET_MAX_KB = 1200
WEBP_QUALITY_MIN = 30
WEBP_QUALITY_MAX = 95
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.bmp', '.tiff', '.gif')

DIRECTORIES_TO_PROCESS = [
    {'source': 'staticfiles/images_1', 'target': 'staticfiles/images'},
    {'source': 'staticfiles/images_folder_1', 'target': 'staticfiles/images_folder'}
]

# SVG desteği için cairosvg import
try:
    import cairosvg
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False
    print("⚠️  SVG desteği yok. SVG dosyalarını işlemek için 'pip install cairosvg' komutunu çalıştırın.")


def get_file_size_kb(buffer):
    return len(buffer.getvalue()) / 1024


def compress_webp(img):
    """WebP formatında sıkıştırma"""
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
    """SVG dosyasını PIL Image objesine dönüştür"""
    if not SVG_SUPPORT:
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


def move_small_file(original_path, source_root):
    """Küçük dosyaları ayrı klasöre taşı"""
    try:
        relative_path = os.path.relpath(original_path, source_root)
        skipped_path = os.path.join("staticfiles", "skipped_small_images", relative_path)
        os.makedirs(os.path.dirname(skipped_path), exist_ok=True)
        os.rename(original_path, skipped_path)
        print(f"📁 Küçük dosya taşındı: {skipped_path}")
    except Exception as e:
        print(f"❌ Küçük dosya taşınamadı: {original_path} → {e}")


def process_single_image(original_image_path, compressed_image_save_path, source_root):
    """Tek bir resim dosyasını WebP formatına çevir ve sıkıştır"""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024
        file_ext = os.path.splitext(original_image_path)[1].lower()

        # Çıktı dosyasının uzantısını .webp olarak değiştir
        base_name = os.path.splitext(os.path.basename(compressed_image_save_path))[0]
        dir_name = os.path.dirname(compressed_image_save_path)
        compressed_image_save_path = os.path.join(dir_name, base_name + '.webp')

        # SVG dosyası kontrolü
        if file_ext == '.svg':
            if not SVG_SUPPORT:
                print(f"⏭ SVG desteği yok, atlanıyor: {original_image_path}")
                return False
            
            img = convert_svg_to_image(original_image_path)
            if img is None:
                return False
            print(f"🔄 SVG WebP'ye dönüştürülüyor: {original_image_path}")
        else:
            img = Image.open(original_image_path)

        # Küçük dosyaları işle
        if original_size_kb < 10:
            print(f"⚠️ Küçük dosya WebP'ye çevriliyor: {original_image_path} ({int(original_size_kb)} KB)")
            # Küçük dosyaları da WebP'ye çevir, yüksek kalite ile
            try:
                # WebP için uygun mod dönüşümü
                if img.mode in ('RGBA', 'LA'):
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                elif img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
                img.save(compressed_image_save_path, format="WEBP", quality=90, optimize=True)
                
                final_size_kb = os.path.getsize(compressed_image_save_path) / 1024
                print(f"📠 Küçük dosya WebP'ye çevrildi: {original_image_path} → {compressed_image_save_path} ({int(final_size_kb)} KB)")
                return True
            except Exception as e:
                print(f"❌ Küçük dosya WebP'ye çevrilirken hata: {e}")
                move_small_file(original_image_path, source_root)
                return False

        # WebP için mod dönüşümleri
        if img.mode == 'P':
            if img.info.get("transparency") is not None:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
        elif img.mode == 'LA':
            img = img.convert("RGBA")
        elif img.mode not in ('RGB', 'RGBA', 'L'):
            img = img.convert("RGB")

        # WebP sıkıştırması
        buffer = compress_webp(img)

        if not buffer or len(buffer.getvalue()) == 0:
            print(f"❌ WebP sıkıştırması başarısız: {original_image_path}")
            # Başarısız durumda standart kalite ile dene
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
        print(f"❌ Dosya bulunamadı: {original_image_path}")
        return False
    except UnidentifiedImageError:
        print(f"❌ Tanınamayan resim dosyası: {original_image_path}")
        return False
    except Exception as e:
        print(f"❌ Genel hata ({original_image_path}): {e}")
        return False


def process_directory_pair(source_dir, target_dir):
    """Bir kaynak-hedef dizin çiftini işle"""
    total_files = 0
    skipped_existing = 0
    processed = 0
    failed = 0
    svg_converted = 0
    small_files_converted = 0

    print(f"📂 Kaynak: {source_dir}")
    print(f"💾 Hedef: {target_dir}")
    
    if not os.path.exists(source_dir):
        print(f"❌ Kaynak dizin mevcut değil: {source_dir}")
        return total_files, skipped_existing, processed, failed, svg_converted, small_files_converted

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                total_files += 1
                original_path = os.path.join(root, file)
                relative_path = os.path.relpath(original_path, source_dir)
                
                # Çıktı dosyasının uzantısını .webp olarak değiştir
                base_name = os.path.splitext(relative_path)[0]
                compressed_path = os.path.join(target_dir, base_name + '.webp')

                if os.path.exists(compressed_path):
                    print(f"⏭ WebP dosyası zaten mevcut: {compressed_path}")
                    skipped_existing += 1
                    continue

                # Dosya boyutunu kontrol et (küçük dosyalar için sayaç)
                original_size_kb = os.path.getsize(original_path) / 1024
                is_svg = file.lower().endswith('.svg')
                is_small = original_size_kb < 10

                if process_single_image(original_path, compressed_path, source_dir):
                    processed += 1
                    if is_svg:
                        svg_converted += 1
                    if is_small:
                        small_files_converted += 1
                else:
                    failed += 1

    return total_files, skipped_existing, processed, failed, svg_converted, small_files_converted


def process_all_directories():
    """Tüm dizin çiftlerini işle"""
    print(f"🚀 WebP dönüştürme başlatıldı ({TARGET_MIN_KB}-{TARGET_MAX_KB} KB hedef boyut)")
    print(f"🔄 Tüm resimler WebP formatına çevrilecektir.")
    if SVG_SUPPORT:
        print("✅ SVG desteği aktif.")
    else:
        print("❌ SVG desteği yok.")
    print("-" * 80)

    totals = [0, 0, 0, 0, 0, 0]  # total, skipped, processed, failed, svg_converted, small_converted

    for pair in DIRECTORIES_TO_PROCESS:
        source, target = pair['source'], pair['target']
        print(f"\n📁 İşleniyor: {source} → {target}")
        print("-" * 60)

        result = process_directory_pair(source, target)
        totals = [sum(x) for x in zip(totals, result)]

        print(f"\n📊 {source} → {target} özeti:")
        print(f"🔎 Toplam resim dosyası: {result[0]}")
        print(f"⏭ Atlanan (zaten var): {result[1]}")
        print(f"✔ WebP'ye çevrilen: {result[2]}")
        print(f"🔄 SVG'den çevrilen: {result[4]}")
        print(f"📠 Küçük dosyalardan çevrilen: {result[5]}")
        print(f"❌ Başarısız: {result[3]}")

    print("\n" + "=" * 80)
    print("🏁 GENEL ÖZET - WebP Dönüştürme")
    print(f"🔎 Toplam resim dosyası bulundu: {totals[0]}")
    print(f"⏭ Toplam atlanan (zaten mevcut): {totals[1]}")
    print(f"✔ Başarıyla WebP'ye çevrilen: {totals[2]}")
    print(f"🔄 SVG'den WebP'ye çevrilen: {totals[4]}")
    print(f"📠 Küçük dosyalardan WebP'ye çevrilen: {totals[5]}")
    print(f"❌ Başarısız olan: {totals[3]}")
    print(f"🛠 İşlenmeye çalışılan toplam: {totals[2] + totals[3]}")
    
    if totals[2] > 0:
        success_rate = (totals[2] / (totals[2] + totals[3])) * 100
        print(f"📈 Başarı oranı: {success_rate:.1f}%")


if __name__ == "__main__":
    process_all_directories()