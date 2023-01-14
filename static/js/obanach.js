API_ENDPOINT = 'http://127.0.0.1:5000';

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-bottom-left",
    "preventDuplicates": true,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

function updateWidgets(){
    $.get( API_ENDPOINT + "/status", function( data ) {
        let json = JSON.parse(data);

        if ( json['success'] !== true){
            toastr["error"](json['message'], "ERROR")
            return false;
        }

        let response = json['data']

        response['light'] === true ? $('#light-widget').html('<i class="fa-regular fa-lightbulb fa-8x" style="color:green;"></i>') : $('#light-widget').html('<i class="fa-regular fa-lightbulb fa-8x" style="color:#970000;"></i>')


        if ( response['windowLeft'] === 'open' ){
            $('#window-left-widget').html('<i class="fa-solid fa-up-long fa-8x"></i>')
        } else if ( response['windowLeft'] === 'close' ) {
            $('#window-left-widget').html('<i class="fa-solid fa-down-long fa-8x"></i>')
        } else {
            $('#window-left-widget').html('<h1 class="widget-text">' + response['windowLeft'] + ' %</h1>')
        }

        if ( response['windowRight'] === 'open' ){
            $('#window-right-widget').html('<i class="fa-solid fa-up-long fa-8x"></i>')
        } else if ( response['windowRight'] === 'close' ) {
            $('#window-right-widget').html('<i class="fa-solid fa-down-long fa-8x"></i>')
        } else {
            $('#window-right-widget').html('<h1 class="widget-text">' + response['windowRight'] + ' %</h1>')
        }

        return true;

    }).fail(function() {
        toastr["error"]("Can not connect to API server", "ERROR")
        return false;
    });
}

function sendWindowData(side, data){
    //TODO: validate params

    $.get( API_ENDPOINT + "/window/set/" + side + "/" + data, function( data ) {
        let json = JSON.parse(data);
        json['success'] === true ? toastr["success"](json['message'], "Success!") : toastr["error"](json['message'], "ERROR")
        return true;
    }).fail(function() {
        toastr["error"]("Can not send window command", "ERROR")
        return false;
    });

}

function sendLightData(data){
    //TODO: validate params

    $.get( API_ENDPOINT + "/light/set/" + data, function( data ) {
        let json = JSON.parse(data);
        json['success'] === true ? toastr["success"](json['message'], "Success!") : toastr["error"](json['message'], "ERROR")
        return true;
    }).fail(function() {
        toastr["error"]("Can not send window command", "ERROR")
        return false;
    });

}


$( "#light-on" ).click(function() {
    sendLightData(1)
});
$( "#light-off" ).click(function() {
    sendLightData(0)
});


$( "#window-left-btn-up" ).click(function() {
    sendWindowData('left', 1)
});
$( "#window-left-btn-stop" ).click(function() {
    sendWindowData('left', 0)
});
$( "#window-left-btn-down" ).click(function() {
    sendWindowData('left', 2)
});


$( "#window-right-btn-up" ).click(function() {
    sendWindowData('right', 1)
});
$( "#window-right-btn-stop" ).click(function() {
    sendWindowData('right', 0)
});
$( "#window-right-btn-down" ).click(function() {
    sendWindowData('right', 2)
});

setInterval(updateWidgets, 1000);