#!/bin/bash

DB_NAME="mydatabase"
USER="aminol"
HOST="127.0.0.1"

# Tabloları buraya ekleyin
TABLES=(
  "products_product"
  "news_news"
  "contact_message"
  "brands_brand"
)

for TABLE in "${TABLES[@]}"
do
  echo "Exporting $TABLE..."
  psql -U $USER -d $DB_NAME -h $HOST -c "\COPY (SELECT * FROM $TABLE) TO '/Aminol/${TABLE}.csv' DELIMITER ',' CSV HEADER;"
done

echo "Tüm tablolar export edildi."
