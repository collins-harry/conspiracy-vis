import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np


app_colors = {
    'background':'#0C0F0A',
    'headtext':'#CECECE',
    'text':'#FFFFFF',
    'coolpink':'#FF206E'
}


def importData():
    """returns csv_eu_first_request and csv_origin"""
    csv_eu_first_request = pd.read_csv('asylumseekers_EU_country_first_request.csv')
    csv_origin = pd.read_csv('asylumseekers_EU_by_origin.csv')

    def make_all_strings(df):
        for col in df.columns:
            df[col] = df[col].astype(str)
        return df

    csv_eu_first_request = make_all_strings(csv_eu_first_request)
    csv_origin = make_all_strings(csv_origin)

    return csv_eu_first_request, csv_origin
csv_eu_first_request, csv_origin = importData()

app = dash.Dash('eu-migrants')

sliderLabels = ['Who are they',
                'Where have they been (2014)',
                'Where have they been (2015)',
                'Where are they expected next']


app.layout = html.Div([

    html.Div([
        html.H2('The Dark EU: who are they, and where are they hiding?',
                style={#'float': 'left',
                       'color': app_colors['headtext'],
                       'padding-left':10,
                       'margin-top':0,
                       }),#className='container-fluid',
        ]),


    html.Div(html.P([
            'In recent years there has been a stark increase in the size of the cabal that is the \'DARK EU\'. '
            'They are entering the EU in the form of refugees looking to take our jobs, our women and to pee in the pool when they go swimming. '
            'In this informative web application we show you the nationalities that make up this nefarious force, '
            'the countries they have entered into so far and finally; we\'ll show you where we think they\'ll be entering in the future. '
            'We will leave you to draw your own conclusions. \"Hide your kids and hide your wives\" - Tim Roelofs'
            ], style={'color':app_colors['text'],
                      'max-width':700,
                      'padding-left':10,})),


    html.Div([ #wrapper for centering slider
        dcc.Slider(
            id='slider-updatemode',
            value=1,
            min=1,
            max=4,
            marks={1: {'label': sliderLabels[0], 'style': {'display': 'inline-block', 'color': app_colors['text']}},
                   2: {'label': sliderLabels[1], 'style': {'display': 'inline-block', 'color': app_colors['text']}},
                   3: {'label': sliderLabels[2], 'style': {'display': 'inline-block', 'color': app_colors['text']}},
                   4: {'label': sliderLabels[3], 'style': {'display': 'inline-block', 'color': app_colors['text']}},
                   },
            updatemode='mouseup',
            included=False,


            ),

        ], style={'text-align':'center',
                  'padding-left':50,
                  'padding-right':83,
                  'margin-bottom':50,
                  #'display':'block',
                  #'border':10,
                  #'height':'10%'
                    }
        ),




    # dcc.Dropdown(id='eu-migrant-data',
    #              options=[{'label': 'Asylumseekers per 1000 (2015)',
    #                        'value': 'Asylumseekers per 1000 (2015)'},
    #                       {'label': 'Asylumseekers per 1000 (2014)',
    #                        'value': 'Asylumseekers per 1000 (2014)'},
    #                       {'label': 'percentage increase',
    #                        'value': 'percentage increase'},
    #                       ],
    #              multi=True,
    #              value='Asylumseekers per 1000 (2015)',),
    #html.Div(children=html.Div(id='text', style={'height':'100%'})),

    html.Div(children=html.Div(id='graphs', style={'height':'100%'}), className='row'),

    #dcc.Interval(
    #    id='graph-update',
    #    interval=1000
    #    ),

    html.Div([html.P([
        '*The final graph\'s data is calculated from the the percentage increase of refugees from 2014 to 2015.'
    ], style={'color': app_colors['text'],
              'max-width': 700,
              'padding-left': 10,
              'fontSize':10,})
    ], style={'text-align':'center',
              'width':'100%'
              }),

    ], className='container', style = {'width': '100%',
                                       #'height':'100%',
                                       #'position':'fixed',
                                       #'bottom':0,
                                       #'top':0,

                                       #'margin-left':10,
                                       #'margin-right':10,
                                       'max-width':840,
                                       'backgroundColor': app_colors['background']}
    )








@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('slider-updatemode', 'value')],
    #events=[dash.dependencies.Event('graph-update', 'interval')]
)
def update_graph(data_names):
    graphs = []
    print('------------------------------------------------------------------------')
    print('------------------------------------------------------------------------')
    print(data_names)

    data_names = [data_names]
    #if len(data_names) > 2:
    #    class_choice = 'col s12 m6 l4'
    #elif len(data_names) == 2:
    #    class_choice = 'col s12 m6 l6'
    #else:
    #    class_choice = 'col s12'

    class_choice = 'col s12'

    for data_name in data_names:

        if data_name==1:
            data_name='normed%*init/cap'
            graphs = barchart(data_name, class_choice)
        elif data_name==2:
            data_name ='Asylumseekers per 1000 (2014)'
            graphs = choropleth(data_name, class_choice, title = 'Asylumseekers per 1000 people (2014)')
        elif data_name==3:
            data_name='Asylumseekers per 1000 (2015)'
            graphs = choropleth(data_name, class_choice, title = 'Asylumseekers per 1000 people (2015)')
        elif data_name==4:
            data_name='percentage increase'
            graphs = choropleth(data_name, class_choice, title= 'Extrapolated results of impending invasion*',bar=True)

        return graphs


def barchart(data_name, class_choice, title='1'):
    graphs = []

    data = go.Bar(
        name = '{}'.format(data_name),
        y = csv_origin['GEO/TIME'],
        x = csv_origin['2014+2015'],
        orientation = 'h',
        marker=dict(
            color='#6B0202'
        ),

    )


    layout = go.Layout(
        title= 'Asylum Seekers by countries from 2014-2015',
        titlefont={'color':app_colors['headtext']},
        height=700,
        paper_bgcolor=app_colors['background'],
        plot_bgcolor=app_colors['background'],
        margin=dict(
            autoexpand=True
        ),
        xaxis=dict(
            rangemode='normal',
            range={0:-0.5, 1:30.5},
            tickfont={'color':app_colors['text']},
            ),
        yaxis=dict(
            tickfont={'color':app_colors['headtext']}
        )

    )

    graphs.append(html.Div(dcc.Graph(
        id='graph',
        animate=False,
        figure={'data': [data], 'layout': layout}
    ), className=class_choice)
    )

    return graphs


def choropleth(data_name, class_choice, title='1', bar=False):
    graphs=[]

    data = go.Choropleth(
        name='{}'.format(data_name),
        hoverinfo='{}'.format(data_name),
        text=csv_eu_first_request['GEO/TIME'] + '<br>' + \
             'Population in 2015 = ' + round(
            csv_eu_first_request['pop_2015'].str.replace(",", "").astype(float) / 1000000, 2).astype(
            str) + ' million' + '<br>' + \
             'Asylumseekers per 1000 (2014) = ' + np.round(
            csv_eu_first_request['Asylumseekers per 1000 (2014)'].astype(float), 2).astype(str) + '<br>' + \
             'Asylumseekers per 1000 (2015) = ' + np.round(
            csv_eu_first_request['Asylumseekers per 1000 (2015)'].astype(float), 2).astype(str),
        z=csv_eu_first_request[data_name],
        locations=csv_eu_first_request['codes'],
        zmax=(100 if bar else 17.9731),
        zmin=(0 if bar else 0.0497),
        locationmode='Europe',
        geo='geo',
        showlegend=True,
        colorbar=dict(tickfont={'color':app_colors['text'],
                                },
                      titlefont={'color':app_colors['headtext']},
                      title=('Percentage, %' if bar else 'per 1000 population')),
    )

    layout = go.Layout(
        title=title,
        titlefont=dict(color=app_colors['headtext']),

        geo=dict(
            scope='europe',
            resolution=50,
            center=dict(lon=15.119999,  # higher means to the left
                        lat=50.79038540560208),  # higher mean down
            projection=dict(type='eckert4',
                            scale='1.33'),
            showcountries=False,
            bgcolor=app_colors['background']
        ),
        paper_bgcolor=app_colors['background']
    )
    # margin={'l':50, 'r':1,'t':45,'b':1}

    graphs.append(html.Div(dcc.Graph(
        id='graph',
        animate=False,
        figure={'data': [data], 'layout': layout}
    ), className=class_choice)
    )

    return graphs



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


server=app.server #flask app
if __name__ == '__main__':
    app.run_server(debug=True)


















