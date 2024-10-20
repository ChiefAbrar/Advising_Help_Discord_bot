import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

def fetch_course_data(course_code):
    url = "" #Put your university's advising panel API, which could be any link with .JSON or any other public/fetched API
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Try again later."
        data = response.json()
        #print(f"Data type: {type(data)}") #debugger
        #print(data)
        if 'data' in data and isinstance(data['data'],list):
            matching_courses = []
            for course in data['data']:
                available_seat = course.get('availableSeat')
                #print(f"Checking course: {course}")
                if course.get('courseCode').upper() == course_code and available_seat and available_seat.strip() and int(available_seat)>0:
                    course_info = (
                        f"**Course & Section:** {course['courseDetails']}\n"
                        f"**Instructor:** {course['empShortName']}\n"
                        f"**Class Time:** {course['classSchedule']}\n"
                        f"**Lab Time:** {course['LabSchedule']}\n"
                        f"**Exam Date:** {course['examDate']}\n"
                        f"**Available Seats:** {available_seat}\n"
                    )
                    matching_courses.append(course_info)
            if matching_courses:
                return split_message("\n\n".join(matching_courses))
            else:
                return f"No data found for {course_code} with available seats."
        return "Data is not in the expected format."
    except requests.RequestException as e:
        return f"Request error occurred: {e}"
    except Exception as e:
        return f"An error occurred while processing the request: {e}"
def split_message(course_info):
    messages = []
    while len(course_info) > 2000:
        messages.append(course_info[:2000])
        course_info = course_info[2000:]
    messages.append(course_info)
    return messages