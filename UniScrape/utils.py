"""
Utils Module

This module contains utility functions for this project.
"""
import json


def package_to_json(title: str, content: str, source: str) -> dict:
    data = {
        "title": title,
        "content": content,
        "source": source
    }

    return json.dumps(data, indent=4, ensure_ascii=False)
