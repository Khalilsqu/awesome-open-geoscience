import sys
import json
import jsonschema

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "category": {"type": "string"},
            "subcategory": {"type": ["string", "null"]},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "url": {"type": "string", "format": "uri"},
        },
        "required": ["category", "name", "description", "url"],
    }
}

def validate_entries(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_file}\n{e}")
        sys.exit(1)  # Exit with a non-zero code to fail the GitHub Action

    # Validate against schema
    jsonschema.validate(instance=data, schema=schema)

    # Check for duplicates
    seen = set()
    duplicates = []
    for entry in data:
        key = (entry['name'], entry['url'])
        if key in seen:
            duplicates.append(entry)
        seen.add(key)

    if duplicates:
        print(f"Found duplicate entries: {duplicates}")
        sys.exit(1)

if __name__ == "__main__":
    validate_entries(sys.argv[1])
