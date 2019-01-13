# import json
# import os
#
# index_data = json.load(open(
#     os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_jsons/hotels.index.json')))
# document_data = json.load(open(
#     os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_jsons/hotels.documents.json')))
#
# from azuresearch import indexes
#
# print("Create Python Index -----------------")
# index = indexes.Index.load(index_data)
#
# print("Update index in Azure -----------------")
# print(index.update().text)
#
# print("List indexes from Azure -----------------")
# index_list = indexes.Index.list().json()
# print(index_list)
# assert len(index_list['value']) == 1
#
# print("Load documents into Azure -----------------")
# response = index.documents.add(document_data)
# print(response.text)
#
# # print(index.update().text)
# print("Query -----------------")
# results = index.search("expensive")
# print(results)
# print(results.text)
#
# print("Cleanup -----------------")
# i = index.delete()
# print(i.status_code)
# print(i.text)
