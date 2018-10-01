
<?php
$servername = "localhost";
$username = "charlesbai321";
$password = "pi1";
$dbname = "robot";

if(!isset($_POST['manual'])) return;

$conn = new mysqli($servername, $username, $password, $dbname);

if($conn->connect_error){
	die("Connection failed: " . $connn->connect_error);
}

$id = $_GET["id"];
$mode  = $_POST['manual']; 

$query = $conn->query("UPDATE ManualInfo SET manual = $mode WHERE robotID = $id;");

echo "done";

?>
