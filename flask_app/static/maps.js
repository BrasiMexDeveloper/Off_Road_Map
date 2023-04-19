
// let map;

// function initMap() {
//     map = new google.maps.Map(document.getElementById("map"), {
//         center: { lat: -34.397, lng: 150.644 },
//         zoom: 8,
//     });
// }

// window.initMap = initMap;

// fetch()
//     .then(response => response.json() )
//     .then(coderData => console.log(coderData) )
//     .catch(err => console.log(err) )

// ? set up map options

var myLatlng = {lat: 47.131, lng: -119.271};
var mapOptions = {
    zoom: 8,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

// ? create map

var map = new google.maps.Map(document.getElementById("maps"), mapOptions);

// ? create a DirectionsService object to use the route method and get a result for our request
var directionsService = new google.maps.DirectionsService();

// ? create a DirectionsRenderer object which we will use to display the route
var directionsDisplay = new google.maps.DirectionsRenderer();

//  ? bind the DirectionsRenderer to the map
directionsDisplay.setMap(map);

// ? define calcRoute function
function getDirections(origin, destination) {
    // ? create request
    var request = {
        origin: origin,
        destination: destination,

        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.IMPERIAL
    }

    // ? pass the request to the route method
    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            // ? Get distance and time
            var output = "<div class='alert-info'>From: " + origin + ".<br />To: " + destination + ".<br /> Driving distance <i class='fas fa-road'></i>: " + result.routes[0].legs[0].distance.text + ".<br />Duration <i class='fas fa-hourglass-start'></i>: " + result.routes[0].legs[0].duration.text + ".</div>";
            // ? output div
            $("#output").html(output);
            // ? display route
            directionsDisplay.setDirections(result);
        } else {
            // ? delete route from map
            directionsDisplay.setDirections({routes: []});
            // ? clear output div
            $("#output").html("");
            // ? show error message
            $("#output").html("<div class='alert-danger'><i class='fas fa-exclamation-triangle'></i> Could not retrieve driving distance.</div>");
        }
    });
}

// ? create autocomplete objects for all inputs
var options = {
    types: ['(places)'],
    componentRestrictions: {country: "us"}
}

var input1 = document.getElementById('origin');
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById('destination');
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);

// ? get route from origin to destination
$("#submit").click(function() {
    getDirections($("#origin").val(), $("#destination").val());
});

// ? delete route from map
$("#delete").click(function() {
    directionsDisplay.setDirections({routes: []});
    $("#output").html("");
    $("#origin").val("");
    $("#destination").val("");
});

// ? center map in Moses Lake
$("#center").click(function() {
    map.setCenter(myLatlng);
});

// ? show all markers
$("#show").click(function() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
});

// ? hide all markers
$("#hide").click(function() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
});

// // ? create markers
// var markers = [
//     {
//         coords: {lat: 47.131, lng: -119.271},
//         content: '<h1>Moses Lake</h1>'
//     },
//     {

//         coords: {lat: 47.606, lng: -122.332},
//         content: '<h1>Seattle</h1>'
//     },
//     {
//         coords: {lat: 47.751, lng: -120.740},
//         content: '<h1>Wenatchee</h1>'
//     }
// ];