let mymap = L.map('mapid');

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw')
.addTo(mymap);

var myLocationIcon = L.icon({
  iconUrl: 'assets/meMarker.png',
  iconAnchor:   [10, 10],
});

let myLocation = undefined;

updateLocation();

function updateLocation() {
  if (!navigator.geolocation) {
    console.log('no geolocation available!');
    return;
  }
  navigator.geolocation.getCurrentPosition(drawPosition);
  setTimeout(updateLocation, 9999)
}

function drawPosition(position) {
  const newLocation = [position.coords.latitude, position.coords.longitude];
  console.log(`new location ${newLocation}`);
  if (myLocation) {
    myLocation = L.marker(newLocation).update(myLocation);
  } else {
    mymap.setView([60.190695, 24.944458], 10);
    myLocation = L.marker(newLocation, {icon: myLocationIcon}).addTo(mymap);
  }
}

L.polygon([
    [61, 24],
    [60, 24],
    [60, 25],
    [61, 25],
  ],
  {
    color: 'red',
    fillColor: '#f03',
  }
).addTo(mymap).bindPopup("Hazard here");
