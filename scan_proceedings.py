import requests
import argparse
import pickle
import os
import json

S2_API_KEY = os.getenv('S2_API_KEY')

def search_for_papers(venue, year, limit=100):
    """Search for papers based on venue."""
    def with_token(token):
        url = 'https://api.semanticscholar.org/graph/v1/paper/search/bulk'
        params = {'venue': venue, 'year': year, 'limit': limit, 'fields': 'title,authors,abstract,citationCount,publicationTypes'}
        headers = {'x-api-key': S2_API_KEY}
        if token is not None:
            params['token'] = token

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return {}
    r = with_token(None)
    out = r['data']
    while r['token'] is not None:
        r = with_token(r['token'])
        out += r['data']
    return out



def main():
    parser = argparse.ArgumentParser(description='Search for papers from Semantic Scholar based on venue and year.')
    parser.add_argument('-v', '--venue', type=str, required=True, help='Venue of the papers to search for.')
    parser.add_argument('-y', '--year', type=int, required=True, help='Year of publication.')
    parser.add_argument('-l', '--limit', type=int, default=100, help='Limit for the number of papers to retrieve.')

    args = parser.parse_args()

    papers = search_for_papers(args.venue, args.year, args.limit)
    with open(f'papers_{args.venue}_{args.year}.pkl', 'wb') as f:
        pickle.dump(papers, f)
    with open(f'papers_{args.venue}_{args.year}.json', 'w') as f:
        json.dump(papers, f)

    if papers:
        for paper in papers:
            print(f"Title: {paper.get('title')}")
            print(f"Authors: {[author['name'] for author in paper.get('authors', [])]}")
            print(f"Abstract: {paper.get('abstract')}")
            print(f"Citation Count: {paper.get('citationCount')}")
            print(f"Publication Types: {paper.get('publicationTypes')}\n")
    else:
        print("No papers found.")

if __name__ == "__main__":
    main()
