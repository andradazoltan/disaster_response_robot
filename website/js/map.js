window.onload = loadGrid();

var grid;
var mapArray;
var numCols;
var numRows;

function loadGrid() {
	$.ajax({
		type: "GET",
		url: 'http://38.88.75.83/db/showgrid.php?id=7',
		cache: false,
		success: function (data) {
			setUpGrid(JSON.parse(data));
		}
	});
}
function setUpGrid(data) {
	mapArray = data;
	numCols = mapArray.length;
	numRows = mapArray[0].length;

	var lastClicked;
	var currentLocation = [0, 0];
	grid = clickableGrid(numCols,numRows, function (el, row, col, i) {
		el.className = 'clicked';
		if (lastClicked) lastClicked.className = '';
		lastClicked = el;
	});

	document.getElementById("map").appendChild(grid);
	refreshMap();
}


function refreshMap() {
	var rows = grid.childNodes;
		for (var i = 0; i < numRows; i++) {
			for (var j = 0; j < numCols; j++) {
				var cols = rows[j].childNodes;
				if (mapArray[j][i] == "unvisited") {
					cols[i].style.backgroundColor = '#CCDDEE';
				} else if (mapArray[j][i] == "visited") {
					cols[i].style.backgroundColor = '#a64bf4';
				}
			}
		}
		window.setInterval(refreshMap, 3000);
}


// function clickableGrid(rows, cols, callback) {
// 	var i = 0;
// 	var grid = document.createElement('table');
// 	grid.className = 'setGrid';
// 	for (var r = 0; r < rows; ++r) {
// 		var tr = grid.appendChild(document.createElement('tr'));
// 		for (var c = 0; c < cols; ++c) {
// 			var cell = tr.appendChild(document.createElement('td'));
// 			//			cell.innerHTML = ++i;
// 			cell.addEventListener('click', (function (el, r, c, i) {
// 				return function () {
// 					callback(el, r, c, i);
// 				}
// 			})(cell, r, c, i), false);
// 		}
// 	}
// 	return grid;
// }


function updateSquare(square, status) {
	if (status == "visited") {
		square.style.backgroundColor = "blue";
	}
	else if (status == "obstacle") {
		square.style.backgroundColor = "red";
	}
}



//**************************************************************************************//
//	function updateMap(){
//		updateVisited();
//		updateCurrent();
//	}

//	function updateVisited(){
//		for(var i = 0; i < visited.length; i++){
//                        var rows = grid.childNodes;
//                        var cols = rows[visited[i][0]].childNodes;
//                        cols[visited[i][1]].style.backgroundColor = "purple";
//                }
//	}
//	function updateCurrent(){
//		var rows = grid.childNodes;
//		var cols = rows[currentLocation[0]].childNodes;
//		cols[currentLocation[1]].style.backgroundColor = "pink";
//	}

//	updateMap();
















// 	var lastClicked;
// 	var grid = clickableGrid(10,10,function(el,row,col,i){
// 	console.log("You clicked on element:",el);
// 	console.log("You clicked on row:",row);
// 	console.log("You clicked on col:",col);
// 	console.log("You clicked on item #:",i);

// 	el.className='clicked';
// 	if (lastClicked) lastClicked.className='';	
// 	lastClicked = el;
// 	});

// 	document.getElementById("map").appendChild(grid);

// 	function clickableGrid( rows, cols, callback ){
// 		var i=0;
// 		var grid = document.createElement('table');
// 		grid.className = 'grid';
// 		for (var r=0;r<rows;++r){
// 			var tr = grid.appendChild(document.createElement('tr'));
// 			for (var c=0;c<cols;++c){
// 				var cell = tr.appendChild(document.createElement('td'));			
// 	//			cell.innerHTML = ++i;
// 				cell.addEventListener('click',(function(el,r,c,i){
// 					return function(){
// 					   callback(el,r,c,i);	
// 			  	    }
// 		   		})(cell,r,c,i),false);						
//         	}	
// 	   }
// 	 return grid;						
//    }
