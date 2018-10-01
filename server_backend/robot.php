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

#no robots 
if($query->num_rows == 0){
	echo "{}";
	return;
}

	$robotID = $id;
	
	$oneRobot = array();
	$beaconData = array();
	$gridData = array();

	#gather the beacon info 
	$query1 = $conn->query("SELECT * FROM BeaconInfo WHERE robotID = $robotID;");
	while($beacon = $query1->fetch_assoc()){
		$beaconData[$beacon["btID"]] = array($beacon["btX"], $beacon["btY"], $beacon["btZ"]);
	}

	#gather the location info
	$query2 = $conn->query("SELECT * FROM LocationInfo WHERE robotID = $robotID;");
	if($query2->num_rows == 0) {
		echo "{}";
	}
	$location = $query2->fetch_assoc();
	
	#gather to search info
	$query3 = $conn->query("SELECT * FROM SearchInfo WHERE robotID = $robotID;");
	if($query3->num_rows == 0){
		echo "{}"; 
	}
	$tosearch = array();
	while($row = $query3->fetch_assoc()){
		$tosearch[$row["rowNum"]] = array($row["start"], $row["end"]);
	}
	
	$gridData["grid_size"] = array($location["gridSizeX"], $location["gridSizeY"]);
	$gridData["to_search"] = $tosearch;

	#put them into the array
	$oneRobot["robot_id"] = $robotID;
	$oneRobot["beacon_info"] = $beaconData;
	$oneRobot["grid"] = $gridData;
	$oneRobot["robot_loc"] = array($location["robotInitPosX"], $location["robotInitPosY"], 0);
	$oneRobot["robot_dir"] = $location["robotInitAng"]; 
	$oneRobot["scale"] = $location["scale"];
	
	echo json_encode($oneRobot, JSON_NUMERIC_CHECK);
?>
