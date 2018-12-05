const context = {
  classRooms: [],
  selectedClassroom: null,
  selectedSession: null,
  selectedCourse: null,
  courses: [],
  userLogin: null,
  userRole: null,
  selectedFormDiary: {
    _id: null,
    courseName: null,
    class_no: null,
    author_id: null,
    author_role: null,
    classRoomName: null,
    session_num: null,
    session_name: null,
    date: null,
    diary: null,
    feedback: null,
    long_name: null,
    members: []
  },
  loading: false,
  toolbarOptions: {
    toolbar: [{ 
      name: 'document', 
      items: [ 'Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Undo', 'Redo', '-', 'Link', 'Unlink', 'Anchor', '-', 'Image', 'Flash', 'Table', 'HorizontalRule', '-', 'TextColor', 'BGColor', '-', 'Smiley', 'SpecialChar', '-','Source']
    }],
  }
}

$(document).ready(async () => {
  await fetchCourse();
  addNewDiary();
  initDiaryDate();
})