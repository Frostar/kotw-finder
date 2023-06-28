import re
import requests

# Set owned expansions
owned_expansions = ['Base', 'Dominion', 'Intrigue', 'Seaside', 'Alchemy', 'Prosperity', 'Dark Ages', 'Guilds', 'Cornucopia']

session = requests.Session()
kotw_title_pattern = re.compile(r"KotW 1?[0-9].+: ")
kotw_expansion_pattern = re.compile(r"\[(.+)\]")
imgur_pattern = re.compile(r"(https?:\/\/imgur.com\/a\/[0-9a-zA-Z]+)")

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


def get_imgurlink(selftext):
    imgur_match = imgur_pattern.search(selftext)
    if imgur_match != None:
        return imgur_match.group(1)


def print_compatible_kotw(json):
    for child in json['data']['children']:
        title = child['data']['title']
        if(match_kotw(title)):
            expansions = get_expansions(title)
            compatible = True
            for expansion in expansions:
                if expansion not in owned_expansions:
                    compatible = False
                    break
            if(compatible):
                print("[+] Found compatible KotW:\n" + title)
                description = child['data']['selftext']
                image_link = get_imgurlink(description)
                if (image_link != None):
                    print("Image link: " + image_link)
                print("")
            
  
if __name__ == '__main__':
    after = None
    while True:
        search_result = search_kotw(after)
        print_compatible_kotw(search_result)
        after = search_result['data']['after']
        if (after == None ):
            break
