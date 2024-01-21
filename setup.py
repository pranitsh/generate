from setuptools import setup, find_packages

with open("README.md", encoding="utf8") as f:
    long_description = f.read()


def main():
    setup(
        name="generate",
        packages=find_packages(exclude=["tests*", "test_*", "*tests*"]),
        version="1.0.0",
        license="GNU",
        description="Recursive Prompting",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Pranit Shah",
        author_email="prsh006@gmail.com",
        url="https://www.pranitshah.cyou",
        download_url="https://github.com/pranitsh/generate",
        keywords=["AI", "GPT4All", "Prompt Engineering"],
        install_requires=[
            "nltk==3.8.1",
            "gpt4all==2.1.0",
        ],
        entry_points={
            "console_scripts": [
                "generate=generator.__main__:main",
            ]
        },
    )


if __name__ == "__main__":
    main()
