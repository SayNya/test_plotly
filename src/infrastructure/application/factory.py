from typing import Iterable

from dash import html
from dash_extensions.enrich import DashBlueprint, DashProxy, DashTransform

__all__ = ("create", "EncostDash")


class EncostDash(DashProxy):
    def __init__(self, transforms: Iterable[DashTransform], **kwargs):
        self.app_container = None
        super().__init__(
            transforms=transforms,
            **kwargs,
        )


def create(
    transforms: Iterable[DashTransform], blueprints: Iterable[DashBlueprint]
) -> EncostDash:
    app = EncostDash(transforms=transforms, name=__name__)
    app.layout = html.Div([bp.embed(app) for bp in blueprints])
    return app
