// element
var map_aa291a4f1eafe5bbd01101418f32837c = L.map(
    "map_aa291a4f1eafe5bbd01101418f32837c",
    {
        center: [18.5204, 73.8567],
        crs: L.CRS.EPSG3857,
        zoom: 12,
        zoomControl: true,
        preferCanvas: false,
    }
);

var tile_layer_b029293d23a731656497915ac91c575e = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            'Data by \u0026copy; \u003ca target="_blank" href="http://openstreetmap.org"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca target="_blank" href="http://www.openstreetmap.org/copyright"\u003eODbL\u003c/a\u003e.',
        detectRetina: false,
        maxNativeZoom: 18,
        maxZoom: 18,
        minZoom: 0,
        noWrap: false,
        opacity: 1,
        subdomains: "abc",
        tms: false,
    }
).addTo(map_aa291a4f1eafe5bbd01101418f32837c);

function findRoute() {
    var start = document.getElementById("start").value;
    var destination = document.getElementById("destination").value;

    document.getElementById("directions-box").style.display = "none";

    // Show the success image
    document.getElementById("success-image").style.display = "block";
}





//   map 

L_NO_TOUCH = false;
L_DISABLE_3D = false;