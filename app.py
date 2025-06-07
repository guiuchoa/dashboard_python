from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Carregamento dos dados
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
            html.Label("Selecione o Produto:", className="text-white"),
            dcc.Dropdown(
                options=[{"label": prod, "value": prod} for prod in sorted(df['produto'].unique())],
                value=df['produto'].unique()[0],
                id="filtro-produto"
            )
        ], width=6)
    ], className="mb-4 justify-content-center"),

    dcc.Graph(id="grafico-vendas-tempo"),
    dcc.Graph(id="grafico-vendas-regiao"),

    html.H3("Tabela de Vendas", className="text-white mt-4"),
    dash_table.DataTable(
        id='tabela-vendas',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'backgroundColor': '#343a40',
            'color': 'white'
        },
        style_header={
            'backgroundColor': '#1f2c56',
            'color': 'white',
            'fontWeight': 'bold'
        }
    )
], fluid=True, style={"padding": "30px"})

# Callback
@app.callback(
    [
        Output("grafico-vendas-tempo", "figure"),
        Output("grafico-vendas-regiao", "figure"),
        Output("tabela-vendas", "data")
    ],
    Input("filtro-produto", "value")
)
def atualizar_dashboard(produto):
    dff = df[df['produto'] == produto]

    fig_tempo = px.line(dff.groupby('data')['total'].sum().reset_index(),
                        x='data', y='total',
                        title=f"Total de Vendas ao Longo do Tempo ({produto})")

    fig_regiao = px.bar(dff.groupby('região')['total'].sum().reset_index(),
                        x='região', y='total',
                        title=f"Total de Vendas por Região ({produto})")

    return fig_tempo, fig_regiao, dff.to_dict("records")

# Executar
if __name__ == '__main__':
    app.run(debug=True)
