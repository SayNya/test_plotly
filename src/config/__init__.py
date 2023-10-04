from pathlib import Path

from pydantic import BaseConfig
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True

    root_dir: Path
    src_dir: Path

    class Config(BaseConfig):
        env_nested_delimiter: str = "__"
        env_file: str = ".env"


ROOT_PATH = Path(__file__).parent.parent

settings = Settings(
    root_dir=ROOT_PATH,
    src_dir=ROOT_PATH / "src",
)
