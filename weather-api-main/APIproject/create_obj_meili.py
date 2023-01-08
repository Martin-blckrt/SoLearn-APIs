import meilisearch
import json
import os

SEARCH_PATH = os.path.join(os.getcwd(), "GeographyData", "search_communes", "communes_sorted_names.json")

meili_client = meilisearch.Client('http://127.0.0.1:7700')

def main():
    with open(SEARCH_PATH, encoding='utf-8') as json_file:
        communes = json.load(json_file)
        meili_client.delete_index('communes')
        meili_client.create_index('communes', {'primaryKey': 'code'})
        meili_client.index('communes').add_documents(communes)

if __name__ == '__main__':
    main()