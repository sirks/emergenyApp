let mymap = L.map('mapid').setView([0, 0], 10);

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw')
.addTo(mymap);

var myLocationIcon = L.icon({
  iconUrl: 'assets/meMarker.png',
  iconAnchor: [10, 10],
});

let myLocationMarker = undefined;

updateLocation();

function updateLocation() {
  if (!navigator.geolocation) {
    console.log('no geolocation available!');
    return;
  }
  navigator.geolocation.getCurrentPosition(manageLocation);
  setTimeout(updateLocation, 9999)
}


function manageLocation(position) {
  const myLocation = [position.coords.latitude, position.coords.longitude];
  console.log(`new location ${myLocation}`);
  if (myLocationMarker) {
    myLocationMarker = L.marker(myLocation).update(myLocationMarker);
  } else {
    mymap.setView([60.190695, 24.944458], 10);
    myLocationMarker = L.marker(myLocation, {icon: myLocationIcon}).addTo(mymap);
  }
}

updatePolygons();

function updatePolygons() {
  if (!navigator.geolocation) {
    console.log('no geolocation available!');
    return;
  }
  navigator.geolocation.getCurrentPosition(managePolygons);
  setTimeout(updatePolygons, 999999)
}

function managePolygons(position) {
  fetch(`https://${location.hostname}:5000/api/polygons?lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
  .then(resp => resp.json())
  .then(json => drawPolygons(json))
  .catch(console.log)
}

function drawPolygons(polygons) {
  debugger;
  console.log(`drawing ${polygons}`);
  Object.values(polygons).forEach(p => L.polygon(p.poldata, {
      color: 'red',
      fillColor: '#f03',
    }
    ).addTo(mymap).bindPopup("Hazard here")
  );
}