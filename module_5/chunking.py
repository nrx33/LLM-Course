if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        List of transformed documents with added document IDs.
    """
    import hashlib

    def generate_document_id(doc):
        combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
        hash_object = hashlib.md5(combined.encode())
        hash_hex = hash_object.hexdigest()
        document_id = hash_hex[:8]
        return document_id

    documents = []

    # If data is a list, loop through each dictionary
    if isinstance(data, list):
        for course_dict in data:
            for doc in course_dict['documents']:
                doc['course'] = course_dict['course']
                doc['document_id'] = generate_document_id(doc)
                documents.append(doc)
    else:
        # If data is a single dictionary
        for doc in data['documents']:
            doc['course'] = data['course']
            doc['document_id'] = generate_document_id(doc)
            documents.append(doc)

    print(len(documents))  # Print the number of documents (chunks)

    return documents


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, list), 'Output is not a list'
    assert all(isinstance(doc, dict) for doc in output), 'Not all elements are dictionaries'
    assert all('course' in doc and 'document_id' in doc for doc in output), 'Missing keys in output dictionaries'
