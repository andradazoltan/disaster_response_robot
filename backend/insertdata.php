<br>
<h1> LOL! </h1>
<br>

<?php
$servername = "localhost";
$username = "charlesbai321";
$password = "pi1";
$dbname = "cynthiasdb";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
} 

$name = $_POST["petname"]; 
$species = $_POST["petspecies"];
$date = date("Y-m-d");
$sql = "INSERT INTO cynthiasdb.pet VALUES('$name', '$species', '$date');";

if($conn->query($sql) == TRUE){
	echo "successfully added";
}
else {
	echo "some sort of error occurred:" . $conn->error;
}

$conn->close();
?>

<html>
<p><a href="table.php">View Table</a></p>
<p><a href="info.php">Back</a></p>
</html>
