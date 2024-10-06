import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
import joblib

def load_data():
    sales_data_1 = pd.read_csv('C:/Users/nayan/OneDrive/Desktop/Internshala projects/Transactional_data_retail_01.csv')
    sales_data_2 = pd.read_csv('C:/Users/nayan/OneDrive/Desktop/Internshala projects/Transactional_data_retail_02.csv')
    customer_data = pd.read_csv('C:/Users/nayan/OneDrive/Desktop/Internshala projects/CustomerDemographics.csv')
    product_data = pd.read_csv('C:/Users/nayan/OneDrive/Desktop/Internshala projects/ProductInfo.csv')
    
    sales_data = pd.concat([sales_data_1, sales_data_2], ignore_index=True)
    return sales_data, customer_data, product_data

def preprocess_data(sales_data):
    sales_data['transaction_date'] = pd.to_datetime(sales_data['InvoiceDate'],errors='coerce')
    
    grouped = sales_data.groupby(['StockCode', 'transaction_date']).agg({'Quantity': 'sum'}).reset_index()
    
    return grouped

def get_top_products(grouped_data):
    top_products = grouped_data.groupby('StockCode')['Quantity'].sum().nlargest(10).index
    print(top_products)
    return top_products

def train_model(grouped_data, stock_code):
    product_data = grouped_data[grouped_data['StockCode'] == stock_code]
    product_data.set_index('transaction_date', inplace=True)
    
    product_data = product_data['Quantity'].resample('W').sum()
    
    model = ARIMA(product_data, order=(5, 1, 0))
    model_fit = model.fit()
    
    return model_fit

def forecast_demand(model_fit, weeks):
    forecast = model_fit.forecast(steps=weeks)
    return forecast




