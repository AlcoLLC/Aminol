import os
import shutil
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Hedef boyut aralıkları
TARGET_MIN_KB = 800
TARGET_MAX_KB = 1200
SMALL_TARGET_MIN_KB = 20  # Küçük dosyalar için minimum boyut
SMALL_TARGET_MAX_KB = 30  # Küçük dosyalar için maksimum boyut

WEBP_QUALITY_MIN = 30
WEBP_QUALITY_MAX = 95
SMALL_WEBP_QUALITY_MIN = 40  # Küçük dosyalar için minimum kalite
SMALL_WEBP_QUALITY_MAX = 70  # Küçük dosyalar için maksimum kalite

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


def compress_webp_small(img, target_width=None, target_height=None):
    """Küçük boyutlar için WebP sıkıştırma (20-30 KB hedef)"""
    # Boyut küçültme işlemi
    if target_width or target_height:
        img.thumbnail((target_width or img.width, target_height or img.height), Image.Resampling.LANCZOS)
    
    last_buffer = None
    
    # Küçük dosyalar için daha düşük kalite aralığı kullan
    for quality in range(SMALL_WEBP_QUALITY_MAX, SMALL_WEBP_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality, optimize=True)
        size_kb = get_file_size_kb(buffer)
        
        if SMALL_TARGET_MIN_KB <= size_kb <= SMALL_TARGET_MAX_KB:
            return buffer
        last_buffer = buffer
        
        # Eğer hala çok büyükse boyutu küçült
        if size_kb > SMALL_TARGET_MAX_KB and quality == SMALL_WEBP_QUALITY_MAX:
            # Boyutu %80'e küçült
            new_width = int(img.width * 0.8)
            new_height = int(img.height * 0.8)
            if new_width > 50 and new_height > 50:  # Minimum boyut kontrolü
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return last_buffer


def compress_webp(img):
    """Normal WebP formatında sıkıştırma"""
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


def create_small_version(img, save_path, target_kb_range=(20, 30)):
    """Resmin küçük versiyonunu oluştur"""
    try:
        # Orijinal boyutları al
        original_width, original_height = img.size
        
        # Farklı boyut seçeneklerini dene
        size_options = [
            (150, 150),   # Küçük kare
            (200, 150),   # Küçük dikdörtgen
            (250, 200),   # Orta küçük
            (300, 250),   # Orta
        ]
        
        best_buffer = None
        best_size_kb = 0
        best_dimensions = None
        
        for target_w, target_h in size_options:
            # Orijinal oranı koru
            ratio = min(target_w / original_width, target_h / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Resmi yeniden boyutlandır
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Farklı kalite seviyeleri dene
            for quality in range(50, 25, -5):
                buffer = BytesIO()
                resized_img.save(buffer, format="WEBP", quality=quality, optimize=True)
                size_kb = get_file_size_kb(buffer)
                
                if target_kb_range[0] <= size_kb <= target_kb_range[1]:
                    # Hedef aralıkta bir sonuç bulduk
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, "wb") as f:
                        f.write(buffer.getvalue())
                    return True, size_kb, (new_width, new_height)
                
                # En iyi seçeneği sakla (hedefe en yakın)
                if (not best_buffer or 
                    abs(size_kb - (target_kb_range[0] + target_kb_range[1]) / 2) < 
                    abs(best_size_kb - (target_kb_range[0] + target_kb_range[1]) / 2)):
                    best_buffer = buffer
                    best_size_kb = size_kb
                    best_dimensions = (new_width, new_height)
        
        # En iyi seçeneği kaydet
        if best_buffer:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(best_buffer.getvalue())
            return True, best_size_kb, best_dimensions
        
        return False, 0, None
        
    except Exception as e:
        print(f"❌ Küçük versiyon oluşturma hatası: {e}")
        return False, 0, None


def process_single_image(original_image_path, compressed_image_save_path, source_root, create_small=False):
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

        # Ana WebP dosyasını oluştur
        buffer = compress_webp(img)
        
        if not buffer or len(buffer.getvalue()) == 0:
            print(f"❌ WebP sıkıştırması başarısız: {original_image_path}")
            return False

        os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        compressed_size_kb = get_file_size_kb(buffer)
        print(f"✔ WebP'ye dönüştürüldü: {original_image_path}")
        print(f"  ↳ Kaydedildi: {compressed_image_save_path}")
        print(f"  📊 {int(original_size_kb)} KB → {int(compressed_size_kb)} KB")

        # Küçük versiyon oluştur
        if create_small:
            small_save_path = compressed_image_save_path.replace('.webp', '_small.webp')
            success, small_size_kb, dimensions = create_small_version(img, small_save_path)
            
            if success:
                print(f"  🔸 Küçük versiyon: {small_save_path}")
                print(f"  📐 Boyut: {dimensions[0]}x{dimensions[1]} - {int(small_size_kb)} KB")
            else:
                print(f"  ❌ Küçük versiyon oluşturulamadı")

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


def process_directory_pair(source_dir, target_dir, create_small_versions=True):
    """Bir kaynak-hedef dizin çiftini işle"""
    total_files = 0
    skipped_existing = 0
    processed = 0
    failed = 0
    svg_converted = 0
    small_versions_created = 0

    print(f"📂 Kaynak: {source_dir}")
    print(f"💾 Hedef: {target_dir}")
    print(f"🔸 Küçük versiyonlar oluşturulacak: {'Evet' if create_small_versions else 'Hayır'}")
    
    if not os.path.exists(source_dir):
        print(f"❌ Kaynak dizin mevcut değil: {source_dir}")
        return total_files, skipped_existing, processed, failed, svg_converted, small_versions_created

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

                is_svg = file.lower().endswith('.svg')

                if process_single_image(original_path, compressed_path, source_dir, create_small_versions):
                    processed += 1
                    if is_svg:
                        svg_converted += 1
                    if create_small_versions:
                        small_path = compressed_path.replace('.webp', '_small.webp')
                        if os.path.exists(small_path):
                            small_versions_created += 1
                else:
                    failed += 1

    return total_files, skipped_existing, processed, failed, svg_converted, small_versions_created


def process_all_directories():
    """Tüm dizin çiftlerini işle"""
    print(f"🚀 WebP dönüştürme başlatıldı")
    print(f"📏 Normal boyut hedefi: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print(f"🔸 Küçük boyut hedefi: {SMALL_TARGET_MIN_KB}-{SMALL_TARGET_MAX_KB} KB")
    print(f"🔄 Tüm resimler WebP formatına çevrilecek + küçük versiyonları oluşturulacaktır.")
    if SVG_SUPPORT:
        print("✅ SVG desteği aktif.")
    else:
        print("❌ SVG desteği yok.")
    print("-" * 80)

    totals = [0, 0, 0, 0, 0, 0]  # total, skipped, processed, failed, svg_converted, small_created

    for pair in DIRECTORIES_TO_PROCESS:
        source, target = pair['source'], pair['target']
        print(f"\n📁 İşleniyor: {source} → {target}")
        print("-" * 60)

        result = process_directory_pair(source, target, create_small_versions=True)
        totals = [sum(x) for x in zip(totals, result)]

        print(f"\n📊 {source} → {target} özeti:")
        print(f"🔎 Toplam resim dosyası: {result[0]}")
        print(f"⏭ Atlanan (zaten var): {result[1]}")
        print(f"✔ WebP'ye çevrilen: {result[2]}")
        print(f"🔄 SVG'den çevrilen: {result[4]}")
        print(f"🔸 Küçük versiyon oluşturulan: {result[5]}")
        print(f"❌ Başarısız: {result[3]}")

    print("\n" + "=" * 80)
    print("🏁 GENEL ÖZET - WebP Dönüştürme")
    print(f"🔎 Toplam resim dosyası bulundu: {totals[0]}")
    print(f"⏭ Toplam atlanan (zaten mevcut): {totals[1]}")
    print(f"✔ Başarıyla WebP'ye çevrilen: {totals[2]}")
    print(f"🔄 SVG'den WebP'ye çevrilen: {totals[4]}")
    print(f"🔸 Küçük versiyon oluşturulan: {totals[5]}")
    print(f"❌ Başarısız olan: {totals[3]}")
    print(f"🛠 İşlenmeye çalışılan toplam: {totals[2] + totals[3]}")
    
    if totals[2] > 0:
        success_rate = (totals[2] / (totals[2] + totals[3])) * 100
        print(f"📈 Başarı oranı: {success_rate:.1f}%")
        
        if totals[5] > 0:
            small_success_rate = (totals[5] / totals[2]) * 100
            print(f"🔸 Küçük versiyon başarı oranı: {small_success_rate:.1f}%")


if __name__ == "__main__":
    process_all_directories()