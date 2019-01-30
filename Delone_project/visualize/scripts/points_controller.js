let view_map_container;
let localize_tree_container;
let zoomMap;
let transform = {x: 0, y: 0, k: 1};


var margin = {top: -5, right: -5, bottom: -5, left: -5};


$(document).ready(start); 

function start() {
    transform = {x: 0, y: 0, k: 1};
    d3.selectAll("svg")
        .transition();

    view_map_container = d3.select("#view_map");
    localize_tree_container = d3.select("#view_localize_tree");

    d3.select("#view_map")
        .on("click", function(d,i) { 
            let boundary = this.getBoundingClientRect();
            let delX = transform.x;
            let delY = transform.y;

            let coordX = d3.event.pageX - boundary.left - this.clientLeft - window.pageXOffset - delX;
            let coordY = d3.event.pageY - boundary.top - this.clientTop - window.pageYOffset  - delY;
            console.log(`x: ${coordX}; y: ${coordY}`); 

            addNewPoint(coordX, coordY);
            addVerticesListener();

            console.log(event.x + " " + event.y);
        });

    view_map_container = d3.select("#view_map")
                     .attr("width", "100%")
                     .attr("height", "100%")
                     .call(d3.zoom().on("zoom", function () {
                        view_map_container.attr("transform", d3.event.transform);
                        transform = d3.event.transform;
                     }))
                     .append("g");

    localize_tree_container = d3.select("#view_localize_tree")
                            .attr("width", "100%")
                            .attr("height", "100%")
                            .call(d3.zoom().on("zoom", function() {
                                localize_tree_container.attr("transform", d3.event.transform);
                            }))
                            .append("g");
}

let vertexCount = 0;
function addNewPoint(coordX, coordY) {
    console.log(coordX + " " + coordY);
    view_map_container.append("circle")
            .attr("vertexIndex", vertexCount++)
            .attr("cx", coordX)
            .attr("cy", coordY)
            .attr("r", generalPointRadius)
            .attr("type", "sourcePoint");
}

function addVerticesListener() {
    d3.selectAll("circle")
        .on(
            "mouseover", function(d, i) {
                console.log(i);
            }
        );
}

function moveMapToCenter() {
    view_map_container.attr("transform", {k: 1, x: 0, y: 0});
}

function boundaryElement(id) {
    let element = document.getElementById(id);
    let positionInfo = element.getBoundingClientRect();

    return [positionInfo.width, positionInfo.height];
}

