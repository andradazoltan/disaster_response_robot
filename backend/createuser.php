<html>
<center><h1> Create User </h1></center>
<br>
<br>

<center>
<form action="createuser.php" method="post">
	Username: <br>
	<input type="text" name="username"><br>
	Password: <br>
	<input type="text" name="password"><br>
	<br>
	<input type="submit" name="createuser" value ="Log In">
</form>
</center>
</html>

<?php
header("Access-Control-Allow-Origin: *");
#if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST['createuser'])){
if(true){
	createuser();
}

function createuser(){
	$servername = "localhost";
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "cynthiasdb";

	$conn = new mysqli($servername, $username, $password, $dbname);
	
	if($conn->connect_error){
		die("Connection failed: " . $conn->connect_error);
	}

	$UserID = $_POST["username"];
	$password = $_POST["password"];
	$date = date("Y-m-d"); 

	$password = password_hash($password, PASSWORD_DEFAULT);
	
	$check = "SELECT UserID FROM cynthiasdb.users WHERE UserID = '$UserID';";
	$rows = $conn->query($check);
	if($rows->num_rows > 0){
		echo "Username already taken, try again";
		return;
	}

	$add_user = "INSERT INTO cynthiasdb.users VALUES('$UserID', '$date', 0, 0, '$password');";

	if($conn->query($add_user) == TRUE){
		echo "Successfully added. log in";
		echo "<a href=\"http://38.88.75.83/db/login.php\"> here </a>";
	}
	else {
		echo "error: " . $conn->error;
	}

	$createFolder = "SELECT Primarykey FROM cynthiasdb.users WHERE USERID = '$UserID';";
	$response = $conn->query($createFolder);
	$foldername = $response->fetch_assoc()['Primarykey'];
	echo $foldername;

	mkdir( "./$foldername", 0777, true);
	chmod("./$foldername", 0777); 
}
?>
	

