import dash_mantine_components as dmc
from dash import html

CARD_STYLE = dict(
    withBorder=True, shadow="sm", radius="md", style={"height": "400px"}
)


def get_layout():
    return html.Div(
        [
            dmc.Paper(
                [
                    dmc.Grid(
                        [
                            dmc.Col(
                                [
                                    dmc.Card(
                                        [
                                            dmc.TextInput(
                                                label="Введите что-нибудь",
                                                id="input",
                                            ),
                                            dmc.Button(
                                                "Первая кнопка", id="button1"
                                            ),
                                            dmc.Button(
                                                "Вторая кнопка", id="button2"
                                            ),
                                            html.Div(id="output"),
                                        ],
                                        **CARD_STYLE,
                                    )
                                ],
                                span=6,
                            ),
                            dmc.Col(
                                [
                                    dmc.Card(
                                        [html.Div("Верхняя правая карточка")],
                                        **CARD_STYLE,
                                    )
                                ],
                                span=6,
                            ),
                            dmc.Col(
                                [
                                    dmc.Card(
                                        [html.Div("Нижняя карточка")],
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
