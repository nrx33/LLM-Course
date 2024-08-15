if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from elasticsearch import Elasticsearch

@data_loader
def load_data(*args, **kwargs):
    """
    Loads the top matching document ID for a given query from Elasticsearch.
    
    Returns:
        The ID of the top matching document.
    """
    query = "When is the next cohort?"
    connection_string = 'http://module_5-elasticsearch-1:9200'  # Update with your actual connection string

    es_client = Elasticsearch(hosts=[connection_string])
    print(f'Connecting to Elasticsearch at {connection_string}')

    # Fetch all indices
    indices = es_client.indices.get_alias(index="*").keys()
    print(f"Available indices: {indices}")

    # Hardcode the index name
    index_name = 'documents_20240815_5930'  # Replace with your desired index name

    if index_name not in indices:
        print(f"Index '{index_name}' not found. Using default index.")
        index_name = sorted(indices)[-1]  # Fallback to the last index in alphabetical order

    print(f"Using index: {index_name}")

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["text", "section", "question"]
            }
        }
    }
    
    response = es_client.search(index=index_name, body=search_body, size=1)
    
    if response['hits']['total']['value'] > 0:
        top_hit = response['hits']['hits'][0]
        document_id = top_hit['_source']['document_id']
        score = top_hit['_score']
        print(f"Top matching document ID: {document_id} with score: {score}")
        return document_id
    else:
        print("No matching documents found.")
        return None


@test
def test_output(output, *args) -> None:
    """
    Tests that the output of the block is a valid document ID.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, str), 'Output is not a string'
    assert len(output) == 8, 'Document ID should be 8 characters long'
