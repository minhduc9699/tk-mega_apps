$(document).ready(function () {
  $("#startDate").flatpickr({
    enableTime: false,
    dateFormat: "Y-m-d",
    maxDate: "today"
  });
  $("#stopDate").flatpickr({
    enableTime: false,
    dateFormat: "Y-m-d",
    maxDate: "today"
  });
});
$(document).on('change', '#startDate', function () {

  if ($('#startDate').val() != '' && $('#stopDate').val() != '') {
    $('#form').submit();
  }
});

$(document).on('change', '#stopDate', function () {

  if ($('#startDate').val() != '' && $('#stopDate').val() != '') {
    $('#form').submit();
  }
});