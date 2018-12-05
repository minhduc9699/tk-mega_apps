const renderDiary = () => {
  context.selectedClassroom.sessions.forEach((session) => {
    $(`#session_${session.session_num.split(" ")[1]}`).on('click', (event) => {
      courseDiv = $($('#course_name')[0].childNodes[0]);
      classesDiv = $($('#course_name')[0].childNodes[2]);
      $(`<span> > </span>`).appendTo(courseDiv[0].childNodes[3]);
      courseName = context.selectedCourse.course;
      
      courseDiv[0].childNodes[5].innerText = `${session.session_num.toUpperCase()}`    
      classesDiv[0].innerText = `Diaries`;
      $('#classrooms').empty();
      
      session.diaries.forEach((diary) => {      
        authorID = diary.author_id;
        context.selectedClassroom.teachers.forEach((teacher) => {
          if (teacher._id === authorID) {
            author = teacher;
          }
        })
        $(`
          <div id ="${diary._id}" class="textbox">
            <div class="d-flex justify-content-between">
              <span>${author.firstName} ${author.lastName}</span>
              <span id="icons_${diary._id}" style="float:right" class="invisible">
                <img id="edit_diary_${diary._id}" style="height: 25px" src="/static/diary/Icons/2x/pen.png">
                <img id="delete_diary_${diary._id}" style="height: 25px" src="/static/diary/Icons/2x/recycle.png">
              </span>
            </div>
              
          </div>
          <div id="modal_${diary._id}" class="diary-modal">
            <div class="show-panel d-flex flex-wrap align-content-center justify-content-center">
              <div id="" class="title d-flex justify-content-between">
                  <h3>Buổi ${diary.session_num} - ${diary.session_name}</h3>
                  
              </div>
              <div id="" class="content-panel">
                <div id="" class=" user-info d-flex align-items-end flex-column">
                  <p>${diary.date}</p>
                  <p>${author.firstName} ${author.lastName}</p>
                  <span id="author_role_${diary._id}" style="display:none">${diary.author_role}</span>
                </div>
                <div id="" class="content">
                  <div id="" class="textbox-modal">
                    <p>Overview :</p>
                    <p>${diary.diary}</p>
                  </div>
                  <div id="" class="textbox-modal">
                    <p>Curriculum :</p>
                    <p>${diary.feedback}</p>
                  </div>
                  <div id="note_for_each" class="textbox-modal">
                    <p>Note for each student :</p>
                    <div id="note-text_${diary._id}">
    
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div id="modal_confirm_${diary._id}" class="diary-confirm-modal distance">
            <div class="w-100 h-100 d-flex justify-content-center align-items-center">
              <div class="show-panel-confirm-modal delete-box">
                
                
                  <div id="" class=" delete-box-text d-flex justify-content-center">
                    <p>Are you sure you want to delete this diary?</p>
                  </div>
                  <div id="" class="button-yes-no d-flex justify-content-between">
                    <button id="btn_yes_${diary._id}" class="btn-yes">Yes</button>
                    <button id="btn_no_${diary._id}" class="btn-no">No</button>
                  </div>
                
              </div>
            </div>
          </div>
        `).appendTo('#classrooms');
        if(context.userRole !== "manager") {
          $(`
            <div id="" class="icon-items" style="">
              <img id="edit_modal_${diary._id}" src="/static/diary/Icons/2x/baseline_edit_white_18dp.png" alt="">
              <img id="delete_modal_${diary._id}" src="/static/diary/Icons/2x/baseline_delete_white_18dp.png" alt="">
            </div>
          `).appendTo($(`#modal_${diary._id}`)[0].childNodes[1].childNodes[1]);
          
        }
        
        deleteDiary(diary._id);
        editDiary(diary._id, diary.session_num);
      })
      initDiary(session.session_num);  
    })
  })
}


const initDiary = ((sessionNum) => {
  context.selectedSession = context.selectedClassroom.sessions.find(session => session.session_num === sessionNum);
  context.selectedSession.diaries.forEach((diary) => {
    $(`#${diary._id}`).on({
      mouseenter: (event) => {
        $(`#${diary._id}`).css({'cursor':'pointer', 'color':'white', 'transition': '0.1s'});
        if(context.userRole !== "manager") {
          $(`#icons_${diary._id}`).removeClass('invisible');
        }
      },
      mouseleave: (event) => {
        $(`#${diary._id}`).css({'color':'black', 'transition': '0.1s'});
        if(context.userRole !== "manager") {
          $(`#icons_${diary._id}`).addClass('invisible');
        }
      },
      click: async (event) => {
        if(event.target.id !== `delete_diary_${diary._id}` && event.target.id !== `edit_diary_${diary._id}`) {
          $(`#modal_${diary._id}`).css('display', 'block');
        };

        $(`#note-text_${diary._id}`).empty();


        members = context.selectedClassroom.members;    
        

        members.forEach((member) => {
          member.notes.forEach((note) => {
            if (note.diary_id === diary._id) {
              if(note.note !== "") {
                $(`
                  <div id="note_${member._id}" class="ml-3" >
                    <span style="font-weight: bold;">${member.fullName}</span>
                    ${note.note}
                    <span style="display:none" >${note._id}</span>
                  </div>
                `).appendTo(`#note-text_${diary._id}`);
              } else {
                $(`
                <div id="note_${member._id}" class="ml-3" >
                  <span style="font-weight: bold;">${member.fullName}</span>
                  <p></p>
                </div>
              `).appendTo(`#note-text_${diary._id}`);
              } 
            } 
          })       
        })

        $(window).on('click', (event) => {
          if (event.target.id === `modal_${diary._id}`) {
            $(`#modal_${diary._id}`).css('display', 'none');
          }
        })
      }
    })
  })
})
