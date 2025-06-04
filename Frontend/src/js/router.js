import $ from 'jquery';

export function loadPage(direction = 'forward') {
    const hash = window.location.hash.slice(1) || 'slide1';
    const validSlides = ['slide1', 'slide2', 'slide3'];
    const page = validSlides.includes(hash) ? hash : 'slide1';
    const path = `/src/js/views/welcomeSlides/${page}.html`;
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
            .catch(() => {
                app.removeClass(animationOut).html(`
          <h1 style="text-align:center;color:red;">Page introuvable</h1>
        `).addClass(animationIn);
                setTimeout(() => app.removeClass(animationIn), 300);
            });
    }, 300);
}
