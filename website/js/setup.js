var lastClicked;
var numBoxRow;
var numBoxCol;
var arryRow;

$(".setup").submit(function (e) {
    e.preventDefault();
});

function createGrid() {
    var length = $("input[name=length]").val();
    var width = $("input[name=width]").val();
    numBoxRow = Math.round(length / 23);
    numBoxCol = Math.round(width / 23);

    //create array
    arryRow = new Array(numBoxRow);
    for (var i = 0; i < numBoxRow; i++) {
        arryRow[i] = new Array(numBoxCol);
        for (var j = 0; j < numBoxCol; j++) {
            arryRow[i][j] = false;
        }
    }

    var grid = clickableGrid(numBoxRow, numBoxCol, function (el, row, col, i) {

        arryRow[row][col] = !arryRow[row][col];

        el.className = 'clicked';
        // if (lastClicked) lastClicked.className='';	
        // lastClicked = el;
    });

    document.getElementById('setupform').style.display = "none";
    document.getElementById("newGrid").textContent = "Select area of search on grid below";
    document.getElementById("newGrid").appendChild(grid);
    document.getElementById('createGridBtn').style.display = "none";
    document.getElementById('initializeRobotBtn').style.display = "inline";
    document.getElementById('robotform').style.display = "inline";

}

function clickableGrid(rows, cols, callback) {
    var i = 0;
    var grid = document.createElement('table');
    var gridHeight = Math.round(350 / rows);

    grid.className = 'setGrid';

    for (var r = 0; r < rows; ++r) {
        var tr = grid.appendChild(document.createElement('tr'));
        for (var c = 0; c < cols; ++c) {
            var node = document.createElement('td');
            node.style.height = gridHeight + 'px';
            var cell = tr.appendChild(node);
            //			cell.innerHTML = ++i;
            cell.addEventListener('click', (function (el, r, c, i) {

                return function () {
                    callback(el, r, c, i);
                }
            })(cell, r, c, i), false);
        }
    }
    return grid;
}


function initializeRobot() {

    var arr = new Array();

    for (var i = 0; i < numBoxRow; i++) {
        var flag = false;

        for (var j = 0; j < numBoxCol; j++) {

            if (!flag && arryRow[i][j]) {
                arr.push(j);
                flag = true;
            }

            if (flag && !arryRow[i][j]) {
                arr.push(j-1);
            }

            if ((j == numBoxCol-1) && arryRow[i][j])  {
                arr.push(j);
            }
        }
    }

    var initX = $("input[name=initX]").val();
    var initY = $("input[name=initY]").val();
    var initAng = $("input[name=initAng]").val();

    $.ajax({
        type: "POST",
        url: 'http://38.88.75.83/db/makerobot.php',
        data: { 
            'robotID': 7, 
            'initX' : initX,
            'initY' : initY,
            'initAng' : initAng,
            'gridSizeX' : numBoxRow,
            'gridSizeY' : numBoxCol,
            'tosearch' : arr
        },
         success: function(data){
              console.log("success");
              console.log(data);
              window.alert("Successfully set up Dr. Robo.");
              location.href = "http://38.88.75.83/Login/home.html";
         }
    });

}
