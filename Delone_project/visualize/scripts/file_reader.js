function processFiles(files) {
	var file = files[0];
	var reader = new FileReader();
	reader.onload = function (e) {
		let inputString = e.target.result;
		rows = inputString.split('\n');
		for (let ind = 0; ind < rows.length; ind += 1) {
			nums = rows[ind].split(' ');
			let x = parseFloat(nums[0]);
			let y = parseFloat(nums[1]);

			addNewPoint(x, y);
		}
	};
	reader.readAsText(file);
}

function showFileInput() {
	var fileInput = document.getElementById('fileInput');
	fileInput.click();
}
