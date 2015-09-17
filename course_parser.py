#!/usr/bin/python3

from pdf_parser import get_read_courses

from lxml import html
import requests
from collections import defaultdict
import sys
import pickle

def dump_pkl(tables):
    with open('tables.pkl', 'wb') as pkl_file:
        # Pickle dictionary using protocol 0.
        pickle.dump(tables, pkl_file)

def read_pkl():
    with open('tables.pkl', 'rb') as pkl_file:
        return pickle.load(pkl_file)

def get_tables(demo):
    if demo:
        page_text = read_pkl()
    else:
        urls = [
            "http://kurser.lth.se/lot/?lasar=15_16&sort1=lp&sort2=slut_lp&sort3=namn&prog=D&forenk=t&val=program&soek=t",
            "http://kurser.lth.se/lot/?lasar=14_15&sort1=lp&sort2=slut_lp&sort3=namn&prog=D&forenk=t&val=program&soek",
        ]
        page_text = ""
        for url in urls:
            page = requests.get(url)
            page_text = "\n".join([page_text, page.text])
        dump_pkl(page_text)

    tree = html.fromstring(page_text)

    tables = tree.xpath('//table[@class="CourseListView border hover zebra"]')
    return tables

def table_info(t, container):
    tp = t.getparent()
    th3 = tp.getprevious()

    course_type = th3.text
    #print(course_type)
    course_body = t.getchildren()[1] #this should give us the "tbody"
    courses = course_body.getchildren()

    for course in courses:
        c = handleCourse(course)
        if c is not None:
            course_code = c['code']
            if course_code in container:
                container[course_code]['types'].append(course_type)
            else:
                c['types'] = [course_type]
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
        #print(c)
    except IndexError as e:
        return None
    return c

def get_info(demo):
    ts = get_tables(demo)
    cs = dict()
    for t in ts:
        table_info(t, cs)

    avail_courses = []
    for k,v in cs.items():
        print(v)
        avail_courses.append(v['code'])
    read_courses = get_read_courses(avail_courses)

    points = 0
    for course in read_courses['fin']:
        points += cs[course]['points']
        print(cs[course]['code'], cs[course]['points'])
    print("points:", points)

def main(argv):
    demo = False;
    if len(argv) == 1 and argv[0].strip() == "demo":
        demo = True
    get_info(demo)

if __name__ == '__main__':
    main(sys.argv[1:])
