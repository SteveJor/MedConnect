// /src/js/router.js
import $ from 'jquery';

// Chemins valides pour les slides animés
const validSlides = ['slide0','slide1', 'slide2', 'slide3'];

/**
 * Charge dynamiquement une page dans le conteneur #app avec animation
 */
export function loadPage(direction = 'forward', status = 1) {
    if (status === 1) {
        if (!window.location.hash.slice(1)) {
            history.pushState(null, '', `#slide0`);
        }
        const hash = window.location.hash.slice(1) || 'slide1';
        const page = validSlides.includes(hash) ? hash : 'slide1';
        const path = `/src/templates/welcomeSlides/${page}.html`;

        const app = $('#app');
        const animationOut = direction === 'forward' ? 'slide-out-left' : 'slide-out-right';
        const animationIn = direction === 'forward' ? 'slide-in-right' : 'slide-in-left';

        app.addClass(animationOut);

        setTimeout(() => {
            fetch(path)
                .then(res => {
                    if (!res.ok) throw new Error('Page not found');
                    return res.text();
                })
                .then(html => {
                    app.removeClass(animationOut).html(html).addClass(animationIn);
                    setTimeout(() => app.removeClass(animationIn), 300);
                })
        }, 1000);

    } else if (status === 2) {
        loadView("loginPages/login.html", () => {
            history.pushState(null, '', `Login`);
        });
    }

}

/**
 * Routeur principal (SPA) basé sur pathname
 */
export function router() {
    const path = window.location.pathname;

    if (path === "/") {

        loadPage('forward', 1); // Accueil avec animation slide1
    }
    else if (path === "/Login") {
        loadView("loginPages/Login.html", () => {
        });
    }
    else if (path === "/Signin") {
        loadView("loginPages/register0.html", () => {
        });
    }
    else if (path === "/Register1") {
        loadView("loginPages/register1.html", () => {
        });
    }
    else if (path === "/Register2") {
        loadView("loginPages/register2.html", () => {
        });
    }
    else if (path === "/Register3") {
        loadView("loginPages/register3.html", () => {
        });
    }
    else if (path === "/Register4") {
        loadView("loginPages/register4.html", () => {
        });
    }
    else if (path === "/Register5") {
        loadView("loginPages/register5.html", () => {
        });
    }
    else if (path === "/Signin1") {
        loadView("produits.html", () => {
            $.getJSON("/api/produits/", function (data) {
                let html = "";
                data.forEach(prod => {
                    html += `<li><a href="/produits/${prod.id}" data-link>${prod.nom}</a></li>`;
                });
                $("#produit-list").html(html);
            });
        });
    } else if (path.startsWith("/produits/")) {
        const id = path.split("/")[2];
        loadView("produit_detail.html", () => {
            $.getJSON(`/api/produits/${id}/`, function (data) {
                $("#produit-nom").text(data.nom);
                $("#produit-description").text(data.description);
            });
        });
    } else if (path === "/produit/ajouter") {
        loadView("produit_form.html", () => {
            $("#form-produit").submit(function (e) {
                e.preventDefault();
                const data = {
                    nom: $("#nom").val(),
                    description: $("#description").val()
                };
                $.ajax({
                    url: "/api/produits/",
                    method: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(data),
                    success: () => {
                        alert("Produit ajouté !");
                        navigateTo("/produits");
                    },
                    error: () => {
                        alert("Erreur !");
                    }
                });
            });
        });
    } else {
        loadView("404.html");
    }
}

/**
 * Charge une vue statique HTML dans #app
 */
function loadView(view, callback) {
    $.get(`src/templates/${view}`, function (data) {
        $("#app").html(data);
        if (callback) callback();
    });
}

/**
 * Navigation sans rechargement de page
 */
function navigateTo(url) {
    history.pushState(null, '', url);
    router();
}

// Navigation SPA au clic sur les liens
$(document).on('click', 'a[data-link]', function (e) {
    e.preventDefault();
    const href = $(this).attr('href');
    navigateTo(href);
});

// Gère le bouton "précédent" et "suivant" du navigateur
window.onpopstate = () => {
    router();
};
