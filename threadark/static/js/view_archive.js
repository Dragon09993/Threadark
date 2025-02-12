document.addEventListener('DOMContentLoaded', function() {
    const tableHeaders = document.querySelectorAll('th a');
    const paginationLinks = document.querySelectorAll('.pagination a');

    tableHeaders.forEach(header => {
        header.addEventListener('click', function(event) {
            event.preventDefault();

            const url = new URL(header.href);
            const params = new URLSearchParams(url.search);
            const currentSort = params.get('sort');
            const currentOrder = params.get('sort_order') || 'asc';

            // Toggle sort order
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            params.set('sort_order', newOrder);

            // Update the hx-get attribute
            header.setAttribute('hx-get', `${url.pathname}?${params.toString()}`);
            header.setAttribute('href', `${url.pathname}?${params.toString()}`);

            // Trigger the HTMX request
            htmx.trigger(header, 'click');
        });
    });

    paginationLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const url = new URL(link.href);
            const params = new URLSearchParams(url.search);

            // Update the hx-get attribute
            link.setAttribute('hx-get', `${url.pathname}?${params.toString()}`);
            link.setAttribute('href', `${url.pathname}?${params.toString()}`);

            // Trigger the HTMX request
            htmx.trigger(link, 'click');
        });
    });
});