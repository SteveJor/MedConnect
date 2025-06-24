// src/js/main.js
import $ from 'jquery';
import { router } from './app/router.js';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// window.addEventListener('hashchange', loadPage);
window.addEventListener('load', () => {
  // Si l'URL ne contient pas de hash, redirige vers #slide1

    router();
});

