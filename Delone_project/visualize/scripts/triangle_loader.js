function loadTriangulation() {
	points = getPoints();
	if (points.length < 3) {
		alert("Невозможно разбить на триугольники множество из менее 3 элементов")
		return;
	}
	if (points.length > 100) {
		alert(`Попытка загрузить ${points.length} точек из 100 возможных`);
		return;
	}

	$("#prev_step").hide();
	$("#next_step").hide();

	return $.ajax({
	        url: apiUrl + "triangulation/",
	        type: 'GET',
	        data: {
	        	points: JSON.stringify(points)
	        },
	        success: function(res) {
	            console.log(res);
	            initEvents(JSON.parse(res));
	            $("#prev_step").show();
	            $("#next_step").show();
	        },
	    }).fail(function (data, textStatus, errorThrown){
	        console.log(data);
	        console.log(errorThrown);
	    });
}

function getPoints() {
	points =  $("circle");
	resPoints = []

	for (let ind = 0; ind < points.length; ++ind) {
		pointObj = {
			type: "Point",
			x: $(points[ind]).attr("cx"),
			y: $(points[ind]).attr("cy")
		};
		resPoints.push(pointObj);
	}

	return resPoints;
}

function initEvents(events) {
	for (let ind = 0; ind < events.length; ++ind) {
		let curEvent = JSON.parse(events[ind]);
		if (curEvent.type == EVENTS.addSegment) {
			eventController.addEvent({
				type: EVENTS.newSegment,
				data: curEvent.data,
				description: ""
			});

			eventController.addEvent({
				type: EVENTS.deselectSegment,
				data: curEvent.data,
				description: ""
			});
		} else if(curEvent.type == EVENTS.selectPoint) {
			eventController.addEvent(curEvent);
			eventController.addEvent({
				type: EVENTS.deselectPoint,
				data: curEvent.data,
				description: ""
			});
		} else if(curEvent.type == EVENTS.deleteSegment) {
			eventController.addEvent({
				type: EVENTS.selectSegment,
				data: curEvent.data,
				description: ""
			});

			eventController.addEvent({
				type: EVENTS.deleteSegment,
				data: curEvent.data,
				description: ""
			});
		} else if(curEvent.type == EVENTS.checkSegment) {
			eventController.addEvent({
				type: EVENTS.selectSegment,
				data: curEvent.data,
				description: ""
			});

			eventController.addEvent({
				type: EVENTS.deselectSegment,
				data: curEvent.data,
				description: ""
			});
		} else {
			eventController.addEvent(curEvent);
		}
	}
}