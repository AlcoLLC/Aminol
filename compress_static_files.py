import os
import shutil
import gzip
import json
import re
from pathlib import Path

# CSS/JS dosyaları için ek uzantılar
STATIC_EXTENSIONS = ('.css', '.js', '.html', '.json', '.xml', '.svg', '.txt')
GZIP_EXTENSIONS = ('.css', '.js', '.html', '.json', '.xml', '.txt')

# Mevcut kod bloğunuzun sonuna eklenecek fonksiyonlar:

def minify_css(css_content):
    """Basit CSS minification"""
    # Yorumları kaldır
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Fazla boşlukları kaldır
    css_content = re.sub(r'\s+', ' ', css_content)
    # Gereksiz karakterleri kaldır
    css_content = css_content.replace(' {', '{')
    css_content = css_content.replace('{ ', '{')
    css_content = css_content.replace(' }', '}')
    css_content = css_content.replace('} ', '}')
    css_content = css_content.replace('; ', ';')
    css_content = css_content.replace(': ', ':')
    css_content = css_content.replace(', ', ',')
    return css_content.strip()

def minify_js(js_content):
    """Basit JavaScript minification"""
    # Tek satır yorumları kaldır (// ile başlayanlar)
    js_content = re.sub(r'//.*$', '', js_content, flags=re.MULTILINE)
    # Çok satırlı yorumları kaldır
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    # Fazla boşlukları kaldır
    js_content = re.sub(r'\s+', ' ', js_content)
    # Noktalı virgülden sonraki boşlukları kaldır
    js_content = js_content.replace('; ', ';')
    return js_content.strip()

def minify_html(html_content):
    """Basit HTML minification"""
    # HTML yorumlarını kaldır
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    # Fazla boşlukları kaldır
    html_content = re.sub(r'\s+', ' ', html_content)
    # Tag'ler arasındaki gereksiz boşlukları kaldır
    html_content = re.sub(r'>\s+<', '><', html_content)
    return html_content.strip()

def compress_static_file(file_path, target_path):
    """Static dosyaları minify et ve gzip ile sıkıştır"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_size = len(content.encode('utf-8'))
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Minification
        if file_ext == '.css':
            content = minify_css(content)
        elif file_ext == '.js':
            content = minify_js(content)
        elif file_ext == '.html':
            content = minify_html(content)
        elif file_ext == '.json':
            try:
                # JSON'u compact format'a çevir
                data = json.loads(content)
                content = json.dumps(data, separators=(',', ':'))
            except:
                pass  # JSON parse edilemezse orijinal halini bırak
        
        minified_size = len(content.encode('utf-8'))
        
        # Dosyayı kaydet
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Gzip versiyonunu da oluştur
        if file_ext in GZIP_EXTENSIONS:
            gzip_path = target_path + '.gz'
            with gzip.open(gzip_path, 'wt', encoding='utf-8') as f:
                f.write(content)
            gzip_size = os.path.getsize(gzip_path)
            print(f"📦 Gzip oluşturuldu: {gzip_path} ({gzip_size} bytes)")
        
        compression_ratio = ((original_size - minified_size) / original_size) * 100 if original_size > 0 else 0
        
        print(f"✔ Minify edildi: {file_path}")
        print(f"  ↳ Kaydedildi: {target_path}")
        print(f"  📊 {original_size} bytes → {minified_size} bytes ({compression_ratio:.1f}% azalma)")
        
        return True
        
    except Exception as e:
        print(f"❌ Static dosya hatası ({file_path}): {e}")
        return False

def process_static_files(source_dir, target_dir):
    """Static dosyaları işle"""
    total_files = 0
    processed = 0
    failed = 0
    
    print(f"\n📁 Static dosyalar işleniyor: {source_dir} → {target_dir}")
    
    if not os.path.exists(source_dir):
        print(f"❌ Kaynak dizin mevcut değil: {source_dir}")
        return total_files, processed, failed
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(STATIC_EXTENSIONS):
                total_files += 1
                original_path = os.path.join(root, file)
                relative_path = os.path.relpath(original_path, source_dir)
                target_path = os.path.join(target_dir, relative_path)
                
                if compress_static_file(original_path, target_path):
                    processed += 1
                else:
                    failed += 1
    
    return total_files, processed, failed

# Mevcut DIRECTORIES_TO_PROCESS'e static dizinleri ekleyin:
STATIC_DIRECTORIES_TO_PROCESS = [
    {'source': 'staticfiles/assets/css', 'target': 'staticfiles/assets/css'},
    {'source': 'staticfiles/assets/js', 'target': 'staticfiles/assets/js'},
    {'source': 'templates/html', 'target': 'templates/html'},
]

def process_all_static_files():
    """Tüm static dosyaları işle"""
    print(f"\n🗜️ STATIC DOSYA COMPRESSION")
    print("-" * 80)
    
    total_static = [0, 0, 0]  # total, processed, failed
    
    for pair in STATIC_DIRECTORIES_TO_PROCESS:
        source, target = pair['source'], pair['target']
        result = process_static_files(source, target)
        total_static = [sum(x) for x in zip(total_static, result)]
    
    print(f"\n📊 STATIC DOSYA ÖZETİ:")
    print(f"🔎 Toplam static dosya: {total_static[0]}")
    print(f"✔ Başarıyla sıkıştırılan: {total_static[1]}")
    print(f"❌ Başarısız: {total_static[2]}")

# Ana process_all_directories() fonksiyonunun sonuna ekleyin:
def process_all_directories_extended():
    
    # Static dosya işleme
    process_all_static_files()

# Script'in sonunda çağırın:
if __name__ == "__main__":
    process_all_directories_extended()