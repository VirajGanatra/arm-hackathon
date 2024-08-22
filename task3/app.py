import random
from flask import Flask, jsonify, render_template, request
import plotly
from stock_price import Stock
import datetime
from graph.price_graph import PriceGraph

app = Flask(__name__)

def generate_price_graph(stock_name):
    stock = Stock(stock_name)
    graph = PriceGraph()

    fig = graph.generate_candlestick(stock.stock_history())
    return fig

@app.route('/')
def index():
    fig = generate_price_graph('TSLA')
    graph_json = plotly.io.to_json(fig)    

    return render_template('index.html', graph_json=graph_json)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    start_date = data.get('start_date', '')
    stock = data.get('stock', '')
    amount_spent = int(data.get('amount_spent', ''))
    
    
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    
    
    if start_date_obj.weekday() >= 5:
        return render_template('index.html', error="Start date cannot be a weekend. Please select a weekday.")
    
    price_diff = Stock(stock).calculate_price_difference(amount_spent, start_date)
    return jsonify({ 'profit' : price_diff })

@app.route('/update-plot', methods=['POST'])
def update_plot():
    print(request.content_type)
    data = request.get_json()
    stock = data.get('stock', '')
    fig = generate_price_graph(stock)

    graph_json = plotly.io.to_json(fig)
    return jsonify(graph_json)

if __name__ == '__main__':
    app.run(debug=True)