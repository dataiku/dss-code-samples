import pytest


def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="default name")
    parser.addoption("--api", action="store", default="default name")
    parser.addoption("--project", action="store", default="default name")


@pytest.fixture
def params(request):
    params = {'host': request.config.getoption('--host'),
              'api': request.config.getoption('--api'),
              'project': request.config.getoption('--project')
              }
    return params
