close =document.getElementById("close");
if (close){
close.addEventListener("click", function(){pywebview.api.quit()});}
minz = document.getElementById("minimize");
if(minz){
minz.addEventListener("click", function(){pywebview.api.min()});
}

scn_fold = document.getElementById("scan_folder");
if (scn_fold != null){
scn_fold.addEventListener("click", function(){pywebview.api.selectfolder().then(function(response){
	if (response == 1){
		swal({
		  title: "Error!",
		  text: "Please Select a Folder",
		  icon: "error",
		  button: "Return",
		});
	}
})});
}

scn_drv = document.getElementById("scan_drive");
if (scn_drv){
	scn_drv.addEventListener("click", function(){pywebview.api.querydrive()});
}
