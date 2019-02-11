""" abstract analyzer
"""
import logging

from azuresearch.azure_search_object import AzureSearchObject

# pylint: disable=abstract-method


class AbstractAnalyzer(AzureSearchObject):
    """ AbstractAnalyzer
    """

    def __init__(self, index_name, name, analyzer_type, **kwargs):
        super().__init__(**kwargs)
        self.index_name = index_name
        self.name = name
        self.type = analyzer_type

    def test(self, text):
        """ test
        """
        # pylint: disable=maybe-no-member
        body = {"analyzer": self.type, "text": text}
        logging.info("Testing analyzer: %s with text: %s", self.type, text)
        return self.endpoint.get(data=body, endpoint=self.index_name, needs_admin=True)

    def update(self, allow_index_downtime=False):
        """ update
        """
        # pylint: disable=maybe-no-member
        if allow_index_downtime:
            logging.warning(
                "Updating analyzer: %s. Index will be down until update is complete", self.name)
            return self.endpoint.put(data=self.to_dict(),
                                     endpoint=self.index_name,
                                     extra={"allowIndexDowntime": allow_index_downtime})
        logging.error(
            "Cannot update analyzer unless the index is turned off")
        raise Exception(
            "Cannot update analyzer unless the index is turned off")
