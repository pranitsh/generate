from generate import ai
from generate import steps
from generate.report import Report
from generate import utils
from datetime import datetime


class Generator:
    """Forces a certain report type."""

    logger = utils.create_logger()

    def __init__(self, prompt: str, name: str, api_type="gpt4all"):
        if api_type == "gpt4all":
            self.cli = ai.Gpt4allAPI()
        self.prompt = prompt
        self.name = name

    def generate_promptStep(self) -> steps.Step:
        yield None

    def process_step(self, step: steps.Step, variables: dict[str, str]) -> str:
        self.logger.debug("Unformatted inputs: " + str(step.inputs))
        self.logger.debug("Old variables: " + str(variables))
        formatted = step.format_inputs(step.inputs, variables)
        self.logger.debug("Formatted inputs: " + str(formatted))
        results = self.cli.process(formatted, step.template)
        results = step.processing(results)
        self.logger.debug("Processed results: " + str(results))
        new_variables = step.match_outputs(results, step.outputs, variables)
        self.logger.debug("New variables: " + str(new_variables))
        results = step.flatten(["## " + step.title] + results)
        return results, new_variables

    def interpret(self) -> Report:
        report = Report(self.prompt, text=["# " + self.prompt], category=self.name)
        variables: dict[str, str] = {"prompt": self.prompt}
        for step in self.generate_promptStep():
            report.prompts += [step]
            results, variables = self.process_step(step, variables)
            report.text += step.flatten(results)

        report.end = datetime.now()
        return report


class BasicGenerator(Generator):
    def generate_promptStep(self) -> steps.Step:
        yield steps.Step("Initial", ["prompt"], ["prompt_answer"])


class CodeGenerator(Generator):
    def generate_promptStep(self) -> steps.Step:
        yield steps.Step("Initial", ["prompt"], ["prompt_answer"])
        yield steps.CodeStep(
            "Code Generation",
            [
                "prompt_answer",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
            ["code_answer"],
        )
        yield steps.Step(
            "Examples Generation",
            [
                "code_answer",
                "Give a number of useful examples that include the resulting output from the code above.",
            ],
            [
                "example_answer",
            ],
        )
        yield steps.ListStep(
            "Math Generation",
            [
                "prompt",
                "code_answer",
                "List at least 5 mathematical improvements and additions on the code above without writing any code.",
            ],
            [
                "math_questions",
            ],
        )

        yield steps.ListStep(
            "Improvement Suggestions",
            [
                "prompt",
                "code_answer",
                "List a number of improvements to the above code.",
            ],
            [
                "improvements",
            ],
        )
        yield steps.ListStep(
            "Coding Outline",
            [
                "prompt",
                "code_answer",
                [
                    "List a coding outline for testing the code above.",
                    "List a coding outline for adding a frontend interface with tkinter and python to the code above.",
                    "List a coding outline for adding a frontend framework with kivy and python.",
                    "List a coding outline for adding a backend API with flask and python to the code above.",
                    "List a coding outline for adding database management with python to the code above.",
                    "List a coding outline for adding authentication with google through python to the code above.",
                    "List a coding outline for adding artificial intelligence with python to the code above.",
                ],
            ],
            [
                "coding_outline_model",
                "coding_outline_tkinter",
                "coding_outline_kivy",
                "coding_outline_flask",
                "coding_outline_db",
                "coding_outline_authentication",
                "coding_outline_ai",
            ],
        )
        yield steps.ListStep(
            "Error Detection",
            [
                "prompt",
                "code_answer",
                "List a number of errors or potential errors for the above code.",
            ],
            ["errors"],
        )
        yield steps.Step(
            "General Answers from Prompt Generation",
            [
                "code_answer",
                "Item:",
                "math_questions",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "General Answers from Prompt Generation",
            [
                "code_answer",
                "Item:",
                "improvements",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "General Answers from Prompt Generation",
            [
                "code_answer",
                "Item:",
                "errors",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "Coding Outline",
            [
                "code_answer",
                "Item:",
                "coding_outline_model",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "Coding Outline",
            [
                "code_answer",
                "Item:",
                "coding_outline_tkinter",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "Coding Outline",
            [
                "code_answer",
                "Item:",
                "coding_outline_kivy",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "Coding Outline",
            [
                "code_answer",
                "Item:",
                "coding_outline_flask",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "Coding Outline",
            [
                "code_answer",
                "Item:",
                "coding_outline_db",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "Coding Outline",
            [
                "code_answer",
                "Item:",
                "coding_outline_authentication",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )
        yield steps.Step(
            "Coding Outline",
            [
                "code_answer",
                "Item:",
                "coding_outline_ai",
                "Turn the above item into a python script with a single class and distinct functions.",
            ],
        )



class AdaptiveGenerator(Generator):
    def generate_promptStep(self) -> steps.Step:
        while True:
            try:
                step_type = (
                    input(
                        "What type of step do you want? { step, liststep, codestep, filestep, exit } [step]: "
                    )
                    or "step"
                )
                if step_type == "step":
                    break
                step_title = (
                    input("What is the title of the step? [Initial]: ") or "Initial"
                )
                step_inputs = input(
                    "What inputs do you want? (Use '+' to split items) [ prompt'] ]: "
                ).split("+") or ["prompt"]
                step_outputs = input(
                    "What outputs do you want? (Use '+' to split items) [ ['prompt_answer'] ]: "
                ).split("+") or ["prompt_answer"]
                step_template = (
                    input("What custom instruction do you want? ['']: ") or ""
                )
                if step_type == "step":
                    yield steps.Step(
                        step_title, step_inputs, step_outputs, step_template
                    )
                elif step_type == "liststep":
                    yield steps.ListStep(
                        step_title, step_inputs, step_outputs, step_template
                    )
                elif step_type == "codestep":
                    yield steps.CodeStep(
                        step_title, step_inputs, step_outputs, step_template
                    )
                elif step_type == "feilstep":
                    yield steps.FileStep(
                        step_title, step_inputs, step_outputs, step_template
                    )
            except KeyboardInterrupt:
                pass
