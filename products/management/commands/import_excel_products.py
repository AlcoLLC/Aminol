import os
import pandas as pd
from django.utils.text import slugify
from django.core.management.base import BaseCommand
import glob
from products.models import Product

def process_all_excel_files(folder_path):    
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls"))    
    all_products = []
    
    for file_path in excel_files:
        try:
            df = pd.read_excel(file_path, header=1)
            df.columns = df.columns.str.strip()
            
            if len(df) > 0:
                first_row = df.iloc[0]            
            processed_rows = 0
            for index, row in df.iterrows():
                product_id = str(row.get('Product ID', '')).strip() if pd.notna(row.get('Product ID')) else ''
                title = str(row.get('Product name', '')).strip() if pd.notna(row.get('Product name')) else ''
                
                product_data = {
                    'product_id': product_id,
                    'title': title,
                    'description': str(row.get('Description', '')).strip() if pd.notna(row.get('Description')) else '',
                    'features': str(row.get('Features & Benefits', '')).strip() if pd.notna(row.get('Features & Benefits')) else '',
                    'application': str(row.get('Application', '')).strip() if pd.notna(row.get('Application')) else '',
                    'recommendations': str(row.get('Recommendation', '')).strip() if pd.notna(row.get('Recommendation')) else '',
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
                    'title': product_data['title'],
                    'description': full_description,
                    'slug': slug,
                    'reccommendations': product_data.get('recommendations', ''),
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

def import_excel_products(folder_path):
    if not os.path.exists(folder_path):
        return
    
    process_all_excel_files(folder_path)
