import sys
import pandas as pd
import plotly.graph_objects as go


def main(args):
    a = str(args[1])
    b = str(args[2])

    df = pd.read_csv(a)
    df2 = pd.read_csv(b, names=[0, 1, 2, 'timestamp', 4, 5, 6, 7, 8, 9, 10, 'side', 'price', 'size', 14, 15, 16, 17, 18, 19, 20])

    df = df[['timestamp', 'bid1', 'bidqty1', 'ask1', 'askqty1']].copy()
    df2 = df2[['timestamp', 'side', 'price', 'size']].copy()

    df['timestamp'] = df['timestamp'].floordiv(1000)
    df2['timestamp'] = df2['timestamp'].floordiv(1000)

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df2["timestamp"] = pd.to_datetime(df2["timestamp"], unit='ms')

    fullog = pd.merge(df, df2, how='outer', on='timestamp')
    fullog = fullog.sort_values(by=['timestamp'])

    fullog['bid1'].fillna(method='ffill', inplace=True)
    fullog['bidqty1'].fillna(method='ffill', inplace=True)
    fullog['ask1'].fillna(method='ffill', inplace=True)
    fullog['askqty1'].fillna(method='ffill', inplace=True)

    mergedlog = fullog.dropna()
    drawgraph(args[3], fullog, mergedlog)


def drawgraph(graph_type, fullog, mergedlog):
    a = int(graph_type)
    if a > 1:
        grouped = fullog.groupby(fullog.side)

        dfsell = grouped.get_group("sell")
        dfbuy = grouped.get_group("buy")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                hovertemplate='<i>Price</i>: %{y:0f}' +
                              '<br>Timestamp: %{x}<br>',
                line=dict(color='purple'),
                x=fullog.timestamp,
                y=fullog.ask1,
                name="Ask"

            ))

        fig.add_trace(
            go.Scatter(
                hovertemplate='<i>Price</i>: %{y:0f}' +
                              '<br>Timestamp: %{x}<br>',
                line=dict(color='blue'),
                x=fullog.timestamp,
                y=fullog.bid1,
                name="Bid"

            ))

        fig.add_trace(
            go.Scatter(
                hovertemplate='<i>Price</i>: %{y:0f}' +
                              '<br>Timestamp: %{x}<br>',
                mode='markers',
                x=dfsell.timestamp,
                y=dfsell.price,
                line=dict(color='red'),
                name="Sell"
            ))

        fig.add_trace(
            go.Scatter(
                hovertemplate='Price: %{y:0f}' +
                              '<br>Timestamp: %{x}<br>',
                mode='markers',
                x=dfbuy.timestamp,
                y=dfbuy.price,
                line=dict(color='green'),
                name="Buy"
            ))

        fig.update_layout(xaxis_rangeslider_visible=False,
                          title="Market Data Vs Trade Price",
                          xaxis_title="Timestamp",
                          yaxis_title="Price",
                          font=dict(
                              family="Arial",
                              size=15
                          )
                          )
        fig.show()

    else:

        fig = go.Figure()

        grouped = mergedlog.groupby(mergedlog.side)

        dfsell = grouped.get_group("sell")
        dfbuy = grouped.get_group("buy")

        fig.add_trace(
            go.Candlestick(
                x=mergedlog.timestamp,
                open=mergedlog['ask1'], high=mergedlog['ask1'],
                low=mergedlog['bid1'], close=mergedlog['bid1'],
                increasing={'line': {'color': 'black'}},
                decreasing={'line': {'color': 'blue'}},
                name="BidAsk",
                yhoverformat="0f"

            ))

        fig.add_trace(
            go.Scatter(
                hovertemplate='<i>Price</i>: %{y:0f}' +
                              '<br>Timestamp: %{x}<br>',
                mode='markers',
                x=dfsell.timestamp,
                y=dfsell.price,
                fillcolor='red',
                name="Sell"))

        fig.add_trace(
            go.Scatter(
                hovertemplate='Price: %{y:0f}' +
                              '<br>Timestamp: %{x}<br>',
                mode='markers',
                x=dfbuy.timestamp,
                y=dfbuy.price,
                fillcolor='green',
                name="Buy"
            ))

        fig.update_layout(xaxis_rangeslider_visible=False,
                          title="BidAsk Vs Trade Price",
                          xaxis_title="Timestamp",
                          yaxis_title="Price",
                          font=dict(
                              family="Arial",
                              size=15
                          )
                          )
        fig.show()


if __name__ == '__main__':
    main(sys.argv)
