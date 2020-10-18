$(document).ready(function() {

    function verifyEmail(event, email) {
        // Validates that the email follows the vailidation rules with regex
        var email_pattern = /^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,63}$/;

        if (!email_pattern.test(email)) {
            alert("Please enter a valid email");
            event.preventDefault();
            return false;
        }
        return true;
    }

    $("#login-form").submit(function(event) {
        verifyEmail(event, $("#login-form input[name='email']").val());
    });

    $("#reset-form").submit(function(event) {
        verifyEmail(event, $("#reset-form input[name='email']").val());
    });

    $("#signup-form").submit(function(event) {
        if (verifyEmail(event, $("#signup-form input[name='email']").val())) {
            var username = $("#signup-form input[name='username']").val();
            var password = $("#signup-form input[name='psw']").val();
            
            if (!/^\w{2,10}$/.test(username)) {
                alert("Username must be 2 to 10 alphanumeric characters");
                event.preventDefault();
                return;
            }

            if (!/^[\w\*\+\!\&]{8,20}$/.test(password)) {
                alert("Password must contain 8 to 20 alphanumeric characters or the following characters (*, +, !, &)");
                event.preventDefault();
                return;
            }

            if (password != $("#signup-form input[name='repsw']").val()) {
                alert("Password doesnt match reentered password");
                event.preventDefault();
                return;
            }
        }
    });

    $("#change-sign-up").click(function() {
        $("#login-con").toggleClass("on-top");
        $("#sign-up-con").toggleClass("on-top");
    });

    $("#change-reset").click(function() {
        $("#login-con").toggleClass("on-top");
        $("#reset-con").toggleClass("on-top");
    });

    $("#back-sign").click(function() {
        $("#login-con").toggleClass("on-top");
        $("#sign-up-con").toggleClass("on-top");
    });

    $("#back-reset").click(function() {
        $("#login-con").toggleClass("on-top");
        $("#reset-con").toggleClass("on-top");
    });

    $(".back-change").click(function() {
        $("#logged-con").toggleClass("on-top");
        $("#change-con").toggleClass("on-top");
    });


    $("#delete-account").submit(function(event) {
        var proceed = confirm("Are you sure you want to delete your account? this action is nonreversible");
        // User clicked cancel -> prevent submit
        if (!proceed) {
            event.preventDefault();
        }
    });

    $("#change-form").submit(function(event) {
        var curr_password = $("#change-form input[name='currpsw']").val();
        var new_password = $("#change-form input[name='newpsw']").val();


        if (!/^[\w\*\+\!\&]{8,20}$/.test(new_password) || !/^[\w\*\+\!\&]{8,20}$/.test(curr_password)) {
            alert("Password must contain 8 to 20 alphanumeric characters or the following characters (*, +, !, &)");
            event.preventDefault();
            return;
        }

        if (new_password != $("#change-form input[name='renewpsw']").val()) {
            alert("Password doesnt match reentered password");
            event.preventDefault();
            return;
        }
    });
});