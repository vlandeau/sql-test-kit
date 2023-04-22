from dataclasses import dataclass


@dataclass
class Column:
    name: str
    type: str
    description: str = ""
