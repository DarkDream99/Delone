function generatePoints() {
	let bounds = boundaryElement("view_map");
	let toX = bounds[0];
	let toY = bounds[1];
	let countPoints = $("#count_points").val();

	for (let i = 0; i < countPoints; ++i) {
		generatePoint(0, toX, 0, toY);
	}
}

function generatePoint(fromX, toX, fromY, toY) {
	coordX = fromX + Math.random() * (toX - fromX);
	coordY = fromY + Math.random() * (toY - fromY);

	addNewPoint(coordX, coordY);
	addVerticesListener();
}

function clearPoints() {
	d3.selectAll("circle").remove();
	d3.selectAll("line").remove();
	eventController.clear();
	localizeTree.clear();
}
