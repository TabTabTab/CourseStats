
### Description ###

A simnple program for calculating course points for D students at lth.

### Instructions ###

    1.) Go to http://www.student.lu.se
    2.) Generate and download a course result summary.
        a.) Make sure it's in english
        b.) Make sure you have course codes included
    3.) go to the repository root directory
    4.) do:
        $ ./course_stats.py [update_courses] 'Resultat.pdf'
    5.) wait, the program scrapes the web for course info and the lth page loads sloowly
    6.) marvel

    # update_courses #
        Scrape the course pages from year 11-12 to 15-16 and update the course data


### Requirements ###

    1.) python 3
    2.) texttopdf

    ## Python libs ##
        1.) lxml
        2.) requests
        3.) pickle
