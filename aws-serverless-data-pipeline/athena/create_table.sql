-- Replace YOUR-BUCKET-NAME with your S3 bucket
CREATE DATABASE IF NOT EXISTS sales_db;

CREATE EXTERNAL TABLE IF NOT EXISTS sales_db.clean_sales (
    order_id      string,
    order_date    date,
    customer_name string,
    city          string,
    product       string,
    category      string,
    quantity      int,
    unit_price    double,
    total_amount  double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar' = ',', 'quoteChar' = '"')
LOCATION 's3://YOUR-BUCKET-NAME/clean/'
TBLPROPERTIES ('skip.header.line.count' = '1');
