from pydantic import BaseModel


class Config(BaseModel):
    calcgame_picfontsize: int = 42