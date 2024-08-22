import plotly.graph_objs as go
import plotly.io as pio

class PriceGraph:

    def generate_candlestick(self, stock_data):
        # Create the candlestick figure
        fig = go.Figure(data=[go.Candlestick(
            x=stock_data.index,
            open=stock_data.loc[:]['Open'],
            high=stock_data.loc[:]['High'],
            low=stock_data.loc[:]['Low'],
            close=stock_data.loc[:]['Close']
        )])

        # Customize the layout
        fig.update_layout(
            title='Stock Price Data',
            yaxis_title='Stock Price',
            xaxis_title='Date',
            xaxis_rangeslider_visible=False
        )

        return fig