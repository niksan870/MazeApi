import json
import re

from dtos.maze import MazeDTO
from dtos.user import UserDTO
from exceptions.exceptions import ValidationException
from utils.funcs import password_check


class BaseMapper:
    def __init__(self, dto):
        self.dto = dto
        self.fields = set(self.dto.__slots__)
        self._required_fields = set()

    def _map_2_dto(self, kwargs):
        if empty_fields := {k for k, v in kwargs.items() if v == ""}:
            raise ValidationException(
                f'Field(s) empty: {"".join(empty_fields)}'
            )
        if missing_fields := self.required_fields - set(kwargs):
            raise ValidationException(
                f'Field(s) missing: {"".join(missing_fields)}'
            )
        if missing_fields := set(kwargs) - self.required_fields:
            raise ValidationException(
                f'Field(s) redundant: {"".join(missing_fields)}'
            )
        return self.dto(**kwargs)

    def map_2_dto(self, kwargs):
        return self._map_2_dto(kwargs)

    @property
    def required_fields(self):
        return self._required_fields

    def db_2_payload(self, dto):
        return {field: getattr(dto, field) for field in self.fields}


class BaseUserMapper(BaseMapper):
    def __init__(self, dto):
        super().__init__(dto)
        self._required_fields = {"name", "password"}

    def map_2_dto(self, kwargs):
        dto = self._map_2_dto(kwargs)
        password_check(dto.password)
        return dto


class BaseMazeMapper(BaseMapper):
    def __init__(self, dto):
        super().__init__(dto)
        self._required_fields = {"entrance", "grid_size", "walls"}

    def map_2_dto(self, kwargs):
        if "gridSize" in kwargs:
            kwargs["grid_size"] = kwargs.pop("gridSize")
        dto = self._map_2_dto(kwargs)
        if not re.search(r"\d+x\d+", dto.grid_size):
            raise ValidationException(
                "Grid size format is wrong, int-x-int was expected"
            )
        if not re.search(r"[A-Z]\d", dto.entrance):
            raise ValidationException(
                "Entrance format is wrong, letter-int was expected"
            )
        dto.walls = json.dumps(dto.walls)
        return dto

    def db_2_payload(self, dto):
        return {
            field: getattr(dto, field)
            if field != "walls"
            else json.loads(getattr(dto, field))
            for field in self.fields
        }


UserMapper = BaseUserMapper(UserDTO)
MazeMapper = BaseMazeMapper(MazeDTO)
