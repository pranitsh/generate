To contribute:

To test before you upload:
```sh
python -m venv env
pip install -e .
```

To format the code before you upload:
```sh
pip install -e .
black .
pylint /keyflare
```

To build the package and upload:
```sh
# Make sure to delete dist/ if necessary
pip install -e .
python setup.py sdist bdist_wheel
twine upload dist/*
```
