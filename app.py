from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime

# Carrega os dados
caminho_csv = r'C:\Users\guie3\OneDrive\Documentos\Python Scripts\Dashboards Python\vendas.csv'
df = pd.read_csv(caminho_csv, encoding='latin1')
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

# Inicializa o app com tema escuro
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Layout
app.layout = dbc.Container([
    html.H1("Dashboard de Vendas", className="text-center text-white mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Produto:", className="text-white"),
            dcc.Dropdown(
                id="filtro-produto",
                options=[{"label": "Todos os Produtos", "value": "Todos"}] +
                        [{"label": prod, "value": prod} for prod in sorted(df['produto'].unique())],
                value="Todos",
                style={'color': 'black'}
            )
        ], width=4),

        dbc.Col([
            html.Label("Operadora:", className="text-white"),
            dcc.Dropdown(
                id="filtro-operadora",
                options=[{"label": "Todas as Operadoras", "value": "Todas"}] +
                        [{"label": op, "value": op} for op in sorted(df['operadora'].unique())],
                value="Todas",
                style={'color': 'black'}
            )
        ], width=4),

        dbc.Col([
            html.Label("Período:", className="text-white"),
            dcc.DatePickerRange(
                id='filtro-data',
                start_date=df['data'].min().date(),
                end_date=df['data'].max().date(),
                display_format='DD/MM/YYYY',
                style={'color': 'black'}
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
    ], className="mb-2"),

    dcc.Download(id="download-tabela"),

    dash_table.DataTable(
        id='tabela-vendas',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'backgroundColor': '#343a40', 'color': 'white'},
        style_header={'backgroundColor': '#1f2c56', 'color': 'white', 'fontWeight': 'bold'}
    )
], fluid=True, style={"padding": "30px"})

# Callback principal
@app.callback(
    [
        Output("grafico-vendas-tempo", "figure"),
        Output("grafico-vendas-regiao", "figure"),
        Output("tabela-vendas", "data")
    ],
    [
        Input("filtro-produto", "value"),
        Input("filtro-operadora", "value"),
        Input("filtro-data", "start_date"),
        Input("filtro-data", "end_date")
    ]
)
def atualizar_dashboard(produto, operadora, data_inicio, data_fim):
    dff = df.copy()

    if produto != "Todos":
        dff = dff[dff['produto'] == produto]

    if operadora != "Todas":
        dff = dff[dff['operadora'] == operadora]

    dff = dff[(dff['data'] >= pd.to_datetime(data_inicio)) & (dff['data'] <= pd.to_datetime(data_fim))]

    # Gráfico por tempo
    fig_tempo = px.line(
        dff.groupby('data')['total'].sum().reset_index(),
        x='data',
        y='total',
        title="Total de Vendas ao Longo do Tempo"
    )

    # Gráfico por região
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
        yaxis_tickformat=',.2f',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    return fig_tempo, fig_regiao, dff.to_dict("records")

# Callback para exportação
@app.callback(
    Output("download-tabela", "data"),
    Input("btn-exportar", "n_clicks"),
    [
        State("filtro-produto", "value"),
        State("filtro-operadora", "value"),
        State("filtro-data", "start_date"),
        State("filtro-data", "end_date")
    ],
    prevent_initial_call=True
)
def exportar_excel(n_clicks, produto, operadora, data_inicio, data_fim):
    dff = df.copy()

    if produto != "Todos":
        dff = dff[dff['produto'] == produto]

    if operadora != "Todas":
        dff = dff[dff['operadora'] == operadora]

    dff = dff[(dff['data'] >= pd.to_datetime(data_inicio)) & (dff['data'] <= pd.to_datetime(data_fim))]

    # Cria o Excel em memória
    return dcc.send_data_frame(dff.to_excel, filename="vendas_filtradas.xlsx", index=False)

# Executa o app
if __name__ == "__main__":
    app.run(debug=True)
