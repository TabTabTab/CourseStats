#!/usr/bin/python3

from pdf_parser import get_read_courses

from lxml import html
import requests
from collections import defaultdict
import sys
import pickle

def dump_pkl(tables):
    with open('info_pages.pkl', 'wb') as pkl_file:
        # Pickle dictionary using protocol 0.
        pickle.dump(tables, pkl_file)

def read_pkl():
    with open('info_pages.pkl', 'rb') as pkl_file:
        return pickle.load(pkl_file)

def get_tables(update_courses):
    page_texts = ""
    if not update_courses:
        page_texts = read_pkl()
    else:
        print("Updating courses..")
        years = ["11_12", "12_13", "13_14","14_15", "15_16"]
        base_url = "http://kurser.lth.se/lot/?lasar=%s&sort1=lp&sort2=slut_lp&sort3=namn&prog=D&forenk=t&val=program"
        for year in years:
            print ("Updating %s"%year)
            url = base_url%year
            page = requests.get(url)
            page.encoding = 'utf-8'
            page_texts = "\n".join([page_texts, page.text])
        dump_pkl(page_texts)

    tree = html.fromstring(page_texts)

    tables = tree.xpath('//table[@class="CourseListView border hover zebra"]')
    return tables

def table_info(t, container):
    tp = t.getparent()
    th3 = tp.getprevious()

    course_type = th3.text
    course_body = t.getchildren()[1] #this should give us the "tbody"
    courses = course_body.getchildren()

    for course in courses:
        c = handleCourse(course)
        if c is not None:
            course_code = c['code']
            if course_code in container:
                container[course_code]['types'].add(course_type)
            else:
                c['types'] = set([course_type])
                container[course_code] = c

def handleCourse(course_element):
    c = dict()
    try:
        vals = ["points", "level"]
        elements = course_element.getchildren()
        code = elements[0].getchildren()[0].text
        info = dict(zip(vals, map(lambda e:e.text, elements[1:])))
        c['code'] = code
        c['points'] = float(info['points'].replace(',','.'))
        c['level'] = info['level']
    except IndexError:
        return None
    return c

def get_info(pdf_file, update_courses):
    ts = get_tables(update_courses)
    cs = dict()
    for t in ts:
        table_info(t, cs)

    avail_courses = []
    for k,v in cs.items():
        avail_courses.append(v['code'])
    read_courses = get_read_courses(pdf_file, avail_courses)

    generate_stats(read_courses, cs)

def generate_stats(read_courses, course_db):
    print()
    print("============ Stats for FINISHED courses =============")
    generate_stats_ct(read_courses['fin'], course_db)
    print()
    print("============ Stats for UNFINISHED courses =============")
    generate_stats_ct(read_courses['unfin'], course_db)

def generate_stats_ct(read_courses, course_db):
    specialisations = defaultdict(dict)
    points  = 0
    for course in read_courses:
        course = course_db[course]
        spls = course['types']
        p = course['points']
        code = course['code']
        level = course['level']
        points += p
        for spl in spls:
            if spl not in specialisations:
                specialisations[spl]['points'] = 0
                specialisations[spl]['codes'] = []
                specialisations[spl]['A'] = 0
            specialisations[spl]['points'] += p
            specialisations[spl]['codes'].append(code)
            if level == 'A':
                specialisations[spl]['A'] += p
    for s,v in specialisations.items():
        print(s,":",v)
    print ("points:", points)

def remove_arg(argv, arg):
    try:
        argv.remove(arg)
    except ValueError:
        pass

def main(argv):
    keys = ['update_courses']
    update_courses = "update_courses" in argv
    print(update_courses)
    [remove_arg(argv, k) for k in keys]
    if len(argv) < 1:
        print("please supply a pdf file, not accepted names are:",", ".join(keys))
        return
    pdf_file = argv[0]
    get_info(pdf_file, update_courses)

if __name__ == '__main__':
    main(sys.argv[1:])
