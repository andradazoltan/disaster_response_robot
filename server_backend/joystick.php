<?php
	if(!isset($_POST['x_coordinate']) && !isset($_POST['y_coordinate'])) return;
  
    $x_coord = $_POST['x_coordinate'];
    $y_coord = $_POST['y_coordinate'];

		
	$servername = "localhost";
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "robot";

	$conn = new mysqli($servername, $username, $password, $dbname);

	if($conn->connect_error){
		die("Connection failed: " . $connn->connect_error);
	}

	$id = 7;
	#$id = $_GET["id"];
	
	$query = $conn->query("UPDATE ManualInfo SET dx = $x_coord, dy = $y_coord WHERE robotID = $id;");

	echo "[$x_coord, $y_coord]";
		

  ?> 
