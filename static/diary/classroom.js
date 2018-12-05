const renderClassroom = () => {
  $("#courses").on('click', async (event) =>{
    $('#course_name').empty();
    $('#classrooms').empty();
    if (event.target.localName === "div") {
      courseID = event.target.id;
    } else if (event.target.localName === "span") {
      courseID = event.target.parentNode.id;
    }
    context.selectedCourse = context.courses.find(course => course._id === courseID);
    
    const courseName = context.selectedCourse.longname;
    $(`
      <div style="font-size:30px; font-weight: bold;">
        <span id="selected_course_${courseID}">${courseName}</span>
        <span></span>
        <span></span>
      </div>
      <div class="mt-3 mb-3" style="font-weight:500">Classes</div>
    `).appendTo('#course_name')
    context.selectedCourse.classrooms.forEach((classroom) => {
      $(`
        <div id="${classroom._id}" style="width:18%;" class="mr-1 mb-1 classroom_detail d-flex justify-content-between align-items-center">
          <span class="ml-3">${classroom.keyword.toUpperCase()}</span>
          <span id="icons_${classroom._id}" style="float:right" class="invisible">
            <img class="icon_pen_recycle" style="height:25px" src="/static/diary/Icons/2x/pen.png">
            <img class="icon_pen_recycle" style="height:25px" src="/static/diary/Icons/2x/recycle.png">
          </span>
        </div>

      `).appendTo('#classrooms');
    })
    initHoverClassroom();
    renderSession();
    initHoverBackClassroom();
  })
}


const initHoverClassroom = (() => {
  context.selectedCourse.classrooms.forEach((classroom) => {
    $(`#${classroom._id}`).on({
      mouseenter: (event) => {
        $(`#${classroom._id}`).css({"cursor": "pointer", "color":"white"})
        if(context.userRole !== "manager") {
          $(`#icons_${classroom._id}`).removeClass('invisible');
        }
      },
      mouseleave: (event) => {
        $(`#${classroom._id}`).css("color","black")
        if(context.userRole !== "manager") {
          $(`#icons_${classroom._id}`).addClass('invisible');
        }
      }
    })
  });
})


const initHoverBackClassroom = () => {
  courseID = context.selectedCourse._id;
  $(`#selected_course_${courseID}`).on({
    mouseenter: (event) => {
      $(`#selected_course_${courseID}`).css({'cursor':'pointer', 'color':'white', 'transition':'0.1s'});
    },
    mouseleave: (event) => {
      $(`#selected_course_${courseID}`).css({'color':'black', 'transition':'0.1s'});
    },
    click: (event) => {
      $(`#${courseID}`).click();
    }
  })
}