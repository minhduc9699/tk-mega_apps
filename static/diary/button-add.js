const addNewDiary = () => {
  $('#btn_add').on('click', () => {
    DiaryForm("POST");
    $(window).on('click', (event) => {
      if (event.target.className === `add-diary`) {
        $(`.add-diary`).css('display', 'none');
        $('#btn_save_diary').unbind('click');
      }
    })
    $('#slt_course').attr('disabled', false);
    $('#slt_course').css("background", "white");
    $('.add-diary')[0].childNodes[1].childNodes[1].innerText = "Add new diary";
  });
}