import os
import pandas as pd
from django.utils.text import slugify
from django.db import transaction
import glob
from products.models import Product

def process_all_excel_files(folder_path):    
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls"))    
    all_products = []
    
    for file_path in excel_files:
        try:
            df_raw = pd.read_excel(file_path, sheet_name=0, header=None)
            
            main_headers = df_raw.iloc[2].fillna("").tolist()
            
            sub_headers = df_raw.iloc[3].fillna("").tolist()
            
            final_headers = []
            for i, h in enumerate(main_headers):
                if str(h).strip() == "Performance" and i < len(sub_headers) and str(sub_headers[i]).strip():
                    final_headers.append(f"Performance {str(sub_headers[i]).strip()}") 
                elif h and str(h).strip():
                    final_headers.append(str(h).strip())
                elif i < len(sub_headers) and str(sub_headers[i]).strip(): 
                    final_headers.append(str(sub_headers[i]).strip())
                else:
                    final_headers.append(f"Column_{i}")
            
            df = df_raw.iloc[4:].copy()
            df.columns = final_headers[:len(df.columns)] 
            df = df.reset_index(drop=True)
            
            df = df.dropna(how='all').reset_index(drop=True)
                  
            processed_rows = 0
            for index, row in df.iterrows():
                product_id = str(row.get('Product ID', '')).strip() if pd.notna(row.get('Product ID')) else ''
                title = str(row.get('Product name', '')).strip() if pd.notna(row.get('Product name')) else ''
                
                if not title:
                    continue
                
                product_data = {
                    'product_id': product_id,
                    'title': title,
                    'description': str(row.get('Description', '')).strip() if pd.notna(row.get('Description')) else '',
                    'features': str(row.get('Features & Benefits', '')).strip() if pd.notna(row.get('Features & Benefits')) else '',
                    'application': str(row.get('Application', '')).strip() if pd.notna(row.get('Application')) else '',
                    'recommendations': str(row.get('Recommendation', '')).strip() if pd.notna(row.get('Recommendation')) else '',
                    'api': str(row.get('Performance API', '')).strip() if pd.notna(row.get('Performance API')) else '',
                    'ilsac': str(row.get('Performance ILSAC', '')).strip() if pd.notna(row.get('Performance ILSAC')) else '',
                    'acea': str(row.get('Performance ACEA', '')).strip() if pd.notna(row.get('Performance ACEA')) else '',
                    'jaso': str(row.get('Performance JASO', '')).strip() if pd.notna(row.get('Performance JASO')) else '',
                    'oem_specifications': str(row.get('Performance OEM specifications', '')).strip() if pd.notna(row.get('Performance OEM specifications')) else '',
                }

                all_products.append(product_data)
                processed_rows += 1
                                
        except Exception as e:
            print(f"Excel dosyası işlenirken hata: {file_path}")
            import traceback
            traceback.print_exc()
            continue
    
    if len(all_products) == 0:
        print("İşlenecek ürün bulunamadı")
        return
    
    created_count = 0
    updated_count = 0
    error_count = 0
    
    try:
        with transaction.atomic():
            for i, product_data in enumerate(all_products):
                try:
                    base_slug = slugify(product_data['title'])
                    slug = base_slug
                    counter = 1
                    while Product.objects.filter(slug=slug).exclude(product_id=product_data['product_id']).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    
                    full_description = product_data['description']
                    if product_data.get('features'):
                        full_description += f"\n\nFeatures & Benefits:\n{product_data['features']}"
                    if product_data.get('application'):
                        full_description += f"\n\nApplication:\n{product_data['application']}"
                    
                    defaults_data = {
                        'title': product_data['title'],
                        'description': full_description,
                        'slug': slug,
                        'recommendations': product_data.get('recommendations', ''), 
                        'api': product_data.get('api', ''),
                        'ilsac': product_data.get('ilsac', ''), 
                        'acea': product_data.get('acea', ''),
                        'jaso': product_data.get('jaso', ''),
                        'oem_specifications': product_data.get('oem_specifications', ''), 
                    }
                    
                    if product_data['product_id']:
                        product, created = Product.objects.update_or_create(
                            product_id=product_data['product_id'],
                            defaults=defaults_data
                        )
                    else:
                        product, created = Product.objects.get_or_create(
                            title=product_data['title'],
                            defaults=defaults_data
                        )
                        if not created:
                            for key, value in defaults_data.items():
                                setattr(product, key, value)
                            product.save()
                    
                    if created:
                        created_count += 1
                        print(f"Yeni ürün oluşturuldu: {product_data['title']}")
                    else:
                        updated_count += 1
                        print(f"Ürün güncellendi: {product_data['title']}")
                        
                except Exception as e:
                    error_count += 1
                    print(f"Ürün işlenirken hata [{i+1}]: {product_data.get('title', 'Bilinmeyen')} - {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue
                    
        print(f"\n=== İmport Sonucu ===")
        print(f"Toplam işlenen: {len(all_products)}")
        print(f"Yeni oluşturulan: {created_count}")
        print(f"Güncellenen: {updated_count}")
        print(f"Hata: {error_count}")
        
    except Exception as e:
        print(f"Transaction hatası: {str(e)}")
        import traceback
        traceback.print_exc()

def import_excel_products(folder_path):
    if not os.path.exists(folder_path):
        print(f"Klasör bulunamadı: {folder_path}")
        return
    
    print(f"Excel dosyaları işleniyor: {folder_path}")
    process_all_excel_files(folder_path)

def test_database_connection():
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Veritabanı bağlantısı başarılı")
            return True
    except Exception as e:
        print(f"Veritabanı bağlantı hatası: {str(e)}")
        return False

def validate_product_model():
    try:
        from products.models import Product
        product = Product()
        fields = [f.name for f in Product._meta.get_fields()]
        print(f"Product model fields: {fields}")
        
        required_fields = ['title', 'description', 'slug', 'product_id']
        missing_fields = [field for field in required_fields if field not in fields]
        
        if missing_fields:
            print(f"Eksik field'lar: {missing_fields}")
            return False
        else:
            print("Tüm gerekli field'lar mevcut")
            return True
            
    except Exception as e:
        print(f"Model validation hatası: {str(e)}")
        return False