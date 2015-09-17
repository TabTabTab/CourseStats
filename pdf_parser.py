#!/usr/bin/python3
import sys, os
from subprocess import Popen
UNF_HEADER = "Credits obtained in unfinished courses"
COURSES = "Courses"
me_dir = os.path.dirname(os.path.realpath(__file__))

temp_file = os.path.join(me_dir, "temp", "temp_pdf")

def get_read_courses(pdf_file, avail_courses):
    course_file = pdf_to_text(pdf_file)
    return parse_text(course_file, avail_courses)

def pdf_to_text(pdf_file):
    p = Popen(['pdftotext', pdf_file, temp_file])
    p.communicate()
    return temp_file

def parse_text(pdf_file, avail_courses):
    fin_courses = []
    unfin_courses = []
    def look_for_course(line, course_l):
        for avail_course in avail_courses:
            if avail_course in line:
                course_l.append(avail_course)
                return

    in_courses = False
    in_unf_courses = False
    with open(pdf_file, 'r') as pdf_file:
        for line in pdf_file:
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
    return {'fin':fin_courses, 'unfin':unfin_courses}

def main(argv):
    if len(argv) < 1:
        print ("Please provide a course pdf file..")
        return
    pdf_file = argv[0].strip()
    get_read_courses(pdf_file, ['EDAN40'])

if __name__ == '__main__':
    main(sys.argv[1:])
