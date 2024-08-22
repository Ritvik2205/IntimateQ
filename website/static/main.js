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
    
    // Chat button redirect to doctors
    $(".chat-btn").on('click', function(event) {
        var sectionId = '#doctors';
        var targetOffset = $('#doctors').offset().top;        
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

    $("#chat-scroll-btn").on('click', function() {
        window.location.href = '/all_doctors';   
    })

    $(".see-all-btn").on('click', function() {
        window.location.href = '/all_doctors';
    });

    function showDoctor() {
        if (window.location.href.includes('all_doctors')) {
            $('.doctor').addClass('show');
        }
    }

    $(window).on('popstate', function() {
        showDoctor();
    })
    showDoctor();

    $('.doctor-consult-btn').on('click', function() {
        var doctorId = $(this).closest('.doctor').data('doctor-id');
        console.log(doctorId);
        $.post(`/generate_room/${doctorId}`, function(data) {
            const roomCode = data.room_code;
            const doctorId = data.doctor_id;
            window.location.href = `/chat/${roomCode}/${doctorId}`;
        });
    });

    // function addMessage(roomCode) {
    //     const messageDiv = $('<div>').addClass('message');
    //     const messageText = $('<p>').text()
    // }
});

$(window).on('scroll', function() {
    const $image = $('#logo');
    const scrollPosition = $(window).scrollTop();
    const scale = Math.max(1 - scrollPosition / 1000, 0.4);
    const offset = 90;

    $image.css('transform', `scale(${scale})`);

    
    
    const initialTop = (($(window).height() - $image.height()) / 2) - offset;
    if ($(window).width() <= 768) {        
        const finalTop = 120;
        const top = Math.min(finalTop, initialTop - scrollPosition);
        $image.css({
            'position': 'fixed',
            'top': `${Math.max(top, -70)}px`
        }); 
    } else {
        const finalTop = -70;
        const top = Math.max(finalTop, initialTop - scrollPosition);
        $image.css({
            'position': 'fixed',
            'top': `${Math.max(top, -70)}px`
        }); 
    }
    

    const homepageHeight = $('#homepage').height();
    if (scrollPosition > homepageHeight) {
        $('#chat-scroll-btn').addClass('show');
    } else {
        $('#chat-scroll-btn').removeClass('show');
    }

    const servicesHeight = $('#services').height();  
    const scrollOffset = 200;  
    if (scrollPosition > (homepageHeight - scrollOffset) && $(window).width() <= 768) {
        $('.service').addClass('show');
    } else {
        $('.service').removeClass('show');
    }

    const heightForDoctors = homepageHeight + servicesHeight;
    if (scrollPosition > (heightForDoctors - scrollOffset)) {
        $('.doctor').addClass('show');
    } else {
        $('.doctor').removeClass('show');
    }

    const heightForWhyUs = heightForDoctors + $('#doctors').height();
    if (scrollPosition > (heightForWhyUs - scrollOffset)) {
        $('.why-us-card').each(function(index) {
            const $this = $(this);
            setTimeout(function() {
                $this.addClass('show');                
            }, index * 250);
        })
    } else {
        $('.why-us-card').removeClass('show');
    }
});