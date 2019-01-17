""" DataSource
"""
import json

from azuresearch.base_api_call import BaseApiCall
from azuresearch.service import Endpoint

SERVICE_NAME = "datasources"


class DataSource(BaseApiCall):
    """
    Manages a data source for Azure Search.
    :param name: data source name
    :param connection_string: connection string to blob storage
    :param container_name: container name in blob storage
    :param type: type of data source. default is 'azureblob'
    :param description: description of data source
    """

    def __init__(self, name, connection_string, container_name,
                 datasource_type='azureblob', description=None,**kwargs):
        super(DataSource, self).__init__(service_name=SERVICE_NAME,**kwargs)
        self.name = name
        self.connection_string = connection_string
        self.container_name = container_name
        self.type = datasource_type
        self.description = description

    def to_dict(self):
        return_dict = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "credentials": {"connectionString": self.connection_string},
            "container": {"name": self.container_name}
        }
        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        """ load
        """
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise Exception("Failed to parse input as Dict")


        data['connection_string'] = data.get("credentials").get("connectionString")
        data['container_name'] = data.get("container").get("name")
        data = cls.to_snake_case_dict(data)
        return cls(**data)


    @classmethod
    def list(cls):
        """ list
        """
        response =  Endpoint(SERVICE_NAME).get(needs_admin=True)
