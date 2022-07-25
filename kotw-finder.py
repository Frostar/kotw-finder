from email import header
import re
import requests

# Set owned expansions
owned_expansions = ['Dominion', 'Intrigue', 'Seaside', 'Alchemy', 'Prosperity', 'Dark Ages', 'Guilds', 'Cornucopia']


session = requests.Session()
kotw_title_pattern = re.compile(r"KotW 1?[0-9]\/[1-3]?[0-9]: ")
kotw_expansion_pattern = re.compile(r"\[(.+)\]")


def search_kotw(after = None):
    base_url = f'https://www.reddit.com/r/dominion/search.json'
    params = {"q": "kotw", "restrict_sr": False, "sort": "new", "after": after}
    headers = {"User-Agent": "KotW-Finder"}
    response = session.get(base_url, headers=headers, params=params)
    return response.json()


def match_kotw(title):
    title_match = kotw_title_pattern.search(title)
    return title_match != None


def get_expansions(title):
    expansion_match = kotw_expansion_pattern.search(title)
    if expansion_match != None:
        return expansion_match.group(1).split(', ')


def print_compatible_kotw(json):
    for child in json['data']['children']:
        title = child['data']['title']
        if(match_kotw(title)):
            expansions = get_expansions(title)
            compabible = True
            for expansion in expansions:
                if expansion not in owned_expansions:
                    compabible = False
                    break
            if(compabible):
                print("[+] Found compatible KotW:\n" + title + "\n")
            
  
after = None
while True:
    search_result = search_kotw(after)
    print_compatible_kotw(search_result)
    after = search_result['data']['after']
    if (after == None ):
        break
