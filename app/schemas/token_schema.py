
from typing import Annotated
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token : Annotated[str, Field(description="Access token for authentication.")]
    token_type : Annotated[str, Field(default="bearer", description="Type of the token.")]

