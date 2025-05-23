import pandas as pd
import os
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from products.models import Product  # Replace with your actual model import


class Command(BaseCommand):
    help = 'Import products from Excel files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--directory',
            type=str,
            help='Directory containing Excel files',
            default='excel_files'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products before import',
        )

    def handle(self, *args, **options):
        directory = options['directory']
        clear_existing = options['clear']
        
        # Clear existing products if requested
        if clear_existing:
            self.stdout.write('Clearing existing products...')
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing products cleared.'))
        
        # Get Excel files directory
        if not os.path.isabs(directory):
            directory = os.path.join(settings.BASE_DIR, directory)
        
        if not os.path.exists(directory):
            raise CommandError(f'Directory does not exist: {directory}')
        
        # Find Excel files
        excel_files = list(Path(directory).glob('*.xlsx'))
        if not excel_files:
            excel_files = list(Path(directory).glob('*.xls'))
        
        if not excel_files:
            raise CommandError(f'No Excel files found in: {directory}')
        
        self.stdout.write(f'Found {len(excel_files)} Excel files')
        
        total_products = 0
        
        for excel_file in excel_files:
            self.stdout.write(f'Processing: {excel_file.name}')
            
            try:
                products_added = self.process_excel_file(excel_file)
                total_products += products_added
                self.stdout.write(
                    self.style.SUCCESS(f'Added {products_added} products from {excel_file.name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {excel_file.name}: {str(e)}')
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(f'Import completed. Total products added: {total_products}')
        )

    def process_excel_file(self, excel_file):
        """Process a single Excel file"""
        
        # Read Excel file
        df = pd.read_excel(excel_file, header=None)
        
        # Find header row
        header_row = self.find_header_row(df)
        if header_row is None:
            self.stdout.write(f'No header found in {excel_file.name}, using row 1')
            header_row = 1
        
        # Set headers
        headers = df.iloc[header_row].fillna('').astype(str).str.strip()
        
        # Get data
        data_df = df.iloc[header_row + 1:].copy()
        data_df.columns = headers
        data_df = data_df.dropna(how='all')
        
        products_added = 0
        
        for idx, row in data_df.iterrows():
            try:
                # Extract product data
                product_data = self.extract_product_data(row, data_df.columns, excel_file)
                
                if not product_data:
                    continue
                
                # Create or update product
                product, created = Product.objects.get_or_create(
                    product_id=product_data['product_id'],
                    defaults=product_data
                )
                
                if created:
                    products_added += 1
                    self.stdout.write(f'  Added: {product_data["product_name"]}')
                else:
                    # Update existing product
                    for key, value in product_data.items():
                        setattr(product, key, value)
                    product.save()
                    self.stdout.write(f'  Updated: {product_data["product_name"]}')
                
            except Exception as e:
                self.stdout.write(f'  Error processing row {idx}: {str(e)}')
                continue
        
        return products_added

    def find_header_row(self, df):
        """Find the row that contains headers"""
        for idx, row in df.iterrows():
            if any(str(cell).strip().lower() in ['product id', 'product name'] 
                   for cell in row if pd.notna(cell)):
                return idx
        return None

    def extract_product_data(self, row, columns, excel_file):
        """Extract product data from a row"""
        
        # Find product ID and name
        product_id = None
        product_name = None
        
        # Try to find by column names
        for col in columns:
            col_lower = str(col).lower().strip()
            if 'product id' in col_lower or col_lower == 'id':
                if pd.notna(row[col]) and str(row[col]).strip():
                    product_id = str(row[col]).strip()
            elif 'product name' in col_lower or col_lower == 'name':
                if pd.notna(row[col]) and str(row[col]).strip():
                    product_name = str(row[col]).strip()
        
        # Fallback to positional approach
        if not product_id and len(row) > 1:
            if pd.notna(row.iloc[1]) and str(row.iloc[1]).strip():
                product_id = str(row.iloc[1]).strip()
        
        if not product_name and len(row) > 2:
            if pd.notna(row.iloc[2]) and str(row.iloc[2]).strip():
                product_name = str(row.iloc[2]).strip()
        
        # Validate required fields
        if (not product_name or not product_id or 
            str(product_id).lower() in ['nan', 'none', ''] or
            str(product_name).lower() in ['nan', 'none', ''] or
            product_name == 'Product name' or product_id == 'Product ID'):
            return None
        
        # Extract other fields
        def safe_extract(index, default=''):
            if len(row) > index and pd.notna(row.iloc[index]):
                value = str(row.iloc[index]).strip()
                return value if value != 'nan' else default
            return default
        
        return {
            'product_id': product_id,
            'product_name': product_name,
            'description': safe_extract(3),
            'features': safe_extract(4),
            'applications': safe_extract(5),
            'api_spec': safe_extract(6),
            'ilsac_spec': safe_extract(7),
            'acea_spec': safe_extract(8),
            'jaso_spec': safe_extract(9),
            'oem_specs': safe_extract(10),
            'recommendations': safe_extract(11),
            'file_source': excel_file.name
        }