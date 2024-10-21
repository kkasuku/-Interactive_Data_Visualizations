import pandas as pd
from dash import Dash, dcc, html, Input, Output
from dash import dash_table  # Updated import
import plotly.express as px

# Load the dataset
file_path = r'C:\Users\dell\Documents\EDUCATION\Datasets\student_performance_prediction.csv'
data = pd.read_csv(file_path)

# Fill missing values
data['Study Hours per Week'].fillna(data['Study Hours per Week'].median(), inplace=True)
data['Attendance Rate'].fillna(data['Attendance Rate'].median(), inplace=True)
data['Previous Grades'].fillna(data['Previous Grades'].median(), inplace=True)
data['Participation in Extracurricular Activities'].fillna(data['Participation in Extracurricular Activities'].mode()[0], inplace=True)
data['Parent Education Level'].fillna(data['Parent Education Level'].mode()[0], inplace=True)

# Create a Dash application
app = Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Student Performance Dashboard", style={'textAlign': 'center'}),

    # Dropdown for filtering by Passed status
    dcc.Dropdown(
        id='passed-filter',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Passed', 'value': 'Passed'},
            {'label': 'Not Passed', 'value': 'Not Passed'}
        ],
        value='All',
        clearable=False,
        placeholder='Filter by Passed Status',
        style={'width': '50%', 'margin': 'auto'}
    ),

    # Additional Dropdown for filtering by Parent Education Level
    dcc.Dropdown(
        id='parent-education-filter',
        options=[{'label': edu, 'value': edu} for edu in data['Parent Education Level'].unique()],
        value='All',
        clearable=False,
        placeholder='Filter by Parent Education Level',
        style={'width': '50%', 'margin': 'auto', 'marginTop': '10px'}
    ),

    # Graph for the bar chart
    dcc.Graph(id='bar-chart'),

    # Graph for the box plot
    dcc.Graph(id='box-plot'),

    # Graph for the line chart
    dcc.Graph(id='line-chart'),

    # Table for detailed view
    html.Div(id='details-table')
])

# Callback to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('passed-filter', 'value'),
    Input('parent-education-filter', 'value')
)
def update_bar_chart(passed_filter, parent_education_filter):
    filtered_data = data
    if passed_filter != 'All':
        filtered_data = filtered_data[filtered_data['Passed'] == passed_filter]
    if parent_education_filter != 'All':
        filtered_data = filtered_data[filtered_data['Parent Education Level'] == parent_education_filter]
    
    if filtered_data.empty:
        return px.histogram()  # Return empty plot or a message

    fig = px.histogram(filtered_data, x='Participation in Extracurricular Activities', color='Passed', barmode='group',
                       hover_data=['Study Hours per Week', 'Previous Grades'])
    fig.update_layout(title_text='Participation in Extracurricular Activities by Passing Status')
    return fig

# Callback to update the box plot
@app.callback(
    Output('box-plot', 'figure'),
    Input('passed-filter', 'value'),
    Input('parent-education-filter', 'value')
)
def update_box_plot(passed_filter, parent_education_filter):
    filtered_data = data
    if passed_filter != 'All':
        filtered_data = filtered_data[filtered_data['Passed'] == passed_filter]
    if parent_education_filter != 'All':
        filtered_data = filtered_data[filtered_data['Parent Education Level'] == parent_education_filter]

    if filtered_data.empty:
        return px.box()  # Return empty plot or a message

    fig = px.box(filtered_data, x='Passed', y='Study Hours per Week', hover_data=['Previous Grades'],
                  title='Study Hours per Week vs Passed')
    return fig

# Callback to update the line chart
@app.callback(
    Output('line-chart', 'figure'),
    Input('passed-filter', 'value'),
    Input('parent-education-filter', 'value')
)
def update_line_chart(passed_filter, parent_education_filter):
    filtered_data = data
    if passed_filter != 'All':
        filtered_data = filtered_data[filtered_data['Passed'] == passed_filter]
    if parent_education_filter != 'All':
        filtered_data = filtered_data[filtered_data['Parent Education Level'] == parent_education_filter]

    if filtered_data.empty:
        return px.line()  # Return empty plot or a message

    fig = px.line(filtered_data, x='Attendance Rate', y='Previous Grades', color='Passed',
                   title='Attendance Rate vs Previous Grades', hover_data=['Study Hours per Week'])
    return fig

# Callback to update the details table
@app.callback(
    Output('details-table', 'children'),
    Input('passed-filter', 'value'),
    Input('parent-education-filter', 'value')
)
def update_details_table(passed_filter, parent_education_filter):
    filtered_data = data
    if passed_filter != 'All':
        filtered_data = filtered_data[filtered_data['Passed'] == passed_filter]
    if parent_education_filter != 'All':
        filtered_data = filtered_data[filtered_data['Parent Education Level'] == parent_education_filter]

    return dash_table.DataTable(
        data=filtered_data.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in filtered_data.columns],
        style_table={'overflowX': 'auto'},
        page_size=10
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)  # Specify port if needed
