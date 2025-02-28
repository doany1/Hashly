from typesense import Client
from typesense.exceptions import TypesenseClientError
from functools import lru_cache


client_pool = Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'your-key',
    'connection_timeout_seconds': 2,
    'num_connections': 5  # Pool size
})

def initialize_typesense():
    return Client({
        'nodes': [{
            'host': 'localhost',
            'port': '8108',
            'protocol': 'http'
        }],
        'api_key': 'Your api key', #add here your api key
        'connection_timeout_seconds': 2
    })

def get_hash_count():
    """Retrieve total number of hashes in the collection"""
    try:
        client = initialize_typesense()
        collection_stats = client.collections['cracked_hashes'].retrieve()
        return collection_stats.get('num_documents', 0)
    except TypesenseClientError as e:
        print(f"Typesense Error: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return 0

@lru_cache(maxsize=1024)

def search_hash(hash_value):
    """Search for a hash in the Typesense database"""
    try:
        client = initialize_typesense()
        search_parameters = {
            'q': hash_value,
            'query_by': 'hash',
            'per_page': 1
        }

        result = client.collections['cracked_hashes'].documents.search(search_parameters)

        response_data = {'found': False}
        if result.get('hits'):
            hit = result['hits'][0]['document']
            response_data.update({
                'found': True,
                'plain_text': hit.get('plain_text', 'Unknown'),
                'algorithm': hit.get('algorithm', 'Unknown'),
                'hash': hash_value
            })
        return response_data

    except TypesenseClientError as e:
        print(f"Search Error: {e}")
        return {'error': f"Database error: {str(e)}"}
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {'error': "Internal server error"}
