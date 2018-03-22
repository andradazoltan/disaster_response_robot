<?php
	session_start();
	
	$folder = $_SESSION["Primarykey"];

	if(isset($_FILES['uploadfile'])){
		$UploadName = $_FILES['uploadfile']['name'];
		$UploadTmp = $_FILES['uploadfile']['tmp_name'];
		#echo '<li><a href='.$UploadTmp.'> STUFF </a></li>';
		$UploadName = preg_replace("#[^a-z0-9.]#i", "", $UploadName);
		#echo $_FILES['uploadfile']['error'];
		#echo './'.$folder.'/'.$UploadName;
		move_uploaded_file($UploadTmp, "./$folder/$UploadName");
		#echo "$UploadTmp";
		#echo "$folder/$UploadName";
		#chmod("$folder/$UploadName", 0666);
	}
?>
