window.onload = getLivePhoto();
window.onload = initialize();

function getLivePhoto() {
    $.ajax({
        type: 'GET',
        url: 'http://38.88.75.83/db/livestream.php',
        data: {
            format: 'json'
        },
        success: function (data) {
            console.log("sucessfully got photo");
            console.log(data);
            updateView(data);
        },
        error: function (data) {
            console.log("error getting data");
        },
    });
    //window.setInterval(getLivePhoto, 2000);
}

function updateView(data) {
    var obj = JSON.parse(data);
    var img = document.getElementById("liveImg");
    console.log(obj.photo);
    img.src = obj.photo;
}


//setting up joystick
$(document).ready(function () {
    var joystickView = new JoystickView(150, function (callbackView) {
        $("#joystickContent").append(callbackView.render().el);
        setTimeout(function () {
            callbackView.renderSprite();
        }, 0);
    });

    //		$.ajax({
    //		type: "POST",
    //		url: 'http://38.88.75.83/db/joystick.php?id=7',
    //		data: {y_coordinate: y, x_coordinate: x},
    //		success: function(data){
    //			alert(data);
    //		}
    //	});
    joystickView.bind("verticalMove", function (y) {
        $("#yVal").html(y);
        //			 $.ajax({
        //			     type: "POST",
        //				 url: 'http://38.88.75.83/db/joystick.php?id=7',
        //		    	 data: {x_coordinate: x, y_coordinate: y},
        //			 });
    });
    joystickView.bind("horizontalMove", function (x) {
        $("#xVal").html(x);
        //			 $.ajax({
        //				 type: "POST",
        //	     		 url: 'http://38.88.75.83/db/joystick.php?id=7',
        //				 data: {x_coordinate: x, y_coordinate: y},
        //				 success: function(data){
        //					 alert(data);
        //				}	
        //			});
    });
});


$('#xVal').bind("DOMSubtreeModified", function () {
    window.setInterval(function () {
        var x = $("#xVal").text();
        var y = $("#yVal").text();

        $.ajax({
            type: "POST",
            url: 'http://38.88.75.83/db/joystick.php?id=7',
            data: { x_coordinate: x, y_coordinate: y },
            //  success: function(data){
            //	  alert(data);
            //  }
        });
    }, 1000);
});

function updateMode(){
    if (document.getElementById('toggle').checked) {
        document.getElementById('mode').textContent = "Manual";
        document.getElementById('joystick').style.display = "inline";
        $.ajax({
            type: "POST",
            url: 'http://38.88.75.83/db/setmode.php?id=7',
            data: { 'manual': 1},
            success: function (data) {
                console.log("success");
            },
            error: function (data) {
                console.log("error getting data");
            },
        });
    } else {
        document.getElementById('mode').textContent = "Automatic";
        document.getElementById('joystick').style.display = "none";
        $.ajax({
            type: "POST",
            url: 'http://38.88.75.83/db/setmode.php?id=7',
            data: { 'manual': 0},
            success: function (data) {
                console.log("success");
            },
            error: function (data) {
                console.log("error getting data");
            },
        });
    } 
}

function initialize() {

    $.ajax({
        type: "GET",
        url: 'http://38.88.75.83/db/manual.php?id=7',
        data: {
            format: 'json'
        },
        success: function (data) {
            var obj = JSON.parse(data);
            if (obj.manual == 1){
                document.getElementById('liveView').style.display = "inline";
                $('#toggle').prop('checked', true);
                document.getElementById('mode').textContent = "Manual";
                document.getElementById('joystick').style.display = "inline";
            } else if (obj.manual == 0) {
                $('#toggle').prop('checked', false);
                document.getElementById('liveView').style.display = "inline";
                document.getElementById('mode').textContent = "Automatic";
                document.getElementById('joystick').style.display = "none";
            } else {
                document.getElementById('status').style.backgroundColor = "red";
            }
        },
        error: function (data) {
            console.log("error getting manual data");
        },
    });
}