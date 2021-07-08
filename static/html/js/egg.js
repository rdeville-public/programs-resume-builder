// A key map of allowed keys
var allowedKeys = {
  37: 'left',
  38: 'up',
  39: 'right',
  40: 'down',
  65: 'a',
  66: 'b'
};

// The 'official' Konami Code sequence
var konamiCode = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a'];

// A variable to remember the 'position' the user has reached so far.
var konamiCodePosition = 0;

// Add keydown event listener
document.addEventListener('keydown', function(e) {
  // Get the value of the key code from the key map
  var key = allowedKeys[e.keyCode];
  // Get the value of the required key from the konami code
  var requiredKey = konamiCode[konamiCodePosition];
  // Compare the key with the required key
  if (key == requiredKey)
  {
    // Move to the next key in the konami code sequence
    konamiCodePosition++;
    // If the last key is reached, activate cheats
    if (konamiCodePosition == konamiCode.length)
    {
      activateCheats();
      konamiCodePosition = 0;
    }
  }
  else
  {
    konamiCodePosition = 0;
  }
});


function sleep(milliseconds)
{
  const date = Date.now();
  let currentDate = null;
  do
  {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}


function activateCheats()
{
  if (document.body.style.fontFamily == "")
  {
    var cdiv = document.getElementById("terminal-overlay");
    cdiv.setAttribute("class","d-block")
    document.body.style.fontFamily = "FuraCode Nerd Font, -apple-system, Helvetica, Arial, sans-serif";
    document.body.style.fontSize = "11pt";
  }
  else
  {
    var cdiv = document.getElementById("terminal-overlay");
    cdiv.setAttribute("class","d-none")
    document.body.style.fontFamily = "";
    document.body.style.fontSize = "";
  }
}


function closeTerm()
{
    var cdiv = document.getElementById("terminal-overlay");
    cdiv.setAttribute("class","d-none")
}

function applyClass(_className)
{
  var body = document.body;
  if (body.classList.contains(_className))
    body.classList.remove(_className);
  else
  {
    body.setAttribute("class","");
    body.setAttribute("class",_className);
  }
}

function photography()
{
  applyClass("photography");
}

function bicycle()
{
  applyClass("bicycle");
}

