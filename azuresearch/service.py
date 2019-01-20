""" service
"""
import copy
import logging
import os

import json
import requests


class MissingEnvironmentVariableError(Exception):
    """ MissingEnvironmentVariableError
    """


class Endpoint():
    """ Endpoint
    """
    api_version = "2017-11-11-Preview"

    def __init__(self, path):
        self.path = "/" + path

    @property
    def _azure_path(self):
        """ _azure_path
        """
        url = os.environ.get('AZURE_SEARCH_URL', None)
        if url is None:
            raise MissingEnvironmentVariableError(
                "The Azure Search URL is required as an environment variable")
        return url

    @property
    def _azure_api_key(self):
        """ _azure_api_key
        """
        api_key = os.environ.get('AZURE_SEARCH_API_KEY', None)
        if api_key is None:
            raise MissingEnvironmentVariableError(
                "The Azure Search api-key is required as an environment variable")
        return api_key

    @property
    def _azure_admin_api_key(self):
        """ _azure_admin_api_key
        """
        admin_api_key = os.environ.get('AZURE_SEARCH_ADMIN_API_KEY', None)
        if admin_api_key is None:
            raise MissingEnvironmentVariableError(
                "The Azure Search admin api-key is required as an environment variable")
        return admin_api_key

    def query_path(self, endpoint):
        """ query_path
        """
        if endpoint:
            return self._azure_path + self.path + "/" + endpoint
        return self._azure_path + self.path

    def query_args(self, extra=None):
        """ query_args
        """
        if extra is None:
            extra = {}
        extra_copy = copy.deepcopy(extra)
        extra_copy.update({"api-version": self.api_version})
        return extra_copy

    def query_headers(self, needs_admin=False, extra=None):
        """ query_headers
        """
        if extra is None:
            extra = {}
        extra_copy = copy.deepcopy(extra)
        if needs_admin:
            key = self._azure_admin_api_key
        else:
            key = self._azure_api_key
        extra_copy.update({"api-key": key})
        return extra_copy

    def get(self, data=None, endpoint=None, needs_admin=False):
        """ get
        """
        if data is None:
            data = {}
        logging.debug("GET request\n"
                      "URL: %s."
                      "Params: %s", self.query_path(endpoint), self.query_args())
        return requests.get(
            self.query_path(endpoint),
            params=self.query_args(),
            headers=self.query_headers(needs_admin),
            json=data
        )

    def post(self, data=None, endpoint=None, needs_admin=False):
        """ post
        """
        if data is None:
            data = {}
        logging.debug("POST request\n"
                      "URL: %s."
                      "Params: %s", self.query_path(endpoint), self.query_args())

        return requests.post(
            self.query_path(endpoint),
            params=self.query_args(),
            headers=self.query_headers(needs_admin),
            json=data
        )

    def put(self, data=None, endpoint=None, needs_admin=False, extra=None):
        """ put
        """
        if data is None:
            data = {}
        logging.debug("PUT request\n"
                      "URL: %s."
                      "Params: %s", self.query_path(endpoint), self.query_args(extra))

        return requests.put(
            self.query_path(endpoint),
            params=self.query_args(extra),
            headers=self.query_headers(needs_admin),
            json=data
        )

    def delete(self, data=None, endpoint=None, needs_admin=False):
        """ delete
        """
        if data is None:
            data = {}
        logging.debug("DELETE request\n"
                      "URL: %s."
                      "Params: %s", self.query_path(endpoint),
                      self.query_args())

        return requests.delete(
            self.query_path(endpoint),
            params=self.query_args(),
            headers=self.query_headers(needs_admin),
            json=data
        )


