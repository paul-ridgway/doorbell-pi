$(document).ready(function() {
    loadConfig();
})

function loadConfig() {
    console.log('loadConfig()');
    $.ajax('/api/config', function(data) {
       console.log("Got data:");
       console.log(data);
    });
}