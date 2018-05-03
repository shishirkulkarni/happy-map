var lib = (function() {
	var populateCitiesLookup = function(err, locations, polarities) {
		var data = []
		
		locations.forEach(function(location) {
			var loc = {}
			loc['loc_name'] = location['location_name'].replace(/\s+/gi, "");
			loc['lat'] = parseFloat(location['lat']);
			loc['long'] = parseFloat(location['long']);
			var loc_name = polarities.filter(function(polarity) { return polarity['Location'] == loc['loc_name']});
			loc['polarity'] = loc_name.length && parseFloat(loc_name[0]['Polarity']) || NaN;
			data.push(loc);
		});

		return data;
	}

	var colorShades = function(pol) {
		if(pol > 0) {
			return '#66ff33';
		} else if (pol === 0.0) {
			return '#ffff33';
		} else {
			return '#ff4d4d';
		}
	}

	var idToStateMap = function() {
		return {
			"04": "AZ",
			"06": "CA",
			"08": "CO",
			"24": "DC",
			"12": "FL",
			"13": "GA",
			"17": "IL",
			"25": "MA",
			"26": "MI",
			"27": "MN",
			"29": "MO",
			"36": "NY",
			"39": "OH",
			"41": "OR",
			"42": "PA",
			"48": "TX",
			"53": "WA"
		}
	}

	return {
		populateCitiesLookup,
		colorShades,
		idToStateMap
	}
})();