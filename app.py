from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Carrega os dados
caminho_csv = r'C:\Users\guie3\OneDrive\Documentos\Python Scripts\Dashboards Python\vendas_eletronicos.csv'
df = pd.read_csv(caminho_csv, encoding='latin1')
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

# Inicializa o app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Layout
app.layout = dbc.Container([
    html.H1("Vendas Bit Shop", className="text-center text-white mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Vendas", className="card-title"),
                html.H2(id="indicador-total", className="card-text")
            ])
        ], color="primary", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Qtd. de Registros", className="card-title"),
                html.H2(id="indicador-registros", className="card-text")
            ])
        ], color="info", inverse=True), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Média por Venda", className="card-title"),
                html.H2(id="indicador-media", className="card-text")
            ])
        ], color="secondary", inverse=True), width=4)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Produto:", className="text-white"),
            dcc.Dropdown(
                id="filtro-produto",
                options=[{"label": prod, "value": prod} for prod in sorted(df['produto'].unique())],
                multi=True,
                value=[],
                placeholder="Todos os produtos",
                style={'color': 'black'}
            )
        ], width=4),

        dbc.Col([
            html.Label("Vendedor:", className="text-white"),
            dcc.Dropdown(
                id="filtro-vendedor",
                options=[{"label": op, "value": op} for op in sorted(df['vendedor'].unique())],
                multi=True,
                value=[],
                placeholder="Todos os vendedores",
                style={'color': 'black'}
            )
        ], width=4),

        dbc.Col([
            html.Label("Período:", className="text-white"),
            dcc.DatePickerRange(
                id='filtro-data',
                start_date=df['data'].min().date(),
                end_date=df['data'].max().date(),
                display_format='DD/MM/YYYY'
            )
        ], width=4)
    ], className="mb-4"),

    dcc.Graph(id="grafico-vendas-regiao"),
    dcc.Graph(id="grafico-vendas-tempo"),

    dbc.Row([
        dbc.Col(html.H3("Tabela de Vendas", className="text-white"), width=9),
        dbc.Col(
            html.Button("Exportar para Excel", id="btn-exportar", className="btn btn-success"),
            width=3, style={"textAlign": "right"}
        )
    ]),

    dcc.Download(id="download-tabela"),

    dash_table.DataTable(
        id='tabela-vendas',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'backgroundColor': '#343a40', 'color': 'white'},
        style_header={'backgroundColor': '#1f2c56', 'color': 'white', 'fontWeight': 'bold'},
        style_data={'whiteSpace': 'normal'},
        style_data_conditional=[]
    )
], fluid=True, style={"padding": "30px"})

# Callback principal
@app.callback(
    [
        Output("grafico-vendas-tempo", "figure"),
        Output("grafico-vendas-regiao", "figure"),
        Output("tabela-vendas", "data"),
        Output("indicador-total", "children"),
        Output("indicador-registros", "children"),
        Output("indicador-media", "children"),
    ],
    [
        Input("filtro-produto", "value"),
        Input("filtro-vendedor", "value"),
        Input("filtro-data", "start_date"),
        Input("filtro-data", "end_date")
    ]
)
def atualizar_dashboard(produtos, vendedores, data_inicio, data_fim):
    dff = df.copy()

    if produtos:
        dff = dff[dff['produto'].isin(produtos)]
    if vendedores:
        dff = dff[dff['vendedor'].isin(vendedores)]

    dff = dff[(dff['data'] >= pd.to_datetime(data_inicio)) & (dff['data'] <= pd.to_datetime(data_fim))]

    # Gráficos
    fig_tempo = px.line(
        dff.groupby('data')['total'].sum().reset_index(),
        x='data',
        y='total',
        title="Total de Vendas ao Longo do Tempo"
    )

    df_regiao = dff.groupby('região')['total'].sum().reset_index()
    df_regiao['total_formatado'] = df_regiao['total'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

    fig_regiao = px.bar(
        df_regiao,
        x='região',
        y='total',
        text='total_formatado',
        title="Total de Vendas por Região"
    )
    fig_regiao.update_traces(textposition='inside')
    fig_regiao.update_layout(
        yaxis_tickprefix='R$ ',
        yaxis_tickformat=',.2f'
    )

    # Indicadores
    total = dff['total'].sum()
    media = dff['total'].mean()
    registros = len(dff)

    total_fmt = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    media_fmt = f"R$ {media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    registros_fmt = f"{registros:,}".replace(",", ".")

    return fig_tempo, fig_regiao, dff.to_dict("records"), total_fmt, registros_fmt, media_fmt

# Exportação
@app.callback(
    Output("download-tabela", "data"),
    Input("btn-exportar", "n_clicks"),
    [
        State("filtro-produto", "value"),
        State("filtro-vendedor", "value"),
        State("filtro-data", "start_date"),
        State("filtro-data", "end_date")
    ],
    prevent_initial_call=True
)
def exportar_excel(n_clicks, produtos, vendedores, data_inicio, data_fim):
    dff = df.copy()

    if produtos:
        dff = dff[dff['produto'].isin(produtos)]
    if vendedores:
        dff = dff[dff['vendedor'].isin(vendedores)]

    dff = dff[(dff['data'] >= pd.to_datetime(data_inicio)) & (dff['data'] <= pd.to_datetime(data_fim))]

    return dcc.send_data_frame(dff.to_excel, filename="vendas_filtradas.xlsx", index=False)

# Roda o servidor
if __name__ == '__main__':
    app.run(debug=True)
