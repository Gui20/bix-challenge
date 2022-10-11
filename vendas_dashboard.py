import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server
# =====================================================================
#  Extract Data
engine_solution = create_engine('postgresql://guilherme:|?7LXmg+FWL&,'
                                '2(@bix-solution.c3ksuxpujoxa.sa-east-1.rds.amazonaws.com/postgres')

# =====================================================================
# Line Chart

df_line_chart = pd.read_sql(""" SELECT * FROM dashboard.line_chart """,
                            con=engine_solution)

line_chart = go.Figure(
    data=go.Bar(
        x=df_line_chart['ano'].tolist(),
        y=df_line_chart['total'].tolist(),
        textfont=dict(
            family="Arial",
            size=18,
            color="white"
        ),
        marker=dict(
            color='rgba(0, 85, 255, 1.0)',
            line=dict(
                color='rgba(50, 171, 96, 0.0)',
                width=1),

        ),

    )
)

line_chart.update_layout(
    title_text='<b> Vendas Anuais </b>',
    title_font_color='white',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor="#242424",
    margin=dict(l=10, r=0, b=10, t=40),
    autosize=True,
    xaxis_tickangle=-45

)
line_chart.update_yaxes(title_text='Vendas R$', color="white")
line_chart.update_xaxes(title_text='Ano', color="white")
# =====================================================================
# Pie Chart

df_total_categoria = pd.read_sql(""" SELECT * FROM dashboard.pie_chart """,
                                 con=engine_solution)

pie = go.Figure(data=[go.Pie(labels=df_total_categoria['categoria'], values=df_total_categoria['total'], hole=.4)])

pie.update_layout(
    title_text='<b> Vendas por Categorias </b>',
    title_font_color='white',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor="#242424",
    margin=dict(l=0, r=0, b=0, t=60),
    autosize=True,
    xaxis_tickangle=-45

)
# =====================================================================
# Table
df_total_funcionario = pd.read_sql(""" SELECT * FROM dashboard.resultado_individual_funcionarios """,
                                   con=engine_solution)

fig_table = go.Figure(data=[go.Table(
    header=dict(values=["Funcionario", "Total [R$]"],
                fill_color="#0066FF",
                align='left'),
    cells=dict(values=[df_total_funcionario['funcionario'], df_total_funcionario['total']],
               fill_color='lavender',
               align='left'))
])
fig_table.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor="#242424",
    margin=dict(l=0, r=0, b=0, t=0),
    autosize=True
)
# =====================================================================
df_faturamento_total = pd.read_sql(""" SELECT * FROM public.vendas_solution ORDER BY data_venda""",
                                   con=engine_solution)

# =====================================================================

# Layout
app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([
                html.Img(id="logo", src=app.get_asset_url("logo.png"), height=100, className='img'),
            ]),
            dbc.Col([
                html.Div([
                    html.H1(children="Vendas Dashboard"),
                ], className="fonte"),
            ])

        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("Total:  ", className="card-text"),
                                html.H3("R$ {:.2f}M".format(df_faturamento_total['venda'].sum() / 1000000),
                                        style={"color": "#adfc92"},
                                        id="total_money"),
                                html.Span("Em: {}".format(datetime.today().strftime("%Y/%m/%d %H:%M:%S")),
                                          className="card-text", id='span_money'),
                                html.H6(id="em vendas"),
                            ])
                        ], color="light", outline=True, style={"margin-top": "10px",
                                                               "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px "
                                                                             "20px 0 rgba(0, 0, 0, 0.19)",
                                                               "color": "#FFFFFF"})

                    ], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("QTD Vendas: ", className="card-text"),
                                html.H3("{}".format(len(df_faturamento_total['venda'])), style={"color": "#adfc92"},
                                        id="total_qtd"),
                                html.Span("Em: {}".format(datetime.today().strftime("%Y/%m/%d %H:%M:%S")),
                                          className="card-text", id='span_qtd'),
                                html.H6(id="kore"),
                            ])
                        ], color="light", outline=True, style={"margin-top": "10px",
                                                               "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px "
                                                                             "20px 0 rgba(0, 0, 0, 0.19)",
                                                               "color": "#FFFFFF"})

                    ], md=6)
                ]),
                html.Div([
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="line", figure=line_chart,
                                            style={'height': '50vh', 'margin-right': '0px'})],
                    ),
                ], style={
                    "background-color": "#1E1E1E",
                    "margin-top": "15px",
                    "margin-left": "0px",
                    "padding": "25px",
                    "height": "545px",
                })
            ], md=6),
            dbc.Col([
                dbc.Row([
                    html.Div([dcc.Loading(
                        id="loading-3",
                        type="default",
                        children=[dcc.Graph(id="table", figure=fig_table,
                                            style={'height': '21vh', 'margin-right': '0px'})],
                    ),
                        html.Div([
                            dcc.Loading(
                                id="loading-2",
                                type="default",
                                children=[dcc.Graph(id="pie", figure=pie,
                                                    style={'height': '35vh', 'margin-right': '0px'})],
                            ),
                        ], style={
                            "margin-top": "40px"
                        })

                    ], style={
                        "background-color": "#1E1E1E",
                        "margin-top": "15px",
                        "margin-left": "0px",
                        "padding": "25px",
                        "height": "700px",

                    }),

                ]
                ),
                dbc.Row([
                    dcc.Interval(
                        id='interval-component',
                        interval=60 * 1000,  # in milliseconds
                        n_intervals=0
                    ),
                ]
                )

            ], md=6),

        ])]
)


# =====================================================================
# Interatividade
@app.callback(
    Output('line', 'figure'),
    Output('pie', 'figure'),
    Output('table', 'figure'),
    Output('total_money', 'children'),
    Output('total_qtd', 'children'),
    Output('span_money', 'children'),
    Output('span_qtd', 'children'),
    [Input('interval-component', "n_intervals")]
)
def stream(n):
    # Tabela

    df_total_funcionario = pd.read_sql(""" SELECT * FROM dashboard.resultado_individual_funcionarios """,
                                       con=engine_solution)
    fig_table = go.Figure(data=[go.Table(
        header=dict(values=["Funcionario", "Total [R$]"],
                    fill_color="#0066FF",
                    align='left'),
        cells=dict(values=[df_total_funcionario['funcionario'], df_total_funcionario['total']],
                   fill_color='lavender',
                   align='left'))
    ])
    fig_table.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor="#242424",
        margin=dict(l=0, r=0, b=0, t=0),
        autosize=True
    )
    # Pie
    df_total_categoria = pd.read_sql(""" SELECT * FROM dashboard.pie_chart """,
                                     con=engine_solution)
    pie = go.Figure(data=[go.Pie(labels=df_total_categoria['categoria'], values=df_total_categoria['total'], hole=.4)])

    pie.update_layout(
        title_text='<b> Vendas por Categorias </b>',
        title_font_color='white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor="#242424",
        margin=dict(l=0, r=0, b=0, t=60),
        autosize=True,
        xaxis_tickangle=-45

    )
    # Line
    df_line_chart = pd.read_sql(""" SELECT * FROM dashboard.line_chart """,
                                con=engine_solution)

    line_chart = go.Figure(
        data=go.Bar(
            x=df_line_chart['ano'].tolist(),
            y=df_line_chart['total'].tolist(),
            textfont=dict(
                family="Arial",
                size=18,
                color="white"
            ),
            marker=dict(
                color='rgba(0, 85, 255, 1.0)',
                line=dict(
                    color='rgba(50, 171, 96, 0.0)',
                    width=1),

            ),

        )
    )

    line_chart.update_layout(
        title_text='<b> Vendas Anuais </b>',
        title_font_color='white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor="#242424",
        margin=dict(l=10, r=0, b=10, t=40),
        autosize=True,
        xaxis_tickangle=-45

    )
    line_chart.update_yaxes(title_text='Vendas R$', color="white")
    line_chart.update_xaxes(title_text='Ano', color="white")
    # Valores
    df_faturamento_total = pd.read_sql(""" SELECT * FROM public.vendas_solution ORDER BY data_venda""",
                                       con=engine_solution)

    return line_chart, pie, fig_table, "R$ {:.2f}M".format(df_faturamento_total['venda'].sum() / 1000000), "{}".format(
        len(df_faturamento_total['venda'])), datetime.today().strftime("%Y/%m/%d %H:%M:%S"), \
           datetime.today().strftime("%Y/%m/%d %H:%M:%S")


# if __name__ == "__main__":
    # app.run_server(debug=True, port=8052)
