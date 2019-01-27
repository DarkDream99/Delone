let EVENTS = {
	newStage: "new_stage",
	addSegment: "add_segment",
	addBaseSegment: "add_base_segment",
	deleteSegment: "delete_segment",
	selectPoint: "select_point",
	deselectPoint: "deselect_point",
	selectBasePoint: "select_base_point", 
	checkSegment: "check_segment",
	selectSegment: "select_segment",

	newSegment: "new_segment",
	deselectSegment: "deselect_segment",

	addLocationRoot: "add_location_root",
	addLocationLayer: "add_location_layer",
	referenceToLocationLayer: "reference_to_location_layer"
};

eventController = {
	_events: [],
	_index: 0,

	reset: function() {
		this._index = 0;
	},

	clear: function() {
		this._events = [];
		this._index = 0;
	},

	addEvent: function(event) {
		this._events.push(event);
	},

	nextStep: function() {
		if (this._index < this._events.length) {
			this._applyEvent(this._events[this._index]);
			this._index += 1;
		} else {
			alert("Алгоритм завершон");
		}
	},

	prevStep: function() {
		if (this._index > 0) {
			this._index -= 1;
			this._deapplyEvent(this._events[this._index]);
		} else {
			alert("Находимся в начале");
		}
	},

	isEnd: function() {
		return this._index == this._events.length;
	},

	isStart: function() {
		return this._index == 0;
	},

	_applyEvent: function(event) {
		if (event.type == EVENTS.selectBasePoint) {
			addBasePoint(event.data.x, event.data.y);
		}

		if (event.type == EVENTS.selectPoint) {
			selectPoint(event.data.x, event.data.y);
		}

		if (event.type == EVENTS.deselectPoint) { 
			deselectPoint(event.data.x, event.data.y);
		}

		if (event.type == EVENTS.addBaseSegment) {
			addBaseSegment(event.data.start, event.data.end);
		}

		if (event.type == EVENTS.newSegment) {
			addSegment(event.data.start, event.data.end);
		}

		if (event.type == EVENTS.selectSegment) {
			selectSegment(event.data.start, event.data.end);
			selectSegment(event.data.end, event.data.start);
		}

		if (event.type == EVENTS.deselectSegment) {
			deselectSegment(event.data.start, event.data.end);
			deselectSegment(event.data.end, event.data.start);
		}

		if (event.type == EVENTS.deleteSegment) {
			deleteSegment(event.data.start, event.data.end);
			deleteSegment(event.data.end, event.data.start);
		}

		if (event.description.length > 0) {
			$("#hint").text(event.description);
		}

		if (event.type == EVENTS.addLocationRoot) {
			showRoot(JSON.parse(event.data.base_node));
		}

		if (event.type == EVENTS.addLocationLayer) {
			let baseNode = JSON.parse(event.data.base_node);
			let leaves = [];
			for (let i = 0; i < event.data.leaves.length; ++i) {
				leaves.push(JSON.parse(event.data.leaves[i]));
			}
			showNewLocalizeLayer(baseNode.number, leaves); 
		}

		if (event.type == EVENTS.referenceToLocationLayer) {
			let baseNode = JSON.parse(event.data.base_node);
			let leaves = [];
			for (let i = 0; i < event.data.leaves.length; ++i) {
				leaves.push(JSON.parse(event.data.leaves[i]));
			}
			addReferenceToLocalizeLayer(baseNode.number, leaves);
		}
	},

	_deapplyEvent: function(event) {
		if (event.type == EVENTS.selectBasePoint) {
			deleteBasePoint(event.data.x, event.data.y);
		}

		if (event.type == EVENTS.selectPoint) {
			deselectPoint(event.data.x, event.data.y);
		}

		if (event.type == EVENTS.deselectPoint) { 
			selectPoint(event.data.x, event.data.y);
		}

		if (event.type == EVENTS.addBaseSegment) {
			deleteSegment(event.data.start, event.data.end);
			deleteSegment(event.data.end, event.data.start);
		}

		if (event.type == EVENTS.newSegment) {
			deleteSegment(event.data.start, event.data.end);
			deleteSegment(event.data.end, event.data.start);
		}

		if (event.type == EVENTS.selectSegment) {
			deselectSegment(event.data.start, event.data.end);
			deselectSegment(event.data.end, event.data.start);
		}

		if (event.type == EVENTS.deselectSegment) {
			selectSegment(event.data.start, event.data.end);
			selectSegment(event.data.end, event.data.start);
		}

		if (event.type == EVENTS.deleteSegment) {
			addSegment(event.data.start, event.data.end);
		}

		if (event.description.length > 0) {
			$("#hint").text(event.description);
		}

		if (event.type == EVENTS.addLocationRoot) {
			deleteRoot(JSON.parse(event.data.base_node));
		}

		if (event.type == EVENTS.addLocationLayer) {
			let baseNode = JSON.parse(event.data.base_node);
			let leaves = [];
			for (let i = 0; i < event.data.leaves.length; ++i) {
				leaves.push(JSON.parse(event.data.leaves[i]));
			}
			deleteLocalizeLayer(baseNode.number, leaves);
		}

		if (event.type == EVENTS.referenceToLocationLayer) {
			let baseNode = JSON.parse(event.data.base_node);
			let leaves = [];
			for (let i = 0; i < event.data.leaves.length; ++i) {
				leaves.push(JSON.parse(event.data.leaves[i]));
			}
			deleteReferenceToLocalizeLayer(baseNode.number, leaves);
		}
	}
}; 

