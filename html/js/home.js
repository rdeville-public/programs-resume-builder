"use strict";

var projectCards;
var isMobile = false, isTablet = false, isLaptop = false;
(function ($) {
  jQuery(document).ready(function () {
    function detectDevice() {
      if (window.innerWidth <= 425) {
        isMobile = true;
        isTablet = false;
        isLaptop = false;
      } else if (window.innerWidth <= 768) {
        isMobile = false;
        isTablet = true;
        isLaptop = false;
      } else {
        isMobile = false;
        isTablet = false;
        isLaptop = true;
      }
    }
    detectDevice();

    // ================= Smooth Scroll ===================
    function addSmoothScroll() {
      // ref: https://css-tricks.com/snippets/jquery/smooth-scrolling/
      // Select all links with hashes
      $('a[href*="#"]')
        // Remove links that don't actually link to anything
        .not('[href="#"]')
        .not('[href="#0"]')
        .click(function (event) {
          // On-page links
          if (
            location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
            &&
            location.hostname == this.hostname
          ) {
            // Figure out element to scroll to
            var target = $(decodeURI(this.hash));
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            // Does a scroll target exist?
            if (target.length) {
              // Only prevent default if animation is actually gonna happen
              event.preventDefault();

              let offset = 60;
              if (isMobile) {
                offset = 710;
              } else if (isTablet) {
                offset = 60;
              }
              $('html, body').animate({
                scrollTop: target.offset().top - offset
              }, 1000, function () {
                // Callback after animation
                // Must change focus!
                var $target = $(target);
                $target.focus();
                if ($target.is(":focus")) { // Checking if the target was focused
                  return false;
                } else {
                  $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                  $target.focus(); // Set focus again
                };
              });
              // Add hash (#) to URL when done scrolling (default click behavior)
              window.location.hash = this.hash
            }
          }
        });
    }
    addSmoothScroll();

    // =========== Typing Carousel ================
    // get data from hidden ul and set as typing data
    if (document.getElementById('typing-carousel-data') != undefined) {
      var ul = document.getElementById('typing-carousel-data').children;

      if (ul.length != 0) {
        var data = [];
        Array.from(ul).forEach(el => {
          data.push(el.textContent);
        })

        ityped.init('#ityped', {
          strings: data,
          startDelay: 200,
          loop: true
        });
      }
    }

    // ============== Fix Timelines Horizontal Lines =========
    var hLines = document.getElementsByClassName("horizontal-line");
    for (let i = 0; i < hLines.length; i++) {
      if (i % 2) {
        hLines[i].children[0].children[0].classList.add("bottom-right");
        hLines[i].children[2].children[0].classList.add("top-left");
      } else {
        hLines[i].children[0].children[0].classList.add("top-right");
        hLines[i].children[2].children[0].classList.add("bottom-left");
      }
    }

    // ================== Project cards =====================
    // Add click action on project category selector buttons
    var projectCardHolder = document.getElementById("project-card-holder");
    if (projectCardHolder != null && projectCardHolder.children.length != 0) {
      projectCards = $(".filtr-projects").filterizr({ layout: 'sameWidth' });
    }

    // re-render custom functions on window resize
    window.onresize = function () {
      detectDevice();
      addSmoothScroll();
    };
  });
})(jQuery);


// Show more rows in the taken courses table
function showMoreCourses(elem) {

  // find the courses
  let courses = elem.parentNode.getElementsByClassName("course");
  if (courses == null) {
    return
  }

  // toggle hidden-course class from the third elements
  for (var i = 0; i < courses.length; i++) {
    if (i > 1 && courses[i].classList !== null) {
      courses[i].classList.toggle("hidden-course");
    }
  }

  // toggle the button text
  let btnText = elem.innerText;
  if (btnText == "Show More") {
    elem.innerText = "Show Less";
  } else {
    elem.innerText = "Show More";
  }
}
