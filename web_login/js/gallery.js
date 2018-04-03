var photoArr = ["IMG_0742.jpg", "IMG_0742.jpg", "IMG_0742.jpg"];

window.onload = setupGallery();


// function getPhotos(){
//     $.ajax({
//         type: 'GET',
//         url: 'https://jsonplaceholder.typicode.com/posts',
//         data: {
//             format: 'json'
//         },
//         success: function(data) {
//             console.log("sucessfully got photos");
//             console.log(data);
//             parseData(data);

//         },
//         error: function(data) {
//             console.log("error getting data");
//         },
//     });
// }

// function parseData(data){

//     var obj = JSON.parse(data);
//     console.log(obj);
// }

function setupGallery(){
    for (var i = 0; i < photoArr.length; i++) {
        var div = document.querySelector('.container-login100');

        var imageDiv = document.createElement('div');
        imageDiv.className = "wrap-login100 m-t-15 m-b-15 p-l-55 p-r-55 p-t-40 p-b-30";

        var img = document.createElement('img');
        img.className = 'list-img';
        img.src = photoArr[i];

        var title = document.createElement('div');
        title.className = 'home-page-label m-t-15';
        title.textContent = "Status: ";
        var span = document.createElement('span');
        span.className = "home-page-text";
        span.textContent += "No similar faces found";

        title.appendChild(span);
        imageDiv.appendChild(img);
        imageDiv.appendChild(title);
        div.appendChild(imageDiv);
    }
}
