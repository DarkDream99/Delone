function Triangle(pointA, pointB, pointC) {
	this.pointA = pointA;
	this.pointB = pointB;
	this.pointC = pointC;

	this.nears = [];
	this.circle = null;

	this.addNear = function(pointA, pointB, pointC) {
		this.nears.push(new Triangle(pointA, pointB, pointC));
	};

	this.addCircle = function(center, radius) {
		this.circle = {
			center: center,
			radius: radius
		};
	};

	this.segments = function() {
		return [
			Segment(this.pointA, this.pointB),
			Segment(this.pointB, this.pointC),
			Segment(this.pointC, this.pointA)
		];
	};
}
