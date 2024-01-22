# generate

`Generate` is a python-based recursive prompting tool for GPT4All, attempting to achieve greater flexibility, caching, and usability than similar prompting tools. It offers the ability to create multiple tasks and performing them conveniently, extending class `generator` for creating recursive prompting structures for your use case, and a number of pre- and post-processing steps for convenience. The source code is readable and examples are provided in the code under `generator.generators`.

Interested? Test the code quickly by running the below (requires python and git):

```sh
# Suggested: create an environment.
python -m venv env
# activate it as per your ecosystem
pip install git+https://github.com/pranitsh/generate.git
generate
```

The code is free and open source (GNU license), suitable for both CPU and GPUs, and has been tested personally to create dozens of reports from scratch. Leave it running overnight and have a couple of ideas to test out the next morning at your convenience. Send an issue and I'll definitely respond and add more features!


Feature:

+ Allows for adaptive, code-based, and basic recursive prompting generators.
+ Offered steps include processing files in the prompts, lists in the responses, code in responses, and a basic step with convenient functions for overriding for flexibility.
+ Outputs, if there are multiple, will be matched to results, else if there is one, outputs will get the entire result.
+ Create tasks and have them sorted by due_date for determining importance.
+ A convenient cli that doubles as a programmatic interface.
