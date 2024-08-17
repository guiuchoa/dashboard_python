# Importe os pacotes necessários
from dash import Dash, html, dash_table
import pandas as pd
import os

# Verifique o diretório atual
print("Diretório atual:", os.getcwd())

# Defina o caminho para o arquivo CSV local
csv_file = 'vendas.csv'

# Verifique se o arquivo existe no diretório atual
if os.path.exists(csv_file):
    # Leia o arquivo CSV local
    df = pd.read_csv(csv_file, encoding='latin-1')
else:
    raise Exception(f'O arquivo {csv_file} não foi encontrado no diretório.')

# Inicialize o aplicativo Dash
app = Dash()

# Layout do aplicativo
app.layout = [
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
]

# Execute o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
