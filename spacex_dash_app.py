# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                        options=[
                                                            {'label': 'All Sites', 'value': 'ALL'},
                                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}                                                            
                                                        ],
                                                        value='ALL',
                                                        placeholder="place holder here",
                                                        searchable=True)),


                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                               
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                        min=0, max=10000, step=1000,
                                                        marks={0: '0',
                                                            1000: '1000',
                                                            5000: '5000',
                                                            10000: '10000'},
                                                        value=[min_payload, max_payload])),
                                

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_graph(entered_site):
    df = spacex_df[["Launch Site", "class"]].groupby(["Launch Site"], as_index=False).sum()
    if entered_site == "ALL":
        fig = px.pie(df, values='class', 
        names='Launch Site', 
        title='Total Success Launch By Site')
        return fig
    else:
        df =  spacex_df[spacex_df['Launch Site']==str(entered_site)]
        success_rate = df["class"].value_counts().to_frame()
        
        fig = px.pie(success_rate, values=success_rate['count'], 
        names=success_rate.index, 
        title=f'Total Success Launches for Site {entered_site}')
        return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

# Add computation to callback function and return graph
def get_graph_payload(entered_site, range_selected):
    df = spacex_df
    range_df = df[(df['Payload Mass (kg)'] >= range_selected[0]) & (df['Payload Mass (kg)'] <= range_selected[1])]
    print(range_selected)
    if entered_site == "ALL":        
        fig = px.scatter(range_df, x='Payload Mass (kg)', y='class', color="Booster Version Category", title="Correletion Between Payload and Success for All Sites")
        return fig
    else:
        df =  range_df[range_df['Launch Site']==str(entered_site)]
              
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color="Booster Version Category", title=f"Correletion Between Payload and Success for {entered_site}")
        return fig
    

# Run the app
if __name__ == '__main__':
    app.run_server()
