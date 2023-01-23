from pydantic import BaseModel
from typing import Union
from numpy import ndarray
from enum import Enum


class DbCredentials(BaseModel):
    host: str = "127.0.0.1"
    port: int = 5432
    drivername: str = "postgresql+psycopg2"
    password: str
    username: str
    database: str


class RasterDataMatrix(BaseModel):
    var_name: str
    col_name: str
    array: ndarray

    class Config:
        arbitrary_types_allowed = True


class DatasetVarsMapping(BaseModel):
    column_name: str
    variable_name: str


class RegexConstantPartsMapping(BaseModel):
    variable_name: str
    value: Union[str, int, float]


class DataIngestionConstants(BaseModel):
    vars_mapping: list[DatasetVarsMapping]
    regex_constants: list[RegexConstantPartsMapping]


class UpsertIfRowExists(Enum):
    ignore = "ignore"
    update = "update"


class LoggingLevel(Enum):
    info = "info"
    warning = "warning"
    error = "error"
    debug = "debug"


class SupportedLogger(Enum):
    stdout = "stdout"
    email = "email"


class QueueItem(BaseModel):
    constants: DataIngestionConstants
    file_path: str
