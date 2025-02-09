document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.card .picel').forEach(function(element) {
        element.addEventListener('click', function() {
            this.classList.toggle('is-128x128');
            this.parentElement.parentElement.classList.toggle('is-block');
        
            
        });
    });
});