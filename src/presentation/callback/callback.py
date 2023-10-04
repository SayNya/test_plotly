from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

__all__ = ("update_div1", "update_div2")


@callback(
    Output("output", "children", allow_duplicate=True),
    State("input", "value"),
    Input("button1", "n_clicks"),
    prevent_initial_call=True,
)
def update_div1(value, click):
    if click is None:
        raise PreventUpdate

    return f"Первая кнопка нажата, данные: {value}"


@callback(
    Output("output", "children", allow_duplicate=True),
    State("input", "value"),
    Input("button2", "n_clicks"),
    prevent_initial_call=True,
)
def update_div2(value, click):
    if click is None:
        raise PreventUpdate

    return f"Вторая кнопка нажата, данные: {value}"
