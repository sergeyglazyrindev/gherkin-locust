import sys
from easytest.request import BaseRequest
import os
from easytest.openapi.config import OpenApiConfig
from gherkin_locust.scenario import (
    SingleScenario, ScenarioStep, ScenarioSuite,
    ScenarioJsonEncoder, ScenarioEndpointMatcher
)
from gherkin_locust.adapters.locust import LocustScenarioConcreteImplementation
from easytest.endpoint import RestEndpoint
from gherkin_locust.adapters.locust import LocustMixin
from locust import HttpLocust, TaskSet
import mock
from easytest.openapi.data_generators import (
    DataGenerator,
    BaseCustomDataGenerator
)


generator = DataGenerator()


class CustomizedGeneratorForFieldEmail(BaseCustomDataGenerator):

    @classmethod
    def generate_if_needed_data_based_on_context(cls, field, request_context):
        if field.name == 'email':
            return 'example@example.com'


generator.register_specific_generator(CustomizedGeneratorForFieldEmail)


class Request(BaseRequest):

    def __init__(self):
        pass

    def force_authenticate_user(self, user):
        pass

    def do_http_request(self):
        pass

    def check_result_after_put(self, testvisitor, resp):
        raise NotImplemented

    def check_result_after_list(self, testvisitor, resp):
        raise NotImplemented

    def check_result_after_get(self, testvisitor, resp):
        raise NotImplemented

    def check_result_after_delete(self, testvisitor, resp):
        raise NotImplemented

    def check_result_after_post(self, testvisitor, resp):
        raise NotImplemented


config = OpenApiConfig(os.path.join(
    os.path.dirname(__file__),
    'django/project/api.json',
))


def on_registered_user(user):
    print('AAAAAAAAAA111')


class UserBehavior(LocustMixin, TaskSet):

    def on_start(self):
        scenario = ScenarioSuite.load_scenario_from_gherkin_file(
            [os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                'test_feature.feature'
            ))]
        )
        locust_implementation = LocustScenarioConcreteImplementation.make_object_from_scenario(
            scenario
        )
        matcher = ScenarioEndpointMatcher()
        registration_scenario_step = ScenarioStep({
            'keyword': 'Given ',
            'text': 'I am on the registration page',
            'type': 'Step'
        })
        locust_implementation.skip_endpoint_if_user_registered(
            registration_scenario_step
        )
        matcher.register_endpoint_for_scenario(RestEndpoint(
            **{'url': '/api/core/register/', 'method': 'POST'}
        ), registration_scenario_step)
        matcher.register_endpoint_for_scenario(RestEndpoint(
        ), ScenarioStep({
            'keyword': 'And ',
            'text': 'I have completed the form with <email> <organisation> <password> and <passwordConfirmation>',
            'type': 'Step'
        }))
        matcher.register_endpoint_for_scenario(RestEndpoint(
        ), ScenarioStep({
            'keyword': 'When ',
            'text': 'I have clicked on the register button',
            'type': 'Step'
        }))
        matcher.register_endpoint_for_scenario(RestEndpoint(
        ), ScenarioStep({
            'keyword': 'Then ',
            'text': 'I will be logged in as <username>',
            'type': 'Step'
        }))
        matcher.register_endpoint_for_scenario(RestEndpoint(
        ), ScenarioStep({
            'keyword': 'And ',
            'text': 'my account will be assigned the role of <role>',
            'type': 'Step'
        }))
        locust_implementation.interpret_scenario_using_matcher(
            matcher
        )
        locust_implementation.register_callback('on_register', on_registered_user)
        with mock.patch.object(locust_implementation, 'execute_request'):
            locust_implementation.start(self)

    def register(self):
        fixture = config.generate_fixture_for(
            generator,
            '/api/core/users/',
            'post',
            Request()
        )
        resp = self.client.post('/api/core/users/', fixture)
        if resp.status_code > 0 and resp.status_code != 201:
            sys.exit(1)
        self.login(fixture)
        return resp

    def login(self, fixture):
        fixture['password'] = '123456'
        resp = self.client.post('/api/core/login/', fixture)
        if resp.status_code > 0 and resp.status_code != 200:
            sys.exit(1)
        return resp


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
