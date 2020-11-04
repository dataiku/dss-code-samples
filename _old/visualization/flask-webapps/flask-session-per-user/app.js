let localModel = {};
let viewIdentifier = Math.random().toString(16).substring(2)
console.log("Use view identifier : " + viewIdentifier)
let init = function() {
    let refresh = function() {
        // show the browser-side model and the python-side model alongside as colored boxes in the plot area
        $.ajax({
                method:'GET',
                headers: {'Flask-View-Id':viewIdentifier},
                url:getWebAppBackendUrl('/get-plot')
            }).done(function(data) {
                $("#plot").empty();
                // the box for the python-side model
                $("#plot").append($.parseHTML(data))
                // the box for the browser side model
                var localHTML = '<div style="background: red; opacity: 0.5; position: absolute; left: '+localModel.X+'%; top: '+localModel.Y+'%; width: 10px; height: 10px"></div>';
                $("#plot").append($.parseHTML(localHTML))
            }).fail(function(data) {
                console.log("error", data);
            });
    };
    
    let change = function(what, value) {
        // store change in the local (browser-wise) model
        localModel[what] = value;
        // store chante in the remote model in the python backend
        data = {}
        data[what] = value
        $.ajax({
                method:'POST',
                headers: {'Flask-View-Id':viewIdentifier},
                url:getWebAppBackendUrl('/set'),
                data:data
            }).done(function(data) {
                // show the impact
                refresh();
            }).fail(function(data) {
                console.log("error", data);
            });
    };
    
    $("#slider1").slider({slide: function(event, ui) {change("X", ui.value);}});
    $("#slider2").slider({slide: function(event, ui) {change("Y", ui.value);}});
    $("#refresh").button();
    $("button").click(function(e) {refresh();});
    
    refresh();
};

init();