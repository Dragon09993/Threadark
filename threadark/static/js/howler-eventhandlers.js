document.addEventListener('DOMContentLoaded', function() {
    var currentSound = null;
    var currentButton = null;

    document.querySelectorAll('.play-audio').forEach(function(button) {
        button.addEventListener('click', function() {
            var audioUrl = this.getAttribute('data-audio-url');
            var cardId = this.getAttribute('data-card-id');
            var cardElement = document.getElementById(cardId);
            var buttonId = this.id;
            var playButton = document.getElementById(buttonId);

            if (currentSound && currentSound.playing()) {
                if (currentButton === playButton) {
                    currentSound.stop();
                    playButton.textContent = 'Play Audio';
                    playButton.classList.remove('stop-audio');
                    return;
                } else {
                    currentSound.stop();
                    currentButton.textContent = 'Play Audio';
                    currentButton.classList.remove('stop-audio');
                }
            }

            currentSound = new Howl({
                src: [audioUrl],
                format: ['mp3'],
                onplay: function() {
                    cardElement.classList.add('audio-highlight');
                    playButton.textContent = 'Stop Audio';
                    playButton.classList.add('stop-audio');
                },
                onend: function() {
                    cardElement.classList.remove('audio-highlight');
                    playButton.textContent = 'Play Audio';
                    playButton.classList.remove('stop-audio');
                    currentSound = null;
                    currentButton = null;
                },
                onstop: function() {
                    cardElement.classList.remove('audio-highlight');
                    playButton.textContent = 'Play Audio';
                    playButton.classList.remove('stop-audio');
                    currentSound = null;
                    currentButton = null;
                }
            });

            currentSound.play();
            currentButton = playButton;
        });
    });
});