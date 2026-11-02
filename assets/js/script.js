
$(document).ready(function () {
    $('.coming-up').click(function () {
        $('#coming-soon').modal('show');
    });
    $('ul.tabs li').click(function () {
        var tab_id = $(this).attr('data-tab');

        $('ul.tabs li').removeClass('current');
        $('.tab-content').removeClass('current');

        $(this).addClass('current');
        $("#" + tab_id).addClass('current');
    })

});
$(window).on('scroll', function () {
    if ($(window).scrollTop() > 100) {
        $('.header').addClass('bg-color animated fadeInDown');
    } else {
        $('.header').removeClass('bg-color animated fadeInDown');
    }
});
new WOW().init();
$('.testi_div').owlCarousel({
    loop: true,
    items: 1,
    margin: 0,
    stagePadding: 0,
    smartSpeed: 450,
    autoplay: true,
    autoPlaySpeed: 3000,
    autoPlayTimeout: 3000,
    autoplayHoverPause: true,
    dots: false,
    nav: true,
    navText: ["<img src='assets/img/left_white_arrow.svg'>", "<img src='assets/img/right_white_arrow.svg'>"],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1
        }
    }
});
$('.banner').owlCarousel({
    loop: true,
    items: 1,
    margin: 0,
    stagePadding: 0,
    smartSpeed: 450,
    autoplay: true,
    autoPlaySpeed: 3000,
    autoPlayTimeout: 3000,
    autoplayHoverPause: true,
    dots: true,
    nav: false,
    navText: ["<img src='assets/img/left_white_arrow.svg'>", "<img src='assets/img/right_white_arrow.svg'>"],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1
        }
    }
});
$('.blog_sec').owlCarousel({
    loop: true,
    items: 1,
    margin: 30,
    stagePadding: 0,
    smartSpeed: 450,
    autoplay: true,
    autoPlaySpeed: 3000,
    autoPlayTimeout: 3000,
    autoplayHoverPause: true,
    rtl: true,
    dots: false,
    nav: true,
    navText: ["<img src='assets/img/blog_right.svg'>", "<img src='assets/img/blog_left.svg'>"],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1.1
        }
    }
});
$('.activities_sec').owlCarousel({
    loop: false,
    items: 1,
    margin: 0,
    stagePadding: 0,
    smartSpeed: 450,
    autoplay: true,
    autoPlaySpeed: 3000,
    autoPlayTimeout: 3000,
    autoplayHoverPause: true,
    dots: false,
    nav: true,
    navText: ["<img src='assets/img/blog_left.svg'>", "<img src='assets/img/blog_right.svg'>"],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1.2
        }
    }
});
$('.why_main').owlCarousel({
    loop: true,
    items: 1,
    margin: 60,
    stagePadding: 0,
    smartSpeed: 450,
    autoplay: true,
    autoPlaySpeed: 3000,
    autoPlayTimeout: 3000,
    autoplayHoverPause: true,
    dots: true,
    nav: false,
    navText: ["<img src='assets/img/left_white_arrow.svg'>", "<img src='assets/img/right_white_arrow.svg'>"],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 3
        }
    }
});


$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#scroll').fadeIn();
        } else {
            $('#scroll').fadeOut();
        }
    });
    $('#scroll').click(function () {
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
});


$('.counter1').counterUp({
    time: 1500
});
$('.counter2').counterUp({
    time: 1500
});
$('.counter3').counterUp({
    time: 1500
});
$('.counter4').counterUp({
    time: 1500
});

$(document).ready(function () {
    $('.popup-gallery').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
        },
        image: {
            markup: '<div class="mfp-figure">' +
                '<div class="mfp-close"></div>' +
                '<div class="mfp-img"></div>' +
                '<div class="mfp-bottom-bar">' +
                '<div class="mfp-title"></div>' +
                '<div class="mfp-counter"></div>' +
                '</div>' +
                '</div>',
            cursor: 'mfp-zoom-out-cur',
            titleSrc: 'title',
            verticalFit: true,
            tError: '<a href="%url%">The image</a> could not be loaded.'
        }
    });
});
$(document).ready(function () {
    $(".at-title").click(function () {
        $(this).toggleClass("active").next(".at-tab").slideToggle().parent().siblings().find(".at-tab").slideUp().prev().removeClass("active");
    });
});
$(document).on('click', '.qty-plus', function () {
    $(this).prev().val(+$(this).prev().val() + 1);
});
$(document).on('click', '.qty-minus', function () {
    if ($(this).next().val() > 0) $(this).next().val(+$(this).next().val() - 1);
});


if (jQuery(window).width() < 1024) {

    $('.bot_head_link').hide();

    $(".mobile-header-icon").click(function () {

        $('.mobile-header-icon').toggleClass('open');

        $('.bot_head_link').slideToggle();
        //  $('.bot_head_link').show();

    });

}
if (jQuery(window).width() < 1024) {


    $(".top_header_btn span").click(function () {

        $('.submenux').slideToggle();

    });

}




