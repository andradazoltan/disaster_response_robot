<?php

$id = $_GET["id"];

if(isset($_POST["robotX"]) && isset($_POST["robotY"])){
	$servername = "localhost";	
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "robot";

	$x = $_POST["robotX"];
	$y = $_POST["robotY"];
	$temp = $_POST["temp"];

	$dir = $_POST["robotdir"];
	$conn = new mysqli($servername, $username, $password, $dbname);

	if($conn->connect_error){
		die("Connection failed: " . $connn->connect_error);
	}

	$query = $conn->query("SELECT gridSizeX, gridSizeY FROM LocationInfo WHERE robotID = $id;");

	if($query->num_rows == 0){
		echo "error";
		return;
	}
	$row = $query->fetch_assoc();
	$upX = $row["gridSizeX"];
	$upY = $row["gridSizeY"];
	
	if($conn->query("UPDATE RobotInfo SET currLocX = $x, currLocY = $y, currDir = $dir, temp = $temp WHERE id = $id;") == TRUE){
		echo "success";
	}
	else {
		echo $conn->error;
	}
}
?>
