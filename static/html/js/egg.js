// a key map of allowed keys
var allowedKeys = {
  37: 'left',
  38: 'up',
  39: 'right',
  40: 'down',
  65: 'a',
  66: 'b'
};

// the 'official' Konami Code sequence
var konamiCode = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a'];

// a variable to remember the 'position' the user has reached so far.
var konamiCodePosition = 0;

// add keydown event listener
document.addEventListener('keydown', function(e) {
  // get the value of the key code from the key map
  var key = allowedKeys[e.keyCode];
  // get the value of the required key from the konami code
  var requiredKey = konamiCode[konamiCodePosition];

  // compare the key with the required key
  if (key == requiredKey) {

    // move to the next key in the konami code sequence
    konamiCodePosition++;

    // if the last key is reached, activate cheats
    if (konamiCodePosition == konamiCode.length) {
      activateCheats();
      konamiCodePosition = 0;
    }
  } else {
    konamiCodePosition = 0;
  }
});


function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

function closeTerm() {
    var cdiv = document.getElementById("terminal-overlay");
    cdiv.setAttribute("class","d-none")
}

function photography() {
  var body = document.body
  if (body.classList.contains("photography"))
    body.classList.remove("photography")
  else {
    body.setAttribute("class","")
    body.setAttribute("class","photography")
  }
}

function bicycle() {
  var body = document.body
  if (body.classList.contains("bicycle"))
    body.classList.remove("bicycle")
  else {
    body.setAttribute("class","")
    body.setAttribute("class","bicycle")
  }
}

function activateCheats() {
  if (document.body.style.fontFamily == "") {
    var cdiv = document.getElementById("terminal-overlay");
    cdiv.setAttribute("class","d-block")
    document.body.style.fontFamily = "FuraCode Nerd Font, -apple-system, Helvetica, Arial, sans-serif";
  }
  else
  {
    var cdiv = document.getElementById("terminal-overlay");
    cdiv.setAttribute("class","d-none")
    document.body.style.fontFamily = "";
  }


}

function cycleFrames (_nyanCat, _currentFrame) {
  _nyanCat.classList = []
  _nyanCat.classList.add(`frame${_currentFrame}`)
}

(function () {
  let nyanCat = document.getElementById('nyan-cat')
  let currentFrame = 1

  setInterval(function () {
    currentFrame = (currentFrame % 6) + 1
    cycleFrames(nyanCat, currentFrame)
  }, 70)
})()


