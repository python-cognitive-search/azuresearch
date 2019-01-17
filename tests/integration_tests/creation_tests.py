from azuresearch.data_source import DataSource
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
        pass


class SkillsetCreationTesting():

    def run(self):
        pass

class IndexerCreationTesting():

    def run(self):
        pass



if __name__ == "__main__":
    DataSourceCreationTesting().run()

    IndexCreationTesting().run()

    SkillsetCreationTesting().run()


