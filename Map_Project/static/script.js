var map;
var markers = [];

function initMap() {
  var center = {lat: 34.096676, lng: -117.719779};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: center
  });
}

// function updateMap() {
//   $.get('/markers', function(data) {
//     clearMarkers();
//     for (var i = 0; i < data.markers.length; i++) {
//       var marker = data.markers[i];
//       addMarker(marker.latitude, marker.longitude, marker.family_income);
//     }
//     updateMiles();
//   });
// }

function updateMap() {
    $.get("data.txt", function(data) {
        var markers = [];
        var lines = data.split('\n');
        for (var i = 0; i < lines.length; i++) {
            if (lines[i]) {
                var parts = lines[i].split(',');
                var lat = parseFloat(parts[0]);
                var lng = parseFloat(parts[1]);
                var address = parts[2];
                var distance = parseFloat(parts[3]);
                var income = parseInt(parts[4]);
                var marker = new google.maps.Marker({
                    position: {lat: lat, lng: lng},
                    map: map,
                    title: address
                });
                markers.push(marker);
            }
        }
        var markerCluster = new MarkerClusterer(map, markers, {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
    });
}

function addMarker(latitude, longitude, family_income) {
  var marker = new google.maps.Marker({
    position: {lat: latitude, lng: longitude},
    map: map
  });
  markers.push(marker);

  var infoWindow = new google.maps.InfoWindow({
    content: 'Family income: ' + family_income
  });
  marker.addListener('click', function() {
    infoWindow.open(map, marker);
  });
}

function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}

function updateMiles() {
  $.get('/miles', function(data) {
    var totalMiles = data.total_miles;
    var averageMiles = data.average_miles;
    $('#totalMiles').text(totalMiles.toFixed(2));
    $('#averageMiles').text(averageMiles.toFixed(2));
  });
}

// This function is called when the form is submitted
function submitCounty(event) {
  // event.preventDefault(); // prevent the form from submitting

  // Get the values from the form
  const addressInput = document.getElementById("address");
  const address = addressInput.value;

  const cityInput = document.getElementById("city");
  const city = cityInput.value;

  const stateInput = document.getElementById("state");
  const state = stateInput.value;

  const countyInput = document.getElementById("county");
  const county = countyInput.value;

  // Make a POST request to the Flask API to save the data
  $.post("/submit", { address : address, city: city, state: state, county: county }, function (data) {
    console.log(data);
  });

  // // Update the map with the new location
  // updateMap(lat, long);
}
  
  
  // This function calculates the total and average distance travelled to get to the locations
  function calculateDistance() {
    // Use the Google Maps Distance Matrix API to calculate the distance between each pair of locations
    const service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix(
      {
        origins: markers,
        destinations: markers,
        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.IMPERIAL,
      },
      function (response, status) {
        if (status !== google.maps.DistanceMatrixStatus.OK) {
          console.log("Error:", status);
          return;
        }
  
        // Calculate the total distance and number of distances
        let totalDistance = 0;
        let numDistances = 0;
        for (let i = 0; i < markers.length; i++) {
          for (let j = 0; j < markers.length; j++) {
            if (i !== j) {
              totalDistance += response.rows[i].elements[j].distance.value;
              numDistances++;
            }
          }
        }
  
        // Calculate the average distance
        const avgDistance = totalDistance / numDistances;
  
        // Display the total and average distance on the page
        const totalDistanceElement = document.getElementById("total-distance");
        const avgDistanceElement = document.getElementById("avg-distance");
        totalDistanceElement.textContent = "Total distance travelled: " + totalDistance.toLocaleString() + " mi";
        avgDistanceElement.textContent = "Average distance travelled: " + avgDistance.toLocaleString() + " mi";
      }
    );
  }

$(document).ready(function() {
  initMap();
  updateMap();
  // setInterval(updateMap, 10000);
});
