Chart.defaults.global.legend.display = false;
Chart.defaults.global.maintainAspectRatio = false;

function loadChart(case_id, responses) {
	// Canvas
	var chartCanvas = document.getElementById("results-chart-canvas");

	var white = 0;
	var gray = 0;
	var black = 0;
	for (var i = 0; i < responses.length; i++) {
		switch(responses[i].response) {
		case "white":
			white++;
			break;
		case "gray":
			gray++;
			break;
		case "black":
			black++;
			break;
		}
	}

	var data = {
		labels : [ "White Hat", "Gray Hat", "Black Hat" ],
		datasets : [ {
			data : [white, gray, black],
			backgroundColor: [
                "#FFFFFF",
                "#666666",
                "#191919"
            ]
		} ]
	};

	var chart = new Chart(chartCanvas, {
		type : 'pie',
		data : data
	});
}