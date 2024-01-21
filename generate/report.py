from generate.steps import Step
from datetime import datetime


class Report:
    """
    A Report representation.

    Attributes:
        title: str - The title of the report.
        start: datetime - The start time of the report.
        end: datetime - The end time of the report.
        promptList: list[PromptStep] - A list of PromptStep objects related to the report.
        text: list[str] - A list of text entries in the report.
    """

    def __init__(
        self,
        title: str = "",
        start: datetime = datetime.now(),
        end: datetime = datetime.now(),
        prompts: list[Step] = [],
        text: list[str] = [],
        category: str = "",
    ):
        self.title = title
        self.start = start
        self.end = end
        self.prompts = prompts
        self.text = text
        self.category = category

    def __str__(self) -> str:
        to_return = f"Report({self.title}, datetime.timedelta={self.end - self.start}, {self.category})"
        display_steps = "\nyield ".join([str(step) for step in self.prompts])
        to_return += f"\n\nPrompts:\nyield {display_steps})"
        display_text = "\n\n".join(self.text)
        to_return += f"\n\nText:\n{display_text}"
        return to_return
