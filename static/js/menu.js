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

L_NO_TOUCH = false;
L_DISABLE_3D = false;


// toggle


function toggleMenu() {
  // Toggle the opacity property of the success image
  var successImage = document.getElementById("success-image");
  successImage.style.opacity = "0";

  // Toggle the display property of the menu container
  var menuContainer = document.getElementById("menu-container");
  menuContainer.style.display =
      menuContainer.style.display === "none" ||
          menuContainer.style.display === ""
          ? "block"
          : "none";
}

let background_box = document.querySelectorAll(".background_box");
let toggleBoxes = document.querySelectorAll(".toggle_box");
let trafficToggleBox = document.getElementById("trafficCheckbox");
let potholeToggleBox = document.getElementById("potholeCheckbox");

let circles = document.querySelectorAll(".circle");

// Add click event listeners to each toggle box
toggleBoxes.forEach(function (toggleBox, index) {
  toggleBox.onclick = function () {
      // Toggle the checkbox
      let checkbox = toggleBox.querySelector("input[type='checkbox']");
      checkbox.checked = !checkbox.checked;

      // Move the circle based on the checkbox state
      let circle = circles[index];
      if (checkbox.checked) {
          circle.style.transform = "translateX(34px)";
          circle.style.backgroundColor = "#000"; // Set "on" color
      } else {
          circle.style.transform = "translateX(0px)";
          circle.style.backgroundColor = "#fff"; // Set "off" color
      }
  };
});

function logout() {
  // You can implement logout logic here
  // For example, redirect to a logout route or perform an API call

  // For demonstration purposes, let's just alert a message
  alert('Logout clicked! Implement your logout logic here.');
}