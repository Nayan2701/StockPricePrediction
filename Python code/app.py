
from flask import Flask, request, jsonify
import joblib
from model import load_data, preprocess_data, get_top_products, train_model, forecast_demand

app = Flask(__name__)


sales_data, customer_data, product_data = load_data()
grouped_data = preprocess_data(sales_data)
top_products = get_top_products(grouped_data)

@app.route('/top-products', methods=['GET'])
def get_top_products_api():
    return jsonify(top_products.tolist())

@app.route('/forecast', methods=['POST'])
def forecast():
    data = request.json
    stock_code = data['StockCode']
    weeks = data['weeks']
    
    if stock_code not in top_products:
        return jsonify({'error': 'Invalid stock code'}), 400
    
    model_fit = train_model(grouped_data, stock_code)
    forecast = forecast_demand(model_fit, weeks)
    
    response = {
        'stock_code': stock_code,
        'forecasted_demand': forecast.tolist()
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')