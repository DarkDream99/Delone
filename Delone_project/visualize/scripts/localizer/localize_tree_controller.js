function showRoot(baseNode) {
	let localizeNode = localizeTree.addRoot(baseNode);
	showLocalizerNode(localizeNode);
}

function deleteRoot(baseNode) {
	let rootNode = localizeTree.getNodeByNumber(baseNode.number);
	deleteLocalizeNode(rootNode);
	localizeTree.deleteLastLayer();
}

function showNewLocalizeLayer(baseNodeNumber, nodes) {
	resNodes = localizeTree.addNewLayer(baseNodeNumber, nodes);
	leaves = resNodes.leaves;

	for (let ind = 0; ind < leaves.length; ++ind) {
		showLocalizerNode(resNodes.leaves[ind]);
		showLocalizeEdge(resNodes.baseNode.position, leaves[ind].position);
	}
}

function deleteLocalizeLayer(baseNodeNumber, nodes) {
	localizeBaseNode = localizeTree.getNodeByNumber(baseNodeNumber);

	for (let ind = 0; ind < nodes.length; ++ind) {
		let localizeChild = localizeTree.getNodeByNumber(nodes[ind].number);
		let chosenSegment = new Segment(
			new Point(localizeBaseNode.position.coordX, localizeBaseNode.position.coordY + localNodeRadius / 2), 
			new Point(localizeChild.position.coordX, localizeChild.position.coordY - localNodeRadius / 2)
		);
		deleteLocalizeNode(localizeChild);
		deleteLocalizeEdge(chosenSegment);
	}

	localizeTree.deleteLastLayer();
}

function addReferenceToLocalizeLayer(baseNodeNumber, nodes) {
	resNodes = localizeTree.referenceToLayer(baseNodeNumber);
	leaves = resNodes.leaves;

	for (let ind = 0; ind < leaves.length; ++ind) {
		showLocalizeEdge(resNodes.baseNode.position, leaves[ind].position);
	}
}

function deleteReferenceToLocalizeLayer(baseNodeNumber, nodes) {
	localizeBaseNode = localizeTree.getNodeByNumber(baseNodeNumber);

	for (let ind = 0; ind < nodes.length; ++ind) {
		let localizeChild = localizeTree.getNodeByNumber(nodes[ind].number);
		let chosenSegment = new Segment(
			new Point(localizeBaseNode.position.coordX, localizeBaseNode.position.coordY + localNodeRadius / 2), 
			new Point(localizeChild.position.coordX, localizeChild.position.coordY - localNodeRadius / 2)
		);
		deleteLocalizeEdge(chosenSegment);
	}
}

function showLocalizerNode(baseNode) {
	localize_tree_container.append("circle")
						.attr("cx", baseNode.position.coordX)
			            .attr("cy", baseNode.position.coordY)
			            .attr("r", localNodeRadius)
			            .attr("type", "localizeNode")
			            .attr("triangleNumber", baseNode.number)
			            .on("mouseover", _handleLocalizeNodeMouseOver)
			            .on("mouseout", _handleLocalizeNodeMouseOut);		
}

function _handleLocalizeNodeMouseOver(d, i) {
	let nodeNumber = $(this).attr("triangleNumber");
	let triangle = localizeTree.getTriangleByNumber(nodeNumber);

	_selectNearTriangle(triangle);

	addSeenSegment(triangle.pointA, triangle.pointB);
	addSeenSegment(triangle.pointB, triangle.pointC);
	addSeenSegment(triangle.pointC, triangle.pointA);
}

function _handleLocalizeNodeMouseOut(d, i) {
	let nodeNumber = $(this).attr("triangleNumber");
	let triangle = localizeTree.getTriangleByNumber(nodeNumber);
	deleteSeenSegment(triangle.pointA, triangle.pointB);
	deleteSeenSegment(triangle.pointB, triangle.pointC);
	deleteSeenSegment(triangle.pointC, triangle.pointA);

	_deselectNearTriangle(triangle);
}

function _selectNearTriangle(triangle) {
	for (let ind = 0; ind < triangle.nears.length; ++ind) {
		let near = triangle.nears[ind];
		_selectNearSegment(near.pointA, near.pointB);
		_selectNearSegment(near.pointB, near.pointC);
		_selectNearSegment(near.pointC, near.pointA);
	}
}

function _selectNearSegment(nodePointA, nodePointB) {
	view_map_container.append("line")
						.attr("x1", nodePointA.coordX)
						.attr("y1", nodePointA.coordY)
						.attr("x2", nodePointB.coordX)
						.attr("y2", nodePointB.coordY)
						.attr("type", "nearSegment")
						.style("stroke", nearColor)
						.style("stroke-width", seenWidth);
}

function _deselectNearTriangle(triangle) {
	for (let ind = 0; ind < triangle.nears.length; ++ind) {
		let near = triangle.nears[ind];
		_deleteNearSegment(near.pointA, near.pointB);
		_deleteNearSegment(near.pointB, near.pointC);
		_deleteNearSegment(near.pointC, near.pointA);
	}
}

function _deleteNearSegment(nodePointA, nodePointB) {
	let segments = $("line");
	for (let ind = 0; ind < segments.length; ++ind) {
		if (parseFloat($(segments[ind]).attr("x1")) == parseFloat(nodePointA.coordX) 
			&& parseFloat($(segments[ind]).attr("y1")) == parseFloat(nodePointA.coordY) 
			&& parseFloat($(segments[ind]).attr("x2")) == parseFloat(nodePointB.coordX) 
			&& parseFloat($(segments[ind]).attr("y2")) == parseFloat(nodePointB.coordY))
		{
			if ($(segments[ind]).attr("type") == "nearSegment") {
				$(segments[ind]).remove();
			}
		}
	}
}

function deleteLocalizeNode(localizeNode) {
	let circles = $("circle");
	for (let ind = 0; ind < circles.length; ++ind) {
		let circle = $(circles[ind]);
		if (parseFloat(circle.attr("cx")) == localizeNode.position.coordX 
			&& parseFloat(circle.attr("cy")) == localizeNode.position.coordY) 
		{
			if (circle.attr("type") == "localizeNode") {
				circle.remove();
			}
		}
	}
}

function addSeenSegment(nodePointA, nodePointB) {
	view_map_container.append("line")
						.attr("x1", nodePointA.coordX)
						.attr("y1", nodePointA.coordY)
						.attr("x2", nodePointB.coordX)
						.attr("y2", nodePointB.coordY)
						.attr("type", "seenSegment")
						.style("stroke", seenColor)
						.style("stroke-width", seenWidth)
}

function deleteSeenSegment(nodePointA, nodePointB) {
	let segments = $("line");
	for (let ind = 0; ind < segments.length; ++ind) {
		if (parseFloat($(segments[ind]).attr("x1")) == parseFloat(nodePointA.coordX) && parseFloat($(segments[ind]).attr("y1")) == parseFloat(nodePointA.coordY) &&
			parseFloat($(segments[ind]).attr("x2")) == parseFloat(nodePointB.coordX) && parseFloat($(segments[ind]).attr("y2")) == parseFloat(nodePointB.coordY))
		{
			if ($(segments[ind]).attr("type") == "seenSegment") {
				$(segments[ind]).remove();
			}
		}
	}
}

function showLocalizeEdge(nodePointA, nodePointB) {
	localize_tree_container.append("line")
    					.attr("x1", nodePointA.coordX)
						.attr("y1", nodePointA.coordY + localNodeRadius / 2)
						.attr("x2", nodePointB.coordX)
						.attr("y2", nodePointB.coordY - localNodeRadius / 2)
						.attr("type", "localizeEdge")
						.style("stroke", generalColor)
						.style("stroke-width", generalSegmentWidth);	
}

function deleteLocalizeEdge(chosenSegment) {
	let nodePointA = chosenSegment.start;
	let nodePointB = chosenSegment.end;
	let segments = $("line");
	for (let ind = 0; ind < segments.length; ++ind) {
		let segment = $(segments[ind]);
		if (parseFloat(segment.attr("x1")) == parseFloat(nodePointA.coordX) 
			&& parseFloat(segment.attr("y1")) == parseFloat(nodePointA.coordY) 
			&& parseFloat(segment.attr("x2")) == parseFloat(nodePointB.coordX) 
			&& parseFloat(segment.attr("y2")) == parseFloat(nodePointB.coordY))
		{
			if (segment.attr("type") == "localizeEdge") {
				segment.remove();
			}
		}
	}
}
