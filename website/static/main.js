$(document).ready(function() {

    // Add smooth scrolling to all links
    $(".tab a").on('click', function(event) {
        if (this.hash !== "") {
            // Prevent default anchor click behavior
            event.preventDefault();
            const hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function() {
                window.location.hash = hash;
            });
        } 
    });
    
});

$(window).on('scroll', function() {
    const $image = $('#logo');
    const scrollPosition = $(window).scrollTop();
    const scale = Math.max(1 - scrollPosition / 1000, 0.5);
    const offset = 90;

    $image.css('transform', `scale(${scale})`);
    
    const initialTop = (($(window).height() - $image.height()) / 2) - offset;
    const finalTop = -50;
    const top = Math.max(finalTop, initialTop - scrollPosition);


    $image.css({
        'position': 'fixed',
        'top': `${Math.max(top, -70)}px`
    }); 
});