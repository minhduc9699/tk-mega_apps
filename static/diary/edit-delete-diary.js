const deleteDiary = (diaryID) => {
  $(`#delete_diary_${diaryID}, #delete_modal_${diaryID}`).on({
    mouseenter: () => {
      $(`#delete_diary_${diaryID}, #delete_modal_${diaryID}`).css({
        "cursor": "pointer",
        "transition": "0.1s"
      })
      $(`#delete_diary_${diaryID}`).css('height','30px');
      $(`#delete_modal_${diaryID}`).css({
        'height':'25px',
        'width': '25px'
      });
    },
    mouseleave: () => {
      $(`#delete_diary_${diaryID}, #delete_modal_${diaryID}`).css({
        "transition": "0.1s"
      })
      $(`#delete_diary_${diaryID}`).css('height','25px');
      $(`#delete_modal_${diaryID}`).css({
        'height':'20px',
        'width': '20px'
      });
    },
    click: (event) => {
      if(event.target.id === `delete_diary_${diaryID}` || event.target.id === `delete_modal_${diaryID}`) {
        $(`#modal_confirm_${diaryID}`).css('display', 'block');
        $(`#btn_yes_${diaryID}`).on('click', () => {
          $(`#modal_${diaryID}`).css('display', 'none');
          deleteDiaryJSON = {
            "_id": diaryID
          }
          submitDeleteDiary(JSON.stringify(deleteDiaryJSON), context.selectedClassroom._id);
          $(`#modal_confirm_${diaryID}`).css('display', 'none');
          $(`#${diaryID}`).css('display','none');
          fetchCourse();
          renderSession();
        });
        $(`#btn_no_${diaryID}`).on('click', () => {
          $(`#modal_confirm_${diaryID}`).css('display', 'none');
        })
      };
      
    }
  })
}


const editDiary = (diaryID, sessionNum) => {
  $(`#edit_diary_${diaryID}, #edit_modal_${diaryID}`).on({
    mouseenter: () => {
      $(`#edit_diary_${diaryID}, #edit_modal_${diaryID}`).css({
        "cursor": "pointer",
        "transition": "0.1s"
      })
      $(`#edit_diary_${diaryID}`).css('height', '30px');
      $(`#edit_modal_${diaryID}`).css({
        'height': '25px',
        'width': '25px'
      });
    },
    mouseleave: () => {
      $(`#edit_diary_${diaryID}, #edit_modal_${diaryID}`).css({
        "transition": "0.1s"
      })
      $(`#edit_diary_${diaryID}`).css('height', '25px');
      $(`#edit_modal_${diaryID}`).css({
        'height': '20px',
        'width': '20px'
      });
    },
    click: async () => {
      $(`#modal_${diaryID}`).css('display','none');
      $('#note_for_each_student').empty();
      context.selectedFormDiary._id = diaryID;
      DiaryForm("PUT");
      $(window).on('click', (event) => {
        if (event.target.className === `add-diary`) {
          $(`.add-diary`).css('display', 'none');
          $('#btn_save_diary').unbind('click');
          $('#btn_cancel_diary').click();
        }
      })
      $('#slt_course').attr('disabled', true);
      $('#slt_course').css('background', '#cccccc');
      $('.add-diary')[0].childNodes[1].childNodes[1].innerText = "Edit diary";
      
      selectedDiary = context.selectedSession.diaries.find(diary => diary._id === diaryID);

      role = selectedDiary.author_role;
      sessionNo = selectedDiary.session_num;
      sessionName = selectedDiary.session_name;
      courseName = context.selectedCourse.course;
      classRoomName = context.selectedClassroom.keyword.toUpperCase();
      date = selectedDiary.date;
      overview = selectedDiary.diary;
      curriculum = selectedDiary.feedback;
      
      $('#slt_course').val(courseName).change();
      $('#slt_classroom').attr('disabled', true);
      $('#slt_classroom').css('background', '#cccccc');
      $('#slt_classroom').val(classRoomName);

      
      CKEDITOR.instances['editor_overview'].setData(overview);
      CKEDITOR.instances['editor_curriculum'].setData(curriculum);
      $('#session_no_diary')[0].value = sessionNo;
      $('#session_name_diary')[0].value = sessionName;      
      $('#diary_date')[0].value = date;
      
      members = context.selectedClassroom.members;
      members.forEach((member) => {
        memberID = member._id;
        memberName = member.fullName;
        member.notes.forEach((note) => {
          if(note.diary_id === selectedDiary._id) {
            memberDiary = note.note;
            noteID = note._id;
            $(`
              <div class="each_student" style="margin-bottom: 75px">
                <div id="" class="student">
                  <label style="font-size: 15px; margin: 0; font-weight: 500; color: white;">Student:</label>
                  <span style="color:white">${memberName}</span>
                  <span style="display:none; color:white">${noteID}</span>
                </div>
                <div id="" class="student-note">
                  <textarea name="" id="area_${diaryID}_${memberID}" cols="30" rows="5">${memberDiary}</textarea>
                </div>
              </div>
            `).appendTo('#note_for_each_student');
        
            CKEDITOR.replace(`area_${diaryID}_${memberID}`, context.toolbarOptions);
            CKEDITOR.instances[`area_${diaryID}_${memberID}`].setData(memberDiary);
          }
        })
      })
    }
  })
}