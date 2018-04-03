<?php
$servername = "localhost";
$username = "charlesbai321";
$password = "pi1";
$dbname = "robot";

$conn = new mysqli($servername, $username, $password, $dbname);

if($conn->connect_error){
	die("Connection failed: " . $connn->connect_error);
}

$id = $_GET["id"];

$query = $conn->query("SELECT * FROM RobotInfo WHERE id = $id;");

$ret = array();
$ret['temp'] = $query->fetch_assoc()['temp'];
echo json_encode($ret, JSON_NUMERIC_CHECK);
