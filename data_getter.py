import requests as req
import io
import time
import json
from bs4 import BeautifulSoup
import calendar

NUM_PAGES = 3
# ARTICLES = 300
# ARTICLES_PER_PAGE = 12
URL = "https://gitstar-ranking.com/repositories?page="
BASE_URL = "https://gitstar-ranking.com"
SUCCESS_CODE = ("FAILED", "SUCCESSFULL")
THRESH = 15


# SEC2DAYS = 86400

# def sec_to_days(secs):

#     return secs // SEC2DAYS
def get_response(url):
    response = req.get(url)
    response.raise_for_status()  # ensure we notice bad responses
    return response


def get_langs(lang_elem):
    langs = set()
    for elem in lang_elem.find_all('li'):
        percents = float(elem.find_all('span', attrs={'class': 'percent'})[0].text[:-1])
        if percents >= THRESH:
            lang_name = elem.find_all('span', attrs={'class': 'lang'})[0].text
            langs.add(lang_name)
    return langs


def get_tags(page_soup):
    tags = set()

    for elem in page_soup.find_all('a'):
        if 'class' in elem.attrs and 'topic-tag-link' in elem.attrs['class']:
            tags.add(elem['href'][8:])
    return tags


def add_lang_data(proj_name, proj_tags, proj_langs, langs):
    for lang in proj_langs:
        if lang not in langs:
            langs[lang] = (proj_tags, {proj_name})
        else:
            langs[lang][0].update(proj_tags)
            langs[lang][1].update({proj_name})


def add_tag_data(proj_name, proj_tags, proj_langs, tags):
    for tag in proj_tags:
        if tag not in tags:
            tags[tag] = (proj_langs, {proj_name})
        else:
            tags[tag][0].update(proj_langs)
            tags[tag][1].update({proj_name})


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def dump_files(projects, langs, tags):
    with open('projects.json', 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=4, default=set_default)
    with open('langs.json', 'w', encoding='utf-8') as f:
        json.dump(langs, f, ensure_ascii=False, indent=4, default=set_default)
    with open('tags.json', 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False, indent=4, default=set_default)


def add_proj_data(name, projects, url, tags, langs):
    # get github link
    try:
        response = get_response(url)
    except:
        return
    soup = BeautifulSoup(response.content, features="html.parser")
    gh_link = soup.find_all('a', attrs={'target': '_blank'})[0].attrs['href']

    # get data from github
    try:
        response = get_response(gh_link)
        soup = BeautifulSoup(response.content, features="html.parser")
        lang_elem = soup.find_all('ol', attrs={'class': 'repository-lang-stats-numbers'})[0]
    except:
        return
    proj_langs = get_langs(lang_elem)
    proj_tags = get_tags(soup)
    projects[name] = (gh_link, proj_langs, proj_tags)
    add_lang_data(name, proj_tags, proj_langs, langs)
    add_tag_data(name, proj_tags, proj_langs, tags)


def get_data():
    projects = {}  # Saving project info
    tags = {}  # Saving project info
    langs = {}  # Saving project info
    for page in range(1, NUM_PAGES + 1):
        # cur_epoch_time = calendar.timegm(time.gmtime())
        response = get_response(URL + str(page))
        soup = BeautifulSoup(response.content, features="html.parser")
        print("======== Collecting page " + str(page) + " ========")
        # Iterate over all projects in page
        for row in soup.find_all('a', attrs={'class': 'list-group-item paginated_item'}):
            url = BASE_URL + row.attrs['href']
            name = row.find_all('span', attrs={'class': 'hidden-md hidden-lg'})[0].text[1:-1]
            print("collecting " + name + " data:", end="  ")
            add_proj_data(name, projects, url, tags, langs)
            print("SUCCESSFUL")

            time.sleep(1.5)
    dump_files(projects, langs, tags)

