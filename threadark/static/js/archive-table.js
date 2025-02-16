document.addEventListener('DOMContentLoaded', function() {
    // Function to get the CSRF token from the cookies


    const csrftoken = getCookie('csrftoken');

    var table = new Tabulator("#thread-table", {
        ajaxURL: request_url,
        ajaxConfig: "GET",
        ajaxContentType: "application/json; charset=utf-8",
        pagination: true,
        paginationMode: "remote",
        ajaxResponse: function (url, params, response) {
            return response; // Ensure only the array is returned
        },
        ajaxRequestFunc: function (url, config, params) {
            config.headers = {
                'X-CSRFToken': csrftoken,
            };
            return fetch(url, config).then(response => response.json());
        },
        layout: "fitColumns",
        columns: [
            { title: "ID", field: "id", sorter: "number" },
            { title: "Thread ID", field: "thread_id", sorter: "number", formatter: function(cell, formatterParams, onRendered) {
                var thread_id = cell.getValue();
                var board = cell.getData().board;
                var url = "/archive/" + board + "/thread/" + thread_id;
                return "<a href='" + url + "' >" + thread_id + "</a>";
            }},
            { title: "Board", field: "board", sorter: "string" },
            { title: "Title", field: "title", sorter: "string", minWidth: 400, formatter: function(cell, formatterParams, onRendered) {
                var thread_id = cell.getData().thread_id;
                var board = cell.getData().board;
                var url = "/archive/" + board + "/thread/" + thread_id;
                return "<a href='" + url + "' >" + cell.getValue() + "</a>";
            }},
            { title: "Status", field: "status", sorter: "string" },
            { title: "URL", field: "url", formatter: "link", formatterParams: { target: "_blank" } },
            { title: "Replies", field: "replies", sorter: "number" },
            { title: "Created At", field: "created_at", sorter: "datetime" },
            { title: "Last Updated", field: "last_updated", sorter: "datetime" }
        ],
    });

    document.getElementById('search-input').addEventListener('input', function() {
        table.setFilter("title", "like", this.value);
    });
});