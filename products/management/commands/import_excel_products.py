import pandas as pd
import sqlite3
import os
from pathlib import Path

def process_excel_files_to_sqlite(excel_directory, db_path):
    """
    Process Excel files and convert them to SQLite database
    """
    
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            product_name TEXT,
            description TEXT,
            features TEXT,
            applications TEXT,
            api_spec TEXT,
            ilsac_spec TEXT,
            acea_spec TEXT,
            jaso_spec TEXT,
            oem_specs TEXT,
            recommendations TEXT,
            file_source TEXT
        )
    ''')
    
    # Get all Excel files
    excel_files = list(Path(excel_directory).glob('*.xlsx'))
    if not excel_files:
        excel_files = list(Path(excel_directory).glob('*.xls'))
    
    print(f"Excel faylları tapıldı: {len(excel_files)}")
    
    total_products = 0
    
    for excel_file in excel_files:
        print(f"\nProcessing file: {excel_file}")
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_file, header=None)
            print(f"Excel shape: {df.shape}")
            
            # Print first few rows to understand structure
            print("İlk 5 sətir:")
            print(df.head())
            
            # Find the header row (usually contains "Product ID", "Product name", etc.)
            header_row = None
            for idx, row in df.iterrows():
                if any(str(cell).strip().lower() in ['product id', 'product name'] for cell in row if pd.notna(cell)):
                    header_row = idx
                    break
            
            if header_row is None:
                print("Header tapılmadı, default olaraq 1-ci sətir istifadə edilir")
                header_row = 1
            
            print(f"Header row: {header_row}")
            
            # Set headers
            headers = df.iloc[header_row].fillna('').astype(str).str.strip()
            print(f"Headers: {headers.tolist()}")
            
            # Get data starting from header_row + 1
            data_df = df.iloc[header_row + 1:].copy()
            data_df.columns = headers
            
            print(f"Data shape after processing: {data_df.shape}")
            
            # Remove empty rows
            data_df = data_df.dropna(how='all')
            
            # Process each row
            products_added = 0
            for idx, row in data_df.iterrows():
                # Find product ID and name columns
                product_id = None
                product_name = None
                
                # Try to find product ID column
                for col in data_df.columns:
                    col_lower = str(col).lower().strip()
                    if 'product id' in col_lower or 'id' in col_lower:
                        if pd.notna(row[col]) and str(row[col]).strip():
                            product_id = str(row[col]).strip()
                            break
                
                # Try to find product name column
                for col in data_df.columns:
                    col_lower = str(col).lower().strip()
                    if 'product name' in col_lower or 'name' in col_lower:
                        if pd.notna(row[col]) and str(row[col]).strip():
                            product_name = str(row[col]).strip()
                            break
                
                # If we don't find explicit columns, use positional approach
                if not product_id and len(data_df.columns) > 1:
                    if pd.notna(row.iloc[1]) and str(row.iloc[1]).strip():
                        product_id = str(row.iloc[1]).strip()
                
                if not product_name and len(data_df.columns) > 2:
                    if pd.notna(row.iloc[2]) and str(row.iloc[2]).strip():
                        product_name = str(row.iloc[2]).strip()
                
                print(f"Row {idx}: Product ID='{product_id}', Product Name='{product_name}'")
                
                # Skip if no product name or ID
                if (not product_name or not product_id or 
                    str(product_id).lower() in ['nan', 'none', ''] or
                    str(product_name).lower() in ['nan', 'none', ''] or
                    product_name == 'Product name' or product_id == 'Product ID'):
                    print(f"  Skipping row {idx}: No valid product data")
                    continue
                
                # Extract other fields
                description = str(row.iloc[3]) if len(row) > 3 and pd.notna(row.iloc[3]) else ''
                features = str(row.iloc[4]) if len(row) > 4 and pd.notna(row.iloc[4]) else ''
                applications = str(row.iloc[5]) if len(row) > 5 and pd.notna(row.iloc[5]) else ''
                api_spec = str(row.iloc[6]) if len(row) > 6 and pd.notna(row.iloc[6]) else ''
                ilsac_spec = str(row.iloc[7]) if len(row) > 7 and pd.notna(row.iloc[7]) else ''
                acea_spec = str(row.iloc[8]) if len(row) > 8 and pd.notna(row.iloc[8]) else ''
                jaso_spec = str(row.iloc[9]) if len(row) > 9 and pd.notna(row.iloc[9]) else ''
                oem_specs = str(row.iloc[10]) if len(row) > 10 and pd.notna(row.iloc[10]) else ''
                recommendations = str(row.iloc[11]) if len(row) > 11 and pd.notna(row.iloc[11]) else ''
                
                # Clean up 'nan' values
                fields = [description, features, applications, api_spec, ilsac_spec, 
                         acea_spec, jaso_spec, oem_specs, recommendations]
                cleaned_fields = [field if field != 'nan' else '' for field in fields]
                
                # Insert into database
                cursor.execute('''
                    INSERT INTO products (
                        product_id, product_name, description, features, applications,
                        api_spec, ilsac_spec, acea_spec, jaso_spec, oem_specs,
                        recommendations, file_source
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    product_id, product_name, *cleaned_fields, str(excel_file.name)
                ))
                
                products_added += 1
                print(f"  Added product: {product_name}")
            
            print(f"File {excel_file.name}: {products_added} products added")
            total_products += products_added
            
        except Exception as e:
            print(f"Error processing {excel_file}: {str(e)}")
            continue
    
    # Commit and close
    conn.commit()
    
    # Print summary
    cursor.execute("SELECT COUNT(*) FROM products")
    total_count = cursor.fetchone()[0]
    print(f"\nSUMMARY:")
    print(f"Total products in database: {total_count}")
    print(f"Products added this session: {total_products}")
    
    # Show sample products
    cursor.execute("SELECT product_id, product_name, file_source FROM products LIMIT 5")
    sample_products = cursor.fetchall()
    print(f"\nSample products:")
    for product in sample_products:
        print(f"  {product[0]} - {product[1]} (from {product[2]})")
    
    conn.close()
    print(f"\nDatabase saved to: {db_path}")

# Usage
if __name__ == "__main__":
    excel_directory = "/path/to/excel/files"  # Excel fayllarının olduğu qovluq
    database_path = "aminol_products.db"      # SQLite database faylının adı
    
    process_excel_files_to_sqlite(excel_directory, database_path)