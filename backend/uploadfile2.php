<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

if(isset($_FILES['UploadFileField'])){
	 # we're going to creat some variables that help us later on
	 $UploadName = $_FILES['UploadFileField']['name'];
	 #temporary file variable
	 $UploadTmp = $_FILES['UploadFileField']['tmp_name'];
	 $UploadType = $_FILES['UploadFileField']['type'];
	 # normalize the file name 
	 $UploadName = preg_replace("#[^a-z0-9.]#i", "", $UploadName);

	 if(!$UploadTmp){
		 die("No file selected");
		 echo "wWHAT HAPPENED NOOO";
     }
     else{
		move_uploaded_file($UploadTmp, "Upload/$UploadName");
		echo "OK I'M DONE~";
	}
}
else {
	echo "What could not find file??";
}

?>

