import sys
import termcolor
from unittest import TestCase
from easytest.framework import Framework
from django.conf import settings
from easytest.di import get_injector_for_framework
from easytest.helpers import humanize_error

from django.contrib.auth import get_user_model


class EmailGenerator:

    @classmethod
    def generate_if_needed_data_based_on_context(cls, field, request):
        if field.name == 'email':
            return 'example@example.com'


class PasswordGenerator:

    @classmethod
    def generate_if_needed_data_based_on_context(cls, field, request):
        if field.name == 'password':
            return '12345678Aa^'


injector = get_injector_for_framework('drf')
test_visitor = injector.get_test_visitor()


def setup():

    framework = Framework('drf')
    framework.load_config(settings.PATH_TO_EASYTEST_CONFIG)
    framework.load_openapi_schema(settings.PATH_TO_API_JSON)
    test_visitor.set_openapi(framework.openapi)
    test_visitor.set_resourceregistry(framework.resource_registry)
    test_visitor.set_datagenerator(framework.datagenerator)
    framework.datagenerator.register_specific_generator(EmailGenerator)
    framework.datagenerator.register_specific_generator(PasswordGenerator)

    user = get_user_model().objects.create(
        email='sergdev@gmail.com',
        last_name='dasdasdas',
        first_name='dsdqweqw',
        username='dqweqweqweqweq'
    )
    user.set_password('12345678Aa^')
    user.save()
    framework.resource_registry.register_resource('current_user', user)
    user = get_user_model().objects.create(
        email='sergdev1@gmail.com',
        last_name='dasdasdas',
        first_name='dsdqweqw',
        username='dqweqweqweqweq1'
    )
    user.set_password('12345678Aa^')
    user.save()
    framework.resource_registry.register_resource('another_user', user)
    openapi = framework.openapi

    def custom_setup_for_build(request):
        request.data.add({'111': 'AAA'})

    def custom_teardown_for_build(request, resp):
        pass

    def custom_matcher_for_build(request, resp):
        pass

    openapi.register_setup_for(
        '/api/cached/build/',
        custom_setup_for_build
    )
    openapi.register_teardown_for(
        '/api/cached/build/',
        custom_teardown_for_build
    )
    openapi.register_custom_matcher_for(
        '/api/cached/build/',
        custom_matcher_for_build,
        method='list'
    )
    return framework


class ResourcesTestCase(TestCase):

    def test(self):
        test_failed = False
        framework = setup()
        for resource_id, endpoint in framework.rest_endpoints():
            request = injector.get_request()
            if not endpoint.anonymous:
                request.force_authenticate_user(
                    framework.resource_registry.get_resource(
                        'current_user'
                    ).obj
                )
            if resource_id:
                request.we_test_resource(
                    framework.resource_registry.get_resource(
                        resource_id
                    )
                )
            request.set_endpoint(endpoint)
            if endpoint.method not in ('get', 'list', 'delete'):
                request.data.add(
                    test_visitor.generate_fixture_for(
                        endpoint.url, endpoint.method,
                        request
                    )
                )

            try:
                request.execute(test_visitor)
            except Exception as e:
                print(termcolor.colored(
                    humanize_error(request, str(e), sys.exc_info()),
                    'red'
                ))
                test_failed = True
        for endpoint in framework.rpc_endpoints():
            print('AAA')

        if test_failed:
            self.assertTrue(
                False,
                'Automatic test of endpoints has been failed'
            )
