function LocalizeNode(number, triangle) {
	this.number = number;
	this.triangle = triangle;
	this.position = new Point(0, 0);

	this.setPosition = function(position) {
		this.position = position;
	}
}