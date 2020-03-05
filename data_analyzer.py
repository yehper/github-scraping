import json
import webbrowser
import os
import data_getter


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
        <table style=\"width: 100%;\">
            <tr>
                <th>{elem}</th>
                <th>Relevant Projects</th>
            </tr>
{rows}
    </table>
    </body>
</html>
'''

row = '''
            <tr>
                <td>{left}</td>
                <td><a href=\"{href}\">{right}</a></td>
            </tr>'''


def get_sorted_langs_lst(langs, tag_projects, all_projects):
    hist = {}
    for lang in langs:
        hist[lang] = 0
    for project in tag_projects:
        for lang in langs:
            if lang in all_projects[project][1]:
                hist[lang] += 1
    res = []
    for lang, count in sorted(hist.items(), reverse=True, key=lambda x: x[1]):
        res.append(lang)
    return res


def get_sorted_tags_lst(tags, lang_projects, all_projects):
    hist = {}
    for tag in tags:
        hist[tag] = 0
    for project in lang_projects:
        for tag in tags:
            if tag in all_projects[project][2]:
                hist[tag] += 1
    res = []
    for tag, count in sorted(hist.items(), reverse=True, key=lambda x: x[1]):
        res.append(tag)
    return res


def get_tag_projects_by_lang(lang, tag_projects, all_projects):
    projects_lst = []
    for proj in tag_projects:
        if lang in all_projects[proj][1]:
            projects_lst.append(proj)
    return projects_lst


def get_lang_projects_by_tag(tag, projects, all_projects):
    projects_lst = []
    for proj in projects:
        if tag in all_projects[proj][2]:
            projects_lst.append(proj)
    return projects_lst


def make_projects_page(title, elem, lst1, projects, all_projects):
    page = content
    length1, length_projects = len(lst1), len(projects)
    rows = ""
    for i in range(max(length1, length_projects)):
        itm1, proj, href = "", "", ""
        if i < length1:
            itm1 = lst1[i]
        if i < length_projects:
            proj = projects[i]
            href = all_projects[proj][0]
        rows += row.format(left=itm1, right=proj, href=href)

    with open('out.htm', 'w', encoding='utf-8') as f:
        f.write(page.format(title=title, elem=elem, rows=rows))


def get_data_by_lang():
    while True:
        os.system('clear')
        # get menu item and validate
        print("Type the number of the language you would like to learn about:")
        langs = get_json_data('langs.json')
        all_projects = get_json_data('projects.json')
        enum_langs = enumerate(langs)
        for i, lang in enum_langs:
            print(i, lang)
        inp = input("your choice:")
        if (is_int(inp)) and int(inp) in range(len(langs)):
            inp = int(inp)
            lang = dict(enumerate(langs))[inp]
            lang_tags, lang_projects = langs[lang]
            # arrange relevant data
            tags_lst = get_sorted_tags_lst(lang_tags, lang_projects, all_projects)
            enum_tags = enumerate(tags_lst)
            os.system('clear')
            print("\n\n\nRelevant tags for the language: {} by order:".format(lang))
            for j, tag in enum_tags:
                print(j, tag)
            inp = input("\n\n you can now choose a tag to be redirected to relevant top projects.\nyour choice:")
            if (is_int(inp)) and int(inp) in range(len(tags_lst)):
                inp = int(inp)
                tag = dict(enumerate(tags_lst))[inp]
                projects_lst = get_lang_projects_by_tag(tag, lang_projects, all_projects)
                title = "Relevant tags by language: {lang} and projects regarding the tag: {tag}".format(tag=tag,
                                                                                                         lang=lang)
                make_projects_page(title, "Relevant tags by language", tags_lst, projects_lst, all_projects)
                webbrowser.open('out.htm')
                break
            break


def get_data_by_tag():
    while True:
        os.system('clear')
        # get menu item and validate
        print("Type the number of the tag you would like to learn about:")
        tags = get_json_data('tags.json')
        all_projects = get_json_data('projects.json')
        enum_tags = enumerate(tags)
        for i, tag in enum_tags:
            print(i, tag)
        inp = input("your choice:")
        if (is_int(inp)) and int(inp) in range(len(tags)):
            inp = int(inp)
            tag = dict(enumerate(tags))[inp]
            tag_langs, tag_projects = tags[tag]
            # arrange relevant data
            lang_lst = get_sorted_langs_lst(tag_langs, tag_projects, all_projects)
            enum_langs = enumerate(lang_lst)
            os.system('clear')
            print("\n\n\nRelevant Languages for the tag: {} by order:".format(tag))
            for j, lang in enum_langs:
                print(j, lang)
            inp = input("\n\n you can now choose a tag to be redirected to relevant top projects.\nyour choice:")
            if (is_int(inp)) and int(inp) in range(len(lang_lst)):
                inp = int(inp)
                lang = dict(enumerate(lang_lst))[inp]
                projects_lst = get_tag_projects_by_lang(lang, tag_projects, all_projects)
                title = "Relevant Languages by tag: {tag} and projects regarding the Language: {lang}".format(tag=tag,
                                                                                                              lang=lang)
                make_projects_page(title, "Relevant Languages by Tag", lang_lst, projects_lst, all_projects)
                webbrowser.open('out.htm')
                break
            break


if __name__ == '__main__':
    options = ['Update data', 'Get Popular tags by order', 'Get Popular Programming languages by order']
    while True:
        for j, lang in enumerate(options):
            print(j, lang)
        inp = input("\nyour choice:")
        if (is_int(inp)) and int(inp) in range(len(options)):
            inp = int(inp)
            if inp == 0:
                data_getter.get_data()
                break
            elif inp == 1:
                get_data_by_tag()
                break
            elif inp == 2:
                get_data_by_lang()
                break

