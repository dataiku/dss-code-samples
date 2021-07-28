# Retrieve all notebooks and provide session data for active notebooks

## Questions

How can I retrieve all jupyter notebooks from all of my projects as well as see session and kernal data for active notebooks?

## Answers

Starting in DSS 9, this is possible by utilizing list_jupyter_notebook() which can list all notebooks in a project or active ones. Using get_jupyter_notebook() along get_sessions() on a jupyter notebook will list session data and kernal data for an active notebook. list_jupyter_notebooks() and get_jupyter_notebook() calls were added in DSS 9 so an upgrade to DSS 9 is required to use those function calls. 
