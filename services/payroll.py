from tk_rest import TKRest


api = TKRest("http://techkids.vn:7791/api")
api_post = TKRest("http://techkids.vn:7791/api/instructor")
payroll = api.course
payroll_post = api_post.record

reset_url = payroll.url
reset_post_url = payroll_post.url
