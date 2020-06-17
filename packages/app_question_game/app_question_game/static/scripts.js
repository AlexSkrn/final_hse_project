function copy() {
  var copyText = document.getElementById("question");
  copyText.select();
  document.execCommand("copy");
  alert("Copied to clipboard: " + copyText.value);
}


function copyPaste(elementId) {
  var text = document.getElementById(elementId).innerHTML;
  let textarea = document.getElementById("target");
  textarea.innerHTML = text;
  textarea.focus();
}
