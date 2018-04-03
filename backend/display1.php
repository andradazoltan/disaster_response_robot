<?php
	session_start();

	#$folder = $_SESSION["Primarykey"];
	#for testing purposes
	$folder = $_POST["folder"];

	$pictures = array();

	if($handle = opendir("./".$folder)){
		$i = 0;
		while(false != ($file = readdir($handle))){
			if($file != "." && $file != ".."){
				$pictures[$i] = 'http://38.88.75.83/db/'.$folder.'/'.$file;
				$i++;
			}
		}
	}

	echo json_encode($pictures, JSON_UNESCAPED_SLASHES);
?>
