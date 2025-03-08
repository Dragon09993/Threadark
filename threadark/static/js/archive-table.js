document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    const csrftoken = getCookie('csrftoken');
    const searchTerm = getQueryParam("search") || ""; // Default to empty string if no search param

    // Set initial params for AJAX request
    let ajaxParams = { search: searchTerm };

    // Initialize Tabulator with search query included
    var table = new Tabulator("#thread-table", {
        ajaxURL: request_url,
        ajaxConfig: "GET",
        ajaxParams: ajaxParams,  // Include initial search param
        ajaxContentType: "application/json; charset=utf-8",
        pagination: "remote",
        paginationMode: "remote",
        filterMode: "remote",
        ajaxRequestFunc: function (url, config, params) {
            config.headers = { 'X-CSRFToken': csrftoken };
            let searchQuery = params.search ? `?search=${encodeURIComponent(params.search)}` : "";
            let fullUrl = url + searchQuery;

            console.log("Fetching:", fullUrl);
            console.log("Request Headers:", config.headers);

            return fetch(fullUrl, config)
                .then(response => response.json())
                .catch(error => console.error("Fetch Error:", error));
        },
        ajaxResponse: function (url, params, response) {
            console.log("API Response:", response);
            return response; // Return the correct array response
        },
        layout: "fitColumns",
        columns: [
            { title: "ID", field: "id", sorter: "number" },
            { title: "Thread ID", field: "thread_id", sorter: "number", formatter: function(cell) {
                var thread_id = cell.getValue();
                var board = cell.getData().board;
                return `<a href='/archive/${board}/thread/${thread_id}'>${thread_id}</a>`;
            }},
            { title: "Board", field: "board", sorter: "string" },
            { title: "Title", field: "title", sorter: "string", minWidth: 400, formatter: function(cell) {
                var thread_id = cell.getData().thread_id;
                var board = cell.getData().board;
                return `<a href='/archive/${board}/thread/${thread_id}'>${cell.getValue()}</a>`;
            }},
            { title: "Status", field: "status", sorter: "string" },
            { title: "URL", field: "url", formatter: "link", formatterParams: { target: "_blank" } },
            { title: "Replies", field: "replies", sorter: "number" },
            { title: "Created At", field: "created_at", sorter: "datetime" },
            { title: "Last Updated", field: "last_updated", sorter: "datetime" }
        ],
    });

    // Check if there's a search parameter and set the input value
    if (searchTerm) {
        document.getElementById('search-input').value = searchTerm;
    }

    // Live search filtering
    document.getElementById('search-input').addEventListener('input', function() {
        var searchValue = this.value.trim();
        console.log("Search Value:", searchValue);

        // Update params dynamically and refresh data
        table.setData(request_url + "?search=" + encodeURIComponent(searchValue));
    });
});
