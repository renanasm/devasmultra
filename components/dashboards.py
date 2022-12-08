from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app
from dash import dash_table
from dash.dash_table.Format import Group

import pdb
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin=dict(l=25, r=25, t=25, b=0)


# =========  Layout  =========== #
layout = dbc.Col([
        dbc.Row([
            # Saldo
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Receita de Vendas"),
                                    html.H5("R$ -", id="p-receitavend-dashboards", style={}),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-university", style=card_icon), 
                                color="warning",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=4),

            # Receita
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Lucro Bruto"),
                                    html.H5("R$ -", id="p-receitaliq-dashboards"),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-smile-o", style=card_icon), 
                                color="success",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=4),

            # Despesa
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Lucro Ecônomico (EVA)"),
                        html.H5("R$ -", id="p-deducoes-dashboards"),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-meh-o", style=card_icon), 
                        color="danger",
                        style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                    )])
                ], width=4),
        ], style={"margin": "10px"}),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                        html.Legend("Filtrar lançamentos", className="card-title"),
                        html.Label("Categorias das receitas"),
                        html.Div(
                            dcc.Dropdown(
                            id="dropdown-receita",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True)                       
                        ),
                        
                        html.Label("Categorias das despesas", style={"margin-top": "10px"}),
                        dcc.Dropdown(
                            id="dropdown-despesa",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True
                        ),
                        html.Legend("Período de Análise: (Dia - Mês - Ano)", style={"margin-top": "10px"}),
                        dcc.DatePickerRange(
                            month_format='MMMM, YY',
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            start_date=date(2022, 1, 1),
                            end_date=datetime.today(),
                            with_portal=True,
                            updatemode='singledate',
                            id='date-picker-config',
                            style={'z-index': '100'})
                            ],

                style={"height": "100%", "padding": "20px"}), 
                ], width=4),

            dbc.Col(dbc.Card(dcc.Graph(id="graph1"), style={"padding": "10px"}), width=8),

            # Despesa

        ], style={"margin": "10px"}),

        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}), width=12),

        ], style={"margin": "10px"}),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}), width=6),
        ], style={"margin": "10px"}),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph5"), style={"padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph6"), style={"padding": "10px"}), width=6),
        ], style={"margin": "10px"}),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bar-graph1', style={"margin-right": "20px"}),
            ], width=12)], style={"margin": "10px"}),
        dbc.Row([
            html.Legend("Tabela de Receitas"),
            html.Div(id="tabela-receitas", className="dbc"),
        ])  
        ], style={"margin": "10px"})



# =========  Callbacks  =========== #
# Dropdown Receita html.Legend("Receita de Vendas"),
@app.callback([Output("dropdown-receita", "options"),
    Output("dropdown-receita", "value"),
    Output("p-receitavend-dashboards", "children")],
    Input("store-receitas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    df_ds = pd.DataFrame(data)
    dfs = [df_ds]
    df_final = pd.concat(dfs)
    df_final['Data'] = pd.to_datetime(df_final['Data'])
    mask = df_final[(df_final['Data'].dt.month >= 9) & (df_final['Data'].dt.month <= 11)]
    valor = mask['Valor'].sum()
    
    val = df.Categoria.unique().tolist()
    return [([{"label": x, "value": x} for x in df.Categoria.unique()]), val, f"R$ {valor:,.2f}"]

# Dropdown   html.Legend("Lucro Ecônomico (EVA)"),
@app.callback([Output("dropdown-despesa", "options"),
    Output("dropdown-despesa", "value"),
    Output("p-deducoes-dashboards", "children")],
    Input("store-despesas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data) 
    df_ds = pd.DataFrame(data)
    dfs = [df_ds]
    df_final = pd.concat(dfs)
    df_final['Data'] = pd.to_datetime(df_final['Data'])
    mask = df_final[(df_final['Data'].dt.month >= 9) & (df_final['Data'].dt.month <= 11)]
    valor = mask['ValorVenda'].sum()

    val = df.Categoria.unique().tolist()
    
    return [([{"label": x, "value": x} for x in df.Categoria.unique()]), val, f"R$ {valor:,.2f}"]

# VALOR - saldo   html.Legend("Lucro Bruto"),  - 26558.55 - 153042,612
@app.callback(
    Output("p-receitaliq-dashboards", "children"),
    [Input("store-despesas", "data"),
    Input("store-receitas", "data")])
def saldo_total(despesas, receitas):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)
    dfs = [df_receitas]
    df_final = pd.concat(dfs)
    df_final['Data'] = pd.to_datetime(df_final['Data'])
    mask = df_final[(df_final['Data'].dt.month >= 8) & (df_final['Data'].dt.month <= 10)]
    valor = mask['deducoes'].sum() 
    return f"R$ {valor:,.2f}"

    
# Gráfico 1
@app.callback(
    Output('graph1', 'figure'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("dropdown-despesa", "value"),
    Input("dropdown-receita", "value"),
    Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date'), 
    Input(ThemeChangerAIO.ids.radio("theme"), "value")])
def update_output(data_despesa, data_receita, despesa, receita, start_date, end_date, theme):
    df_ds = pd.DataFrame(data_despesa).sort_values(by='Data', ascending=True)
    df_rc = pd.DataFrame(data_receita).sort_values(by='Data', ascending=True)

    dfs = [df_ds, df_rc]
    for df in dfs:
        df['Acumulo'] = df['Valor'].cumsum()
        df["Data"] = pd.to_datetime(df["Data"])
        df["Mes"] = df["Data"].apply(lambda x: x.month)

    df_receitas_mes = df_rc.groupby("Mes")["Valor"].sum()
    df_despesas_mes = df_ds.groupby("Mes")["Valor"].sum()
    df_saldo_mes = df_receitas_mes - df_despesas_mes
    df_saldo_mes.to_frame()
    df_saldo_mes = df_saldo_mes.reset_index()
    df_saldo_mes['Acumulado'] = df_saldo_mes['Valor'].cumsum()
    df_saldo_mes['Mes'] = df['Mes'].apply(lambda x: calendar.month_abbr[x])

    df_ds = df_ds[df_ds['Categoria'].isin(despesa)]
    df_rc = df_rc[df_rc['Categoria'].isin(receita)]
    
    dfs = [df_ds, df_rc]
    df_final = pd.concat(dfs)
    
    mask = (df_final['Data'] > start_date) & (df_final['Data'] <= end_date) 
    df_final = df_final.loc[mask]

    df_final = df_final[df_final['Categoria'].isin(receita) | df_final['Categoria'].isin(despesa)]
    

    fig = go.Figure()
    
    # fig.add_trace(go.Scatter(name='Despesas', x=df_ds['Data'], y=df_ds['Acumulo'], fill='tonexty', mode='lines'))
    fig.add_trace(go.Scatter(name='Receitas', x=df_rc['Data'], y=df_rc['Acumulo'], fill='tonextx', mode='lines'))
    # fig.add_trace(go.Scatter(name='Saldo Mensal', x=df_saldo_mes['Mes'], y=df_saldo_mes['Acumulado'], mode='lines'))
    fig.update_layout(title={'text': "Desenvolvimento de vendas do mês de 01 Jan - 06 Dez"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# Gráfico 2


@app.callback(
    Output('graph2', 'figure'),
    [Input('store-receitas', 'data'),
    Input('store-despesas', 'data'),
    Input('dropdown-receita', 'value'),
    Input('dropdown-despesa', 'value'),
    Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date'), 
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]    
)
def graph2_show(data_receita, data_despesa, receita, despesa, start_date, end_date, theme):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)
    
    mask = (df_final['Data'] > start_date) & (df_final['Data'] <= end_date) 
    df_final = df_final.loc[mask]

    df_final = df_final[df_final['Categoria'].isin(receita) | df_final['Categoria'].isin(despesa)]
    
    
    
    fig = px.histogram(df_final, x=df_final['Data'], y="Valor", color='Output', barmode="group",text_auto='.2s')
    
    fig.update_layout(title={'text': "Gráfico para Análise"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    

    return fig
# Gráfico 3
@app.callback(
    Output('graph3', "figure"),
    [Input('store-receitas', 'data'),
    Input('dropdown-receita', 'value'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_receita(data_receita, receita, theme):
    df = pd.DataFrame(data_receita)
    df = df[df['Categoria'].isin(receita)]

    fig = px.pie(df, values=(df['Valor']), names=df.Categoria, hole=.2)
    fig.update_layout(title={'text': "Receita de vendas"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                  
    return fig    

# Gráfico 4
@app.callback(
    Output('graph4', "figure"),
    [Input('store-despesas', 'data'),
    Input('dropdown-receita', 'value'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_despesa(data_despesa, despesa, theme):
    df = pd.DataFrame(data_despesa)
    df = df[df['Categoria'].isin(despesa)]
    

    fig = px.pie(df, values=(df['Valor']), names=df.Categoria, hole=.2)
    fig.update_layout(title={'text': "Deduções "})

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig

# Gráfico 5          
@app.callback(
    Output('bar-graph1', 'figure'),
    [Input('store-receitas', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def bar_chart(data, theme):
    df = pd.DataFrame(data)   
    df_grouped = df.groupby("Categoria").sum()[["Valor"]].reset_index()
    
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Receitas Gerais ",text_auto='.2s')
    graph.update_layout(margin=graph_margin, template=template_from_url(theme))
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph
#Grafico 6












#tabela
@app.callback(
    Output('tabela-receitas', 'children'),
    Input('store-receitas', 'data')
)
def imprimir_tabela (data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date

    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'

    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'

    df = df.fillna('-')

    df.sort_values(by='Data', ascending=False)

    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",  
        selected_columns=[],        
        selected_rows=[],          
        page_action="native",      
        page_current=0,             
        page_size=10,                        
    ),

    return tabela