<?php
	$servername = "localhost";
	$username = "charlesbai321";
	$password = "pi1";
	$dbname = "cynthiasdb";

	$conn = new mysqli($servername, $username, $password, $dbname);

	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} 

	$result = mysqli_query($conn, "SELECT * FROM cynthiasdb.pet");

	echo "<table border='3'>
	<tr>
	<th>Pet Name</th>
	<th>Species</th>
	<th>Birthdate</th>
	</tr>";
	while ($row = mysqli_fetch_array($result)) {
		echo "<tr>";
		echo "<td>" . $row['petName'] . "</td>";
		echo "<td>" . $row['petSpecies'] . "</td>";
		echo "<td>" . $row['birthdate'] . "</td>";
		echo "</tr>";
	}
	echo "</table>";

	$conn->close();
?>

<html><p>
<a href="info.php">Back</a>
</p></html>
