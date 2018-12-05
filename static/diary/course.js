const renderCourse = () => {
  $("#courses").empty();
  context.courses.forEach((eachCourse) => {
    $(`
    <div id="${eachCourse._id}" tabindex="1" class="row bg-light-brown-text-white radius-right" style="height: 67px;">
      <div class="col-1"></div>
      <span class="" style="padding-top: 8px;">${eachCourse.longname}<span>
    </div>
    `).appendTo('#courses');
  })
  renderClassroom();
}