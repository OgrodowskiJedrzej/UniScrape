import json


def package_to_json(title: str, content: str, source: str) -> dict:
    data = {
        "title": title,
        "content": content,
        "source": source
    }

    return json.dump(data, indent=4)
