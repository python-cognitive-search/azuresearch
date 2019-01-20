from azuresearch.data_source import DataSource
from azuresearch.indexes import Index
from azuresearch.skills import Skillset
from tests.test_helpers import get_json_file


class DataSourceCreationTesting():

    def run(self):
        config = get_json_file("blob_config.json",dir='integration_tests')
        datasource = DataSource.load(config)
        datasource.delete_if_exists()
        datasource.create()

        datasources = DataSource.list()
        print(datasources)

        datasource.update()

        datasource.delete()

        print("Successfully deleted, created, updated and deleted a data-source")


class IndexCreationTesting():

    def run(self):
        index = Index.load(get_json_file("index.json"))
        index.delete_if_exists()
        index.create()

        indexes = Index.list()
        print(indexes)

        index.update()

        index.delete()

        print("Successfully deleted, created, updated and deleted an index")



class SkillsetCreationTesting():

    def run(self):
        skillset = Skillset.load(get_json_file("skillset.json"))
        skillset.delete_if_exists()
        skillset.create()

        skillsets = Skillset.list()
        print(skillsets)

        skillset.update()

        skillset.delete()

        print("Successfully deleted, created, updated and deleted a skillset")


class IndexerCreationTesting():

    def run(self):
        pass



if __name__ == "__main__":
    DataSourceCreationTesting().run()

    IndexCreationTesting().run()

    SkillsetCreationTesting().run()


