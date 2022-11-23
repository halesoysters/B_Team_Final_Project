import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
from pathlib import Path
from whitenoise import WhiteNoise
import os
#from urllib.request import urlopen
#import json
#with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    #counties = json.load(response)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root=os.path.join(os.path.dirname(__file__), "Assets"), prefix="Assets/",)

file = Path('data/health_outcomes_df.csv')    
data = pd.read_csv(file)
county_df = data
df = county_df[["CountyFIPS", "CANCER"]]
df["CountyFIPS"] = df["CountyFIPS"].apply(str)

#Import data for mapping
locationfile = Path('data/mapping_df.csv')  
mapping_data = pd.read_csv(locationfile)
mapping_df = county_df.merge(mapping_data, how="inner", on="CountyFIPS")

#import data for interactiuve viz of health risks and cancer rates
cancer_hr_df_file = Path('data/cancer_hr_df.csv')
cancer_hr_df = pd.read_csv(cancer_hr_df_file)

#Import data for boxplots
health_status_file = Path('data/health_status_df.csv')  
status_data = pd.read_csv(health_status_file)
health_outcomes_file = Path('data/health_outcomes_df.csv')  
outcomes_data = pd.read_csv(health_outcomes_file)
health_risk_behaviors_file = Path('data/health_risk_behaviors_df.csv')  
risk_data = pd.read_csv(health_risk_behaviors_file)
prevention_file = Path('data/prevention_df.csv')  
prevention_data = pd.read_csv(prevention_file)


#actual_vs_predicted ML viz
accuracy_df_file = Path('data/accuracy_df.csv')
accuracy_df = pd.read_csv(accuracy_df_file)

#Feature importances
feature_df_file = Path('data/feature_df.csv')
feature_df = pd.read_csv(feature_df_file)

# Image paths
image_path = 'assets/correlation_matrix.png'
accuracy_path = 'assets/Accuracy.png'
actual_v_predicted_path = 'assets/actual_vs_predicted.png'
graph_path = 'assets/Graph.png'

#import data for zip
zip_file = Path('data/Zip_County_FIPS.csv')  
zip_data = pd.read_csv(zip_file)


app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        html.H2("US Health", className="display-4"),
        html.Hr(),
        html.P(
            "Counties 2021", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Dashboard", href="/page-1", active="exact"),
                dbc.NavLink("Analysis", href="/page-2", active="exact"),
                dbc.NavLink("Machine Learning", href="/page-3", active="exact"),
                dbc.NavLink("References", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


#Callback for zip feature
@app.callback(
    Output('zip-output', 'figure'),
    Input('zip-input', 'value'))

# Function for zip feature
def make_bargraph(inputvalue):
    a = zip_data.query(f'ZIP == {inputvalue}')["STCOUNTYFP"].values[0]
    status_data_1 = status_data.rename(columns={"MHLTH": "Mental Health Rating",
                                    "PHLTH": "Physical Health Rating",
                                    "GHLTH": "Good Health Rating"})
    fig1 = px.bar(status_data_1[status_data_1.CountyFIPS == a], x=["Mental Health Rating", "Physical Health Rating", 
                                                            "Good Health Rating"], barmode="group", orientation="h",
                                                            color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_layout(transition_duration=500, yaxis_visible=False, yaxis_showticklabels=False)
    fig1.update_xaxes(title='Average of Rating for County', visible=True, showticklabels=True)
    return fig1



# Figure variables
fig2 = px.scatter_mapbox(mapping_df, lat="Lat", lon="Lon", text = 'CountyName', zoom = 2, size = 'total_population', 
            color = 'CANCER', color_continuous_scale=px.colors.sequential.Viridis,
            mapbox_style='open-street-map')
fig3 = px.box(status_data, y=['MHLTH', 'PHLTH', 'GHLTH'] )
fig4 = px.box(outcomes_data, y=['ARTHRITIS', 'CASTHMA', 'BPHIGH', 'CANCER', 'HIGHCHOL', 'KIDNEY', 'COPD', 'CHD', 'DEPRESSION', 'DIABETES', 'OBESITY', 'TEETHLOST', 'STROKE'] )
fig5 = px.box(prevention_data, y=['ACCESS', 'CHECKUP', 'DENTAL', 'BPMED', 'CHOLSCREEN', 'MAMMOUSE', 'CERVICAL', 'COLON_SCREEN', 'COREM', 'COREW'] )
fig6 = px.box(risk_data, y=['BINGE', 'CSMOKING', 'LPA', 'SLEEP'] )

fig7 = px.scatter(accuracy_df, x = 'Actual', y = 'Predicted', trendline = 'ols', trendline_color_override='red',
                color = 'Variance', color_continuous_scale=px.colors.sequential.YlGnBu, width = 700,
                title = 'Predicted vs Actual Results With Linear Regression Line and Variance')
fig8 = px.bar(feature_df, x= 'Feature Importance', y = 'Feature Name', orientation = 'h', 
             hover_data = ['Feature Name', 'Feature Importance'], color = 'Feature Importance', 
             color_continuous_scale=px.colors.sequential.Viridis, width = 800, height = 700,
             title = 'Feature Importances Sorted')

fig9 = go.Figure()

for column in cancer_hr_df.columns.to_list():
    fig9.add_trace(
        go.Scatter(
            x = cancer_hr_df.index,
            y = cancer_hr_df[column],
            name = column
           
        )
    )
    
fig9.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active=0,
        buttons=list(
            [dict(label = 'All',
                method = 'update',
                args = [{'visible': [False, False, True, True, True, True, True, True]},
                    {'title': 'All',
                    'showlegend':True}]),
            dict(label = 'binge',
                method = 'update',
                args = [{'visible': [False, False, True, True, False, False, False, False]}, # the index of True aligns with the indices of plot traces
                        {'title': 'Binge Drinking',
                        'showlegend':True}]),
            dict(label = 'csmoking',
                method = 'update',
                args = [{'visible': [False, False, True, False, True, False, False, False]},
                        {'title': 'Smoking',
                        'showlegend':True}]),
            dict(label = 'lpa',
                method = 'update',
                args = [{'visible': [False, False, True, False, False, True, False, False]},
                        {'title': 'Limited Physical Activity',
                        'showlegend':True}]),
            dict(label = 'sleep',
                method = 'update',
                args = [{'visible': [False, False, True, False, False, False, True]},
                        {'title': '> 7 Hours of Sleep',
                        'showlegend':True}]),
            
            ])
        )
    ])



# Callback for different pages
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return [
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H3("Introduction to Project", style={'textAlign':'center'}),
                        html.Br(),
                        html.P("Leveraging US county level estimates for health related measure, we seek to answer the following questions"),
                        html.H4("Main Questions:"),
                        html.P("Can we predict the percentage of the national population that has cancer based on various other categories of health metrics at a county level?"),
                        html.P("Are there features related to health: preventive measure, risk behaviors, or other medical outcomes that are correlated to cancer outcomes?"),
                    ], width=6),
                    dbc.Col([ 
                        dbc.Card([dbc.CardImg(src=graph_path),], style={"width": "30rem"},),
                        ], width=3)
                    ])
                    ])
                    
        ]

    elif pathname == "/page-1":
        return [
            html.H1 ("Dashboard", style = {'textAlign':'center'}),
            dcc.Graph(figure = fig2),
            dcc.Input(id="zip-input", value="# Enter zip to update table below",
            size="30"),
            dcc.Graph(id = "zip-output"),  
            
            dcc.Graph(figure = fig9),   

# Delete if we want to keep the existing map        
#            dcc.Graph(figure = px.choropleth_mapbox(df, geojson=counties, locations='CountyFIPS', color='CANCER',
#                           color_continuous_scale="Viridis",
#                           range_color=(0, 12),
#                           mapbox_style="carto-positron",
#                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
#                           opacity=0.5,
#                           labels={'unemp':'unemployment rate'},
#                           width=1000, height=600))            
             ]

    elif pathname == "/page-2":
        return [ 
            html.H1("Analysis", style={'textAlign':'center'}),
            html.Br(),
            html.P("We reviewed distributions by using box plots to better understand the various measures in our dataset.   We chose to keep outliers to keep our data's integrity in our analysis. We compared the crude with the age adjusted columns, and determined to keep the age adjusted columns based on our approach of comparing measures accross counties.  We also completed some quick scatterplots and saw that some of the relationships between measures appeared to be linear."),
            html.Br(),
            html.P("Completing a correlation table, we were able to see how the measure may or may not be correlated with each other."),
            dcc.Graph(figure = fig3),
            dcc.Graph(figure = fig4),
            dcc.Graph(figure = fig5),
            dcc.Graph(figure = fig6),
            dbc.Card([dbc.CardImg(src=image_path),],style={"width": "50rem"},),
            ]

    elif pathname == "/page-3":
        return [
            html.H1("Machine Learning", style={'textAlign':'center'}),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        #dbc.Card([dbc.CardImg(src=actual_v_predicted_path),], style={"width": "30rem"},),
                        dbc.Card([dbc.CardImg(src=accuracy_path),],style={"width": "30rem"},),
                    ]),
                    dbc.Col([
                        html.H3("Model Choice", style={'textAlign':'center'}),
                        html.Br(),                        
                        html.P("A multiple linear regression model will be used to predict cancer rate using the categorized health data as features. R-squared and P-values will be examined to determine effectiveness and confidence of the data's relationships. There is limiations that come with multiple linear regression. Linear regression is very sensitive to outliers and falsely concluding correlation is causation can occur. The benefit of this model is that many features can be used to predict the cancer rate, and it lets the strength of the relationship be assessed between each feature and the prediction."),
                        html.Br(),                        
                        html.P("The model predicts the percentage of population with cancer with a relatively low mean square error value, and an accuracy score above 90%.")
                    ]),
            dcc.Graph(figure = fig7),
            dcc.Graph(figure = fig8),    ])
            ])
        ]


    elif pathname == "/page-4":
        return [
            html.H1("References", style={'textAlign':'center'}),
            html.H3("Our references include"),

            dbc.Card([
                dbc.CardBody([
                    html.H4("County Health Measures", className="card-title"),
                    html.P("All health measures and population data sourced from the CDC Places dataset.",
                    className="card-text"),
                dbc.Button("Go to the CDC Webpage", href="https://chronicdata.cdc.gov/500-Cities-Places/PLACES-County-Data-GIS-Friendly-Format-2021-releas/kmvs-jkvx", 
                external_link=True, color="primary"),
                ]),
                ],
                style={"width": "25rem"},),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Definitions for Measures", className="card-title"),
                    html.P("Complete definitions for health measures.",
                    className="card-text",),
                dbc.Button("Go to the measure-definitions page",href="https://www.cdc.gov/places/measure-definitions/index.html", 
                external_link=True, color="primary"),
                ]),
                ],
                style={"width": "25rem"},),
            dbc.Card([
                dbc.CardBody([
                    html.H4("County Populations", className="card-title"),
                    html.P("2020 population measures for US counties.",
                    className="card-text",),
                dbc.Button("Go to the population report page",href="http://www.socialexplorer.com/pub/reportdata/HtmlResults.aspx?reportid=R13242424", 
                external_link=True, color="primary"),
                ]),
                ],
                style={"width": "25rem"},),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Zip Code Reference", className="card-title"),
                    html.P("Table to look up FIPS IDs by zip code source from Kaggle.",
                    className="card-text",),
                dbc.Button("Go to Kaggle", href="https://www.kaggle.com/datasets/danofer/zipcodes-county-fips-crosswalk", 
                external_link=True, color="primary"),
                ]),
                ],
                style={"width": "25rem"},)
            ]
        


    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )
if __name__=='__main__':
    app.run_server(port=8887)