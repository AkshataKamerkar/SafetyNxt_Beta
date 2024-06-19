// Initialize the map
var map = L.map("map").setView([18.5285, 73.8744], 13);

// Add tile layer to the map
var mapLink = "<a href='http://openstreetmap.org'>OpenStreetMap</a>";
L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: 'Leaflet &copy; ' + mapLink + ', contribution',
    maxZoom: 18
}).addTo(map);

var fromMarker, toMarker, routeControl;
var fromLat, fromLon;
var trafficMarkers = [];
var accidentMarkers = [];
var potholeMarkers = [];

// Custom icons for different types of incidents and density levels
var trafficLightIcon = L.icon({
    iconUrl: 'static/img/traffic_green.png',
    iconSize: [35, 55],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var trafficModerateIcon = L.icon({
    iconUrl: 'static/img/traffic_yellow.png',
    iconSize: [35, 55],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var trafficHeavyIcon = L.icon({
    iconUrl: 'static/img/map/traffic_red.png',
    iconSize: [35, 55],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var potholeLightIcon = L.icon({
    iconUrl: 'static/img/map/pothole_green.png',
    iconSize: [30, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var potholeModerateIcon = L.icon({
    iconUrl: 'static/img/map/pothole_yellow.png',
    iconSize: [30, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var potholeHeavyIcon = L.icon({
    iconUrl: 'static/img/map/pothole_red.png',
    iconSize: [30, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var accidentIcon = L.icon({
    iconUrl: 'static/img/map/accident_marker.png',
    iconSize: [40, 60],
    iconAnchor: [12, 41]
});

// Creating a Density Label
function getDensityLabel(num) {
    if (num < 0.3) {
        return 'LIGHT';
    } else if (num >= 0.3 && num < 0.6) {
        return 'MODERATE';
    } else {
        return 'HEAVY';
    }
}

function getRoute() {
    var fromLocation = document.getElementById("from").value;
    var toLocation = document.getElementById("to").value;

    if (!fromLocation || !toLocation) {
        alert("Please provide locations");
        return;
    }

    // Remove existing markers and route
    if (fromMarker) map.removeLayer(fromMarker);
    if (toMarker) map.removeLayer(toMarker);
    if (routeControl) map.removeControl(routeControl);

    // Get coordinates for the 'from' location
    axios.get("https://nominatim.openstreetmap.org/search", {
        params: { format: 'json', q: fromLocation }
    }).then(function (response) {
        fromLat = response.data[0].lat;
        fromLon = response.data[0].lon;
        fromMarker = L.marker([fromLat, fromLon]).addTo(map); // Use custom icon
        map.setView([fromLat, fromLon], 13);

        // Get coordinates for the 'to' location
        return axios.get("https://nominatim.openstreetmap.org/search", {
            params: { format: 'json', q: toLocation }
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

        // Add route control to the map
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
                return { lat: coord.lat, lon: coord.lng };
            });
            routeCoordinates.waypoints = waypoints;
        }).addTo(map);

        // Send route coordinates to the server
        return axios.post("coordinates/", routeCoordinates);
    }).then(function (response) {
        if (response.data.status === 'success') {
            updateMarkers(response.data.detected_list);
        } else {
            console.error('Error:', response.data.message);
        }
    }).catch(function (error) {
        console.error("Error:", error);
        alert(error);
    });
}

// Function to reverse the inputs
function reverseInputs() {
    var startInput = document.getElementById("from");
    var destinationInput = document.getElementById("to");
    var temp = startInput.value;
    startInput.value = destinationInput.value;
    destinationInput.value = temp;
}

// Example locations for Pune
var puneLocations = ['Aundh, Pune', 'Koregaon Park, Pune', 'Magarpatta, Pune', 'Shivaji Nagar, Pune', 'Shaniwar Wada, Pune',
    'Aga Khan Palace, Pune', 'Sinhagad Fort, Pune', 'Osho Ashram, Pune', 'Dagadusheth Halwai Ganpati Temple, Pune',
    'Raja Dinkar Kelkar Museum, Pune', 'Lal Mahal, Pune', 'Khadakwasla Dam, Pune', 'Pataleshwar Cave Temple, Pune',
    'Parvati Hill, Pune', 'Bund Garden, Pune', 'Vetal Tekdi, Pune', 'Pu La Deshpande Garden, Pune', 'Mulshi Lake and Dam, Pune',
    'Phoenix Marketcity, Pune', 'FC Road (Fergusson College Road), Pune', 'Koregaon Park, Pune', 'Saras Baug, Pune',
    'Darshan Museum, Pune', 'Rajiv Gandhi Zoological Park, Pune'];

// Populate datalist with suggestions
puneLocations.forEach(function (location) {
    var option = document.createElement('option');
    option.value = location;
    document.getElementById('location-suggestions').appendChild(option.cloneNode(true));
});

// Initialize Awesomplete for input fields
var startInput = new Awesomplete(document.getElementById('from'), { list: "#location-suggestions" });
var destinationInput = new Awesomplete(document.getElementById('to'), { list: "#location-suggestions" });

// Function to update markers on the map
function updateMarkers(detectedList) {
    // Clear existing markers from the arrays
    trafficMarkers.forEach(marker => map.removeLayer(marker));
    accidentMarkers.forEach(marker => map.removeLayer(marker));
    potholeMarkers.forEach(marker => map.removeLayer(marker));

    trafficMarkers = [];
    accidentMarkers = [];
    potholeMarkers = [];

    // Add new pothole markers
    detectedList.potholes.forEach(function(pothole) {
        var icon;
        var densityLabel = getDensityLabel(pothole.num);
        if (densityLabel === 'LIGHT') {
            icon = potholeLightIcon;
        } else if (densityLabel === 'MODERATE') {
            icon = potholeModerateIcon;
        } else {
            icon = potholeHeavyIcon;
        }
        var marker = L.marker([pothole.lat, pothole.lon], {icon: icon}).bindPopup(`Pothole detected: ${densityLabel}`);
        potholeMarkers.push(marker);
    });

    // Add new traffic markers
    detectedList.traffic.forEach(function(traffic) {
        var icon;
        var densityLabel = getDensityLabel(traffic.num);
        if (densityLabel === 'LIGHT') {
            icon = trafficLightIcon;
        } else if (densityLabel === 'MODERATE') {
            icon = trafficModerateIcon;
        } else {
            icon = trafficHeavyIcon;
        }
        var marker = L.marker([traffic.lat, traffic.lon], {icon: icon}).bindPopup(`Traffic detected: ${densityLabel}`);
        trafficMarkers.push(marker);
    });

    // Add new accident markers
    detectedList.accidents.forEach(function(accident) {
        var marker = L.marker([accident.lat, accident.lon], {icon: accidentIcon}).bindPopup('Accident detected here.');
        accidentMarkers.push(marker);
    });
}
