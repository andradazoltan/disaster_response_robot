<?php
	error_reporting(E_ALL);
	session_start();
	$folder = $_SESSION["Primarykey"];

	if(isset($_FILES['uploadfile'])){
		$UploadName = $_FILES['uploadfile']['name'];
		$UploadType = $_FILES['uploadfile']['type'];
		$UploadTmp = $_FILES['uploadfile']['tmp_name'];
		#echo '<li><a href='.$UploadTmp.'> STUFF </a></li>';
		$UploadName = preg_replace("#[^a-z0-9.]#i", "", $UploadName);
		#echo $_FILES['uploadfile']['error'] . "\n";
		#echo './'.$folder.'/'.$UploadName . "\n";
		
		if(!$UploadTmp){
			echo "no upload file selected";
		}
		else {
			move_uploaded_file($UploadTmp, "$folder/$UploadName");
			echo "DONE\n";
		}

		#echo "$UploadTmp";
		#echo "$folder/$UploadName";
		#chmod("$folder/$UploadName", 0666);
	}

	if($handle = opendir("./".$folder)){
	while (false != ($file = readdir($handle))) {
			if ($file != "." && $file != "..") {
				$thelist .= '<li><a href="'.$folder.'/'.$file.'">'.$file.'</a></li>';
			}
	    }
	}
	else {
		echo "Error opening stuff";
		echo $handle->error;
	}
?>	 

<h1>List of files:</h1>
<ul><?php echo $thelist; ?></ul>
<br><br>

<form action="display.php" method="post" enctype="multipart/form-data" name="uploadform" id="uploadform">
	Upload an Image: 
	<br>
	<label for="uploadfile"></label>
	<input type="file" name="uploadfile" id="uploadfile" />
	<input type="submit" name="submit" id="submit" value="Upload" />
</form>
