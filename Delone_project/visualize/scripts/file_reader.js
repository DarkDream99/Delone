function processFileAddition(files) {
	var file = files[0];
	var reader = new FileReader();
	reader.onload = function (e) {
		let inputString = e.target.result;
		rows = inputString.split('\n');
		points = readPoints(rows);

		for (let ind = 0; ind < points.length; ++ind) {
			addNewPoint(points[ind].coordX, points[ind].coordY);
		}
	};

	reader.readAsText(file);
	$("#fileInput").val("");
}

function processFileLoad(files) {
	var file = files[0];
	var reader = new FileReader();
	clearPoints();

	reader.onload = function (e) {
		let inputString = e.target.result;
		rows = inputString.split('\n');
		points = readPoints(rows);

		for (let ind = 0; ind < points.length; ++ind) {
			addNewPoint(points[ind].coordX, points[ind].coordY);
		}
	};

	reader.readAsText(file);
	$("#fileLoad").val("");
}

function readPoints(rows) {
	points = [];

	if (rows.length > 100) {
		alert("Количество точек не должно превышать 100");
		return;
	}

	for (let ind = 0; ind < rows.length; ind += 1) {
		nums = rows[ind].split(' ');
		let x, y;
		if (isNumeric(nums[0]) && isNumeric(nums[1])) {
			x = parseFloat(nums[0]);
			y = parseFloat(nums[1]);
		} else {
			alert("Параметры в файле должны быть численными значениями");
			return [];
		}
		
		if (x < -2000 || x > 2000 || y < -2000 || y > 2000) {
			alert("Значения координат не должны превышать по модулю 2000");
			return [];
		}

		points.push(new Point(x, y));
	}

	return points;
}

function showFileAddition() {
	let fileInput = document.getElementById('fileInput');
	fileInput.click();
}

function showFileLoad() {
	let fileLoad = document.getElementById('fileLoad');
	fileLoad.click();
}

function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}
