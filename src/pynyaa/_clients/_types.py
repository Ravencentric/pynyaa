from pydantic import Field
from typing_extensions import Annotated

SearchLimit = Annotated[int, Field(gt=0, le=75)]
