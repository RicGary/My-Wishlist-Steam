from datetime import date
import plotly.graph_objects as go


def plotly_graph(account_name, df):

    layout = go.Layout(
        template='plotly_dark'
    )

    fig = go.Figure(
        layout=layout,
        data=[
            go.Bar(
                name='Discount',
                x=df['name'],
                y=df['full_price'],
                marker=dict(color='palegreen'),
                hovertext=[
                    f"<b>Full price:</b> {df['full_price'][i]:.2f}<br>" +
                    f"<b>With discount:</b> {df['price'][i]:.2f}<br>" +
                    f"<b>Discount:</b> {df['full_price'][i] - df['price'][i]:.2f}<br>"+
                    f"<b>Discount percentage:</b> {round(100 - df['price'][i]/df['full_price'][i] * 100, 2)}%"
                    for i in range(len(df))
                ]
            ),
            go.Bar(
                name='Current Price',
                x=df['name'],
                y=df['price'],
                marker=dict(color=df['full_price']),
                hovertext=[
                    f"<b>Current price:</b> {round(df['price'][i], 2)}"
                    for i in range(len(df))
                ]
            )
        ]
    )

    fig.update_layout(
        barmode='overlay',
        title=f"""
        <span style="font-size: 18px;"><b>{account_name} Wishlist: </b>{date.today()}</span>
        <br><span style="font-size: 14px;"><b>Sum without discount: </b>{round(df['full_price'].sum(), 2)}</span>
        <br><span style="font-size: 14px;"><b>Sum with discount: </b>{round(df['price'].sum(), 2)}</span>
        """,
        yaxis=dict(tickmode='linear', dtick=50),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        #plot_bgcolor='#1b2838',
        #paper_bgcolor='#1b2838'
    )

    fig.update_yaxes(gridcolor='#2a475e')

    return fig


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_parquet('parquets/76561198113335827_2022-09-12.parquet')

    full_price = df['price'] / (1 - df['discount_pct']/100)
    df['full_price'] = full_price

    df_noSQL = df[['name', 'price', 'full_price']].sort_values('full_price')
    df_noSQL = df_noSQL[df_noSQL.full_price != 0].reset_index()

    plotly_graph('Eric', df_noSQL).show()
