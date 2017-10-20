# -*- coding: utf-8 -*-

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger


class HttpClientListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, requests_lib):
        self._requests_lib = requests_lib

    def end_test(self, data, result):
        self._requests_lib.delete_all_sessions()


class HttpClient(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ADD_CSRF_METHODS = {'post_request', 'patch_request', 'put_request'}

    def __init__(self):
        self._bi = BuiltIn()
        self._requests = self._bi.get_library_instance('RequestsLibrary')
        self.ROBOT_LIBRARY_LISTENER = HttpClientListener(self._requests)

    def _set_variable(self, response):
        self._bi.set_test_variable('${last_response}', response)
        return response

    def _get_csrf_token(self, alias):
        try:
            return self._requests._cache.get_connection(alias).cookies['csrftoken']
        except KeyError:
            logger.warn('No CSRF token found')
            return ''

    def post_protected_request(self, *args, **kw):
        return self._run_request('post_request', *args, **kw)

    def _run_request(self, method_name, *args, **kw):
        alias = self._bi.get_variable_value('${session}')
        method = getattr(self._requests, method_name)
        headers = kw.setdefault('headers', {})

        if not kw.get('files'):
            headers.setdefault('content-type', 'application/x-www-form-urlencoded')

        if method_name in self.ADD_CSRF_METHODS:
            headers['x-csrftoken'] = self._get_csrf_token(alias)

        response = method(alias, *args, **kw)
        self._set_variable(response)
        return response
