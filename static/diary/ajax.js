const fetchCourse = async () => {
  setLoading(true);
  const res = await $.ajax({
    url: `/diary/api/course`,
    type: "GET"
  })
  if (res && res.data) {
    context.courses = res.data;
    context.userLogin = res.user_id;
    context.userRole = await res.user_role;
    renderCourse();
    renderCourseSelection();
    if (context.userRole !== "manager") {
      $('#btn_add').css("display","flex");
    }
  }
  setLoading(false);
}


const postDiary = async (diaryJSON, classroom_id, method) => {
  setLoading(true);
  const res = await $.ajax({
    url:`/diary/api/diaries?classroom_id=${classroom_id}`,
    type: method,
    data: diaryJSON,
    dataType: 'json',
    contentType: 'application/json'
  })
  setLoading(false);
}


const submitDeleteDiary = async (diaryJSON, classroom_id) => {
  const res = await $.ajax({
    url:`/diary/api/diaries?classroom_id=${classroom_id}`,
    type: "DELETE",
    data: diaryJSON,
    dataType: 'json',
    contentType: 'application/json'
  })
}