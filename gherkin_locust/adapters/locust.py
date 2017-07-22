from functools import partial
from .interface import (
    GherkinScenarioI,
    RequestI,
    ResponseI
)


class LocustRequest(RequestI):

    def __init__(self, locust_request_handler, endpoint):
        self.locust_request_handler = locust_request_handler
        self.endpoint = endpoint

    def execute_wrapper(self):
        def wrapper(locust_request, locust):
            if locust_request.endpoint.is_able_to_prepare_request():
                locust_request.endpoint.prepare_request(locust)
            else:
                locust_request.locust_request_handler.prepare_request(
                    locust_request, locust
                )
            if locust_request.endpoint.is_executable():
                resp = locust_request.endpoint.execute(locust)
            else:
                resp = locust_request.locust_request_handler.execute_request(
                    locust_request, locust
                )
                # resp = self.execute_request(request_handler)
            if locust_request.endpoint.is_able_to_analyze_response():
                locust_request.endpoint.analyze_response(locust, resp)
            else:
                locust_request.locust_request_handler.analyze_response(
                    locust_request, locust, resp
                )

        return partial(wrapper, self)


class LocustResponse(ResponseI):
    pass


class LocustScenarioConcreteImplementation(GherkinScenarioI):

    def start(self, locust):
        if not self.is_user_already_registered():
            user = locust.register()
            self.on_register(user)
        else:
            user = locust.login()
        for scenario in self.scenario_suite:
            for step in scenario:
                if self.is_to_be_skipped_step(step):
                    continue
                endpoint = self.matcher.get_endpoint_for_scenario(
                    step
                )
                request_handler = LocustRequest(self, endpoint)
                locust.add_task(
                    request_handler.execute_wrapper(), endpoint.priority
                )

    def prepare_request(self, request_handler, locust):
        """
        :param request_handler: Request to be prepared
        :type request_handler: :class:`gherkin_locust.interface.RequestI`
        :param locust: locust currently executable client
        :type locust: :class:`locust.core.TaskSet`
        :returns: self
        :rtype: self
        """
        return self

    def analyze_response(self, request_handler, locust, resp):
        """
        :param request_handler: Request to be prepared
        :type request_handler: :class:`gherkin_locust.interface.RequestI`
        :param locust: locust currently executable client
        :type locust: :class:`locust.core.TaskSet`
        :param resp: Prepare request to be sent to `endpoint`
        :type resp: :class:`gherkin_locust.interface.ResponseI`
        :returns: self
        :rtype: self
        """
        pass

    def execute_request(self, locust_request, locust):
        """Executes request

        :param endpoint: Prepare request to be sent to `endpoint`
        :type endpoint: :class:`easytest.endpoint.RestEndpoint`
        :param locust: locust currently executable client
        :type locust: :class:`locust.core.TaskSet`
        :returns: response object
        :rtype: :class:`requests.Response`

        """
        pass


class LocustMixin:

    def add_task(self, callable_func, priority=1):
        """Add task to list of available tasks

        :param callable_func: Function which accepts locust file
        :type callable_func: func
        :param priority: Integer with priority
        :type priority: int
        :returns: self
        :rtype: self
        """
        for i in range(0, priority):
            self.tasks.append(callable_func)
