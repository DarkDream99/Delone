let localizeTree = {
	_layers: [],
	_nodes: [],

	addRoot: function(baseNode) {
		let node = new LocalizeNode(
			baseNode.number, 
			new Triangle(
				new Point(baseNode.triangle.point_a.x, baseNode.triangle.point_a.y), 
				new Point(baseNode.triangle.point_b.x, baseNode.triangle.point_b.y), 
				new Point(baseNode.triangle.point_c.x, baseNode.triangle.point_c.y)
			)
		);
		this._layers.push([node]);
		this._nodes.push(node);

		return node;
	},

	addNewLayer: function(baseNodeNumber, nodes) {
		this._layers.push([]);
		let countLayers = this._layers.length;
		let lastLayer = this._layers[countLayers - 1];
		let baseNode = this.getNodeByNumber(baseNodeNumber);

		for (let ind = 0; ind < nodes.length; ++ind) {
			let triangle = new Triangle(
					new Point(nodes[ind].triangle.point_a.x, nodes[ind].triangle.point_a.y), 
					new Point(nodes[ind].triangle.point_b.x, nodes[ind].triangle.point_b.y), 
					new Point(nodes[ind].triangle.point_c.x, nodes[ind].triangle.point_c.y)
			);
			let center = new Point(nodes[ind].triangle.circle.x, nodes[ind].triangle.circle.y);
			triangle.addCircle(center, nodes[ind].triangle.circle.r);
			for (let i = 0; i < nodes[ind].triangle.nears.length; ++i) {
				let near = nodes[ind].triangle.nears[i];
				triangle.addNear(
					new Point(near[0].x, near[0].y), 
					new Point(near[1].x, near[1].y), 
					new Point(near[2].x, near[2].y)
				);
			}
			let newNode = new LocalizeNode(
				nodes[ind].number, 
				triangle	
			);
			let coordX = baseNode.position.coordX + this._layers[countLayers - 1].length * 90;
			newNode.setPosition(new Point(coordX, this._layers.length * 90));
			this._layers[countLayers - 1].push(newNode);
			this._nodes.push(newNode);
		}

		return {
			baseNode: baseNode,
			leaves: this._layers[countLayers - 1]
		};
	},

	deleteLastLayer: function() {
		let countLayers = this._layers.length;
		let lastLayer = this._layers[countLayers - 1];

		for (let ind = 0; ind < lastLayer.length; ++ind) {
			this._deleteNodeByNumber(lastLayer[ind].number);
		}
		this._layers.pop();
	},

	referenceToLayer: function(baseNodeNumber) {
		let countLayers = this._layers.length;
		let baseNode = this.getNodeByNumber(baseNodeNumber);
		let lastLayer = this._layers[countLayers - 1];
		return {
			baseNode: baseNode,
			leaves: lastLayer
		};
	},

	getTriangleByNumber: function(nodeNumber) {
		for (let ind=0; ind < this._nodes.length; ++ind) {
			let node = this._nodes[ind];
			if (node.number == nodeNumber) {
				return node.triangle;
			}
		}
		return undefined;
	},

	getNodeByNumber: function(nodeNumber) {
		for (let ind = 0; ind < this._nodes.length; ++ind) {
			if (parseInt(this._nodes[ind].number) == parseInt(nodeNumber)) {
				return this._nodes[ind];
			}
		}
	},

	_deleteNodeByNumber: function(nodeNumber) {
		for (let ind = 0; ind < this._nodes.length; ++ind) {
			if (parseInt(this._nodes[ind].number) == parseInt(nodeNumber)) {
				this._nodes.splice(ind, 1);
			}
		}
	},

	clear: function() {
		this._nodes.length = 0;
		this._layers.length = 0;
	}
};