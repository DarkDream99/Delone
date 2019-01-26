function selectBasePoint(coordX, coordY) {
	let circles = $("circle"); 
	let exist = false;
	for (let ind = 0; ind < circles.length; ++ind) {
		if ($(circles[ind]).attr("cx") == parseFloat(coordX) && $(circles[ind]).attr("cy") == parseFloat(coordY)) {
			$(circles[ind])
				.attr("r", selectedPointRadius)
				.css("fill", baseColor);
			exist = true;
		}
	}

	if (!exist) {
		addNewPoint(coordX, coordY);
		selectBasePoint(coordX, coordY);
	}
}

function selectPoint(coordX, coordY) {
	let circles = $("circle"); 
	for (let ind = 0; ind < circles.length; ++ind) {
		if ($(circles[ind]).attr("cx") == parseFloat(coordX) && $(circles[ind]).attr("cy") == parseFloat(coordY)) {
			$(circles[ind])
				.attr("r", selectedPointRadius)
				.css("fill", selectColor);
		}
	}
}

function deselectPoint(coordX, coordY) {
	let circles = $("circle");
	for (let ind = 0; ind < circles.length; ++ind) {
		if ($(circles[ind]).attr("cx") == parseFloat(coordX) && $(circles[ind]).attr("cy") == parseFloat(coordY)) {
			$(circles[ind])
				.attr("r", generalPointRadius)
				.css("fill", generalColor);
		}
	}
}

function deletePoint(coordX, coordY) {
	let circles = $("circle");
	for (let ind = 0; ind < circles.length; ++ind) {
		if ($(circles[ind]).attr("cx") == parseFloat(coordX) && $(circles[ind]).attr("cy") == parseFloat(coordY)) {
			$(circles[ind]).remove();
		}
	}
}

function addBaseSegment(pointA, pointB) {
	view_map_container.append("line")
						.attr("x1", pointA.x)
						.attr("y1", pointA.y)
						.attr("x2", pointB.x)
						.attr("y2", pointB.y)
						.style("stroke", baseColor)
						.style("stroke-width", generalSegmentWidth)
}

function addSegment(pointA, pointB) {
	view_map_container.append("line")
						.attr("x1", pointA.x)
						.attr("y1", pointA.y)
						.attr("x2", pointB.x)
						.attr("y2", pointB.y)
						.style("stroke", newColor)
						.style("stroke-width", generalSegmentWidth)
}

function selectSegment(pointA, pointB) {
	let segments = $("line");
	for (let ind = 0; ind < segments.length; ++ind) {
		if (parseFloat($(segments[ind]).attr("x1")) == parseFloat(pointA.x) && parseFloat($(segments[ind]).attr("y1")) == parseFloat(pointA.y) &&
			parseFloat($(segments[ind]).attr("x2")) == parseFloat(pointB.x) && parseFloat($(segments[ind]).attr("y2")) == parseFloat(pointB.y))
		{
			$(segments[ind])
				.css("stroke", selectColor)
				.css("stroke-width", selectedSegmentWidth);
		}
	}
}

function deselectSegment(pointA, pointB) {
	let segments = $("line");
	for (let ind = 0; ind < segments.length; ++ind) {
		if (parseFloat($(segments[ind]).attr("x1")) == parseFloat(pointA.x) && parseFloat($(segments[ind]).attr("y1")) == parseFloat(pointA.y) &&
			parseFloat($(segments[ind]).attr("x2")) == parseFloat(pointB.x) && parseFloat($(segments[ind]).attr("y2")) == parseFloat(pointB.y))
		{
			$(segments[ind])
				.css("stroke", generalColor)
				.css("stroke-width", selectedSegmentWidth);
		}
	}
}

function deleteSegment(pointA, pointB) {
	let segments = $("line");
	for (let ind = 0; ind < segments.length; ++ind) {
		if (parseFloat($(segments[ind]).attr("x1")) == parseFloat(pointA.x) && parseFloat($(segments[ind]).attr("y1")) == parseFloat(pointA.y) &&
			parseFloat($(segments[ind]).attr("x2")) == parseFloat(pointB.x) && parseFloat($(segments[ind]).attr("y2")) == parseFloat(pointB.y))
		{
			$(segments[ind]).remove();
		}
	}
}

function nextStep() {
	console.log($("#auto").prop("checked"));
	if ($("#auto").prop("checked") == true) {
		eventController.nextStep();
		setTimeout(nextStep, 600);
	} else {
		eventController.nextStep();
	}
}

function prevStep() {
	if ($("#auto").prop("checked") == true) {
		eventController.prevStep();
		setTimeout(prevStep, 600);
	} else {
		eventController.prevStep();
	}
}

