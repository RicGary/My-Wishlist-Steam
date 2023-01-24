from dash import Dash, html, dcc, Input, Output
from plots.graph import plotly_graph
from lxml import html as html_lxlml
from flask import Flask
import pandas as pd
import webbrowser
import requests
import json


app = Dash(__name__)
server = app.server


def pricingRight(price):
    price = str(price)
    start = price[0:-2]
    end = price[-2:]
    return float(start + '.' + end)


# 76561198113335827
# callback vai aqui
@app.callback(
    Output(component_id='graph-output', component_property='children'),
    Input(component_id='userSteamID', component_property='value')
)
def programInit(userID):
    userID = str(userID)

    # if digit
    if userID.isdigit():
        profile_type = 'profiles'
    else:
        profile_type = 'id'

    # user -> if wrong site -> Error
    urlUser = f'https://steamcommunity.com/{profile_type}/{userID}/'
    responseUser = requests.get(urlUser)
    tree = html_lxlml.fromstring(responseUser.content)
    userName = tree.xpath('//title/text()')[0].split(':: ')[-1]

    # wishlist
    urlWishlist = f'https://store.steampowered.com/wishlist/{profile_type}/{userID}/wishlistdata/?p=0'
    responseWishlist = requests.get(urlWishlist).content
    wishDict = json.loads(responseWishlist)

    tempList = []

    try:

        for keys_id in wishDict.keys():
            if wishDict[keys_id]['subs']:
                subs = wishDict[keys_id]['subs'][0]

                tempList.append(
                    [
                        wishDict[keys_id]['name'],
                        pricingRight(subs['price']),
                        pricingRight(subs['price']) / (1 - (subs['discount_pct'] / 100))
                    ]

                )

        df = pd.DataFrame(tempList, columns=['name', 'price', 'full_price'])

        df_noSQL = df[['name', 'price', 'full_price']].sort_values('full_price')
        df_noSQL = df_noSQL[df_noSQL.full_price != 0].reset_index()

        steamGraph = dcc.Graph(
            id='graphSteam',
            figure=plotly_graph(userName, df_noSQL),
            className='mainGraph',
            config={'displayModeBar': False,
                    'modeBarButtonsToRemove': ['Discount', 'Actual Price']}
        )

        return steamGraph

    except TypeError:

        instructions = html.Div(children=
                                [html.H2('Instructions', className='instructionTitle'),
                                 html.H3('1° - Go to your steam profile URL.'),
                                 html.H3('2° - Copy your id or your profile from the url.'),
                                 html.H3('Example:', className='example_id'),
                                 html.H3(['https://steamcommunity.com/profiles/',
                                          html.Span('123456789', className='span_ex'), '/'],
                                         className='url_ex'), html.H3('or', className='url_ex'),
                                 html.H3(['https://steamcommunity.com/id/', html.Span('yourName', className='span_ex'),
                                          '/'],
                                         className='url_ex'),
                                 html.H3('3° - Paste in the superior box.', id='final_instruction')
                                 ], className='divInstructions')

        return instructions


app.layout = html.Div(className='mainDiv',
                          children=[
                              html.Div(className='topBar',
                                       children=[
                                           html.Div(className='steamTitleDiv', children=[
                                               html.Img(className='steamLogo',
                                                        src='assets/images/Steam_Logo.png',
                                                        alt='image')
                                               , html.H1('STEAM', className='steamTitle'),
                                               html.H1('.WISHLIST', className='wishlistTitle')]),
                                           dcc.Input(id='userSteamID', className='userInputError'),
                                           html.Div(className='aboutMeDiv', children=[
                                               html.A('CONTACT ME', className='link', href='https://ericnaiber.com',
                                                      target='_blank')]),
                                       ], ),
                              html.Div(id='graph-output', className='outputContent'),
                          ])

if __name__ == '__main__':
    # webbrowser.open('http://127.0.0.1:8050', new=0)
    # app.run_server(host="0.0.0.0", port=8080, debug=True)
    app.run()