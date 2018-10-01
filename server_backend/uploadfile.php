<?php
	session_start();
	#$folder = $_SESSION["Primarykey"];
	$folder = 36;	

	$ret = array();
	if(isset($_FILES['uploaded-img'])){
		$UploadName = $_FILES['uploaded-img']['name'];
		$UploadType = $_FILES['uploaded-img']['type'];
		$UploadTmp = $_FILES['uploaded-img']['tmp_name'];
		
		if(!$UploadTmp){
			$ret['status'] = 'no file';
			echo json_encode($ret);
		}
		else {
			move_uploaded_file($UploadTmp, "$folder/$UploadName");
			$ret['status'] = 'done';
			echo json_encode($ret);
		}
	}
?>	 
