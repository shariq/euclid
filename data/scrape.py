import requests
import datetime
import cPickle
from dateutil.parser import parse as parse_datetime
from bs4 import BeautifulSoup


def parse_weekdays(weekdays_string):
    weekday_dict = {'M':0, 'Tu':1, 'W':2, 'Th':3, 'F':4, 'Sa':5, 'Su':6}
    weekdays = []
    buffer = weekdays_string[0]
    for c in weekdays_string[1:]:
        if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            weekdays.append(buffer)
            buffer = ''
        buffer += c
    weekdays.append(buffer)
    return map(weekday_dict.__getitem__, weekdays)

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
    print department
    if 'BIOE' > department:
        continue
    url = 'https://ntst.umd.edu/soc/' + semester + '/' + department
    department_soup = BeautifulSoup(requests.get(url).text)
    courses = filter(lambda x: 'class' in x.attrs and 'course' in x['class'],
                     department_soup.find_all('div')
                     )
    for course in courses:
        course_id = course['id']
        data[course_id] = {}
        print course_id
        description = ''
        description_container = filter(lambda x: 'class' in x.attrs and 'approved-course-text' in x['class'],
                                       course.find_all('div')
                                       )
        if description_container:
            description += ' '.join(map(lambda x: x.text.strip(), description_container))
        title = filter(lambda x: 'class' in x.attrs and 'course-title' in x['class'],
                       course.find_all('span')
                       )[0].text.strip()
        data[course_id]['description'] = description
        data[course_id]['title'] = title
        data[course_id]['meetings'] = []
        section_text = requests.get('https://ntst.umd.edu/soc/' + semester + '/sections',
                                    params = {'courseIds': course_id}
                                    ).text
        sections_soup = BeautifulSoup(section_text)
        sections = filter(lambda x: 'class' in x.attrs and 'section' in x['class'],
                          sections_soup.find_all('div')
                          )
        lectures = {}
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
                location_container = filter(lambda x: 'class' in x.attrs and 'section-class-building-group' in x['class'],
                                            meeting.find_all('div')
                                            )
                if not location_container:
                    continue
                location = location_container[0].text.strip().replace('\n',' ')
                if not location:
                    continue
                days_container = filter(lambda x: 'class' in x.attrs and 'section-days' in x['class'],
                                        meeting.find_all('span')
                                        )
                if not days_container:
                    continue
                days = days_container[0].text.strip()
                if not days:
                    continue
                start_time_container = filter(lambda x: 'class' in x.attrs and 'class-start-time' in x['class'],
                                              meeting.find_all('span')
                                              )
                if not start_time_container:
                    continue
                start_time = start_time_container[0].text.strip()
                end_time_container = filter(lambda x: 'class' in x.attrs and 'class-end-time' in x['class'],
                                            meeting.find_all('span')
                                            )
                if not end_time_container:
                    continue
                end_time = end_time_container[0].text.strip()
                if not start_time or not end_time:
                    continue
                start_time_parsed = parse_datetime(start_time).time()
                end_time_parsed = parse_datetime(end_time).time()
                meeting_type_container = filter(lambda x: 'class' in x.attrs and 'class-type' in x['class'],
                                                meeting.find_all('span')
                                                )
                meeting_type = ''
                if meeting_type_container:
                    meeting_type += meeting_type_container[0].text.strip()
                else:
                    meeting_type += 'Lecture'
                for weekday in parse_weekdays(days):
                    d = {}
                    d['type'] = meeting_type
                    d['weekday'] = weekday
                    d['start'] = start_time_parsed
                    d['end'] = end_time_parsed
                    d['instructor'] = lecturer
                    d['location'] = location
                    d['size'] = seats
                    if meeting_type.lower().strip() == 'lecture':
                        lecture_key = str(d['start'])+','+str(d['end'])+','+str(weekday)+','+location
                        if lecture_key not in lectures:
                            lectures[lecture_key] = {}
                            lectures[lecture_key]['seats'] = 0
                            lectures[lecture_key]['info'] = d
                        lectures[lecture_key]['seats'] += int(seats)
                    else:
                        data[course_id]['meetings'].append(d)
        for lecture_key in lectures:
            d = lectures[lecture_key]['info']
            d['size'] = lectures[lecture_key]['seats']
            data[course_id]['meetings'].append(d)

filename =  str(datetime.datetime.now().time()).replace(':','_').replace('.','_') + '.bin'
cPickle.dump(data, open(filename, 'wb'), -1)

