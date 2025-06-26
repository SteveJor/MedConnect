
// Fonction pour basculer la visibilité du mot de passe
import {router} from "/src/js/app/router.js";
export function mainScripts() {
    const sidebar = document.querySelector(".sidebar");
    const userBtn = document.querySelector(".user");
    const closeBtn = document.querySelector(".close-btn");
    const username = document.querySelector("#username");

    userBtn.addEventListener("click", () => {
        sidebar.classList.add("active");
    });

    closeBtn.addEventListener("click", () => {
        sidebar.classList.remove("active");
    });

    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    username.innerHTML = userData.infoUser.username
    document.getElementById("details_name").innerHTML = userData.infoUser.username

    function goBack(event, url) {
        event.preventDefault();

        history.pushState(null, '', url);
        router();
    }

    window.goBack = goBack;
}
