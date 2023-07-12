/* CAROUSEL VARS */
var isDragging = false;
var startPosition;
var startScrollLeft;
var startY;
/* CAROUSEL VARS END */

var scrollTop = $(window).scrollTop();

$(document).ready(function() {
    scripts_lazyLoadImages();
    scripts_carouselarrows();
    scripts_scrollwindow();        
    scripts_hiddendropdowns();    

    /* NAVBAR */
    $(".navbar.mobile .content .menu").html($(".navbar .content .menu").html());

    $(document).on("click", "[dropdown]", function(event) {
        event.stopPropagation();
        $(this).toggleClass("active");
        $(this).siblings($(this).attr("dropdown")).fadeToggle(90, function() {
            $(this).css("display", ($(this).css("display") === "none") ? "none" : "flex");
        });
    });

    $(document).on("click", function() {
        scripts_hiddendropdowns();
    });

    $(window).scroll(function() {
        scripts_scrollwindow();
    });        
    /* NAVBAR END */

    /* CAROUSEL */
    $(document).on("click", ".carousel .left-arrow", function() {
        var carousel = $(this).siblings(".container");
        var carouselWidth = carousel.outerWidth();
        var carouselPage = parseInt($(this).siblings("input[name='page']").val());

        if (carouselPage > 1) {
            carouselPage--;
            var page_start = carouselPage - 1;
            $(this).siblings("input[name='page']").val(carouselPage);
            carousel.animate({ scrollLeft: page_start * carouselWidth }, "slow");
            scripts_carouselarrows();
        }
    });

    $(document).on("click", ".carousel .right-arrow", function() {
        var carousel = $(this).siblings(".container");
        var carouselWidth = carousel.outerWidth();
        var carouselPage = parseInt($(this).siblings("input[name='page']").val());
        var itemWidth = carousel.find(".content .data").outerWidth();
        var visibleItems = Math.floor(carouselWidth / itemWidth);
        var totalPages = Math.ceil(carousel.find(".data").length / visibleItems);

        if (carouselPage < totalPages) {
            carouselPage++;
            var page_start = carouselPage - 1;
            $(this).siblings("input[name='page']").val(carouselPage);
            carousel.animate({ scrollLeft: page_start * carouselWidth }, "slow");
            scripts_carouselarrows();     
        }
    });

    setInterval(function(){
        scripts_lazyLoadImages();
    }, 1000);
    /* CAROUSEL END */
});

/* GENERIC FUNCTIONS */
function scripts_carouselarrows() {
    $(".carousel").each(function() {
        var carousel = $(this);
        var carouselContainer = carousel.find(".container");
        var carouselContainerWidth = carouselContainer.outerWidth();
        var carouselPage = parseInt(carousel.find("input[name='page']").val());
        var itemWidth = carouselContainer.find(".content .data").outerWidth();
        var visibleItems = Math.floor(carouselContainerWidth / itemWidth);
        var totalPages = Math.ceil(carouselContainer.find(".data").length / visibleItems);

        if (carouselPage <= 1) {
            carousel.find(".left-arrow").removeClass("active");
        } else {
            carousel.find(".left-arrow").addClass("active");
        }

        if (carouselPage >= totalPages) {
            carousel.find(".right-arrow").removeClass("active");
        } else {
            carousel.find(".right-arrow").addClass("active");
        }
    });
}

function scripts_hiddendropdowns(){
    $(".dropdown").each(function() {
        var btn = $(this).attr("id");
        $(`[dropdown="#${btn}"]`).removeClass("active");
        $(this).css("display", "none");
    });
}

function scripts_getMousePosition(event) {
    return event.pageX || event.originalEvent.touches[0].pageX;
}

function scripts_isMobile() {
    return window.innerWidth <= 900;
}

function scripts_scrollwindow() {
    var newScrollTop = $(window).scrollTop();
    var navbar = $(".navbar");
    var navbarSecond = $(".navbar.mobile");

    if (scripts_isMobile()) {
        if (newScrollTop > scrollTop) {
            navbar.css("background", "var(--navbar)");
            navbarSecond.css("background", "var(--navbar)");
            setTimeout(function() {
                navbarSecond.css("margin-top", "-70px");
            }, 500);
        } else {
            navbar.css("background", "var(--navbar)");
            navbarSecond.css("background", "var(--navbar)");
            setTimeout(function() {
                navbarSecond.css("margin-top", "70px");
            }, 100);
        }

        if (scrollTop > 70) {
            navbar.css("background", "var(--navbar)");
            navbar.find(".content .user").removeClass("transparent");
            navbar.find(".content .menu").removeClass("transparent");
        } else {
            navbar.find(".content .user").addClass("transparent");
            navbar.find(".content .menu").addClass("transparent");
            navbar.css("background", "linear-gradient(to bottom, var(--navbar), var(--navbar-gradient-2))");
            navbarSecond.css("background", "linear-gradient(to bottom, var(--navbar-gradient-2), var(--navbar-gradient-1))");
        }
    } else {
        if (scrollTop > 70) {
            navbar.css("background", "var(--navbar)");
            navbar.find(".content .user").removeClass("transparent");
            navbar.find(".content .menu").removeClass("transparent");
        } else {
            navbar.find(".content .user").addClass("transparent");
            navbar.find(".content .menu").addClass("transparent");
            navbar.css("background", "linear-gradient(to bottom, var(--navbar), var(--navbar-gradient-1))");
        }
    }

    scrollTop = newScrollTop;
}

function scripts_isInViewport(element) {
    var rect = element.getBoundingClientRect();
    var margin = 200;

    return (
        rect.top >= -margin &&
        rect.left >= -margin &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) + margin &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) + margin
    );
}

function scripts_lazyLoadImages() {
    setTimeout(function() {
        var lazyImages = $(".img__preloader");
    
        lazyImages.each(function() {
            var image = $(this);
    
            if (scripts_isInViewport(image[0])) {
                if (image.css("background-image") == "none") {
                    var tempImage = new Image();
                    tempImage.onload = function() {
                        image.css("background-image", "url(" + image.data("src") + ")");
                        image.removeClass("loading");
                    };
                    tempImage.src = image.data("src");
                }
            }
        });
    }, 500);
}

/* GENERIC FUNCTIONS END */
