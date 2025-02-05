import panel as pn
import pandas as pd
import plotly.express as px


def build_app():
    pn.extension('plotly', sizing_mode="stretch_width")

    listings_df = pd.read_csv('https://ben-denham.github.io/python-eda/data/inside_airbnb_listings_nz_2023_09.csv')
    color_col_select = pn.widgets.Select(
        name='Colour',
        options=['room_type', 'review_scores_rating'],
    )

    def callback(color_col):
        fig = px.scatter_mapbox(listings_df, lon='longitude', lat='latitude',
                                color=color_col, zoom=3, height=530)
        fig.update_layout(mapbox_style='open-street-map')
        return fig

    return pn.Column(
        color_col_select,
        pn.bind(callback, color_col_select)
    )
