""" Documents
"""


class Documents():
    """ Documents
    """

    def __init__(self, index):
        self.index = index

    def check_document(self, document):
        """ check_document
        """
        for field in self.index.fields:
            if field.python_type is not None and field.name in document.keys():
                if not isinstance(document[field.name], field.python_type):
                    raise Exception
        return True

    def add(self, documents):
        """ add
        """
        docs = []
        for doc in documents:
            if self.check_document(doc):
                doc["@search.action"] = "mergeOrUpload"
                docs.append(doc)

        data = {'value': docs}
        return self.index.endpoint.post(endpoint=self.index.name + "/docs/index",
                                        data=data, needs_admin=True)

    def delete(self, documents):
        """ delete
        """
        docs = []
        for doc in documents:
            if self.check_document(doc):
                doc["@search.action"] = "delete"
                docs.append(doc)

        data = {'value': docs}
        return self.index.endpoint.post(endpoint=self.index.name + "/docs/index",
                                        data=data, needs_admin=True)
