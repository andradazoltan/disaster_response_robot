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

$query = $conn->query("SELECT * FROM ManualInfo WHERE robotID = $id;");

if($query->num_rows == 0){
	echo "{}";
	return;
}

$line = $query->fetch_assoc();
$ret = array();

$ret['dx'] = $line['dx'];
$ret['dy'] = $line['dy'];
$ret['manual'] = $line['manual'];

echo json_encode($ret, JSON_NUMERIC_CHECK);
