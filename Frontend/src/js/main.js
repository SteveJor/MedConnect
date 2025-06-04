// src/js/main.js
import $ from 'jquery';
import { loadPage } from './router.js';

window.addEventListener('hashchange', loadPage);
window.addEventListener('load', () => {
  // Si l'URL ne contient pas de hash, redirige vers #slide1
  if (!window.location.hash) {
    window.location.hash = '#slide1';
  } else {
    loadPage();
  }
});

