import plotly.graph_objs as go
import plotly.io as pio

# Sample data
stock_data = {
    'Date': ['2024-08-01', '2024-08-02', '2024-08-05', '2024-08-06', '2024-08-07'],
    'Open': [150, 152, 148, 151, 153],
    'High': [155, 157, 152, 154, 158],
    'Low': [148, 149, 146, 149, 150],
    'Close': [153, 151, 149, 152, 157]
}

# Create the candlestick figure
fig = go.Figure(data=[go.Candlestick(
    x=stock_data['Date'],
    open=stock_data['Open'],
    high=stock_data['High'],
    low=stock_data['Low'],
    close=stock_data['Close']
)])

# Customize the layout
fig.update_layout(
    title='Stock Price Data',
    yaxis_title='Stock Price',
    xaxis_title='Date',
    xaxis_rangeslider_visible=False
)

# Show the figure
fig.show()