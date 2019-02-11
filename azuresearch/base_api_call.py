""" BaseApiCall
"""
import json
import logging

import requests

from azuresearch.azure_search_object import AzureSearchObject
from azuresearch.service import Endpoint


class AzureSearchServiceException(Exception):
    """
    Exception for any Azure Search related calls
    """


class ServiceDoesNotExistException(Exception):
    """
    Exception for trying to delete a service which doesn't exist
    """


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

    def to_dict(self):
        pass

    def create(self):
        """ create
        """
        result = self.endpoint.post(self.to_dict(), needs_admin=True)
        # pylint: disable=maybe-no-member
        if result.status_code != requests.codes.created:
            raise Exception(
                "Error posting {service_name}. result: {result}"
                .format(service_name=self.service_name, result=json.load(result.content)))
        else:
            logging.debug(
                "Successfully created service %s", self.service_name)

    def get(self):
        """ get
        """
        # pylint: disable=maybe-no-member
        result = self.endpoint.get(endpoint=self.name, needs_admin=True)
        if result.status_code != requests.codes.ok:
            raise AzureSearchServiceException(
                "Error getting {service_name}. result: {result}"
                .format(service_name=self.service_name, result=result.content))
        return result.content

    def delete_if_exists(self):
        """ delete if already exists
        """
        try:
            self.delete()
        except ServiceDoesNotExistException:
            pass

    def delete(self):
        """ delete
        """
        # pylint: disable=maybe-no-member
        result = self.endpoint.delete(endpoint=self.name, needs_admin=True)
        if result.status_code == requests.codes.not_found:
            raise ServiceDoesNotExistException(
                "Error deleting {service_name}. result: {result}"
                .format(service_name=self.service_name, result=result.content))

        if result.status_code != requests.codes.no_content:
            raise ServiceDoesNotExistException(
                "Error deleting {service_name}. result: {result}"
                .format(service_name=self.service_name, result=result.content))

    def update(self):
        """ update
        """
        try:
            self.delete()
        except AzureSearchServiceException as exc:
            logging.warning(
                "Failed to delete service. Return result = %s", exc)
        return self.create()

    def verify(self):
        """ verify
        """
        return self.get()

    @classmethod
    def list(cls):
        """ list
        """
        # pylint: disable=maybe-no-member
        service_name = cls.SERVICE_NAME
        result = Endpoint(service_name).get(needs_admin=True)
        if result.status_code != requests.codes.ok:
            raise Exception(
                "Error getting {service}. Result: {result}"
                .format(service=service_name, result=result))

        sources = json.loads(result.content)['value']

        insts = []
        for source in sources:
            inst = cls.load(source)
            insts.append(inst)
        return insts
