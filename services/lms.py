from tk_rest import TKRest


api = TKRest("https://learn.techkids.vn/api")
classroom = api.classrooms
users = api.users
courses = api.courseclassroom
auth = api.auth

reset_url_classroom = classroom.url
reset_url_course = courses.url
