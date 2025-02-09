document.addEventListener('DOMContentLoaded', () => {
    const quoteLinks = document.querySelectorAll('.quotelink');

    quoteLinks.forEach(link => {
        link.addEventListener('mouseover', (event) => {
            const messageId = event.target.getAttribute('href').substring(2);
            const message = document.querySelector(`.message[data-message-no="${messageId}"]`);
            if (message) {
                message.classList.add('highlight');
            }
        });

        link.addEventListener('mouseout', (event) => {
            const messageId = event.target.getAttribute('href').substring(2);
            const message = document.querySelector(`.message[data-message-no="${messageId}"]`);
            if (message) {
                message.classList.remove('highlight');
            }
        });
    });
});

// Add this CSS to your stylesheet to define the highlight class
// .highlight {
//   background-color: yellow;
// }