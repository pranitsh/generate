from generator.generators import Generator
from enum import Enum

GeneratorType = Enum(
    "GeneratorType",
    {
        cls.__name__.upper().replace("GENERATOR", ""): cls
        for cls in Generator.__subclasses__()
    },
)


def from_string(name: str):
    return GeneratorType[name.upper()]
