from abc import ABCMeta, abstractmethod


class RequestI:
    __metaclass__ = ABCMeta

    def __init__(self, endpoint):
        """Asks given endpoint
        :param endpoint: Endpoint to be used for following scenario
        :type endpoint: :class:`easytest.endpoint.RestEndpoint`
        :returns: nothing
        :rtype: None
        """
        self.endpoint = endpoint

    @abstractmethod
    def execute_wrapper(self):
        raise NotImplemented


class ResponseI:
    __metaclass__ = ABCMeta


class GherkinScenarioI:
    __metaclass__ = ABCMeta

    user = None

    def __init__(self, scenario_suite):
        """Initializes concrete implementation of gherkin scenario handler

        :param scenario: Scenario object composed from scenario file
        :type scenario: :class:`gherkin_locust.scenario.ScenarioSuite`
        :returns: nothing
        :rtype: None
        """
        self.scenario_suite = scenario_suite
        self.scenario_steps_to_be_skipped_if_user_registered = []
        self.callbacks = {}

    def use_users(self, user):
        """Use user while tests

        :param user: user
        :type user: :class:`gherkin_locust.models.User`
        :returns: nothing
        :rtype: None
        """
        self.user = user

    def is_user_already_registered(self):
        """Checks if user already registered

        :returns: boolean
        :rtype: bool
        """

        return bool(self.user)

    def register_callback(self, event_name, executable):
        """Registers callback as to be executed after some event

        :param event_name: Event name
        :type event_name: str
        :param executable: executable function
        :type executable: callable
        :returns: self
        :rtype: self

        """

        self.callbacks[event_name] = executable

    def on_register(self, request_handler, user):
        """Calls callback in case of user registration

        :param request_handler: Request to be prepared
        :type request_handler: :class:`gherkin_locust.interface.RequestI`
        :param user: Users data returned by server
        :returns: self
        :rtype: self

        """
        self.callbacks['on_register'](request_handler, user)

    def is_to_be_skipped_step(self, step):
        """Checks if the step should be skipped according the status of user, etc

        :param step: Scenario step candidate to be skipped
        :type step: :class:`gherkin_locust.scenario.ScenarioStep`
        :returns: boolean
        :rtype: bool
        """
        if self.is_user_already_registered():
            for scenario_step in self.scenario_steps_to_be_skipped_if_user_registered:
                if scenario_step == step:
                    return True

    def skip_endpoint_if_user_registered(self, endpoint):
        """Checks if user already registered

        :param endpoint: Endpoint to be skipped if user already registered
        :type endpoint: :class:`easytest.endpoint.RestEndpoint`
        :returns: self
        :rtype: self
        """

        self.scenario_steps_to_be_skipped_if_user_registered.append(
            endpoint
        )
        return self

    @classmethod
    def make_object_from_scenario(cls, scenario_suite):
        """Make concrete scenario implementation from parsed gherkin scenario

        :param scenario: Scenario object composed from scenario file
        :type scenario: :class:`gherkin_locust.scenario.ScenarioSuite`
        :returns: Concrete implementation of handler to proceed scenario
        :rtype: :class:`gherkin_locust.adapters.interface.GherkinScenarioI`
        """
        return cls(scenario_suite)

    def interpret_scenario_using_matcher(self, matcher):
        """Uses scenario endpoint matcher

        :param matcher: Scenario endpoint matcher
        :type matcher: :class:`gherkin_locust.scenario.ScenarioEndpointMatcher`
        :returns: self
        :rtype: self
        """
        self.matcher = matcher
        return self

    @abstractmethod
    def start(self, *args):
        raise NotImplemented

    @abstractmethod
    def prepare_request(self, request_handler, concrete_request_handler):
        """
        :param request_handler: Request to be prepared
        :type request_handler: :class:`gherkin_locust.interface.RequestI`
        :returns: nothing
        :rtype: None
        """
        raise NotImplemented

    @abstractmethod
    def execute_request(self, request_handler, concrete_request_handler):
        """
        :param request_handler: Request to be prepared
        :type request_handler: :class:`gherkin_locust.interface.RequestI`
        :returns: nothing
        :rtype: None
        """
        raise NotImplemented

    @abstractmethod
    def analyze_response(self, request, concrete_request_handler, resp):
        """
        :param request: current request
        :type request: :class:`gherkin_locust.interface.RequestI`
        :param resp: response of the request
        :type resp: :class:`gherkin_locust.interface.ResponseI`
        :returns: self
        :rtype: self
        """
        raise NotImplemented
