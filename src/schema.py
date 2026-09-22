from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

HTTPS_URL = r"^https://\S+$"

class Book(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    title: str = Field(min_length=1)
    product_url: str = Field(pattern=HTTPS_URL)
    price_text: str
    price_gbp: float = Field(gt=0, strict=True)
    availability_text: str
    rating_text: str
    description: str | None = None
    source_page: str = Field(pattern=HTTPS_URL)
    fetched_at: datetime