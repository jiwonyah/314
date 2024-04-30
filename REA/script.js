document.getElementById("user-profile").addEventListener("change", function () {
    var selectedProfile = this.value;
    var usernameInput = document.getElementById("username");
    var passwordInput = document.getElementById("password");
    var loginButton = document.getElementById("loginButton");

    if (selectedProfile) {
        usernameInput.disabled = false;
        passwordInput.disabled = false;
        loginButton.disabled = false;
    } else {
        usernameInput.disabled = true;
        passwordInput.disabled = true;
        loginButton.disabled = true;
    }
});