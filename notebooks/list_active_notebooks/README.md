# Retrieve all notebooks and provide session data for active notebooks

## Questions

How can I retrieve all Jupyter notebooks from all of my projects as well as see session and kernal data for active notebooks?

## Answers

Starting in DSS 9, this is possible by utilizing `list_jupyter_notebook()` which can list all notebooks in a project or active ones. Using `get_jupyter_notebook()` along with `get_sessions()` on a Jupyter notebook will list session data and kernel data for an active notebook. 

