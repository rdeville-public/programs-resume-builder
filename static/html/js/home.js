//"use strict";
// Auto hide nav drop-down when on mobil
const navLinks = document.querySelectorAll('.nav-item')
const menuToggle = document.getElementById('top-nav-items')
const bsCollapse = new bootstrap.Collapse(menuToggle, {toggle:false})
navLinks.forEach((l) => {
    l.addEventListener('click', () => { bsCollapse.toggle() })
})

// Put content of egg in page
$("#egg").load("egg.html")

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
    /*
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
    */

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
      // addSmoothScroll();
    };
    var storedTheme = localStorage.getItem('theme')
      || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    if (storedTheme)
        document.documentElement.setAttribute('data-theme', storedTheme)
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

function toggleTheme() {
    var toggle = document.getElementById("theme-switch");
    var storedTheme = localStorage.getItem('theme')
    var currentTheme = document.body.getAttribute("data-theme");
    var targetTheme = "light";
    var targetClass = "fas fa-sun"
    var targetIconClass = "avatar-icon-light"
    var targetIconTmpID = "avatar-tmp-icon-light"

    if (currentTheme === "light") {
        targetTheme = "dark";
        targetClass = "fas fa-moon"
        targetIconClass = "avatar-icon-dark"
        targetIconTmpID = "avatar-tmp-icon-dark"
    }

    document.body.setAttribute('data-theme', targetTheme)
    localStorage.setItem('theme', targetTheme);
    var icon = document.getElementById("theme-switcher-icon");
    icon.setAttribute("class",targetClass);
    var avatar = document.getElementById("avatar-icon");
    var avatar_temp_src = document.getElementById(targetIconTmpID).getAttribute("title");
    var avatar_src = document.getElementById("avatar-icon");
    avatar_src.setAttribute("src",avatar_temp_src);
    var logo_src = document.getElementById("logo");
    logo_src.setAttribute("src",avatar_temp_src);
    var favicon_src = document.getElementById("favicon");
    favicon_src.setAttribute("href",avatar_temp_src);
};

//Get the button:
mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

function toggleSkillDetail(id) {
  var card_body = document.getElementById("skill-card-body-" + id);
  var detail_icon = document.getElementById("skill-card-detail-" + id);
  if (card_body.classList.contains('d-block')) {
    card_body.classList.remove('d-block');
    card_body.classList.add('d-none');
    detail_icon.innerHTML = '<span style="font-size:1.5em" class="fa-angle-right fas"></span>'
  } else {
    card_body.classList.remove('d-none');
    card_body.classList.add('d-block');
    detail_icon.innerHTML = '<span style="font-size:1.5em" class="fa-angle-down fas"></span>'
  }
}


function openDataPrivacy() {
    var cdiv = document.getElementById("data-privacy-overlay");
    cdiv.setAttribute("class","d-block")
}

function closeDataPrivacy() {
    var cdiv = document.getElementById("data-privacy-overlay");
    cdiv.setAttribute("class","d-none")
}

