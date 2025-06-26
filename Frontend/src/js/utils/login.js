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

    window.submitForm = async function (event) {
        event.preventDefault();

        // Récupérer les champs
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        const errorDiv = document.getElementById("error-message");
        errorDiv.textContent = ""; // reset erreurs

        if (!email || !password) {
            errorDiv.textContent = "Veuillez remplir tous les champs.";
            return;
        }

        // Affiche le loader
        document.getElementById("loader").style.display = "flex";
        document.querySelector('.glass-card').style.display = 'none';
        document.querySelector('.topgreen-screen').style.display = 'none';

        try {
            const response = await fetch("http://127.0.0.1:8000/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Authentification réussie
                const token = data.token;
                const user = data.user;

                // Sauvegarde du token et de l'utilisateur dans le localStorage
                localStorage.setItem("authToken", token);
                localStorage.setItem("userData", JSON.stringify(user));

                // Redirection après 2 secondes
                setTimeout(() => {
                    history.pushState(null, '', '/Home');
                    router(); // mise à jour de la page
                }, 2000);
            } else {
                // Affiche une erreur
                document.getElementById("loader").style.display = "none";
                document.querySelector('.glass-card').style.display = 'block';
                document.querySelector('.topgreen-screen').style.display = 'block';

                errorDiv.textContent = data.error || "Erreur lors de la connexion.";
            }

        } catch (error) {
            console.error("Erreur réseau :", error);
            document.getElementById("loader").style.display = "none";
            document.querySelector('.glass-card').style.display = 'block';
            document.querySelector('.topgreen-screen').style.display = 'block';

            errorDiv.textContent = "Erreur réseau. Veuillez vérifier votre connexion.";
        }
    };

}

