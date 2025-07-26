# Bit Shop - Dashboard de Vendas

Dashboard interativo construído com [Dash](https://dash.plotly.com/) e [Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) para visualização e análise de vendas de uma loja de eletrônicos fictícia.

---

## 📊 Funcionalidades

* **Indicadores**: Total de vendas, quantidade de registros e média por venda.
* **Filtros interativos**:

  * Por produto
  * Por vendedor
  * Por período (com seletor de datas)
* **Gráficos dinâmicos**:

  * Linha do tempo com total de vendas
  * Barras por região com valores formatados
* **Tabela de dados**: Estilizada, paginada e exportável para Excel.

---

## 🛠️ Tecnologias Utilizadas

* Python 3
* Dash
* Plotly Express
* Dash Bootstrap Components
* Pandas

---

## ▶️ Como Rodar

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/bitshop-dashboard.git
   cd bitshop-dashboard
   ```

2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Coloque o arquivo `vendas_eletronicos.csv` na pasta raiz do projeto.

5. (Opcional) Adicione uma imagem `logo.png` na pasta `assets/`.

6. Rode a aplicação:

   ```bash
   python app.py
   ```

---

## 📁 Estrutura do Projeto

```
├── app.py
├── vendas_eletronicos.csv
├── assets
│   ├── logo.png
│   └── preview.png
└── README.md
```

---

## 📃 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar e modificar.
