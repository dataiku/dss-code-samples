/* Javascript code for your Webapp */
$('#btn').on('click', function () {
    $.getJSON(getWebAppBackendUrl("get-sensitive-data"), function(data) {
        alert("Received data: " + JSON.stringify(data))});
});