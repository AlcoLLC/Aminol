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

def process_all_excel_files(folder_path):    
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls"))
    
    print(f"Excel fayllar tapıldı: {len(excel_files)}")
    for file in excel_files:
        print(f"  - {file}")
    
    all_products = []
    
    for file_path in excel_files:
        print(f"\nProcessing file: {file_path}")
        try:
            # Excel faylını oxu
            df_raw = pd.read_excel(file_path, sheet_name=0, header=None)
            print(f"Excel shape: {df_raw.shape}")
            
            # İlk bir neçə sətiri göstər
            print("İlk 5 sətir:")
            print(df_raw.head())
            
            # Header satırını tap (row 1 - 0-indexed)
            headers = df_raw.iloc[1].fillna("").tolist()
            print(f"Headers (row 2): {headers}")
            
            # Clean up headers - remove empty ones and fix naming
            clean_headers = []
            for i, header in enumerate(headers):
                header_str = str(header).strip()
                if header_str and header_str != "nan":
                    clean_headers.append(header_str)
                else:
                    clean_headers.append(f"Column_{i}")
            
            print(f"Clean headers: {clean_headers}")
            
            # Performance sütunlarını tap və düzəlt
            performance_start_idx = None
            for i, header in enumerate(clean_headers):
                if "Performance" in str(header) or header in ["API", "ILSAC", "ACEA", "JASO", "OEM specifications"]:
                    if performance_start_idx is None:
                        performance_start_idx = i
                    # Performance sütunlarını adlandır
                    if header == "API":
                        clean_headers[i] = "Performance API"
                    elif header == "ILSAC":
                        clean_headers[i] = "Performance ILSAC"
                    elif header == "ACEA":
                        clean_headers[i] = "Performance ACEA"
                    elif header == "JASO":
                        clean_headers[i] = "Performance JASO"
                    elif header == "OEM specifications":
                        clean_headers[i] = "Performance OEM specifications"
            
            print(f"Final headers: {clean_headers}")
            
            # Datanı 2ci sətirdən başlat (row 2 - 0-indexed, yəni 3cü sətir)
            df = df_raw.iloc[2:].copy()
            df.columns = clean_headers[:len(df.columns)]
            df = df.reset_index(drop=True)
            df = df.dropna(how='all').reset_index(drop=True)
            
            print(f"Data shape after processing: {df.shape}")
            print("İlk data sətiri:")
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
                
                print(f"Row {index}: Product ID='{product_id}', Product Name='{product_name}'")
                
                # Əgər product name yoxdursa, skip et
                if not product_name or product_name == 'nan':
                    print(f"  Skipping row {index}: No product name")
                    continue
                
                # Digər sütunları tap
                description = ""
                features = ""
                application = ""
                recommendation = ""
                api = ""
                ilsac = ""
                acea = ""
                jaso = ""
                oem_specs = ""
                
                for col in df.columns:
                    col_str = str(col).strip().lower()
                    value = str(row[col]).strip() if pd.notna(row[col]) and str(row[col]).strip() != 'nan' else ''
                    
                    if "description" in col_str and not description:
                        description = value
                    elif "features" in col_str or "benefits" in col_str:
                        features = value
                    elif "application" in col_str and not application:
                        application = value
                    elif "recommendation" in col_str:
                        recommendation = value
                    elif "performance api" in col_str or col_str == "api":
                        api = value
                    elif "performance ilsac" in col_str or col_str == "ilsac":
                        ilsac = value
                    elif "performance acea" in col_str or col_str == "acea":
                        acea = value
                    elif "performance jaso" in col_str or col_str == "jaso":
                        jaso = value
                    elif "performance oem" in col_str or "oem specifications" in col_str:
                        oem_specs = value
                
                product_data = {
                    'product_id': product_id or '',
                    'title': product_name,
                    'description': description,
                    'features': features,
                    'application': application,
                    'recommendations': recommendation,
                    'api': api,
                    'ilsac': ilsac,
                    'acea': acea,
                    'jaso': jaso,
                    'oem_specifications': oem_specs,
                }

                print(f"  Product data: {product_data}")
                all_products.append(product_data)
                processed_rows += 1
                                
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
    error_count = 0
        
    for i, product_data in enumerate(all_products):
        print(f"\nProcessing product {i+1}: {product_data['title']}")
        try:
            base_slug = slugify(product_data['title']).lower()
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(product_id=product_data['product_id']).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Full description yaratmaq
            full_description = product_data['description']
            if product_data.get('features'):
                full_description += f"\n\nFeatures & Benefits:\n{product_data['features']}"
            if product_data.get('application'):
                full_description += f"\n\nApplication:\n{product_data['application']}"
            
            print(f"  Creating/updating with slug: {slug}")
            
            product, created = Product.objects.update_or_create(
                product_id=product_data['product_id'] if product_data['product_id'] else None,
                defaults={
                    'product_id': product_data['product_id'],
                    'title': product_data['title'],
                    'description': full_description,
                    'slug': slug,
                    'recommendations': product_data.get('recommendations', ''),
                    'api': product_data.get('api', ''),
                    'ilsag': product_data.get('ilsac', ''),  # Model field adı ilsag-dır
                    'acea': product_data.get('acea', ''),
                    'jaso': product_data.get('jaso', ''),
                    'oem_sertification': product_data.get('oem_specifications', ''),
                }
            )

            if created:
                created_count += 1
                print(f"  ✓ Created new product: {product.title}")
            else:
                updated_count += 1
                print(f"  ✓ Updated existing product: {product.title}")
                
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
    print(f"  Errors: {error_count}")
    print(f"{'='*50}")

def import_excel_products(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder mövcud deyil: {folder_path}")
        return
    
    process_all_excel_files(folder_path)