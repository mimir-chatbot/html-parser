from pydantic import BaseModel


class Settings(BaseModel):
    relevant_selectors: str
    skip_selectors: str
