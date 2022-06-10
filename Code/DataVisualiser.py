# -*- coding: utf-8 -*-
"""
Created on Fri May 6 2022
Python Version : 3.9.7
Panda version : 1.3.3
MatPlotLib : 3.4.3
plotly Version: 5.8.0
Summary : Visualise data from FilteredData and save results to Charts folder.
@author: me
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'  # to show geojson map in web browser

data_source_filename = 'RawScrapedData.csv'
jobs_df = pd.read_csv(data_source_filename)
jobs_df.drop_duplicates(
    subset=None, keep='first', inplace=False)  # drop duplicates

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 500)


def HorizontalLollipopChart(source_filename, destination_filename, title):
    # using data from csv file
    df = pd.read_csv(source_filename, sep='\t')

    # get rid of data with 0 frequency
    df = df[df['Frequency'] != 0]

    column_headings = df.columns

    # my_labels = df[column_headings[0]].tolist()
    my_data = df[column_headings[1]].tolist()

    # when using data from dictionary
    # df = pd.DataFrame(list(dictionary.items()), columns=['Name', 'Value'])

    # Reorder it based on the values:
    ordered_df = df.sort_values(by=column_headings[1])  # VARIABLE
    my_range = range(1, len(df.index)+1)
    plt.style.use('fivethirtyeight')

    plt.hlines(y=my_range, xmin=0,
               xmax=ordered_df[column_headings[1]])  # , color='skyblue'
    plt.plot(ordered_df[column_headings[1]], my_range, "o")

    plt.yticks(my_range, ordered_df[column_headings[0]])
    plt.title(title, weight='bold')

    # plt.savefig(destination_filename, bbox_inches='tight')
    plt.show()
    plt.close()


def HorizontalBarChart(source_filename, destination_filename, my_color, title):
    # =============================================================================
    #     for key in list(dictionary):
    #         if dictionary[key] == 0:
    #             dictionary.pop(key, None)
    # =============================================================================
    df = pd.read_csv(source_filename, sep='\t')
    df = df.sort_values(by=['Frequency'])

    # get rid of data with 0 frequency
    df = df[df['Frequency'] != 0]

    column_headings = df.columns

    my_labels = df[column_headings[0]].tolist()
    my_data = df[column_headings[1]].tolist()

# =============================================================================
#     # when reading from dictionary
#     my_labels = list(dictionary.keys())
#     my_data = list(dictionary.values())
# =============================================================================

    # colors = ['red', 'yellow', 'green', 'blue', 'orange', 'black']
    cmap = plt.cm.tab10
    # colors = cmap(np.arange(len(my_labels)) % cmap.N)
    plt.style.use('ggplot')

    plt.barh(my_labels, my_data, color=my_color)
    plt.title(title, weight='bold')
    # plt.ylabel(column_headings[0])  # VARIABLE
    plt.xlabel(column_headings[1])
    # plt.savefig(destination_filename, bbox_inches='tight')

    plt.show()
    plt.close()


def PieChart(source_filename, destination_filename):
    # =============================================================================
    #     # filter out languages which have not been used at all
    #     for lang in list(languages):
    #         if languages[lang] == 0:
    #             languages.pop(lang, None)
    #
    #     languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    #     x, y = zip(*languages)  # unpack a list of pairs into two tuples
    # =============================================================================

    df = pd.read_csv(source_filename, sep='\t')
    column_headings = df.columns

    my_labels = df[column_headings[0]].tolist()
    my_data = df[column_headings[1]].tolist()
    # create a figure and set different background
    fig = plt.figure()
    # fig.patch.set_facecolor('black')

    # Change color of text
    plt.rcParams['text.color'] = 'black'

    # Create a circle at the center of the plot
    my_circle = plt.Circle((0, 0), 0.7, color='white')

    # Pieplot + circle on it
    plt.pie(my_data, labels=my_labels, shadow=True, autopct='%1.1f%%')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.savefig(destination_filename)

    plt.legend()
    plt.show()
    plt.close()


def donutChart(source_filename, destination_path, title):
    # https://medium.com/@krishnakummar/donut-chart-with-python-matplotlib-d411033c960b
    df = pd.read_csv(source_filename, sep='\t')

# =============================================================================
#     # shorten long names for CLoud
#     df.loc[df.CloudPlatforms == 'Google Cloud Platform',
#            'CloudPlatforms'] = 'Google Cloud'
#     print(df)
# =============================================================================
    # get rid of data with 0 frequency
    df = df[df['Frequency'] != 0]

    column_headings = df.columns
    my_labels = df[column_headings[0]].tolist()
    my_data = df[column_headings[1]].tolist()

    # colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    colors = ['#ff6384', '#ffce56', '#36a2eb']
    # explode = (0.1, 0.1, 0.1)  # explode a slice if required.
    # len(explode) = number of rows in df. Then add explode = explode below

    plt.pie(my_data, startangle=5, pctdistance=0.75, colors=colors,
            autopct='%1.0f%%', shadow=True, radius=1.3,
            # explode=explode,
            wedgeprops={"edgecolor": "black",
                        'linewidth': 1,
                        'antialiased': True}
            )
    plt.title(title, weight='bold')
    # draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle(
        (0, 0), 0.65, color='black', fc='white', linewidth=1.0)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.legend(my_labels, loc="upper right", fontsize=10,
               bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=0.95)

    plt.show()


def CreateMap(source_path, destination_path):

    # PROBLEM WITH LOCATION RIVIEERE DU REMPART - showing SMALL ISLANDS
    # ADD animations then deploy on github

    districts = json.load(open("mauritius-districts-geojson.json", 'r'))
    df = pd.read_csv(source_path, sep='\t')

    # create a log scale to deal with outliers in JobCount
    # get rid of 0s in column (log 0 invalid)
    df["JobCount"].replace(0, 1, inplace=True)
    df['log(JobCount)'] = np.log10(df['JobCount'])

    fig = px.choropleth(df, geojson=districts,
                        featureidkey='properties.name_1',
                        locations='Location',  # column in dataframe which contains districts names
                        # data from this column in dataframe is plotted
                        color='log(JobCount)',
                        color_continuous_scale="turbo",  # turbo or blackbody
                        range_color=[0, max(df['log(JobCount)'])],
                        hover_name='Location',
                        hover_data={
                            'JobCount': True,
                            'Location': False,
                            'log(JobCount)': False
                        },

                        # animation_frame="Location",
                        )
    fig.update_geos(fitbounds="locations")
    fig.update_layout(margin={"r": 300, "t": 50, "l": 300, "b": 50})
    fig.update_layout(
        title='May-July 2022 MU IT jobs by District',
        margin=dict(l=100, r=100, t=100, b=100),
        font=dict(size=10),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    # customise legend as well #
    fig.write_html(
        "choropleth-map-plotly-python.html")
    # fig.write_image(destination_path + ".pdf")  # .svg or .pdf

    fig.show()


def main():
    source_path = 'FilteredData/'  # folder containing filtered data
    destination_path = 'Charts/'  # folder to store charts

    CreateMap(source_path + "LocationData.csv",
              destination_path + "JobCountMap")

    HorizontalBarChart(source_path + "DatabaseData.csv",
                       destination_path + "DatabaseChart", '#5FE916', "Databases")
    HorizontalBarChart(source_path + "LanguageData.csv",
                       destination_path + "LanguageChart", 'orange',
                       "Programming languages")
    HorizontalBarChart(source_path + "LibrariesData.csv",
                       destination_path + "LibrariesChart", '#0FF0A3', "Libraries")
    HorizontalBarChart(source_path + "ToolsData.csv",
                       destination_path + "ToolsChart", '#a016e9', "Tools")
    HorizontalBarChart(source_path + "WebData.csv",
                       destination_path + "WebChart", '#F00F5C', "Web frameworks")

    # HorizontalLollipopChart(source_path + "WebData.csv",
    # destination_path + "WebLollipopChart", "Web frameworks")

    # add explanation for percentage in donut chart
    donutChart(source_path + "OSData.csv", destination_path +
               "OSChart", "Operating systems")
    donutChart(source_path + "CloudData.csv",
               destination_path + "CloudChart", "Cloud platforms")


main()
source_path = 'FilteredData/'  # folder containing filtered data
destination_path = 'Charts/'  # folder to store charts
# CreateMap(source_path + "LocationData.csv", destination_path + "JobCountMap")
