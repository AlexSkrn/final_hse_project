var button = document.getElementById('speak');

var speechMsgInput = document.getElementById('question');

function speak(text) {
	var msg = new SpeechSynthesisUtterance();
	msg.text = text;
	window.speechSynthesis.speak(msg);
}

button.addEventListener('click', function(e) {
	if (speechMsgInput.value.length > 0) {
		speak(speechMsgInput.value);
	}
});
