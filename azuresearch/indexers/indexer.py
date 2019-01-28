""" Indexer
"""
import json

import requests

from azuresearch.azure_search_object import AzureSearchObject
from azuresearch.base_api_call import BaseApiCall
from azuresearch.indexers import IndexerSchedule
from azuresearch.indexers.indexer_parameters import IndexerParameters
from azuresearch.field_mapping import FieldMapping

class Indexer(BaseApiCall):
    """ Indexer
    """
    SERVICE_NAME = 'indexers'

    def __init__(self, name, data_source_name, target_index_name,
                 skillset_name, field_mappings=None,
                 output_field_mappings=None, schedule=None,
                 disabled=False, parameters=IndexerParameters(), **params):
        super().__init__(service_name=Indexer.SERVICE_NAME, **params)
        self.output_field_mappings = output_field_mappings
        self.field_mappings = field_mappings
        self.skillset_name = skillset_name
        self.target_index_name = target_index_name
        self.data_source_name = data_source_name
        self.name = name
        self.schedule = schedule
        self.disabled = disabled
        self.parameters = parameters

        self.field_mappings = [FieldMapping(source_field_name="metadata_storage_path",
          target_field_name="id",
          mapping_function={"name": "base64Encode"}),
          FieldMapping("content", "content")]

    def __repr__(self):
        """ __repr__
        """
        return "<Indexer: \n" \
               "indexer name: {name}\n, " \
               "data_source_name: {data_source_name}\n" \
               "target_index_name: {target_index_name}\n" \
               "skillset_name: {skillset_name}\n" \
               "field_mappings: {field_mappings}\n" \
               "output_field_mappings: {output_field_mappings}".format(
            name=self.name,
            data_source_name=self.data_source_name,
            target_index_name=self.target_index_name,
            skillset_name=self.skillset_name,
            field_mappings=self.field_mappings,
            output_field_mappings=self.output_field_mappings)

    def to_dict(self):
        """ to_dict
        """
        return_dict = {
            "name": self.name,
            "dataSourceName": self.data_source_name,
            "targetIndexName": self.target_index_name,
            "skillsetName": self.skillset_name,
            "fieldMappings": [fm.to_dict() for fm in self.field_mappings] if self.field_mappings else None,
            "outputFieldMappings": [fm.to_dict() for fm in
                                    self.output_field_mappings] if self.output_field_mappings else None,
            "schedule": self.schedule.to_dict() if self.schedule else None,
            "disabled": self.disabled,
            "parameters": self.parameters.to_dict()
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
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")

        if 'parameters' in data:
            data['parameters'] = IndexerParameters.load(data['parameters'])
        if 'schedule' in data:
            data['schedule'] = IndexerSchedule.load(data['schedule'])
        data = cls.to_snake_case_dict(data)

        return cls(**data)

    def run(self):
        """ run
        """
        result = self.endpoint.post(endpoint="run")
        if result.status_code != requests.codes.accepted:
            raise Exception(
                "Error running indexer. result: {result}".format(result=result))

    def reset(self):
        """ reset
        """
        result = self.endpoint.post(endpoint="reset")
        if result.status_code != requests.codes.no_content:
            raise Exception(
                "Error resetting indexer. result: {result}".format(result=result))

    def update(self):
        """ update
        """
        result = self.endpoint.post(endpoint="reset")
        if result.status_code != requests.codes.no_content:
            raise Exception(
                "Error resetting indexer. result: {result}".format(result=result))

    def get_status(self):
        """
        Get status of running indexer
        :return:
        """
        result = self.endpoint.get(endpoint=self.name+"/status")
        if result.status_code != requests.codes.ok:
            raise Exception(
                "Error retrieving indexer status. result: {result}".format(result=result))

        return json.loads(result.content)

