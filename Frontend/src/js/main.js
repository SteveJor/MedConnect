// src/js/main.js
import $ from 'jquery';
import { router } from './app/router.js';

// window.addEventListener('hashchange', loadPage);
window.addEventListener('load', () => {
  // Si l'URL ne contient pas de hash, redirige vers #slide1

    router();
});

