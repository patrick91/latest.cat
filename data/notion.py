import json
import logging
import requests

from .config import notion_db, notion_token


class Notion:
    @staticmethod
    async def increment_counter(software: str) -> int:
        headers = {
            "Authorization": "Bearer " + notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }

        query_data = {"filter": {"property": "software", "title": {"equals": software}}}

        query_response = requests.post(
            f"https://api.notion.com/v1/databases/{notion_db}/query",
            headers=headers,
            json=query_data,
        )
        query_response = json.loads(query_response.text)

        if query_response["object"] == "error":
            logging.error("notion:" + query_response["message"])
            return

        if query_response["results"]:
            page_id = query_response["results"][0]["id"]
            count = query_response["results"][0]["properties"]["count"]["number"]
            count += 1

            data = {"properties": {"count": {"number": count}}}
            requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=data
            )
            return count
        else:
            data = {
                "parent": {"database_id": notion_db},
                "properties": {
                    "software": {
                        "type": "title",
                        "title": [{"type": "text", "text": {"content": software}}],
                    },
                    "count": {"type": "number", "number": 1},
                },
            }
            requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
            return 1
