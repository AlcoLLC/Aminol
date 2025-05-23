import os
import pandas as pd
from django.utils.text import slugify
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
            import traceback
            traceback.print_exc()
            continue
    
    if len(all_products) == 0:
        return
    
    created_count = 0
    updated_count = 0
    error_count = 0
        
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
            
            product, created = Product.objects.update_or_create(
                product_id=product_data['product_id'],
                defaults={
                    'product_id': product_data['product_id'],
                    'title': product_data['title'],
                    'description': full_description,
                    'slug': slug,
                    'reccommendations': product_data.get('recommendations', ''),
                    'api': product_data.get('api', ''),
                    'ilsag': product_data.get('ilsac', ''),
                    'acea': product_data.get('acea', ''),
                    'jaso': product_data.get('jaso', ''),
                    'oem_sertification': product_data.get('oem_specifications', ''),
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1
                
        except Exception as e:
            error_count += 1
            import traceback
            traceback.print_exc()
            continue
        
    print(f"Import tamamlandı: {created_count} yeni, {updated_count} güncellendi, {error_count} hata")

def import_excel_products(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder mövcud deyil: {folder_path}")
        return
    
    process_all_excel_files(folder_path)