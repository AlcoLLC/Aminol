import os
import pandas as pd
from django.utils.text import slugify
import glob
from products.models import Product
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import Excel files from a folder and update Product database.'

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str, help='Path to folder containing Excel files')

    def handle(self, *args, **kwargs):
        folder_path = kwargs['folder_path']

        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f"Folder not found: {folder_path}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Processing folder: {folder_path}"))
        
        # Excel fayllarının mövcudluğunu yoxla
        excel_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls"))
        
        if not excel_files:
            self.stdout.write(self.style.ERROR(f"No Excel files found in: {folder_path}"))
            return
        
        self.stdout.write(self.style.SUCCESS(f"Found {len(excel_files)} Excel files"))
        for file in excel_files:
            self.stdout.write(f"  - {file}")
        
        process_all_excel_files(folder_path)
        self.stdout.write(self.style.SUCCESS("Done!"))

def compare_and_update_product(product, new_data):
    """
    Mevcut ürün ile yeni veriyi karşılaştır ve sadece değişen alanları güncelle
    """
    changes = {}
    fields_to_check = [
        'title', 'description', 'features_benefits', 'application', 
        'recommendations', 'api', 'ilsac', 'acea', 'jaso', 'oem_sertification'
    ]
    
    for field in fields_to_check:
        old_value = getattr(product, field, '') or ''
        new_value = new_data.get(field, '') or ''
        
        # Değerler farklıysa kaydet
        if old_value.strip() != new_value.strip():
            changes[field] = {
                'old': old_value,
                'new': new_value
            }
    
    # Slug kontrolü
    new_slug = new_data.get('slug', '')
    if product.slug != new_slug:
        changes['slug'] = {
            'old': product.slug,
            'new': new_slug
        }
    
    return changes

def process_all_excel_files(folder_path):    
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls"))
    
    print(f"Excel fayllar tapıldı: {len(excel_files)}")
    for file in excel_files:
        print(f"  - {file}")
    
    all_products = []
    
    for file_path in excel_files:
        print(f"\nProcessing file: {file_path}")
        try:
            # Bütün sheet adlarını əldə et
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            print(f"Found {len(sheet_names)} sheets: {sheet_names}")
            
            # Hər sheet-i ayrı-ayrılıqda process et
            for sheet_name in sheet_names:
                print(f"\n  Processing sheet: {sheet_name}")
                
                # Excel sheet-ini oxu
                df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                print(f"  Sheet shape: {df_raw.shape}")
                
                # Əgər sheet boşdursa və ya çox kiçikdirsə, skip et
                if df_raw.shape[0] < 4 or df_raw.shape[1] < 2:
                    print(f"  Skipping sheet {sheet_name}: Too small or empty")
                    continue
                
                # İlk bir neçə sətiri göstər
                print("  İlk 5 sətir:")
                print(df_raw.head())
                
                # Header satırları: row 1 (main) və row 2 (sub)
                main_headers = df_raw.iloc[1].fillna("").tolist()
                sub_headers = df_raw.iloc[2].fillna("").tolist()
                
                print(f"  Main headers (row 2): {main_headers}")
                print(f"  Sub headers (row 3): {sub_headers}")
                
                # Final headers yaradırıq - performance sütunları üçün xüsusi məntiq
                final_headers = []
                for i, h in enumerate(main_headers):
                    h_str = str(h).strip()
                    sub_h_str = str(sub_headers[i]).strip() if i < len(sub_headers) else ""
                    
                    if h_str == "Performance" and sub_h_str and sub_h_str != "nan":
                        # Performance alt başlığını istifadə et
                        final_headers.append(sub_h_str)
                    elif h_str and h_str != "nan":
                        # Ana başlığı istifadə et
                        final_headers.append(h_str)
                    elif sub_h_str and sub_h_str != "nan":
                        # Ana başlıq boşdursa, alt başlığı istifadə et
                        final_headers.append(sub_h_str)
                    else:
                        final_headers.append(f"Column_{i}")
                
                print(f"  Final headers: {final_headers}")
                
                # Datanı 3cü sətirdən başlat (row 3 - 0-indexed, yəni 4cü sətir)
                df = df_raw.iloc[3:].copy()
                df.columns = final_headers[:len(df.columns)]
                df = df.reset_index(drop=True)
                df = df.dropna(how='all').reset_index(drop=True)
                
                print(f"  Data shape after processing: {df.shape}")
                print("  İlk data sətiri:")
                if not df.empty:
                    print(df.iloc[0].to_dict())
                
                # Hər sətiri process et
                processed_rows = 0
                for index, row in df.iterrows():
                    # Product ID və Product name sütunlarını tap
                    product_id = None
                    product_name = None
                    
                    # Sütun adlarını yoxla
                    for col in df.columns:
                        col_str = str(col).strip().lower()
                        if "product id" in col_str and product_id is None:
                            product_id = str(row[col]).strip() if pd.notna(row[col]) else ''
                        elif "product name" in col_str and product_name is None:
                            product_name = str(row[col]).strip() if pd.notna(row[col]) else ''
                    
                    print(f"    Row {index}: Product ID='{product_id}', Product Name='{product_name}'")
                    
                    # Əgər product name yoxdursa, skip et
                    if not product_name or product_name == 'nan':
                        print(f"    Skipping row {index}: No product name")
                        continue
                    
                    # Digər sütunları tap
                    description = ""
                    features_benefits = ""
                    application = ""
                    recommendation = ""
                    api = ""
                    ilsac = ""
                    acea = ""
                    jaso = ""
                    oem_specs = ""
                    
                    for col in df.columns:
                        col_str = str(col).strip()
                        col_lower = col_str.lower()
                        value = str(row[col]).strip() if pd.notna(row[col]) and str(row[col]).strip() != 'nan' else ''
                        
                        if "description" in col_lower and not description:
                            description = value
                        elif "features" in col_lower or "benefits" in col_lower:
                            features_benefits = value
                        elif "application" in col_lower and not application:
                            application = value
                        elif "recommendation" in col_lower:
                            recommendation = value
                        # Performance sütunlarını daha dəqiq yoxla
                        elif col_str == "API" or "api" == col_lower:
                            api = value
                        elif col_str == "ILSAC" or "ilsac" == col_lower:
                            ilsac = value
                        elif col_str == "ACEA" or "acea" == col_lower:
                            acea = value
                        elif col_str == "JASO" or "jaso" == col_lower:
                            jaso = value
                        elif "oem" in col_lower and ("specification" in col_lower or "spec" in col_lower):
                            oem_specs = value
                    
                    product_data = {
                        'product_id': product_id or '',
                        'title': product_name,
                        'description': description,
                        'features_benefits': features_benefits,
                        'application': application,
                        'recommendations': recommendation,
                        'api': api,
                        'ilsac': ilsac,
                        'acea': acea,
                        'jaso': jaso,
                        'oem_specifications': oem_specs,
                    }

                    print(f"    Product data: {product_data}")
                    all_products.append(product_data)
                    processed_rows += 1
                
                print(f"  Processed {processed_rows} rows from sheet: {sheet_name}")
                                
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\nTotal products collected: {len(all_products)}")
    
    if len(all_products) == 0:
        print("No products to process!")
        return
    
    created_count = 0
    updated_count = 0
    no_change_count = 0
    error_count = 0
        
    for i, product_data in enumerate(all_products):
        print(f"\nProcessing product {i+1}: {product_data['title']}")
        try:
            # Slug oluştur
            base_slug = slugify(product_data['title']).lower()
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(product_id=product_data['product_id']).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            product_data['slug'] = slug
            
            # Önce ürünün mevcut olup olmadığını kontrol et
            existing_product = None
            if product_data['product_id']:
                try:
                    existing_product = Product.objects.get(product_id=product_data['product_id'])
                    print(f"  Found existing product by product_id: {existing_product.title}")
                except Product.DoesNotExist:
                    print(f"  No existing product found with product_id: {product_data['product_id']}")
            
            # Product ID ile bulunamadıysa, title ile ara
            if not existing_product:
                try:
                    existing_product = Product.objects.get(title=product_data['title'])
                    print(f"  Found existing product by title: {existing_product.title}")
                except Product.DoesNotExist:
                    print(f"  No existing product found with title: {product_data['title']}")
                except Product.MultipleObjectsReturned:
                    print(f"  Multiple products found with title: {product_data['title']}, using first one")
                    existing_product = Product.objects.filter(title=product_data['title']).first()
            
            if existing_product:
                # Mevcut ürün var, değişiklikleri kontrol et
                changes = compare_and_update_product(existing_product, {
                    'title': product_data['title'],
                    'description': product_data.get('description', ''),
                    'features_benefits': product_data.get('features_benefits', ''),
                    'application': product_data.get('application', ''),
                    'recommendations': product_data.get('recommendations', ''),
                    'api': product_data.get('api', ''),
                    'ilsac': product_data.get('ilsac', ''),
                    'acea': product_data.get('acea', ''),
                    'jaso': product_data.get('jaso', ''),
                    'oem_sertification': product_data.get('oem_specifications', ''),
                    'slug': slug
                })
                
                if changes:
                    print(f"  Changes detected:")
                    for field, change in changes.items():
                        print(f"    {field}: '{change['old']}' -> '{change['new']}'")
                    
                    # Sadece değişen alanları güncelle
                    for field in changes:
                        if field != 'slug':  # slug ayrı kontrol edilecek
                            if field == 'oem_sertification':
                                setattr(existing_product, field, product_data.get('oem_specifications', ''))
                            else:
                                setattr(existing_product, field, product_data.get(field, ''))
                        else:
                            setattr(existing_product, field, slug)
                    
                    # Product ID'yi de güncelle (eğer boş ise)
                    if not existing_product.product_id and product_data['product_id']:
                        existing_product.product_id = product_data['product_id']
                        print(f"    Updated product_id: {product_data['product_id']}")
                    
                    existing_product.save()
                    updated_count += 1
                    print(f"  ✓ Updated existing product: {existing_product.title}")
                else:
                    no_change_count += 1
                    print(f"  = No changes needed for: {existing_product.title}")
            else:
                # Yeni ürün oluştur
                new_product = Product.objects.create(
                    product_id=product_data['product_id'] if product_data['product_id'] else None,
                    title=product_data['title'],
                    description=product_data.get('description', ''),
                    features_benefits=product_data.get('features_benefits', ''),
                    application=product_data.get('application', ''),
                    slug=slug,
                    recommendations=product_data.get('recommendations', ''),
                    api=product_data.get('api', ''),
                    ilsac=product_data.get('ilsac', ''),
                    acea=product_data.get('acea', ''),
                    jaso=product_data.get('jaso', ''),
                    oem_sertification=product_data.get('oem_specifications', ''),
                )
                created_count += 1
                print(f"  ✓ Created new product: {new_product.title}")
                
        except Exception as e:
            error_count += 1
            print(f"  ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
        
    print(f"\n{'='*50}")
    print(f"Import completed:")
    print(f"  Created: {created_count}")
    print(f"  Updated: {updated_count}")
    print(f"  No changes: {no_change_count}")
    print(f"  Errors: {error_count}")
    print(f"{'='*50}")

def import_excel_products(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder mövcud deyil: {folder_path}")
        return
    
    process_all_excel_files(folder_path)