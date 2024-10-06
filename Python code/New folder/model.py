import pandas as pd
import numpy as np
from datetime import datetime

# Load the datasets
df1 = pd.read_csv('/Transactional_data_retail_01.csv')
df2 = pd.read_csv('/Transactional_data_retail_02.csv')

# Combine the two datasets
data = pd.concat([df1, df2])

# Convert transaction date to datetime

# The errors='coerce' argument handles mismatched dates by setting them to NaT (Not a Time)
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'],infer_datetime_format=True,errors='coerce', format='mixed')

# Handle missing values (for simplicity, let's fill them with 0)
data.fillna(0, inplace=True)

# Filter data for top 10 best-selling products
top_10_products = data.groupby('StockCode')['Quantity'].sum().sort_values(ascending=False).head(10).index
top_10_data = data[data['StockCode'].isin(top_10_products)]

# Aggregate data by week for each product
top_10_data['Week'] = top_10_data['InvoiceDate'].dt.to_period('W')
weekly_sales = top_10_data.groupby(['StockCode', 'Week'])['Quantity'].sum().reset_index()

# Convert 'Week' back to datetime for time series
weekly_sales['Week'] = weekly_sales['Week'].apply(lambda x: x.start_time)

# Pivot for easier model application
sales_pivot = weekly_sales.pivot(index='Week', columns='StockCode', values='Quantity').fillna(0)
