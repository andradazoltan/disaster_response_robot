<?php
	if($handle = opendir("./Upload/Livestream")){
		while(false != ($file = readdir($handle))){
			if($file != "." && $file != ".."){
				$ret = array();
				$ret['photo'] = 'http://38.88.75.83/db/Upload/Livestream/'.$file;
				echo json_encode($ret, JSON_UNESCAPED_SLASHES);
				return; 
			}
		}
	}
	$ret = array();
	$ret['photo'] = 'hi';
	echo json_encode($ret, JSON_UNESCAPED_SLASHES);
?>
