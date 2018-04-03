<?php
if(isset($_POST['username'])){
	login();
}
else {
	$ret = array();
	$ret['status'] = 'no info';
	echo json_encode($ret);
}

function login(){
	session_start();
	$ret = array();

	$servername = "localhost";
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "cynthiasdb";
	
	

	$conn = new mysqli($servername, $username, $password, $dbname);

	if($conn->connect_error){
		$ret['status'] = 'database error';
		echo json_encode($ret);
		return;
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
				$ret['status'] = 'success';
				echo json_encode($ret);
				return;
			}
		}
		$ret['status'] = 'wrong pass';
		echo json_encode($ret);
	}
	else {
		$ret['status'] = 'no such user';
		echo json_encode($ret);
	}
}

