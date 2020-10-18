var last_rating, curr_rating;

$(document).ready(function() {
    
    db_rating = $(".stars-con .checked").length;
    curr_rating = db_rating;

    $(".stars-con .fa-star").click(function() {
        if ($(this).hasClass("checked") && $(this).is($(".stars-con .checked:last"))) {
            $(".stars-con").children().removeClass("checked");
            curr_rating = 0;
        }
        else {
            $(this).nextAll().removeClass("checked");
            $(this).prevAll().addClass("checked");
            $(this).addClass("checked");
            curr_rating = $(".stars-con .checked").length;
        }
    });

    $("#rating-save").click(function() {
        if (curr_rating != db_rating) {
            $.ajax({
                 url: window.location.href,
                 type: "POST",
                 data: JSON.stringify({recipe_rate: curr_rating}), 
                 dataType: "json",
                 contentType: "application/json; charset=utf-8"
            })
            .done(function() {
                db_rating = curr_rating;
                alert("Rating updated!");
            })
            .fail(function() {
                alert("An error occurred!");
            });
        }
    });
});