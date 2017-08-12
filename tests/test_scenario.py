import json
import os
from unittest import TestCase
from gherkin_locust.scenario import (
    SingleScenario, ScenarioStep, ScenarioSuite,
    ScenarioJsonEncoder, ScenarioEndpointMatcher
)
from easytest.endpoint import RestEndpoint
from gherkin_locust.exceptions import EndpointNotFoundForScenario


class ScenarioTestCase(TestCase):

    def test_gherkin(self):

        scenario = ScenarioSuite.load_scenario_from_gherkin_file(
            [os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                'test_feature.feature'
            ))]
        )
        self.assertEquals(
            json.loads(json.dumps(scenario, cls=ScenarioJsonEncoder)),
            {
                'keyword': 'Load testing',
                'name': 'Load testing',
                'scenarios': [{
                    "name": "Register with valid details",
                    "steps": [
                        {
                            "keyword": "Given ",
                            "type": "Step",
                            "text": "I am on the registration page"
                        },
                        {
                            "keyword": "And ",
                            "type": "Step",
                            "text": "I have completed the form with <email> <organisation> <password> and <passwordConfirmation>"
                        },
                        {
                            "keyword": "When ",
                            "type": "Step",
                            "text": "I have clicked on the register button"
                        },
                        {
                            "keyword": "Then ",
                            "type": "Step",
                            "text": "I will be logged in as <username>"
                        },
                        {
                            "keyword": "And ",
                            "type": "Step",
                            "text": "my account will be assigned the role of <role>"
                        }
                    ],
                    "keyword": "Scenario Outline",
                    "examples": [
                        {
                            "role": "Admin",
                            "username": "usernamea",
                            "organisation": "Bytes",
                            "password": "password1",
                            "email": "usernamea",
                            "passwordConfirmation": "password1"
                        },
                        {
                            "role": "Admin",
                            "username": "usernameb",
                            "organisation": "Bytes",
                            "password": "password2",
                            "email": "usernameb",
                            "passwordConfirmation": "password2"
                        },
                        {
                            "role": "Admin",
                            "username": "usernamec",
                            "organisation": "Bytes",
                            "password": "password3",
                            "email": "usernamec",
                            "passwordConfirmation": "password3"
                        },
                        {
                            "role": "Admin",
                            "username": "usernamed",
                            "organisation": "Bytes",
                            "password": "password4",
                            "email": "usernamed",
                            "passwordConfirmation": "password4"
                        },
                        {
                            "role": "Admin",
                            "username": "usernamee",
                            "organisation": "Bytes",
                            "password": "password5",
                            "email": "usernamee",
                            "passwordConfirmation": "password5"
                        }

                    ]
                }]
            }
        )


class ScenarioEndpointMatcherTestCase(TestCase):

    def setUp(self):
        self.scenario_step_attrs = {
            'keyword': 'keyword',
            'text': 'text',
            'type': 'type'
        }
        self.scenario_step = ScenarioStep(
            self.scenario_step_attrs
        )
        self.matcher = ScenarioEndpointMatcher()
        self.endpoint = RestEndpoint(url='/aaa/', method='POST')

    def test_success(self):
        self.matcher.register_endpoint_for_scenario(
            self.endpoint,
            self.scenario_step_attrs
        )
        self.assertEquals(
            self.matcher.get_endpoint_for_scenario(self.scenario_step),
            self.endpoint
        )

    def test_failure(self):
        self.matcher.register_endpoint_for_scenario(
            self.endpoint,
            {'dsdasds': 1}
        )
        self.matcher.get_endpoint_for_scenario(self.scenario_step)
