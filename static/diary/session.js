const renderSession = () => {
  context.selectedCourse.classrooms.forEach((classroom) => {
    $(`#${classroom._id}`).on('click', (event) => {
      courseDiv = $($('#course_name')[0].childNodes[0]);
      classesDiv = $($('#course_name')[0].childNodes[2]);
      $(`<span> > </span>`).appendTo(courseDiv[0].childNodes[1]);
      
      // $(` > `).appendTo('')
      $(courseDiv[0].childNodes[3]).attr('id', `selected_classroom_${classroom._id}`)
      courseDiv[0].childNodes[3].innerText = `${classroom.keyword.toUpperCase()}`    
      classesDiv[0].innerText = `Session`;
      $('#classrooms').empty();
      
      classroom.sessions.forEach((session) => {      
        $(`
          <div id="session_${session.session_num.split(" ")[1]}" class="textbox">
            <div class="d-flex justify-content-between">
              <span> ${session.session_num.toUpperCase()} </span>
            </div>
          </div>
        `).appendTo('#classrooms');

      })
      initSession(classroom._id);
      renderDiary();
      initHoverBackSession();
    })
  })
}


const initSession = ((classroomID) => {
  context.selectedClassroom = context.selectedCourse.classrooms.find(classroom => classroom._id === classroomID);
  
  context.selectedClassroom.sessions.forEach((session) => {
    $(`#session_${session.session_num.split(" ")[1]}`).on({
      mouseenter: (event) => {
        $(`#session_${session.session_num.split(" ")[1]}`).css({'cursor':'pointer', 'color':'white', 'transition': '0.1s'});
        // if(context.userRole !== "manager") {
        //   $(`#icons_${session._id}`).removeClass('invisible');
        // }
      },
      mouseleave: (event) => {
        $(`#session_${session.session_num.split(" ")[1]}`).css({'color':'black', 'transition': '0.1s'});
        // if(context.userRole !== "manager") {
        //   $(`#icons_${session._id}`).addClass('invisible');
        // }
      },
    })
  })
})


const initHoverBackSession = () => {
  courseID = context.selectedCourse._id;
  classroomID = context.selectedClassroom._id;
  $(`#selected_classroom_${classroomID}`).on({
    mouseenter: (event) => {
      $(`#selected_classroom_${classroomID}`).css({'cursor':'pointer', 'color':'white', 'transition':'0.1s'});
    },
    mouseleave: (event) => {
      $(`#selected_classroom_${classroomID}`).css({'color':'black', 'transition':'0.1s'});
    },
    click: async (event) => {
      await $(`#${courseID}`).click();
      $(`#${classroomID}`).click();
    }
  })
}