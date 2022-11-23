# David Theobald - Python Test

## How to run
You can run by cloning this repository and following the setup process below:

1) creating a python3.8 environment
2) run `pip install -r src/app/requirements.txt`
3) run `python src/app/main.py`

## Deployment
Alternatively, you can go to the below url where the app is hosted:

{place_holder for URL}

## Testing
There are some testing utilities within this git repository. To get these to run,
follow the below steps:

1) cd src
2) pip install -e .[test]
3) pytest test_app


### Shortcuts
In this application, shortcuts have been made to speed up delivery:

1) Using a local sqlite database. The limitations of this is that the data won't
   persist after restart. Moreover, only one process can be used.
2) Testing isn't extensive and has only being implemented on to "/add" endpoint.
3) There is no DB Migration tool in effect so will be harder to make schema changes
4) This is not running on a production-ready server (like gunicorn)
5) For convenience, this app runs on all addresses but would result in security risks.
