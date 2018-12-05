$(document).ready(() => {
  buttonLogout();
});

const buttonLogout = () => {
  $('#logout-icon').on({
    click: () => {
      $('#logout-box').css({"display":"block"})
      $(window).on('click', (event) => {
        console.log(event);
        if (event.target.className !== "logout-info" && event.target.id !== "logout-icon") {
          $('#logout-box').css({"display":"none"})
        }
      })
    },
    mouseenter: () => {
      $('#logout-icon').css({"cursor":"pointer"})
    }
  })
}