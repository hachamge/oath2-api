function initMap() {
	let latitude = 45.56734;
	let longitude = -122.85974;

	let mapOptions = {
		center: {lat: latitude, lng: longitude},
		zoom: 12,
	};

	let map = new google.maps.Map(document.getElementById('GoogleMap'), mapOptions);

	let locations = "{{GOOGLE_MAPS_API_KEY}}";
	console.log('map.js: ', locations);
}

document.addEventListener('DOMContentLoaded', function() {
	initMap();
});
