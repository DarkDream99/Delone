function Triangle(pointA, pointB, pointC) {
	this.pointA = pointA;
	this.pointB = pointB;
	this.pointC = pointC;

	this.nears = []

	this.addNear = function(pointA, pointB, pointC) {
		this.nears.push(new Triangle(pointA, pointB, pointC));
	}

	this.segments = function() {
		return [
			Segment(this.pointA, this.pointB),
			Segment(this.pointB, this.pointC),
			Segment(this.pointC, this.pointA)
		];
	};
}