import uuid
from typing import List, Optional

from errors import ImproperlyConfigured 
from pydantic import UUID4, BaseModel, ConfigDict, Field
from utils import get_logger 
#from pymongo import errors

from db.mongo import connection

_database = connection.get_database("scrabble")

logger = get_logger(__name__)


class BaseDocument(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    