from pydantic import BaseModel


class Msg(BaseModel):
    text: str