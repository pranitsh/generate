import re
import nltk
import os

nltk.download("popular", quiet=True)


class Step:
    """
    A prompting step.

    Arguments:
        title: str
        inputs: list[list[str] | str] (only two layers of lists)
        output: list[str]
        processing: function
    """

    def __init__(
        self,
        title: str = "",
        inputs: list[str | list[str]] = [],
        outputs: list = [],
        template: str = "Respond as an expert teacher would for the material at hand. Mainly, assume your work will be integrated in a larger one, so do not use intros and conclusions, use plenty of headers (`###`) to split each topic, and (most importantly) make sure to follow the prompt's categorization if provided. If you see any code, show a variety of examples regarding that code. If you see a lesson transcript/documentation, reformat the text while correcting any transcribing errors for the purpose of studying.",
    ):
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.template = template

    def format_inputs(self, inputs: list[str], variables: dict[str, str]) -> list:
        formatted = []
        for item in inputs:
            if type(item) == str:
                formatted.append(variables.get(item, item))
            elif type(item) == list:
                subitems = []
                for subitem in item:
                    subitems.append(variables.get(subitem, subitem))
                formatted.append(subitems)
        return formatted

    def match_outputs(self, results: list, outputs: list, variables: dict):
        if len(outputs) == 1:
            if len(results) == 1:
                variables[outputs[0]] = results[0]
            elif len(results) > 1:
                variables[outputs[0]] = results[0]
        else:
            for output_str, result_str in zip(outputs, results):
                variables[output_str] = result_str
        return variables

    def processing(self, responses: list[str]) -> list[str | list[str]]:
        to_return = []
        for response in responses:
            to_return.append(self.processing_text(response))
        return to_return

    def processing_text(self, response: str) -> str:
        return response

    @staticmethod
    def flatten(lst):
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(Step.flatten(item))
            else:
                result.append(item)
        return result

    def __str__(self) -> str:
        return f"step.Step('{self.title}', {self.inputs}, {self.outputs}, '{self.template}')"


class FileStep(Step):
    def format_inputs(self, inputs: list[str], variables: dict[str, str]) -> list:
        formatted = []
        for item in inputs:
            if type(item) == str:
                item = variables.get(item, item)
                if os.path.exists(item):
                    with open(item, "r", encoding="utf8") as file:
                        formatted.append(file.read())
                else:
                    formatted.append(item)
            elif type(item) == list:
                subitems = []
                for subitem in item:
                    subitem = variables.get(subitem, subitem)
                    if os.path.exists(subitem):
                        with open(subitem, "r", encoding="utf8") as file:
                            subitems.append(file.read())
                    else:
                        subitems.append(subitem)
                formatted.append(subitems)
        return formatted

    def __str__(self) -> str:
        return f"step.FileStep('{self.title}', {self.inputs}, {self.outputs}, '{self.template}')"


class ListStep(Step):
    def __init__(
        self,
        title: str = "",
        inputs: list[str | list[str]] = [],
        outputs: list = [],
        template: str = "Respond as an expert Engineer would for the material at hand. Mainly, assume your work will be integrated in a larger one, so do not use intros and conclusions, use only one header (`###`), and (most importantly) make sure to use only one list with either numbers or bullets for your entire response. Be as thorough as possible.",
    ):
        super().__init__(title, inputs, outputs, template)

    # override
    def processing_text(self, response: str) -> str:
        patterns = [
            r"[\s,#,\\]*[0-9]+\.",  # For numbered lists
            r"[\s,#,\\]*[a-z]+\.",  # For alphabetically ordered lists
            r"[\s,#,\\]*[+,\-,*]+",  # For bullet points lists (plus, minus, asterisk)
        ]
        pattern = ""
        lines = response.strip().split("\n")
        for line in lines:
            for try_pattern in patterns:
                if re.match(pattern, line):
                    pattern = try_pattern
                    break
            if pattern:
                break

        if pattern:
            list_items = re.split(pattern, response)
            list_items = [item.strip() for item in list_items if item.strip()]
            return list_items

        return response

    def __str__(self) -> str:
        return f"step.ListStep('{self.title}', {self.inputs}, {self.outputs}, '{self.template}')"


class CodeStep(Step):
    def __init__(
        self,
        title: str = "",
        inputs: list[str | list[str]] = [],
        outputs: list = [],
        template: str = "Respond as an expert Software Engineer would for the material at hand. Mainly, assume your work will be integrated in a larger one, so plan out your work, do not use intros and conclusions, use a header (`###`), and (most importantly) make sure your code is following the points in the prompt and only in one place. Be as thorough as possible.",
    ):
        super().__init__(title, inputs, outputs, template)

    def processing_text(self, response: str) -> str:
        code_blocks = re.findall(r"```(.*?)```", response, re.DOTALL)
        cleaned_code_blocks = []

        # Keep 'python' in the first block and remove it from others
        for idx, block in enumerate(code_blocks):
            if idx == 0:
                cleaned_code_blocks.append(block)
            else:
                cleaned_code_blocks.append(block.replace("python", ""))

        combined_code_block = "\n".join(
            cleaned_code_blocks
        ).strip()  # Join all the code blocks with a newline separator
        if combined_code_block:
            return "```" + combined_code_block + "```"
        else:
            return response

    def __str__(self) -> str:
        return f"step.CodeStep('{self.title}', {self.inputs}, {self.outputs}, '{self.template}')"


class SentenceStep(Step):
    def processing_text(self, response: str) -> str:
        return nltk.tokenize.sent_tokenize(response)

    def __str__(self) -> str:
        return f"step.SentenceStep('{self.title}', {self.inputs}, {self.outputs}, '{self.template}')"
