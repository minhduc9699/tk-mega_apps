const initDiaryDate = () => {
  $("#diary_date").flatpickr({
    maxDate: "today",
    defaultDate: "today",
  });
}


const setLoading = (loading) => {
  context.loading = loading;
  if (context.loading) {
    $('#loading_indicator').css('display','block');
  } else {
    $('#loading_indicator').css('display','none');
    $(`.add-diary`).css('display', 'none');
  }
}