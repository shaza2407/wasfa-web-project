document.addEventListener("DOMContentLoaded", function () {
    var signUpForm = document.getElementById("signupForm");
    var usernameInput = document.getElementById("username");
    var emailInput = document.getElementById("email");
    var passwordInput = document.getElementById("password");
    var confirmPasswordInput = document.getElementById("confirmPassword");

    signUpForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var username = usernameInput.value;
        var email = emailInput.value;
        var password = passwordInput.value;
        var confirmPassword = confirmPasswordInput.value;

        var warningElements = document.getElementsByClassName("warning");
        for (var i = 0; i < warningElements.length; i++) {
            warningElements[i].innerHTML = "";
        }

        if (username.trim() === "" || username.trim().length < 10) {
            document.getElementById("usernameWarning").innerHTML = `<p>The username must be at least 10 characters long.</p>`;
            return false;
        }
        

        // check validation of email must have (.) and one of ['net', 'org', 'edu', 'gov', 'com']
	    if (email.indexOf(".") === -1) {
		document.getElementById("emailWarning").innerHTML = `<p>Please enter a valid email address.</p>`;
            return false; 
	    }

	    var domain = email.split(".")[1];
	    var validDomains = ["net", "org", "edu", "gov", "com"];
	    if (validDomains.indexOf(domain) == -1) {
            document.getElementById("emailWarning").innerHTML = `<p>Please enter a valid email address.</p>`;
            return false;
        }

        if (password === "" || password.trim().length < 8) {
            document.getElementById("passwordWarning").innerHTML = `<p>The password must be at least 8 characters long.</p>`;
            return false;
        }

        if (password !== confirmPassword) {
            document.getElementById("confirmPasswordWarning").innerHTML = `<p>Passwords don't match.</p>`;
            return false;
        }

    });
});
