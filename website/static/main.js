$(document).ready(function() {

    // Add smooth scrolling to all links
    $(".tab").on('click', function(event) {
        var sectionId = $(this).data('section-id');
        var targetOffset = $(`section${sectionId}`).offset().top;        
        // Prevent default anchor click behavior
        event.preventDefault();
        const scrollDuration = 800;

        // Smooth scroll to the target element
        $('html, body').animate({
            scrollTop: targetOffset
        }, scrollDuration, function() {
            window.location.hash = sectionId;
        });        
    });
    
});

$(window).on('scroll', function() {
    const $image = $('#logo');
    const scrollPosition = $(window).scrollTop();
    const scale = Math.max(1 - scrollPosition / 1000, 0.4);
    const offset = 90;

    $image.css('transform', `scale(${scale})`);
    
    const initialTop = (($(window).height() - $image.height()) / 2) - offset;
    const finalTop = -70;
    const top = Math.max(finalTop, initialTop - scrollPosition);


    $image.css({
        'position': 'fixed',
        'top': `${Math.max(top, -70)}px`
    }); 
});