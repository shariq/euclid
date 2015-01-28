from bs4 import BeautifulSoup
import requests
import datetime
from dateutil.parser import parse as parse_datetime

semester = '201501'

homepage = requests.get('https://ntst.umd.edu/soc/').text
homepage_soup = BeautifulSoup(homepage)

departments = map(lambda x:x.text,
                  filter(lambda x:'class' in x.attrs and 'prefix-abbrev' in x['class'],
                         homepage_soup.find_all('span')
                         )
                  )

data = {}

for department in departments:
    url = 'https://ntst.umd.edu/soc/' + semester + '/' + department
    department_soup = BeautifulSoup(requests.get(url).text)
    classes = filter(lambda x: 'class' in x.attrs and 'course' in x['class'],
                     department_soup.find_all('div')
                     )
    for class in classes:
        course_id = class['id']
        description = filter(lambda x: 'class' in x.attrs and 'approved-course-text' in x['class'],
                             class.find_all('div')
                             )[0].text.strip()
        title = filter(lambda x: 'class' in x.attrs and 'course-title' in x['class'],
                       class.find_all('span')
                       )[0].text.strip()
        section_text = requests.get('https://ntst.umd.edu/soc/' + semester + '/sections',
                                    params = {'courseIds': course_id}
                                    ).text
        sections_soup = BeautifulSoup(section_text)
        sections = filter(lambda x: 'class' in x.attrs and 'section' in x['class'],
                          sections_soup.find_all('div')
                          )
        lectures = []
        for section in sections:
            lecturer = filter(lambda x: 'class' in x.attrs and 'section-instructor' in x['class'],
                              section.find_all('span')
                              )[0].text.strip()
            seats = filter(lambda x: 'class' in x.attrs and 'total-seats-count' in x['class'],
                           section.find_all('span')
                           )[0].text.strip()
            meeting_container = filter(lambda x: 'class' in x.attrs and 'class-days-container' in x['class'],
                                       section.find_all('div')
                                       )[0]
            meetings = filter(lambda x: 'class' in x.attrs and 'row' in x['class'],
                              meeting_container.find_all('div')
                              )
            for meeting in meetings:
                location = filter(lambda x: 'class' in x.attrs and 'section-class-building-group' in x['class'],
                                  meeting.find_all('div')
                                  )[0].text.strip()
                days = filter(lambda x: 'class' in x.attrs and 'section-days' in x['class'],
                              meeting.find_all('span')
                              )[0].text.strip()
                start_time = filter(lambda x: 'class' in x.attrs and 'class-start-time' in x['class'],
                                    meeting.find_all('span')
                                    )[0].text.strip()
                end_time = filter(lambda x: 'class' in x.attrs and 'class-end-time' in x['class'],
                                  meeting.find_all('span')
                                  )[0].text.strip()
                start_time_parsed = parse_datetime(start_time).time()
                end_time_parsed = parse_datetime(end_time).time()
