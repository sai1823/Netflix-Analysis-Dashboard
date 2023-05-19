# Netflix-Analysis-Dashboard

This is a dashboard application built using Dash and Plotly libraries in Python. The application provides insights and visualizations based on the Netflix dataset. It allows users to filter and analyze Netflix content based on various criteria such as type, release year, country, and genre.

## Prerequisites

Make sure you have the following libraries installed in your Python environment:
- Dash
- Plotly
- Pandas
- Dash Bootstrap Components
- Wordcloud

You can install the required libraries using pip:
```
pip install dash plotly pandas dash-bootstrap-components wordcloud
```

## Getting Started

1. Clone the repository or download the code files.

2. Open the code file in a Python IDE or text editor.

3. Run the code file to start the application.

4. Access the dashboard by opening a web browser and navigating to `http://localhost:8050`.

## Features

The Netflix Analysis Dashboard provides the following features:

- Type Selection: Filter content by type (TV Show or Movie).
- Number of Countries: Select the number of top countries to include in the analysis.
- Released Year: Filter content by the release year.
- Country: Filter content by specific countries.
- Genre: Filter content by genre.
- Total Content: Shows the total number of content based on the applied filters.
- Total Content Released in Summer: Displays the total number of content released in May.
- Average Duration: Calculates and displays the average duration of content based on the selected type.
- Histogram: Visualizes the distribution of content based on release year.
- Bar Chart: Displays the top countries with the most content.
- Pie Chart: Shows the distribution of content by type (TV Show or Movie).
- Line Chart: Displays the trend of content releases over the years.
- Word Cloud: Generates a word cloud based on the titles of the content.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and distribute the code as needed.

## Acknowledgments

- The Netflix dataset used in this application is sourced from [Kaggle](https://www.kaggle.com/shivamb/netflix-shows).
