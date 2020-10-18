$(document).ready(function() {
    $("#arrowright").on("click", function() {
        var currImg = $(".visible");
        var nextImg = currImg.next();
        if (nextImg.length) // Run if next image exists
        {
            currImg.toggleClass("visible");
            nextImg.toggleClass("visible");
        }
        else {
            currImg.toggleClass("visible");
            $("#innerimages").children(":first").toggleClass("visible");
        }
    }); 

    $("#arrowleft").on("click", function() {
        var currImg = $(".visible");
        var prevImg = currImg.prev();
        if (prevImg.length) // Run if prev image exists
        {
            currImg.toggleClass("visible");
            prevImg.toggleClass("visible");
        }
        else {
            currImg.toggleClass("visible");
            $("#innerimages").children(":last").toggleClass("visible");
        }
    }); 
});