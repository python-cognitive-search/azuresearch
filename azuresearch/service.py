import copy
import logging
import os

import requests


class MissingEnvironmentVariableError(Exception):
    pass


class Endpoint(object):
    api_version = "2017-11-11-Preview"

    def __init__(self, path):
        self.path = "/" + path

    @property
    def _azure_path(self):
        url = os.environ.get('AZURE_SEARCH_URL', None)
        if url is None:
            raise MissingEnvironmentVariableError("The Azure Search URL is required as an environment variable")
        return url

    @property
    def _azure_api_key(self):
        api_key = os.environ.get('AZURE_SEARCH_API_KEY', None)
        if api_key is None:
            raise MissingEnvironmentVariableError("The Azure Search api-key is required as an environment variable")
        return api_key

    @property
    def _azure_admin_api_key(self):
        admin_api_key = os.environ.get('AZURE_SEARCH_ADMIN_API_KEY', None)
        if admin_api_key is None:
            raise MissingEnvironmentVariableError(
                "The Azure Search admin api-key is required as an environment variable")
        return admin_api_key

    def query_path(self, endpoint):
        if endpoint:
            return self._azure_path + self.path + "/" + endpoint
        return self._azure_path + self.path

    def query_args(self, extra=None):
        if extra is None:
            extra = {}
        x = copy.deepcopy(extra)
        x.update({"api-version": self.api_version})
        return x

    def query_headers(self, needs_admin=False, extra=None):
        if extra is None:
            extra = {}
        x = copy.deepcopy(extra)
        if needs_admin:
            key = self._azure_admin_api_key
        else:
            key = self._azure_api_key
        x.update({"api-key": key})
        return x

    def get(self, data=None, endpoint=None, needs_admin=False):
        if data is None:
            data = {}
        logging.debug("GET request\n"
                      "URL: {url}."
                      "Params: {params}".format(url=self.query_path(endpoint), params=self.query_args()))
        return requests.get(
            self.query_path(endpoint),
            params=self.query_args(),
            headers=self.query_headers(needs_admin),
            json=data
        )

    def post(self, data=None, endpoint=None, needs_admin=False):
        if data is None:
            data = {}
        logging.debug("POST request\n"
                      "URL: {url}."
                      "Params: {params}".format(url=self.query_path(endpoint), params=self.query_args()))

        return requests.post(
            self.query_path(endpoint),
            params=self.query_args(),
            headers=self.query_headers(needs_admin),
            json=data
        )

    def put(self, data=None, endpoint=None, needs_admin=False, extra=None):
        if data is None:
            data = {}
        logging.debug("PUT request\n"
                      "URL: {url}."
                      "Params: {params}".format(url=self.query_path(endpoint), params=self.query_args(extra)))

        return requests.put(
            self.query_path(endpoint),
            params=self.query_args(extra),
            headers=self.query_headers(needs_admin),
            json=data
        )

    def delete(self, data=None, endpoint=None, needs_admin=False):
        if data is None:
            data = {}
        logging.debug("DELETE request\n"
                      "URL: {url}."
                      "Params: {params}".format(url=self.query_path(endpoint), params=self.query_args()))

        return requests.delete(
            self.query_path(endpoint),
            params=self.query_args(),
            headers=self.query_headers(needs_admin),
            json=data
        )
