
import requests
import os
from dotenv import load_dotenv

load_dotenv()
notion_token = os.getenv('NOTION_API_TOKEN')
database_id = os.getenv('NOTION_DATABASE_ID')


def create_notion_page(token, database_id, title, content):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()



def append_to_page(token, page_id, content):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=data)
    return response.json()
import requests

def get_database_pages(token, database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    response = requests.post(url, headers=headers)
    results = response.json().get("results", [])

    pages = []
    for page in results:
        title = "Untitled"
        properties = page.get("properties", {})
        for prop in properties.values():
            if prop.get("type") == "title":
                title_obj = prop.get("title", [])
                if title_obj:
                    title = title_obj[0]["plain_text"]
                break
        pages.append((title, page["id"]))
    return pages

if __name__ == '__main__':
    title = "Sample Page"
    content = "This is appended content to the existing Notion page."

    # Test creating a page
    response = create_notion_page(notion_token, database_id, title, content)
    print("Notion page created:", response)

    # Test appending to a page
    # response = append_to_page(notion_token, title, content)
    # print("Append response:", response)
