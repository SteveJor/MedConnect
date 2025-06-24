// login.js
import { router } from '/src/js/app/router.js';

export function initLoginView() {
    window.togglePasswordVisibility = function (id) {
        const passwordField = document.getElementById(id);
        const toggleIcon = passwordField.nextElementSibling;
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            toggleIcon.textContent = '🤐';
        } else {
            passwordField.type = 'password';
            toggleIcon.textContent = '👁';
        }
    };

    window.submitForm = function (event) {
        event.preventDefault();
        // Affiche le loader
        document.getElementById('loader').style.display = 'flex';

        // Masque le formulaire (facultatif)
        document.querySelector('.glass-card').style.display = 'none';
        document.querySelector('.topgreen-screen').style.display = 'none';

        // Attendre 2 secondes puis accéder à /Home
        setTimeout(() => {
            history.pushState(null, '', '/Home');
            router(); // navigation vers la page Home
        }, 3000);
    };
}

