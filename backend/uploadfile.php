<head>

<style>
.fileuploadholder{
	width:400px;
	height:200px;
	margin:60px auto 0px auto;
}
</style>

<body>
<div class="fileuploadholder" style="background-color:lightblue">
	<!--post vs get, action is what runs when it clicks, enctype is for multimedia files,-->
	<form action="uploadfile2.php" method="post" enctype="multipart/form-data" name="FileUploadForm" id="FileUploadForm">
		<label for="UploadFileField"></label>
		<!-- this has type file, so I can just access it straight from php with the name parameter -->
		<input type="file" name="UploadFileField" id="UploadFileField" />
		<input type="submit" name="UploadButton" id="UploadButton" value="Upload" />
</div>
</body>
