var map = L.map("map").setView([18.5285, 73.8744], 13);

mapLink = "<a href='http://openstreetmap.org'>OpenStreetMap</a>";
L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: 'Leaflet &copy; ' + mapLink + ', contribution',
    maxZoom: 18
}).addTo(map);

var fromMarker, toMarker, routeControl;
var fromLat, fromLon; // Move the variable declaration here

function getRoute() {
    var fromLocation = document.getElementById("from").value;
    var toLocation = document.getElementById("to").value;

    if (!fromLocation || !toLocation) {
        alert("Please Provide location");
        return;
    }

    if (fromMarker) {
        map.removeLayer(fromMarker);
    }

    if (toMarker) {
        map.removeLayer(toMarker);
    }

    if (routeControl) {
        map.removeControl(routeControl);
    }

    axios.get("https://nominatim.openstreetmap.org/search", {
        params: {
            format: 'json',
            q: fromLocation
        }
    }).then(function (response) {
        fromLat = response.data[0].lat;
        fromLon = response.data[0].lon;
        fromMarker = L.marker([fromLat, fromLon]).addTo(map);
        map.setView([fromLat, fromLon], 13);

        return axios.get("https://nominatim.openstreetmap.org/search", {
            params: {
                format: 'json',
                q: toLocation
            }
        });
    }).then(function (response) {
        var toLat = response.data[0].lat;
        var toLon = response.data[0].lon;
        toMarker = L.marker([toLat, toLon]).addTo(map);

        var routeCoordinates = {
            fromLat: fromLat,
            fromLon: fromLon,
            toLat: toLat,
            toLon: toLon,
            waypoints: []
        };

        routeControl = L.Routing.control({
            waypoints: [
                L.latLng(fromLat, fromLon),
                L.latLng(toLat, toLon),
            ],
            router: L.Routing.osrmv1({
                serviceUrl: "https://router.project-osrm.org/route/v1"
            })
        }).on('routeselected', function (e) {
            var waypoints = e.route.coordinates.map(function (coord) {
                return { lat: coord[0], lon: coord[1] };
            });
            routeCoordinates.waypoints = waypoints;
        }).addTo(map);

        return axios.post("coordinates/", routeCoordinates).then(function (response) {
            console.log(response.data);
             if (response.data.status === 'success') {
                addMarkers(response.data.detected_list);
            } else {
                console.error('Error:', response.data.message);
            }
        }).catch(function (error) {
            console.log("Check error", error);
            alert(error);
        });
    });
}



function reverseInputs() {
    // Get the values from the starting and destination input boxes
    var startInput = document.getElementById("from");
    var destinationInput = document.getElementById("to");

    // Swap the values
    var temp = startInput.value;
    startInput.value = destinationInput.value;
    destinationInput.value = temp;
}

// Code for the AutoComplete Location Feature
// Example locations for Pune
var puneLocations = ['Aundh, Pune', 'Koregaon Park, Pune', 'Magarpatta, Pune', 'Shivaji Nagar, Pune', 'Shaniwar Wada, Pune',
    'Aga Khan Palace, Pune',
    'Sinhagad Fort, Pune',
    'Osho Ashram, Pune',
    'Dagadusheth Halwai Ganpati Temple, Pune',
    'Raja Dinkar Kelkar Museum, Pune',
    'Lal Mahal, Pune',
    'Khadakwasla Dam, Pune',
    'Pataleshwar Cave Temple, Pune',
    'Parvati Hill, Pune',
    'Bund Garden, Pune',
    'Vetal Tekdi, Pune',
    'Pu La Deshpande Garden, Pune',
    'Mulshi Lake and Dam, Pune',
    'Phoenix Marketcity, Pune',
    'FC Road (Fergusson College Road), Pune',
    'Koregaon Park, Pune',
    'Saras Baug, Pune',
    'Darshan Museum, Pune',
    'Rajiv Gandhi Zoological Park, Pune'];

// Populate datalist with suggestions
puneLocations.forEach(function (location) {
    var option = document.createElement('option');
    option.value = location;
    document.getElementById('location-suggestions').appendChild(option.cloneNode(true));
});

// Initialize Awesomplete for input fields
var startInput = new Awesomplete(document.getElementById('from'), { list: "#location-suggestions" });
var destinationInput = new Awesomplete(document.getElementById('to'), { list: "#location-suggestions" });


// Function to add markers to the map
function addMarkers(detectedList) {
    // Add pothole markers
    detectedList.potholes.forEach(function(pothole) {
        L.marker([pothole.lat, pothole.lon]).addTo(map)
            .bindPopup('Pothole detected here.');
    });

    // Add traffic markers
    detectedList.traffic.forEach(function(traffic) {
        L.marker([traffic.lat, traffic.lon]).addTo(map)
            .bindPopup('Traffic detected here.');
    });

    // Add accident markers
    detectedList.accidents.forEach(function(accident) {
        L.marker([accident.lat, accident.lon]).addTo(map)
            .bindPopup('Accident detected here.');
    });
}

// Logout
function logout() {
  // You can implement logout logic here
  // For example, redirect to a logout route or perform an API call

  // For demonstration purposes, let's just alert a message
  alert('Logout clicked! Implement your logout logic here.');
}