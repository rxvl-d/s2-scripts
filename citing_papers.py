import requests
import json
import sys
import os

S2_API_KEY = os.getenv('S2_API_KEY')

def get_paper_id(title):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "fields": "paperId"
    }
    headers = {'x-api-key': S2_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data['total'] > 0:
        return data['data'][0]['paperId']
    else:
        return None

def fetch_citations(paper_id):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"
    params = {
        "fields": "title,abstract"
    }
    headers = {'x-api-key': S2_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return [{"title": citation['citingPaper'].get("title", ""), "abstract": citation['citingPaper'].get("abstract", "")} for citation in data['data']]

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main(title):
    paper_id = get_paper_id(title)
    if paper_id:
        citations = fetch_citations(paper_id)
        save_to_json(citations, title.replace(' ', '_') + '.json')
    else:
        print("Paper not found.")

if __name__ == "__main__":
    main(sys.argv[1])

