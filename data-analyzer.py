import json
import webbrowser


def is_int(strng):
    try:
        int(strng)
        return True
    except ValueError:
        return False


def get_json_data(file_name):
    with open(file_name, encoding='utf-8') as f:
        dict = json.load(f)
    return dict


content = '''<html>
	<head>
	</head>

	<body>
	<h2>{title}</h2> 
	
	<ul>
	{list_elems}
	</ul></body>
</html>
'''

li = '''      <li><a href=\"{link}\">{text}</a></li>
'''


def make_tags_by_lang_page(lang, tags, projectsa):



def get_sorted_tags_lst(tags, projects):
    hist = {}
    for tag in tags:
        tags[tag] = 0
    for project in projects:
        for tag in tags:
            if tag in project[1]:
                tag += 1
    return list(sorted(hist.values()))


def get_data_by_lang():
    while True:
        print("Type the number of the language you would like to learn about:")
        langs = get_json_data('langs.json')
        enum_langs = enumerate(langs)
        for i, lang in enum_langs:
            print(i, lang)
        inp = input("your choice:")
        if (is_int(inp)) and int(inp) in range(len(langs)):
            inp = int(inp)
            # lang=enum_langs[1][inp]
            lang = dict(enumerate(langs))[inp]
            tags, projects = langs[lang]
            tags_lst = get_sorted_tags_lst(tags, projects)
            rel_projects=[]
            for proj in projects:
                if
            break


if __name__ == '__main__':
    get_data_by_lang()
    # page=content1
    # for lang in langs:
    #     page+=li.format(link='127.0.0.1',text=lang)
    # page+=content2
    # with open('out.htm', 'w', encoding='utf-8') as f:
    #     f.write(page)
    # webbrowser.open('out.htm')
