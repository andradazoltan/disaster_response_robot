<?php
if(isset($_POST['username'])){
	login();
}
else {
	echo "{\"no info\"}";
}

function login(){
	session_start();

	$servername = "localhost";
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "cynthiasdb";

	$conn = new mysqli($servername, $username, $password, $dbname);

	if($conn->connect_error){
		die("Connection failed: " . $conn->connect_error);
	}

	$UserID = $_POST["username"];

	$sql = "SELECT password, Primarykey FROM cynthiasdb.users WHERE UserID = '$UserID';";
	$result = $conn->query($sql);
	
	#should only give one result 
	if($result->num_rows > 0){
		$userpass = $_POST["password"];

		#should only give one result XD
		while($row = $result->fetch_assoc()){
			if(password_verify($userpass, $row['password'])){
				$key = $row['Primarykey'];
				$_SESSION["Primarykey"] = $key;
				echo "{\"success\"}";
				return;
			}
		}
		echo "{\"wrong pass\"}";
	}
	else {
		echo "{\"no such user\"}";
	}
}

