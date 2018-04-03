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

$query = $conn->query("SELECT * FROM GridInfo WHERE robotID = $id;");

#no robots 
if($query->num_rows == 0){
	echo "{}";
	return;
}

$ret = array();

while($row = $query->fetch_assoc()){
	$ret[$row['y']][$row['x']] = $row['status'];
}

echo json_encode($ret, JSON_NUMERIC_CHECK);
