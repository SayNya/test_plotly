from typing import Iterable

from dash_extensions.enrich import DashProxy, DashTransform

from src.presentation.callback.callback import *  # noqa

__all__ = ("create", "EncostDash")

from src.presentation.layout.layout import get_layout


class EncostDash(DashProxy):
    def __init__(self, transforms: Iterable[DashTransform], **kwargs):
        self.app_container = None
        super().__init__(
            transforms=transforms,
            **kwargs,
        )


def create(transforms: Iterable[DashTransform]) -> EncostDash:
    app = EncostDash(transforms=transforms, name=__name__)
    app.layout = get_layout()
    return app
