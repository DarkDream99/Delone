function generatePoints() {	
	let bounds = boundaryElement("view_map");
	let toX = bounds[0];
	let toY = bounds[1];
	let countPoints = $("#count_points").val();

	if (countPoints <= 0) {
		alert("Количество точек должно быть натуральным числом");
		return;
	}
	if (countPoints > 100) {
		alert("Допускается до 100 точек");
		return;
	}

	if (!eventController.isStart() && !eventController.isEnd()) {
	let ok = confirm("Вы уверены что хотите создать новые точки? Текущее состояние триангуляции будет утеряно.");
		if (ok) {
			clearPoints();
		} else {
			return;
		}
	}

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

function converToTest() {
	let points = $("circle");
	test = ""
	for (let ind = 0; ind < points.length; ++ind) {
		let point = $(points[ind]);
		if (point.attr("type") == "sourcePoint") {
			test += `${point.attr("cx")} ${point.attr("cy")} \n`;
		}
	}

	console.log(test);
}

function clearPoints() {
	d3.selectAll("circle").remove();
	d3.selectAll("line").remove();
	eventController.clear();
	localizeTree.clear();

	start();
}
