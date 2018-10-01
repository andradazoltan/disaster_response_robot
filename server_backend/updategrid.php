<?php
$id = $_GET["id"];

if(isset($_POST["xpos"]) && isset($_POST["ypos"])){
	$servername = "localhost";	
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "robot";
	
	$status = $_POST["status"];
	$x = $_POST["xpos"];
	$y = $_POST["ypos"];
	
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
	
	if($x < 0 || $x >= gridSizeX || $y < 0 || $y >= gridSizeY){
		echo "out of bounds";
		return;
	}

	if($conn->query("UPDATE GridInfo SET status = '$status' WHERE robotID = $id && x = $x && y = $y;") == TRUE){
		echo "success";
	}
	else {
		echo $conn->error;
	}
}
?>
