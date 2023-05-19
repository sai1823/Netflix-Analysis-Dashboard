

import dash                              # pip install dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import datetime      # pip install wordcloud
import plotly.graph_objs as go
from wordcloud import WordCloud

netflix=pd.read_csv('C:/Users/Radhe-Radhe/Downloads/netflix_titles.csv')
df = netflix.copy()

df=df.dropna()
df.shape

# convert in Date Format
df["date_added"] = pd.to_datetime(df['date_added'])
df['day_added'] = df['date_added'].dt.day
df['year_added'] = df['date_added'].dt.year
df['month_added']=df['date_added'].dt.month
df['year_added'].astype(int);
df['day_added'].astype(int);

year_options = [{'label': str(year), 'value': year} for year in sorted(df['release_year'].unique(), reverse=True)]


constraint=df['director'].apply(lambda x: str(x).split(', ')).tolist()
df_new=pd.DataFrame(constraint,index=df['title'])
df_new=df_new.stack()
df_director=pd.DataFrame(df_new)
df_director.reset_index(inplace=True)
df_director=df_director[['title',0]]
df_director.rename(columns={0:'director'})

constraint=df['cast'].apply(lambda x: str(x).split(', ')).tolist()
df_new=pd.DataFrame(constraint,index=df['title'])
df_new=df_new.stack()
df_cast=pd.DataFrame(df_new)
df_cast.reset_index(inplace=True)
df_cast=df_cast[['title',0]]
df_cast.rename(columns={0:'cast'})

constraint=df['country'].apply(lambda x: str(x).split(', ')).tolist()
df_new=pd.DataFrame(constraint,index=df['title'])
df_new=df_new.stack()
df_country=pd.DataFrame(df_new)
df_country.reset_index(inplace=True)
df_country=df_country[['title',0]]
df_country.rename(columns={0:'country'})


constraint=df['listed_in'].apply(lambda x: str(x).split(', ')).tolist()
df_new=pd.DataFrame(constraint,index=df['title'])
df_new=df_new.stack()
df_listedin=pd.DataFrame(df_new)
df_listedin.reset_index(inplace=True)
df_listedin=df_listedin[['title',0]]
df_listedin.rename(columns={0:'genre'})

x= df_director.merge(df_cast,left_on="title",right_on="title",how="left")
x=x.rename(columns={'0_x':'director','0_y':'cast'})

y= x.merge(df_country,left_on="title",right_on="title",how="left")
y=y.rename(columns={0:'country'})

z= y.merge(df_listedin,left_on="title",right_on="title",how="left")
z=z.rename(columns={0:'genre'})

#Dropping columns in original dataset
df=df.drop(['director', 'cast','country','listed_in'], axis=1)
#Merge columns to Single dataset column
df= z.merge(df,left_on="title",right_on="title",how="left")
df.head()

data_dict1 = {'country': df.groupby('country').size().sort_values(ascending=False)[:20].index,
             'Number of content': df.groupby('country').size().sort_values(ascending=False)[:20].values
             }

print(df.columns)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H1("Netflix Analysis",style={"color": "#FFFBF5",'backgroundColor': '#1C1C1C','text-align': 'center'} )
            ],style={"backgroundColor": '#1C1C1C','border': '1px solid black'},className='mb-2'),
        ], width=12),
    ],style={"backgroundColor": '#1C1C1C'},className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src="https://media.giphy.com/media/JnvHE3lTHPr3WrSsrl/giphy.gif",style={"width":"200px", "height":"200px","border-radius":"50%"})
            ],style={"backgroundColor": '#1C1C1C'},className='mb-2'),
        ],style={"backgroundColor": '#1C1C1C','border': '1px solid 1C1C1C'}, width=2),
        
        dbc.Col([
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([ 
                            dbc.Col([
                                html.P("Type",style={"color": "#FFFBF5",}),
                                dcc.Dropdown(id="type", clearable=False,
                                            value="All", options=[{'label':'All', 'value':'All'}] + [{'label':x, 'value':x} for x in df['type'].unique()],style={"color": "#1C1C1C",'backgroundColor':'#C2C2C2'})
                            ], width=2, ),

                            dbc.Col([
                                html.P("Number of Countries",style={"color": "#FFFBF5",}),
                                dcc.Dropdown(id="num_countries", clearable=False,options=[{'label':i, 'value':i} for i in range(1, 21)],style={"color": "#1C1C1C",'backgroundColor':'#C2C2C2'},
                                            value=20)
                            ], width=2),
                                            
                            dbc.Col([
                                html.P("Released Year",style={"color": "#FFFBF5",}),
                                dcc.Dropdown(id="Year", clearable=False,value=max(df['release_year']),
                                            options=year_options,style={"color": "#1C1C1C",'backgroundColor':'#C2C2C2'})
                                            
                            ], width=2),

                            dbc.Col([
                                html.P("Country",style={"color": "#FFFBF5",}),
                                dcc.Dropdown(id="country", clearable=False,
                                            multi=True,
                                            options=[{'label':'All', 'value':'All'}] +[{'label': i, 'value': i} for i in df['country'].sort_values().unique()],
                                            value=['All'],
                                            style={"color": "#1C1C1C",'backgroundColor':'#C2C2C2'})
                            ], width=3),

                            dbc.Col([
                                html.P("Genre",style={"color": "#FFFBF5",'backgroundColor':'BFCCB5'}),
                                dcc.Dropdown(id="Genre", clearable=False,value=['All'],
                                            multi=True,options=[{'label':'All', 'value':'All'}] +[{'label': i, 'value': i} for i in df['genre'].sort_values().unique()],style={"color": "#1C1C1C",'backgroundColor':'#C2C2C2'})
                            ], width=3),
                        ])
                    ])
                ],style={'backgroundColor': '#1C1C1C','border': '1px solid black'})
            ]) ,

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Total Content available",style={"color": "#f5f5f5"}),
                            html.H4(id="content",children="000",style={"color": "#f5f5f5",}),
                        ], style={'textAlign':'center'})
                    ],style={"backgroundColor": '#1C1C1C','border': '1px solid black'}), 
                ], width=3),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Total released in summer(May)",style={"color": "#f5f5f5"}),
                            html.H4(id="summer_content",children="000",style={"color": "#f5f5f5",}),
                        ], style={'textAlign':'center'})                       
                    ],style={"backgroundColor": '#1C1C1C','border': '1px solid black','height':'100','width':'400'}),
                ], width=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Avg Duration",style={"color": "#f5f5f5"}),
                            html.H4(id="duration",children="000",style={"color": "#f5f5f5",}),
                            ], style={'textAlign':'center'})                      
                    ],style={"backgroundColor": '#1C1C1C','border': '1px solid black'}),
                ], width=4),

            ],style={"backgroundColor": '#1C1C1C'},className='mb-2'),       
        ], width=10),

    ],style={"backgroundColor": '#1C1C1C'},className='mb-2 mt-2'),
    
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='histogram', figure={},config={'displayModeBar': False}, style={'height': '100%', 'width': '100%'}),
                ])
            ],style={'height': '100%',"backgroundColor": '#1C1C1C','border': '1px solid black'}),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                ])
            ],style={"backgroundColor": '#1C1C1C','border': '1px solid black'}),
        ], width=5),
        

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie_chart', figure={}, config={'displayModeBar': False}),
                ])
            ],style={"backgroundColor": '#1C1C1C','border': '1px solid black'}),
        ], width=3),

    ],style={"backgroundColor": '#1C1C1C'},className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ],style={"backgroundColor": '#1C1C1C','border': '1px solid black'}),
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='word_cloud', figure={}, config={'displayModeBar': False},style={'height': '100%'}),
                ],)
            ],style={"backgroundColor": '#1C1C1C','border': '1px solid black'}),
        ], width=6),
    ],style={"backgroundColor": '#1C1C1C'},className='mb-2'),
], style={"backgroundColor": '#1C1C1C'},fluid=True)

@app.callback(
    Output("content", "children"),
    [Input("type", "value"),
     Input("Year", "value"),
     Input("country", "value"),
     Input("Genre", "value"),
     Input("num_countries", "value")]
)
def update_total_content(type_val, year_val, country_val, genre_val, num_countries_val):
    filtered_df = df.copy()
    if type_val != "All":
        filtered_df = filtered_df[filtered_df["type"] == type_val]
    if year_val is not None:
        filtered_df = filtered_df[filtered_df["release_year"] == year_val]
    if country_val != ['All']:
        filtered_df = filtered_df[filtered_df["country"].isin(country_val)]
    if genre_val != ['All']:
        filtered_df = filtered_df[filtered_df["genre"].isin(genre_val)]
    if num_countries_val != 20:
        top_countries = filtered_df["country"].value_counts().head(num_countries_val).index
        filtered_df = filtered_df[filtered_df["country"].isin(top_countries)]
    return len(filtered_df)



@app.callback(
    Output("summer_content", "children"),
    Input("type", "value"),
    Input("country", "value"),
    Input("Year", "value")
)
def update_summer_content(type_val, country_val, year_val):
    filtered_df = df.copy()
    
    # Apply type filter
    if type_val != "All":
        filtered_df = filtered_df[filtered_df["type"] == type_val]

    if country_val != ['All']:
        filtered_df = filtered_df[filtered_df["country"].isin(country_val)]
    # Apply year filter
    filtered_df = filtered_df[filtered_df["release_year"] == year_val]
    
    # Filter for content released in May
    may_content = filtered_df[(filtered_df["date_added"].dt.month == 5)]
    
    # Calculate total content released in May
    summer_content = len(may_content)
    
    return f"{summer_content:,.0f}"


@app.callback(
    Output("duration", "children"),
    Input("type", "value"),
    Input("country", "value"),
    Input("Year", "value"),
    Input("Genre", "value"),
    Input("num_countries", "value")
)
def avg_duration(type_val, country_val, year_val, genre_val, num_countries_val):
    filtered_df = df.copy()
    if type_val != "All":
        filtered_df = filtered_df[filtered_df["type"] == type_val]
    if year_val is not None:
        filtered_df = filtered_df[filtered_df["release_year"] == year_val]
    if country_val != ['All']:
        filtered_df = filtered_df[filtered_df["country"].isin(country_val)]
    if genre_val != ['All']:
        filtered_df = filtered_df[filtered_df["genre"].isin(genre_val)]
    if num_countries_val != 20:
        top_countries = filtered_df["country"].value_counts().head(num_countries_val).index
        filtered_df = filtered_df[filtered_df["country"].isin(top_countries)]

    # separate rows with 'Seasons' and 'min' duration into two separate data frames
    tv_shows_df = filtered_df[filtered_df["duration"].str.contains("Season")]
    movies_df = filtered_df[~filtered_df["duration"].str.contains("Season")]

    # calculate the average durations separately
    if type_val == "TV Show":
        avg_duration = tv_shows_df["duration"].str.extract("(\d+)", expand=False).astype(int).mean()
        avg_duration = f"{avg_duration:.2f} Seasons"
    elif type_val == "Movie":
        avg_duration = movies_df["duration"].str.extract("(\d+)", expand=False).astype(int).mean()
        avg_duration = f"{avg_duration:.2f} min"
    else:
        avg_duration_tv_shows = tv_shows_df["duration"].str.extract("(\d+)", expand=False).astype(int).mean()
        avg_duration_movies = movies_df["duration"].str.extract("(\d+)", expand=False).astype(int).mean()
        avg_duration = f"{avg_duration_tv_shows:.2f} Seasons, {avg_duration_movies:.2f} min"

    return avg_duration

@app.callback(
    Output('histogram', 'figure'),
    Input('type', 'value'),
    Input('num_countries', 'value'),
    Input('Year', 'value'),
    Input('country', 'value'),
    Input('Genre', 'value'))

def update_histogram(type_val, num_countries_val, year_val, country_val, genre_val):
    filtered_df = df.copy()
    # Filter based on the inputs
    if type_val != "All":
        filtered_df = filtered_df[filtered_df["type"] == type_val]
    if year_val is not None:
        filtered_df = filtered_df[filtered_df["release_year"] == year_val]
    if country_val != ['All']:
        filtered_df = filtered_df[filtered_df["country"].isin(country_val)]
    if genre_val != ['All']:
        filtered_df = filtered_df[filtered_df["genre"].isin(genre_val)]
    if num_countries_val != 20:
        top_countries = filtered_df["country"].value_counts().head(num_countries_val).index
        filtered_df = filtered_df[filtered_df["country"].isin(top_countries)]

    # Create histogram plot
    fig = px.histogram(filtered_df, x='rating', nbins=30, color_discrete_sequence=['#E74646'])

    # Update the layout
    fig.update_layout(
        plot_bgcolor='#1C1C1C',
        paper_bgcolor='#1C1C1C',
        title="Histogram of Rating",
        title_font=dict(size=18, color="#f5f5f5"),
        xaxis=dict(
        tickfont=dict(color="#f5f5f5"),  # Change color of x-axis elements
        title_font=dict(color="#f5f5f5")  # Change color of x-axis title
    ),
        yaxis=dict(
        tickfont=dict(color="#f5f5f5"),  # Change color of y-axis elements
        title_font=dict(color="#f5f5f5")  # Change color of y-axis title
        ),title_x=0.5 

    )
    return fig

@app.callback(
    Output("line-chart", "figure"),
    Input('type', 'value'),
    Input('num_countries', 'value'),
    Input('Year', 'value'),
    Input('country', 'value'),
    Input('Genre', 'value'))



def update_trend(type_val, num_countries_val, year_val, country_val, genre_val):
    filtered_df = df.copy()
    # Group the data by genre and year and count the number of titles
    df_genre_year = filtered_df.groupby(['genre', 'release_year']).size().reset_index(name='count')
    # Calculate the running sum of the count for each genre
    df_genre_year['running_sum'] = df_genre_year.groupby('genre')['count'].cumsum()
    # Plot the trend of genres using a line chart
    fig = px.line(df_genre_year, x='release_year', y='running_sum', color='genre')
    fig.update_layout(
        plot_bgcolor='#1C1C1C',
        paper_bgcolor='#1C1C1C',
        title="Trend of genre",
        title_font=dict(size=20, color="#f5f5f5"),xaxis=dict(
        tickfont=dict(color="#f5f5f5"),  # Change color of x-axis elements
        title_font=dict(color="#f5f5f5")  # Change color of x-axis title
    ),font=dict(color="#F9F9F9"),
        yaxis=dict(
        tickfont=dict(color="#f5f5f5"),  # Change color of y-axis elements
        title_font=dict(color="#f5f5f5")  # Change color of y-axis title
        ),title_x=0.5 
    )
    return fig


@app.callback(
    Output("bar-chart", "figure"),
    Input('type', 'value'),
    Input('num_countries', 'value'),
    Input('Year', 'value'),
    Input('country', 'value'),
    Input('Genre', 'value'))


def update_bar_chart(type_val, num_countries_val, year_val, country_val, genre_val):
    filtered_df = df.copy()
    if type_val != "All":
        filtered_df = filtered_df[filtered_df["type"] == type_val]
    if year_val is not None:
        filtered_df = filtered_df[filtered_df["release_year"] == year_val]
    if country_val != ['All']:
        filtered_df = filtered_df[filtered_df["country"].isin(country_val)]
    if genre_val != ['All']:
        filtered_df = filtered_df[filtered_df["genre"].isin(genre_val)]
    if num_countries_val != 20:
        top_countries = filtered_df["country"].value_counts().head(num_countries_val).index
        filtered_df = filtered_df[filtered_df["country"].isin(top_countries)]

    topdirs = pd.value_counts(filtered_df['duration'],)
    fig = go.Figure(data=[go.Bar(
        x=topdirs.index,
        y=topdirs.values,
        text=topdirs.values,
        marker_color='#E74646',
        texttemplate='%{text:.2s}',
        textposition='outside'
    )])
    fig.update_layout(
        plot_bgcolor='#1C1C1C',
        paper_bgcolor='#1C1C1C',
        height=500,
        title="Bar Chart of Duration",
        title_font=dict(size=20, color="#F9F9F9"),
        xaxis=dict(
            title='Duration',
            tickfont=dict(color="#f5f5f5"),  # Change color of y-axis elements
            title_font=dict(color="#f5f5f5") 
        ),
        yaxis=dict(
        title='Count',
        tickfont=dict(color="#f5f5f5"),  # Change color of y-axis elements
        title_font=dict(color="#f5f5f5")  # Change color of y-axis title
        ),title_x=0.5 
        
    )
    return fig

@app.callback(
    Output("word_cloud", "figure"),
    Input('type', 'value'),
    Input('num_countries', 'value'),
    Input('Year', 'value'),
    Input('country', 'value'),
    Input('Genre', 'value'))

def update_word_cloud(type_val, num_countries_val, year_val, country_val, genre_val):
    filtered_df = df.copy()
    if type_val != "All":
        filtered_df = filtered_df[filtered_df["type"] == type_val]
    if year_val is not None:
        filtered_df = filtered_df[filtered_df["release_year"] == year_val]
    if country_val != ['All']:
        filtered_df = filtered_df[filtered_df["country"].isin(country_val)]
    if genre_val != ['All']:
        filtered_df = filtered_df[filtered_df["genre"].isin(genre_val)]
    if num_countries_val != 20:
        top_countries = filtered_df["country"].value_counts().head(num_countries_val).index
        filtered_df = filtered_df[filtered_df["country"].isin(top_countries)]

    df_country = filtered_df.groupby('country').size().reset_index(name='count')
    # Create word cloud of countries
    text = ' '.join(filtered_df['country'].astype(str))
    wordcloud = WordCloud(background_color='#f5f5f5').generate(text)

    # Plot the word cloud
    fig_wordcloud = go.Figure(data=[go.Image(z=wordcloud.to_array())])
    fig_wordcloud.update_layout(
        plot_bgcolor='#C2C2C2',
        paper_bgcolor='#1C1C1C',   
        title="Country Word Cloud",
        title_font=dict(size=20, color="#f5f5f5"),xaxis=dict(
        tickfont=dict(color="#f5f5f5"),  # Change color of x-axis elements
        title_font=dict(color="#f5f5f5")  # Change color of x-axis title
    ),
        yaxis=dict(
        tickfont=dict(color="#f5f5f5"),  # Change color of y-axis elements
        title_font=dict(color="#f5f5f5")  # Change color of y-axis title
        ),title_x=0.5,      
    )
    return  fig_wordcloud
    

@app.callback(
    Output("pie_chart", "figure"),
    Input('type', 'value'),
    Input('num_countries', 'value'),
    Input('Year', 'value'),
    Input('country', 'value'),
    Input('Genre', 'value')
)
def update_pie(type_val, num_countries_val, year_val, country_val, genre_val):
    filtered_df = df.copy()
    if type_val != "All":
        filtered_df = filtered_df[filtered_df["type"] == type_val]
    if year_val is not None:
        filtered_df = filtered_df[filtered_df["release_year"] == year_val]
    if country_val != ['All']:
        filtered_df = filtered_df[filtered_df["country"].isin(country_val)]
    if genre_val != ['All']:
        filtered_df = filtered_df[filtered_df["genre"].isin(genre_val)]
    if num_countries_val != 20:
        top_countries = filtered_df["country"].value_counts().head(num_countries_val).index
        filtered_df = filtered_df[filtered_df["country"].isin(top_countries)]

    fig = px.pie(filtered_df, names='type', color_discrete_sequence=['#E74646'])
    fig.update_traces(textfont=dict(color='#1C1C1C'))

    fig.update_layout(
        plot_bgcolor='#C2C2C2',
        paper_bgcolor='#1C1C1C',
        title="Pie chart for type",
        width=350,
        height=500,
        title_font=dict(size=20, color="#1C1C1C"),xaxis=dict(
            tickfont=dict(color="#1C1C1C"),  # Change color of x-axis elements
            title_font=dict(color="#1C1C1C")  # Change color of x-axis title
        ),font=dict(color="#F9F9F9"),
            yaxis=dict(
            tickfont=dict(color="#f5f5f5"),  # Change color of y-axis elements
            title_font=dict(color="#f5f5f5")  # Change color of y-axis title
            ),
        title_x=0.5,
)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
