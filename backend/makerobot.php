<?php

if(isset($_POST["robotID"])){
	#assume that if we have a robotID, we will have all the other information
	#let's parse all of this information that we will recieve:
	$robotID = $_POST['robotID']; 
	$initX = $_POST['initX']; 
	$initY = $_POST['initY'];
	$initAng = $_POST['initAng'];
	$gridSizeX = $_POST['gridSizeX'];
	$gridSizeY = $_POST['gridSizeY'];
	#DEPRECATED-----------------------	
	#$bt1ID = $_POST['bt1ID'];
	#$bt2ID = $_POST['bt2ID']; 
	#$bt3ID = $_POST['bt3ID']; 
	#$bt1X = $_POST['bt1X']; 
	#$bt1Y = $_POST['bt1Y']; 
	#$bt1Z = $_POST['bt1Z'];
	#$bt2X = $_POST['bt2X']; 
	#$bt2Y = $_POST['bt2Y'];
	#$bt2Z = $_POST['bt2Z'];
	#$bt3X = $_POST['bt3X']; 
	#$bt3Y = $_POST['bt3Y'];   
	#$bt3Z = $_POST['bt3Z'];
	#---------------------------------
	echo "here";

	#TODO: initialize grid for GridInfo

	$tosearch = array();
	foreach($_POST['tosearch'] as $key => $value){
		$index = (int)$key/2;
		if($key % 2 == 0){
			$tosearch[$index] = array();
			$tosearch[$index][0] = $value;		
		}
		else {
			$tosearch[$index][1] = $value;
		}
	}
	 	
	#information is parsed: time to upload to the server	
	$servername = "localhost";	
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "robot";
	
	$conn = new mysqli($servername, $username, $password, $dbname);

	if($conn->connect_error){
		die("Connection failed: " . $connn->connect_error);
	}
	if($conn->query("SELECT * FROM RobotInfo WHERE robotID = $robotID;")->numrows != 0){
		die("Robot with this ID exists already");
	}
	
	#insert info onto database 
	$updateRobotInfo = "INSERT INTO RobotInfo VALUES($robotID, $initX, $initY, $initAng);";
	$updateBeacon1 = "INSERT INTO BeaconInfo VALUES($robotID, '$bt1ID', $bt1X, $bt1Y, $bt1Z);";	
	$updateBeacon2 = "INSERT INTO BeaconInfo VALUES($robotID, '$bt2ID', $bt2X, $bt2Y, $bt2Z);";
	$updateBeacon3 = "INSERT INTO BeaconInfo VALUES($robotID, '$bt3ID', $bt3X, $bt3Y, $bt3Z);";
	$updateLocationInfo = "INSERT INTO LocationInfo VALUES($robotID,  $gridSizeX, $gridSizeY, $initX, $initY, 23, $initAng);";
	$initializemanual = "INSERT INTO ManualInfo VALUES($robotID, 0.0, 0.0, 0);";

	#DEBUG
	echo $updateRobotInfo;
	echo $updateBeacon1;
	echo $updateBeacon2;
	echo $updateBeacon3;
	echo $updateLocationInfo;
	
	if(!$conn->query($updateRobotInfo)) exit("could not update info");
	#if(!$conn->query($updateBeacon1) || !$conn->query($updateBeacon2) || !$conn->query($updateBeacon3)) exit("coud not update bt");
	if(!$conn->query($updateLocationInfo)) exit("could not update location");
	if(!$conn->query($initializemanual)) exit("could not initialize to automatic mode");

	#update to_search area

	$y = 0;
	#tosearch should be as tall as the graph
	foreach($tosearch as $key => $value){
		$start = $tosearch[$key][0];
		$stop = $tosearch[$key][1];
		$line = "INSERT INTO SearchInfo VALUES($robotID, $key, $start, $stop);";
		#DEBUG
		#echo $line;
		if(!$conn->query($line)) exit("could not update query");

		for($i = 0; $i < $gridSizeY; $i++){
			if($i < $start-1 || $i > $stop-1){
				$line1 = "INSERT INTO GridInfo VALUES($robotID, $i, $y, \"outside\");";
				$conn->query($line1);
			}
			else {
				$line1 = "INSERT INTO GridInfo VALUES($robotID, $i, $y, \"unvisited\");";
				$conn->query($line1);
			}
		}
		$y++;		
	}
	echo "done";
}
?>
