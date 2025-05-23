import os
import pandas as pd
from django.utils.text import slugify
from django.core.management.base import BaseCommand
from products.models import Product
import glob

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
        process_all_excel_files(folder_path)
        self.stdout.write(self.style.SUCCESS("Done!"))


def process_all_excel_files(folder_path):
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx")) + glob.glob(os.path.join(folder_path, "*.xls"))
    all_products = []

    for file_path in excel_files:
        try:
            df = pd.read_excel(file_path, header=[2, 3])
            df.columns = [' '.join(col).strip() for col in df.columns.values]

            for index, row in df.iterrows():
                product_id = str(row.get('Product ID', '')).strip()
                title = str(row.get('Product name', '')).strip()

                product_data = {
                    'product_id': product_id,
                    'title': title,
                    'description': str(row.get('Description', '')).strip(),
                    'features': str(row.get('Features & Benefits', '')).strip(),
                    'application': str(row.get('Application', '')).strip(),
                    'recommendations': str(row.get('Recommendation', '')).strip(),
                    'api': str(row.get('Performance API', '')).strip(),
                    'ilsac': str(row.get('Performance ILSAC', '')).strip(),
                    'acea': str(row.get('Performance ACEA', '')).strip(),
                    'jaso': str(row.get('Performance JASO', '')).strip(),
                    'oem_specifications': str(row.get('Performance OEM specifications', '')).strip(),
                }

                all_products.append(product_data)

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue

    for product_data in all_products:
        try:
            from products.models import Product  # Optional: If circular import issue

            slug = base_slug = slugify(product_data['title'])
            counter = 1
            while Product.objects.filter(slug=slug).exclude(product_id=product_data['product_id']).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            full_description = product_data['description']
            if product_data.get('features'):
                full_description += f"\n\nFeatures & Benefits:\n{product_data['features']}"
            if product_data.get('application'):
                full_description += f"\n\nApplication:\n{product_data['application']}"

            Product.objects.update_or_create(
                product_id=product_data['product_id'],
                defaults={
                    'product_id': product_data['product_id'],
                    'title': product_data['title'],
                    'description': full_description,
                    'slug': slug,
                    'recommendations': product_data.get('recommendations', ''),
                    'api': product_data.get('api', ''),
                    'ilsag': product_data.get('ilsac', ''),
                    'acea': product_data.get('acea', ''),
                    'jaso': product_data.get('jaso', ''),
                    'oem_sertification': product_data.get('oem_specifications', ''),
                }
            )
        except Exception as e:
            print(f"Error saving product {product_data['product_id']}: {e}")


def import_excel_products(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder mövcud deyil: {folder_path}")
        return
    
    process_all_excel_files(folder_path)