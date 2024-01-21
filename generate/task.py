from datetime import datetime
from generate import enum


class Task:
    """
    A Task representation.

    Attributes:
        prompt: str - A description of the task.
        due_date: date - The due date for the task.
        category: str - The category or type of the task.
        pathList: list - A list of file paths related to the task.
    """

    def __init__(
        self,
        prompt: str = "",
        due_date: datetime = datetime.now(),
        category: str = "BASIC",
        generator: str = "gpt4all",
    ):
        self.prompt = prompt
        self.due_date = due_date
        self.category = enum.from_string(category)
        self.generator = generator

    def get_generator(self):
        return self.category.value(self.prompt, self.category.name, self.generator)

    def __str__(self) -> str:
        return f"Task({self.prompt}, {self.due_date}, {self.category.name}, {self.generator})"
