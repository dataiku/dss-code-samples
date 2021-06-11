import pytest
import dataikuapi


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


# Using pytest function to create 1 test case per test scenario
def pytest_generate_tests(metafunc):
    if "scenario_id" in metafunc.fixturenames:
        p_host = metafunc.config.getoption('--host')
        p_api = metafunc.config.getoption('--api')
        p_project = metafunc.config.getoption('--project')
        client = dataikuapi.DSSClient(p_host, p_api)
        project = client.get_project(p_project)
        list_scenarios = []
        for scenario in project.list_scenarios():
            if scenario["id"].startswith("TEST_"):
                print("Adding scenario to test :", scenario["id"])
                list_scenarios.append(scenario["id"])
        metafunc.parametrize("scenario_id", list_scenarios)
