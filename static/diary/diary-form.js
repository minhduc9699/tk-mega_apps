const DiaryForm = async (method) => {
  let validateEmpty = false;
  let validateSession = false;
  $(`.add-diary`).css('display', 'block');
  if (!CKEDITOR.instances[`editor_overview`]) {
    CKEDITOR.replace(`editor_overview`, context.toolbarOptions);
    CKEDITOR.replace(`editor_curriculum`, context.toolbarOptions);
  }

  const resetForm = () => {
    $('#slt_course')[0].value = "...";
    $('#slt_classroom')[0].value = "...";
    $('#slt_classroom').attr('disabled', true);
    $('#slt_classroom').css('background', '#cccccc');
    $('#session_no_diary')[0].value = "";         
    $('#session_name_diary')[0].value = "";         
    initDiaryDate();
    $('#note_for_each_student').empty();
    CKEDITOR.instances['editor_overview'].setData("");
    CKEDITOR.instances['editor_curriculum'].setData("");
    $('.add-diary').css('display', 'none');
    $('#note_for_each_student').css('margin-bottom', '0px');
    $('#add_failed').addClass('invisible');
    $('#btn_save_diary').attr('disabled', false);
    $('#btn_save_diary').unbind('click');
  }
  
  $('#btn_cancel_diary').on({
    mouseenter: () => {
      $('#btn_cancel_diary').css({
        "color": "white",
        "background": "#DA9E8A"
      })
    },

    mouseleave: () => {
      $('#btn_cancel_diary').css({'background':"#87321b", "color":"white"})
    },

    click: () => {
     resetForm();
    }
  })

  context.selectedFormDiary.members = [];

  $('#btn_save_diary').on({
    click: async (event) => {
      context.selectedFormDiary.courseName = $('#slt_course')[0].selectedOptions[0].value;
      context.selectedFormDiary.classRoomName = $('#slt_classroom')[0].selectedOptions[0].value;
      context.selectedFormDiary.session_num = $('#session_no_diary')[0].value;
      context.selectedFormDiary.session_name = $('#session_name_diary')[0].value;
      context.selectedFormDiary.date = $('#diary_date')[0].value; 
      context.selectedFormDiary.diary = CKEDITOR.instances['editor_overview'].getData();
      context.selectedFormDiary.feedback = CKEDITOR.instances['editor_curriculum'].getData();
      context.selectedFormDiary.author_id = context.userLogin;
      context.selectedFormDiary.author_role = $('#slt_role')[0].selectedOptions[0].text.toLowerCase();
      context.selectedFormDiary.long_name = context.selectedCourse.longname;
      context.selectedFormDiary.class_no = context.selectedClassroom.classroom;

      $('#note_for_each_student')[0].childNodes.forEach((student) => {
        ckeID = $(student)[0].childNodes[3].childNodes[1].id;
        
        note = CKEDITOR.instances[ckeID].getData();
        if (method === "PUT") {
          memberID = ckeID.replace('area_', '').split('_')[1];          
          noteID = parseInt($(student)[0].childNodes[1].childNodes[5].innerText);
        } else if (method === "POST") {
          memberID = ckeID.replace('area_', '');
          noteID = ""
        }
        
        eachMember = {
            _id: noteID,
            member_id: memberID,
            note: note
          }
          context.selectedFormDiary.members.push(eachMember);
        })
        
      for (const [key, value] of Object.entries(context.selectedFormDiary)) {
        if (value === "") {
          $('#fields').removeClass('invisible');
          validateEmpty = true;
          break;
        }
        else{
          validateEmpty = false;
        }
        
      }
      for (let index = 0; index < context.selectedFormDiary.members.length; index++) {
        const member = context.selectedFormDiary.members[index];
        
        if (member.note === "") {
          context.selectedFormDiary.members.slice(index, 1);
          context.selectedFormDiary.members = context.selectedFormDiary.members.filter(item => item !== member)
          $('#fields').removeClass('invisible');
          $('#session').addClass('invisible');
          validateEmpty = true;
        }
        else{
          validateEmpty = false;
        }
      }
      if (!validateEmpty) {
        for (let index = 0; index < context.selectedClassroom.sessions.length; index++) {
          const diary = context.selectedClassroom.sessions[index];
          if(diary.session_num === parseInt(context.selectedFormDiary.session_num)) {
            $('#session').removeClass('invisible');
            $('#fields').addClass('invisible');
            validateSession = true;
            break;
          } else{
            $('#session').addClass('invisible');
            $('#fields').addClass('invisible');
            validateSession = false;
          }
        }
      }
      if (!validateSession && !validateEmpty) {   
        await postDiary(JSON.stringify(context.selectedFormDiary), context.selectedClassroom._id, method);
        setTimeout(async () => {
          await fetchCourse();
          renderSession();
          $(`#${context.selectedCourse._id}`).click();
          resetForm();
        }, 0);
      }
    },
    
    mouseenter: () => {
      $('#btn_save_diary').css({
        "color": "white",
        "background": "#DA9E8A"
      })
    },

    mouseleave: () => {
      $('#btn_save_diary').css({'background':"#87321b", "color":"white"})
    }
  })
}


const renderCourseSelection = () => {
  $('#slt_course').empty();
  $(`
    <option>...</option>
  `).appendTo('#slt_course');
  context.courses.forEach((eachCourse) => {
    $(`
    <option value="${eachCourse.course}" id="slt_${eachCourse._id}">${eachCourse.course}</option>
    `).appendTo('#slt_course');
  })
  renderClassroomSelection();
}


const renderClassroomSelection = () => {
  $('#slt_course').on('change', (event) => {
    $('#slt_classroom').empty();
    $('#note_for_each_student').empty();
    $('#slt_classroom').attr('disabled', false);
    $('#slt_classroom').css('background', 'white');
    sltCourseID = event.target.selectedOptions[0].id;
    courseID = sltCourseID.split('_')[1];
    context.selectedCourse = context.courses.find(course => course._id === courseID);
    $(`
        <option>...</option>
      `).appendTo('#slt_classroom');
    context.selectedCourse.classrooms.forEach((classroom) => {
      $(`
        <option value="${classroom.keyword.toUpperCase()}" id="slt_${classroom._id}">${classroom.keyword.toUpperCase()}</option>
      `).appendTo('#slt_classroom');
    })
  })
  renderMemberSelection();
}


const renderMemberSelection = () => {
  $('#slt_classroom').on('change', (event) => {
    $('#note_for_each_student').css('margin-top', '35px');
    sltClassroomID = event.target.selectedOptions[0].id;
    classroomID = sltClassroomID.split('_')[1]; 
    context.selectedClassroom = context.selectedCourse.classrooms.find(classroom => classroom._id === classroomID);
    members = context.selectedClassroom.members;
    teachers = context.selectedClassroom.teachers;
    $('#note_for_each_student').empty();
    
    authorID = context.userLogin;
    if(!teachers.find(teacher => teacher._id === authorID)){
      $('#add_failed').removeClass('invisible');
      $('#btn_save_diary').attr('disabled', true);
    } else {
      $('#add_failed').addClass('invisible');
      $('#btn_save_diary').attr('disabled', false);
      members.forEach((member) => {
      $(`
        <div class="each_student" style="margin-bottom: 15px">
          <div id="" class="student">
            <label style="font-size: 15px; margin: 0; font-weight: 500; color: white;">Student:</label>
            <span style="color:white">${member.fullName}</span>
          </div>
          <div id="" class="student-note">
            <textarea name="" id="area_${member._id}" cols="30" rows="5"></textarea>
          </div>
        </div>
      `).appendTo('#note_for_each_student');
        
      CKEDITOR.replace(`area_${member._id}`, context.toolbarOptions);
    })
  }
  })
}