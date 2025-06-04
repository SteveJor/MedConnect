import $ from 'jquery';






const screens = [
  ``,
  ``,
  ``
];

let current = 0;

function renderScreen(index) {
  $('#onboarding-container').fadeOut(300, function () {
    $(this).html(screens[index]).fadeIn(300);
  });
}

function setupEvents() {
  $('#onboarding-container').on('click', '.start', () => {
    if (current < screens.length - 1) {
      current++;
      renderScreen(current);
    } else {
      // Charger login.html ou afficher le formulaire
      $('#onboarding-container').fadeOut(300, function () {
        $(this).html('<h1>Formulaire de connexion ici...</h1>').fadeIn(300);
      });
    }
  });

  $('#onboarding-container').on('click', '.skip', () => {
    $('#onboarding-container').fadeOut(300, function () {
      $(this).html('<h1>Formulaire de connexion ici...</h1>').fadeIn(300);
    });
  });
}

$(document).ready(function () {
  renderScreen(current);
  setupEvents();
});