<?php

$servername = "localhost";
$username = "charlesbai321";
$password = "pi1";
$dbname = "robot";

$conn = new mysqli($servername, $username, $password, $dbname);


$id = (int)$_GET['id'];

$conn->query("delete from BeaconInfo where robotID = $id;");

$conn->query("delete from SearchInfo where robotID = $id;");

$conn->query("delete from LocationInfo where robotID = $id;");

$conn->query("delete from RobotInfo where id = $id;");

$conn->query("delete from GridInfo where robotID = $id;");

$conn->query("delete from ManualInfo where robotID = $id;");

echo "done";
