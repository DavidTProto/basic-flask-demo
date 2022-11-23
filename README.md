# David Theobald - Basic Flask Demo

## How to run locally
You can run by cloning this repository and following the setup process below:

1) Create and activate a python3.8 environment
2) run `cd project-app` 
3) run `pip install .[test]`
4) run `python src/project_app/main.py`
5) Load http://localhost:5000


## Deployment
Alternatively, you can go to the below url where the app is hosted:

http://ec2-35-178-115-185.eu-west-2.compute.amazonaws.com/


## Testing
There are some testing utilities within this git repository. To get these to run,
follow the below steps:

1) Create and activate a python3.8 environment (if not done so already)
2) Run `cd project-app`
3) If not done so already, run `pip install .[test]`
3) Run `pytest test_app`


### Shortcuts
In this application, shortcuts have been made to speed up delivery:

1) Using a local sqlite database. The limitations of this is that the data won't
   persist after restart. Moreover, only one process can be used.
2) Testing isn't extensive and has only being implemented on to "/add" endpoint.
3) There is no DB Migration tool in effect so will be harder to make schema changes
4) This is not running on a production-ready server (like gunicorn)
5) For convenience, this app runs on all addresses but would result in security risks.
