/* CAROUSEL VARS */
var isDragging = false;
var startPosition;
var startScrollLeft;
var startY;
/* CAROUSEL VARS END */

var scrollTop = $(window).scrollTop();

$(document).ready(function() {
    scripts_lazyLoadImages();    
    scripts_scrollwindow();        
    scripts_hiddendropdowns();    

    /* NAVBAR */
    $(".menu.mobile").html($(".navbar .content .menu").html());

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
        }
    });

    $(document).on("click", ".carousel .right-arrow", function() {
        scripts_carouselnext(this);
    });           

    setInterval(function(){  
        scripts_carouselarrows();
    }, 100);

    setInterval(function(){  
        scripts_lazyLoadImages();
    }, 500);

    setInterval(function(){ 
        if (!document.hidden) {
            $(".section-0 .carousel .right-arrow").click();
        }
    }, 5000);
    /* CAROUSEL END */
});

/* GENERIC FUNCTIONS */
function scripts_carouselarrows() {
    $(".carousel").each(function() {
        var carousel = $(this);
        var carouselPage = parseInt(carousel.find("input[name='page']").val());

        if (carouselPage <= 1) {
            carousel.find(".left-arrow").removeClass("active");
        } else {
            carousel.find(".left-arrow").addClass("active");
        }
    });
}

function scripts_carouselnext(e){
    var carousel = $(e).siblings(".container");
    var carouselWidth = carousel.outerWidth();
    var carouselPage = parseInt($(e).siblings("input[name='page']").val());
    var itemWidth = carousel.find(".content .data").outerWidth();
    var visibleItems = Math.floor(carouselWidth / itemWidth);
    var totalPages = Math.ceil(carousel.find(".data").length / visibleItems);

    if (carouselPage < totalPages) {
        carouselPage++;
        var page_start = carouselPage - 1;
        $(e).siblings("input[name='page']").val(carouselPage);
        carousel.animate({ scrollLeft: page_start * carouselWidth }, "slow");
    } else {
        $(e).siblings("input[name='page']").val(1);
        carousel.animate({ scrollLeft: 0 * carouselWidth }, "slow");
    }
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
    var menumobile = $(".menu.mobile");

    if(scripts_isMobile()){
        if (newScrollTop > scrollTop) {      
            menumobile.fadeOut(200);
            setTimeout(function(){
                navbar.css("height", "70px")
            }, 500);            
        } else {  
            navbar.css("height", "120px")   
            setTimeout(function(){   
                menumobile.fadeIn(200); 
            }, 100);     
        }
    } else {
        navbar.css("height", "70px")
    }

    if (scrollTop > 70) {            
        navbar.find(".content").addClass("active");
        menumobile.addClass("active")
    } else {            
        navbar.find(".content").removeClass("active");
        menumobile.removeClass("active")        
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
