from dash_extensions.enrich import (
    MultiplexerTransform,
    ServersideOutputTransform,
)

from src.infrastructure import application

app: application.EncostDash = application.create(
    transforms=[ServersideOutputTransform(), MultiplexerTransform()]
)

if __name__ == "__main__":
    app.run_server(debug=True)
