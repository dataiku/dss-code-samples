import dataikuapi
import radon.raw as cc_raw
import radon.visitors as cc_visitors


def test_scenario(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])

    # Check that there is at least one scenario TEST_XXXXX & one TEST_SMOKE
    scenarios = project.list_scenarios()
    test_scenario = False
    smoketest_scenario = False
    for scenario in scenarios:
        if scenario["id"].startswith("TEST"):
            test_scenario = True
            if scenario["id"] == "TEST_SMOKE":
                smoketest_scenario = True
    assert test_scenario, "You need at least one test scenario (name starts with 'TEST_')"
    assert smoketest_scenario, "You need at least one smoke test scenario (name 'TEST_SMOKE')"

    
def test_coding_recipes_complexity(params):
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])

    recipes = project.list_recipes()
    for recipe in recipes:
        if recipe["type"] == "python":
            print(recipe)
            payload = project.get_recipe(recipe["name"]).get_settings().get_code()
            code_analysis = cc_raw.analyze(payload)
            print(code_analysis)
            assert code_analysis.loc < 100
            assert code_analysis.lloc < 50
            v = cc_visitors.ComplexityVisitor.from_code(payload)
            assert v.complexity < 21, "Code complexity of recipe " + recipe["name"] + " is too complex: " + v.complexity + " > max value (21)"
