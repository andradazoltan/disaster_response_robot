<?php
	$pictures = array();
	if($handle = opendir("./Upload/Persons")){
		$i = 0;
		while(false != ($file = readdir($handle))){
			if($file != "." && $file != ".."){
				$ret[$i] = 'http://38.88.75.83/db/Upload/Persons/'.$file;
				$i++;
			}
		}
	}
	echo json_encode($ret, JSON_UNESCAPED_SLASHES);
?>
