import cmd
from datetime import datetime
from generate.task import Task
from generate import utils


class Organizer(cmd.Cmd):
    prompt = "(prompt-organizer) "
    intro = "Welcome to the Prompt Organizer. Type help or ? to list commands."
    logger = utils.create_logger()

    def __init__(self):
        super(Organizer, self).__init__()

    def do_tasks(self, empty: str | int = ""):
        """Logs all tasks, then removes the tasks from the list based on the provided numbers."""
        tasks = list(utils.manage_set("task"))
        if isinstance(empty, int):
            del tasks[empty]
        elif isinstance(empty, str):
            if empty and empty.isnumeric():
                del tasks[int(empty.strip())]
        to_print = ""
        tasks.sort(key=lambda task: task.due_date)
        for idx, a_task in enumerate(tasks):
            to_print += f"\n{idx}. {a_task}"
        self.logger.critical(to_print)
        utils.manage_set("task", set(tasks))

    def do_reports(self, empty: str | int = ""):
        """Logs all tasks, then removes the tasks from the list based on the provided numbers."""
        reports = list(utils.manage_set("report"))
        if isinstance(empty, int):
            del reports[empty]
        elif isinstance(empty, str):
            if empty and empty.isnumeric():
                del reports[int(empty.strip())]
        to_print = ""
        for idx, a_report in enumerate(reports):
            to_print += f"\n{idx}. {a_report}"
        self.logger.critical(to_print)
        utils.manage_set("report", set(reports))

    def do_create_prompt(self, args=""):
        """Create a prompt that will be added to the prompt list and sorted for the next task."""
        parser = utils.CustomArgumentParser(
            prog="create_prompt", description="Create a new prompt."
        )
        parser.add_argument(
            "--prompt", default="How do I make coffee?", help="The prompt text"
        )
        parser.add_argument(
            "--datetime",
            default=datetime.now(),
            type=lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"),
            help="Datetime for the task in format YYYY-MM-DD HH:MM:SS",
        )
        parser.add_argument(
            "--enum",
            default="BASIC",
            help="The type of enum. { 'BASIC', 'AI', 'CODE', 'APPLICATION', 'REPORT', 'ADAPTIVE' }",
        )
        parser.add_argument(
            "--generator",
            default="gpt4all",
            help="The type of generator. { 'gpt4all', 'openai' }",
        )
        if isinstance(args, str) or isinstance(args, list[str]):
            args = parser.parse_args(args)
            to_add = Task(args.prompt, args.datetime, args.enum, args.generator)
        else:
            to_add = None
        if to_add:
            new_set = utils.manage_set("task")
            new_set.add(to_add)
            utils.manage_set("task", new_set)
        self.do_tasks()

    def do_complete(self, empty=""):
        """Mark a prompt as complete. This will add the prompt to Generated.md. Usage: complete"""
        tasks = list(utils.manage_set("task"))
        tasks.sort(key=lambda task: task.due_date)
        if tasks:
            current_task = tasks[0]
            report = current_task.get_generator().interpret()
            new_set = utils.manage_set("report")
            new_set.add(report)
            utils.manage_set("report", new_set)
            self.logger.critical(report)
            self.do_tasks(0)

    def do_auto_complete(self, line=""):
        """Automatically and continuously run the complete command. Usage: auto_complete"""
        self.logger.warn("Starting automatic completion. Press Ctrl-C to stop.")
        try:
            while self.current_task:
                self.do_complete(None)
        except KeyboardInterrupt:
            self.logger.warn("\nAutomatic completion stopped.")

    def do_exit(self, line=""):
        """Exit the Prompt Organizer. This command will terminate the program and return to the system command prompt."""
        self.logger.debug("Exiting the Prompt Organizer.")
        return True


if __name__ == "__main__":
    Organizer().cmdloop()
