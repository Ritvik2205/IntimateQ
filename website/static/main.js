$(document).ready(function() {
    $(window).on('scroll', function() {
        const $image = $('img');
        const scrollPosition = $(window).scrollTop();
        const scale = Math.max(1 - scrollPosition / 1000, 0.5);
    
        $image.css('transform', `scale(${scale})`);
        
        const initialTop = ($(window).height() - $image.height()) / 2;
        const finalTop = -70;
        const top = Math.max(finalTop, initialTop - scrollPosition);
    
    
        $image.css({
            'position': 'fixed',
            'top': `${Math.max(top, -70)}px`
        }); 
    });
});
