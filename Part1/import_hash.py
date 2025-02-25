import json
import typesense

# Initialize the Typesense client
client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'Nf18/I+ojFgMdSmzDmvJC9nOknI29bbTUDM8hse7qKw=',  # Replace with your actual API key
    'connection_timeout_seconds': 2
})

# Delete the existing 'cracked_hashes' collection (if it exists)
try:
    client.collections['cracked_hashes'].delete()
    print("Existing collection deleted.")
except Exception as e:
    print("No existing collection to delete or error encountered:", e)

# Define the collection schema (hash field is now not faceted)
schema = {
    "name": "cracked_hashes",
    "fields": [
        {"name": "hash", "type": "string"},  # Removed "facet": True
        {"name": "plain_text", "type": "string"},
        {"name": "algorithm", "type": "string"}
    ]
}

# Create the collection with the updated schema
try:
    client.collections.create(schema)
    print("Collection created.")
except Exception as e:
    print("Error during collection creation:", e)

# Parse the hash file and support both 3-field and 4-field formats (preserving original case)
documents = []
with open("hash01.txt", "r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        try:
            parts = line.split(":")
            if len(parts) == 4:
                # Format: hash:plain_text:extra_field:algorithm
                hash_val, plain_text, extra_field, algorithm = parts
                documents.append({
                    "hash": hash_val.strip(),
                    "plain_text": plain_text.strip(),
                    "algorithm": algorithm.strip()
                })
            elif len(parts) == 3:
                # Format: hash:plain_text:algorithm
                hash_val, plain_text, algorithm = parts
                documents.append({
                    "hash": hash_val.strip(),
                    "plain_text": plain_text.strip(),
                    "algorithm": algorithm.strip()
                })
            else:
                print(f"Skipping malformed line: {line}")
        except UnicodeDecodeError:
            print(f"Skipping malformed line due to decode error: {line}")

# Import documents into Typesense (using newline-delimited JSON)
ndjson = "\n".join([json.dumps(doc) for doc in documents])
response = client.collections['cracked_hashes'].documents.import_(ndjson, {"action": "create"})
print("Import response:", response)