import sqlite3

import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import Patch, dcc, html
from dash_extensions.enrich import DashBlueprint, Input, Output, State

__all__ = ("bp",)

CARD_STYLE = dict(
    withBorder=True, shadow="sm", radius="md", style={"height": "600px"}
)

with sqlite3.connect("../testDB.db") as conn:
    df = pd.read_sql_query("SELECT * FROM sources", conn)

FILTER_VALUES = [
    {"value": reason, "label": reason} for reason in df["reason"].unique()
]
COLORS = dict(zip(df["reason"].unique(), df["color"].unique()))
LABELS = {label: label.capitalize().replace("_", " ") for label in df.columns}
GANTT_HOVER_DATA = [
    "state",
    "reason",
    "duration_min",
    "shift_day",
    "period_name",
    "operator",
]

pie_chart = px.pie(
    df,
    values="duration_min",
    names="reason",
    color="reason",
    color_discrete_map=COLORS,
    labels=LABELS,
)

gantt_chart = px.timeline(
    df,
    x_start="state_begin",
    x_end="state_end",
    y="endpoint_name",
    color="reason",
    color_discrete_map=COLORS,
    labels=LABELS,
    custom_data=GANTT_HOVER_DATA,
)
gantt_chart.update_layout(showlegend=False)
gantt_chart.update_traces(
    hovertemplate=(
        "<br>Состояние - <b>%{customdata[0]}</b>"
        "<br>Причина - <b>%{customdata[1]}</b>"
        "<br>Начало - <b>%{base|%H:%M:%S</b> (%d.%m)}"
        "<br>Длительность - <b>%{customdata[2]:.2f}</b> min."
        "<br>"
        "<br>Сменный день - <b>%{customdata[3]|%d.%m.%Y}</b>"
        "<br>Смена - <b>%{customdata[4]}</b>"
        "<br>Оператор - <b>%{customdata[5]}</b><extra></extra>"
    )
)


bp = DashBlueprint()

bp.layout = html.Div(
    [
        dmc.Paper(
            [
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dmc.Card(
                                    [
                                        html.H1(
                                            f"Клиент: {df['client_name'][0]}"
                                        ),
                                        dmc.Text(
                                            f"Сменный день: {df['shift_day'][0]}"
                                        ),
                                        dmc.Text(
                                            f"Точка учёта: {df['endpoint_name'][0]}"
                                        ),
                                        dmc.Text(
                                            f"Начало периода: {df['state_begin'].min()}"
                                        ),
                                        dmc.Text(
                                            f"Конец периода: {df['state_end'].max()}"
                                        ),
                                        dmc.MultiSelect(
                                            id="reason-multi-select",
                                            data=FILTER_VALUES,
                                            searchable=True,
                                            clearable=True,
                                        ),
                                        dmc.Button(
                                            "Фильтровать", id="filter-button"
                                        ),
                                    ],
                                    **CARD_STYLE,
                                )
                            ],
                            span=6,
                        ),
                        dmc.Col(
                            [
                                dmc.Card(
                                    [
                                        html.H4(
                                            "Круговая диаграмма причин состояний"
                                        ),
                                        dcc.Graph(
                                            id="circle-chart", figure=pie_chart
                                        ),
                                    ],
                                    **CARD_STYLE,
                                )
                            ],
                            span=6,
                        ),
                        dmc.Col(
                            [
                                dmc.Card(
                                    [
                                        html.H4(
                                            "Диаграмма Ганта длительностей причин состояний"
                                        ),
                                        dcc.Graph(
                                            id="gantt-chart",
                                            figure=gantt_chart,
                                        ),
                                    ],
                                    **CARD_STYLE,
                                )
                            ],
                            span=12,
                        ),
                    ],
                    gutter="xl",
                )
            ]
        )
    ]
)


@bp.callback(
    Output("circle-chart", "figure"),
    Input("filter-button", "n_clicks"),
    State("reason-multi-select", "value"),
)
def pie_filtering(_, filtered_reasons):
    series = (
        df[df.reason.isin(filtered_reasons)]["reason"].value_counts()
        if filtered_reasons
        else df["reason"].value_counts()
    )

    df_result = pd.DataFrame(series)
    df_result = df_result.reset_index()
    df_result.columns = ["reason", "total"]

    fig = px.pie(df_result, values="total", names="reason")
    return fig


@bp.callback(
    Output("gantt-chart", "figure"),
    Input("filter-button", "n_clicks"),
    State("reason-multi-select", "value"),
    State("gantt-chart", "figure"),
    prevent_initial_call=True,
)
def gantt_filtering(_, filtered_reasons, fig):
    filtered_traces = [
        i
        for i in range(len(fig["data"]))
        if fig["data"][i]["name"] in filtered_reasons
    ]
    patched_fig = Patch()
    for i in range(len(fig["data"])):
        patched_fig["data"][i]["opacity"] = 1 if i in filtered_traces else 0.2
    return patched_fig
