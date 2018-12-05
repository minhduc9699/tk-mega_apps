context = {
  likes: null,
  statusLike: 0
}

$(document).ready( async () => {
  await fetchLike();
  renderStatusLike();
  buttonLike();
  renderNumberLikes();
})


const fetchLike = async () => {
  const base = window.location.origin;
  const path = window.location.pathname;
  const fullLink = base + "/like" + path;
  const res = await $.ajax({
    url: fullLink,
    type: "GET"
  }) 
  if (res && res.data) {
    context.likes = res.data;
  }
}


const postLike = async () => {
  const base = window.location.origin;
  const path = window.location.pathname;
  const fullLink = base + "/like" + path;
  const res = await $.ajax({
    url: fullLink,
    type: "POST"
  })
}


const renderStatusLike = () => {
  if (context.likes.liked === 1 ) {
    $('#btn_like').css('opacity','inherit');
  } else {
    $('#btn_like').css('opacity', '');
  }
}


const renderNumberLikes = () => {
  if (context.likes.total_like < 2) {
    $('#btn_like')[0].parentNode.parentNode.childNodes[0].textContent = context.likes.total_like + " like";
  } else {
    $('#btn_like')[0].parentNode.parentNode.childNodes[0].textContent = context.likes.total_like + " likes";
  }
}


const buttonLike = () => {
  $('#btn_like').on({
    click: async () => {
      await postLike();
      await fetchLike();
      renderNumberLikes();
      if (context.likes.liked === 0) {
        $('#btn_like').css('opacity', '');
      } else {
        $('#btn_like').css('opacity', 'inherit');
      }
    },
  })
}