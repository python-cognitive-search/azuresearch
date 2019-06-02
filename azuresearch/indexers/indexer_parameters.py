from azuresearch.azure_search_object import AzureSearchObject


class IndexerParameters(AzureSearchObject):

    def __init__(self, max_failed_items=-1,
                 max_failed_items_per_batch=-1,
                 configuration=None,
                 **kwargs):
        """

        :param max_failed_items:
        :param max_failed_items_per_batch:
        :param configuration:
        :param kwargs:
        """
        if not configuration:
            configuration = self.default_indexer_configuration()

        self.configuration = configuration
        self.max_failed_items_per_batch = max_failed_items_per_batch
        self.max_failed_items = max_failed_items

        super().__init__(**kwargs)

    def default_indexer_configuration(self):
        return_dict = {
            "parsing_mode": "default",
            "excluded_file_name_extensions": [],
            "data_to_extract": "contentAndMetadata",
            "image_action": "generateNormalizedImages",
        }
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)

        return return_dict

    def to_dict(self):
        return_dict = {"max_failed_items": self.max_failed_items,
                       "max_failed_items_per_batch": self.max_failed_items_per_batch,
                       "configuration": self.configuration}
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = IndexerParameters.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = IndexerParameters.remove_empty_values(return_dict)

        return return_dict
