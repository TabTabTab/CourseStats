#!/usr/bin/python3
import sys
from tkinter import *

from tkinter.scrolledtext import ScrolledText

UNF_HEADER = "Credits obtained in unfinished courses"
COURSES = "Courses"

def get_pasted_pdf():
    text = [""]
    root = Tk()
    s = ScrolledText(root)
    s.pack()
    b = Button(root, text = "OK", width = 10, command = lambda : show_entry_fields(s, root, text))
    b.pack()
    mainloop()
    return text[0]

def show_entry_fields(s, root, text):
    text[0] = s.get(0.0, END)
    root.quit()


def get_read_courses(avail_courses):
    text = get_pasted_pdf()
    print(text)
    return parse_text(text, avail_courses)

def parse_text(text, avail_courses):
    fin_courses = []
    unfin_courses = []
    def look_for_course(line, course_l):
        for avail_course in avail_courses:
            if avail_course in line:
                course_l.append(avail_course)
                return

    in_courses = False
    in_unf_courses = False
    for line in text.split('\n'):
        line = line.strip()
        if not in_courses:
            if line == COURSES:
                in_courses = True

        if in_courses:
            if not in_unf_courses:
                if line == UNF_HEADER:
                    in_unf_courses = True
                else:
                    look_for_course(line, fin_courses)
            else:
                look_for_course(line, unfin_courses)
    print("fin",fin_courses)
    print("unfin", unfin_courses)
    return {'fin':fin_courses, 'unfin':unfin_courses}

def main(argv):
    get_read_courses(['EDAN35'])

if __name__ == '__main__':
    main(sys.argv[1:])
