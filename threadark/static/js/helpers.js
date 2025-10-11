function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addCSRFTokenToHTMXHeaders() {
    try {
        const csrftoken = getCookie('csrftoken');
        
        if (!csrftoken) {
            console.warn('CSRF token not found');
            return;
        }
        
        // Wait for htmx to be available
        if (typeof htmx !== 'undefined') {
            // Method 1: Using htmx event system (preferred)
            document.body.addEventListener('htmx:configRequest', function(evt) {
                evt.detail.headers['X-CSRFToken'] = csrftoken;
            });
            
            // Method 2: Fallback using htmx.config
            if (htmx.config) {
                if (!htmx.config.requestClass) {
                    htmx.config.requestClass = 'htmx-request';
                }
            }
        } else {
            // htmx not loaded yet, try again after a short delay
            setTimeout(function() {
                if (typeof htmx !== 'undefined') {
                    document.body.addEventListener('htmx:configRequest', function(evt) {
                        evt.detail.headers['X-CSRFToken'] = csrftoken;
                    });
                } else {
                    console.warn('HTMX still not available after delay');
                }
            }, 100);
        }
    } catch (error) {
        console.error('Error setting up CSRF token for HTMX:', error);
    }
}