from flask import Flask, render_template, request
from stock_price import StockPrice
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start_date = request.form['start_date']
    stock = request.form['stock']
    amount_spent = request.form['amount_spent']
    
    price_diff = StockPrice(stock, amount_spent, start_date).calculate_price_difference(start_date)
    
    return render_template('result.html', price_diff=price_diff)



if __name__ == '__main__':
    app.run(debug=True)