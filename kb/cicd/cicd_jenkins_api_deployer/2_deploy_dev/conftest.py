import pytest


def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="default name")
    parser.addoption("--api", action="store", default="default name")
    parser.addoption("--api_service_id", action="store", default="default name")
    parser.addoption("--api_endpoint_id", action="store", default="default name")
    parser.addoption("--api_dev_infra_id", action="store", default="default name")

@pytest.fixture
def params(request):
    params = {'host': request.config.getoption('--host'),
              'api': request.config.getoption('--api'),
              'api_service_id': request.config.getoption('--api_service_id'),
              'api_endpoint_id': request.config.getoption('--api_endpoint_id'),
              'api_dev_infra_id': request.config.getoption('--api_dev_infra_id')
              }
    return params
