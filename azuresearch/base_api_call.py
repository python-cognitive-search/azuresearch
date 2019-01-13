""" BaseApiCall
"""
from abc import ABC, abstractmethod

import requests

from azuresearch.azure_search_object import AzureSearchObject
from azuresearch.service import Endpoint


class BaseApiCall(AzureSearchObject):

    """
    Abstract class for wrapping common calls to Azure Search services
    """

    def __init__(self, service_name, endpoint=None, **kwargs):
        """
        :param service_name: Name of Azure Search service (e.g. indexes, datasources, skillsets)
        :param endpoint:
        """
        super().__init__(**kwargs)
        self.service_name = service_name
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = Endpoint(service_name)

    def create(self):
        """ create
        """
        result = self.endpoint.post(self.to_dict(), needs_admin=True)
        if result.status_code != requests.codes.created:
            raise Exception(
                "Error posting {service_name}. result: {result}"
                .format(service_name=self.service_name, result=result))

    def get(self):
        """ get
        """
        result = self.endpoint.get(endpoint=self.name, needs_admin=True)
        if result.status_code != requests.codes.ok:
            raise Exception(
                "Error getting {service_name}. result: {result}"
                .format(service_name=self.service_name, result=result))
        return result

    def delete(self):
        """ delete
        """
        result = self.endpoint.delete(endpoint=self.name, needs_admin=True)
        if result.status_code != requests.codes.no_content:
            raise Exception(
                "Error deleting {service_name}. result: {result}"
                .format(service_name=self.service_name, result=result))

    def update(self):
        """ update
        """
        self.delete()
        return self.create()

    def verify(self):
        """ verify
        """
        return self.get()
