<?php
ini_set("display_errors", 1);

if(!isset($_FILES['photo'])) return;

# we're going to creat some variables that help us later on
$UploadName = $_FILES['photo']['name'];
#temporary file variable
$UploadTmp = $_FILES['photo']['tmp_name'];
$UploadType = $_FILES['photo']['type'];
# normalize the file name 

if(preg_match("*face*", $UploadName)){
	move_uploaded_file($UploadTmp, "Upload/Persons/$UploadName");
}
else {
	move_uploaded_file($UploadTmp, "Upload/Livestream/$UploadName");
}
?>

