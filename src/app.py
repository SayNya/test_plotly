from dash_extensions.enrich import (
    MultiplexerTransform,
    ServersideOutputTransform,
)

from src.infrastructure import application
from src.presentation.blueprints import bp

app: application.EncostDash = application.create(
    transforms=[ServersideOutputTransform(), MultiplexerTransform()],
    blueprints=[bp],
)

if __name__ == "__main__":
    app.run_server(debug=True)
