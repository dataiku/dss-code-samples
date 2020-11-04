/* Javascript code for your Webapp */
$.getJSON(getWebAppBackendUrl("get-sensitive-data"), function(data) {
    alert("Received data: " + JSON.stringify(data))
})