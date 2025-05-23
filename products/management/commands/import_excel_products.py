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
            
            # Headerları tap
            main_headers = df_raw.iloc[2].fillna("").tolist()
            sub_headers = df_raw.iloc[3].fillna("").tolist()
            
            print(f"Main headers (row 3): {main_headers}")
            print(f"Sub headers (row 4): {sub_headers}")
            
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
            
            print(f"Final headers: {final_headers}")
            
            # Datanı başdan təyin et
            df = df_raw.iloc[4:].copy()
            df.columns = final_headers[:len(df.columns)] 
            df = df.reset_index(drop=True)
            df = df.dropna(how='all').reset_index(drop=True)
            
            print(f"Data shape after processing: {df.shape}")
            print("İlk data sətiri:")
            if not df.empty:
                print(df.iloc[0].to_dict())
            
            processed_rows = 0
            for index, row in df.iterrows():
                product_id = str(row.get('Product ID', '')).strip() if pd.notna(row.get('Product ID')) else ''
                title = str(row.get('Product name', '')).strip() if pd.notna(row.get('Product name')) else ''
                
                print(f"Row {index}: Product ID='{product_id}', Title='{title}'")
                
                if not title:
                    print(f"  Skipping row {index}: No title")
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
            
            full_description = product_data['description']
            if product_data.get('features'):
                full_description += f"\n\nFeatures & Benefits:\n{product_data['features']}"
            if product_data.get('application'):
                full_description += f"\n\nApplication:\n{product_data['application']}"
            
            print(f"  Creating/updating with slug: {slug}")
            
            product, created = Product.objects.update_or_create(
                product_id=product_data['product_id'],
                defaults={
                    'product_id': product_data['product_id'],
                    'title': product_data['title'],
                    'description': full_description,
                    'slug': slug,
                    'recommendations': product_data.get('recommendations', ''),
                    'api': product_data.get('api', ''),
                    'ilsag': product_data.get('ilsac', ''),  # Typo düzəldin: ilsac -> ilsag
                    'acea': product_data.get('acea', ''),
                    'jaso': product_data.get('jaso', ''),
                    'oem_sertification': product_data.get('oem_specifications', ''),  # Typo: certification
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