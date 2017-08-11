from json import JSONEncoder
import json
from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner
import warnings


class ScenarioJsonEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, (ScenarioStep, ScenarioSuite, SingleScenario)):
            return o.__dict__
        return super().default(o)


class ScenarioStep:

    keyword = None
    text = None
    type = None

    def __init__(self, params):
        """Initializes scenario step based on passed params in dictionary format

        :param params: Step parameters in dictionary format. Examples will be added later
        :type params: dict
        :returns: nothing
        :rtype: None

        """
        for key, val in params.items():
            if not hasattr(self, key):
                continue
            setattr(self, key, val)

    def __json__(self):
        return self.__dict__

    def __eq__(self, scenario_step):
        for key, val in self.__dict__.items():
            if getattr(scenario_step, key) != val:
                return False
        return True


class SingleScenario:

    name = None
    keyword = None
    examples = ()

    def __init__(self, params):
        """Initializes scenario based on passed params in dictionary format

        :param params: Scenario description and steps. Detailed format will be added later :) Not clear at the moment
        :type params: dict
        :returns: nothing
        :rtype: None

        """
        for key, val in params.items():
            if key == 'steps':
                continue
            if key == 'examples':
                self.examples = []
                for val1 in val:
                    fields = [
                        field['value']
                        for field in val1['tableHeader']['cells']
                    ]
                    for example in val1['tableBody']:
                        self.examples.append(
                            {
                                fields[field_idx]: cell['value']
                                for field_idx, cell in enumerate(example['cells'])
                            }
                        )
                continue
            if not hasattr(self, key):
                continue
            setattr(self, key, val)
        self.steps = []
        for step in params['steps']:
            self.steps.append(ScenarioStep(step))

    def __iter__(self):
        for step in self.steps:
            yield step


class ScenarioSuite:

    name = None
    keyword = None

    def __init__(self):
        self.scenarios = []

    @classmethod
    def load_scenario_from_gherkin_file(cls, files):
        """Load scenario from gherkin file

        :param file_path: Path to the file with gherkin scenarios
        :type file_path: str
        :returns: return ScenarioSuite described in file
        :rtype: :class:`gherkin_locust.scenario.ScenarioSuite`
        """
        suite = ScenarioSuite()
        suite.name = 'Load testing'
        suite.keyword = 'Load testing'
        for file in files:
            parsed_scenario = GherkinScenario.return_steps_from_file(file)
            scenarios = parsed_scenario['children']
            for scenario in scenarios:
                suite.add_scenario(SingleScenario(scenario))
        return suite

    @classmethod
    def make_suite_from_steps(cls, scenarios):
        """Make scenario suite from list of scenarios

        :param steps: List of scenarios in dictionary format
        :type steps: dict
        :returns: New scenario suite built using given scenarios
        :rtype: :class:`gherkin_locust.scenario.ScenarioSuite`
        """
        new_suite = cls()
        for scenario in scenarios:
            new_suite.add_scenario(SingleScenario(scenario))

        return new_suite

    def __iter__(self):
        for scenario in self.scenarios:
            yield scenario

    def add_scenario(self, scenario):
        """Add scenario user to be tested through

        :param scenario: SingleScenario
        :type scenario: :class:`gherkin_locust.scenario.SingleScenario`
        :returns: nothing
        :rtype: None

        """
        self.scenarios.append(scenario)


class GherkinScenario:

    @classmethod
    def return_steps_from_file(cls, file_path):
        parser = Parser()
        parsed = parser.parse(
            TokenScanner(open(file_path, 'r').read())
        )
        return parsed['feature']


class ScenarioEndpointMatcher:

    def __init__(self):
        self.endpoint_per_scenario_attrs = []

    def register_endpoint_for_scenario(self, endpoint, match_attrs):
        """Use endpoint for scenario

        :param endpoint: Endpoint to be used for following scenario
        :type endpoint: :class:`easytest.endpoint.RestEndpoint`
        :param match_attrs: Attributes of scenario to be matched. Please look into :class:`gherkin_locust.scenario.ScenarioStep`
        :type match_attrs: dict | :class:`gherkin_locust.scenario.ScenarioStep`
        :returns: self
        :rtype: self
        """
        scenario_step = match_attrs
        if not isinstance(scenario_step, ScenarioStep):
            scenario_step = ScenarioStep(match_attrs)
        self.endpoint_per_scenario_attrs.append(
            (endpoint, scenario_step)
        )

    def get_endpoint_for_scenario(self, scenario):
        """Get endpoint for scenario

        :param scenario: Scenario step
        :type scenario: :class:`gherkin_locust.scenario.ScenarioStep`
        :returns: Endpoint to be used for scenario passed as parameter
        :rtype: :class:`easytest.endpoint.RestEndpoint`
        """
        for endpoint, match_attrs in self.endpoint_per_scenario_attrs:
            if scenario == match_attrs:
                return endpoint
        warnings.warn('ENDPOINT NOT FOUND FOR ' + repr(scenario.__dict__))
