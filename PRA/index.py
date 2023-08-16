

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine, text

# Conexión a la base de datos
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='empresas_pra'
)

# Crea el motor de SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:@localhost/empresas_pra')

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='risk-rating-graph'),
        dcc.Dropdown(
            id='sector-dropdown',  # ID del Dropdown
            options=[
                {'label': 'Sector 1', 'value': 'sector1'},  
                # Agrega más opciones según tus necesidades
            ],
            value='sector1'  # Valor inicial
        ),
    dcc.Graph(id='risk-rating-graph'),
])

@app.callback(
    Output('risk-rating-graph', 'figure'),
    [Input('sector-dropdown', 'value')] 
    # Agrega más inputs y outputs para tus callbacks aquí
)
def update_graph(selected_sector):
    # Crea una conexión para ejecutar la consulta
    connection = engine.connect()

    # Crea un objeto de texto SQL ejecutable
    query = text("SELECT nit, nombre_empresa, tipo_de_sector, calificador_de_riesgos, tipo_de_riesgos, ponderacion_de_calificacion FROM tabla_datos")

    # Ejecuta la consulta y obtén los resultados
    results = connection.execute(query).fetchall()

    # Cierra la conexión
    connection.close()

    # Procesa tus datos aquí y crea la visualización
    df = pd.DataFrame(results, columns=['nit', 'nombre_empresa', 'tipo_de_sector', 'calificador_de_riesgos', 'tipo_de_riesgos', 'ponderacion_de_calificacion'])

    fig = px.scatter(df, x='tipo_de_sector', y='calificador_de_riesgos', color='tipo_de_riesgos', size='ponderacion_de_calificacion',
                     labels={'tipo_de_sector': 'Tipo de Sector', 'calificador_de_riesgos': 'Calificador de Riesgos'},
                     title='Calificación de Riesgos por Tipo de Sector')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
