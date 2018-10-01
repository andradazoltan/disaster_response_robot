<html>
<center><h1> Log In </h1></center>
<br>
<br>

<center>
<form action="login.php" method="post">
	Username: <br>
	<input type="text" name="username"><br>
	Password: <br>
	<input type="text" name="password"><br>
	<br>
	<input type="submit" name="login" value ="Log In">
</form>
</center>
</html>

<?php
if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST["username"])){
	login();
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

	if($result->num_rows > 0){
		$userpass = $_POST["password"];

		while($row = $result->fetch_assoc()){
			if(password_verify($userpass, $row['password'])){
				$_SESSION["Primarykey"] = $row['Primarykey'];
				$key = $row['Primarykey'];
				header("Location: http://38.88.75.83/db/display.php");
				exit;
				return; 
			}
		}
		echo "password incorrect";
	}
	else {
		echo "UserName not taken. Do you want to ";
		echo "<a href=\"http://38.88.75.83/createuser.php\"> Create an account? </a>";
	}

	 
}

