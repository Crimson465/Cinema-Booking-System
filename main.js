/*
For setting the home page background as an image 
stretched across the screen
*/

var ready = (callback) => {
    if (document.readyState != "loading") callback();
    else document.addEventListener("DOMContentLoaded", callback);
}
ready(() => {
    document.querySelector(".header").style.height = window.innerHeight + "px";
})

// Login page  variables
var login_email = document.getElementById("login_email").value;
var login_password = document.getElementById("login_password").value;


// Register page variables
var name = document.get.getElementById("name").value;
var register_email = document.getElementById("register_email").value;
var register_password1 = document.getElementById("register_password1").value;
var register_password2 = document.getElementById("regiater_password2").value;

function register() {
    /* Push the name, email, and password variables to mySQL database */
}



document.getElementById("login-button").onclick = function () {

    print("Clicked")
    if (login_email === "admin" && login_password == "admin") {
        window.open("movies.html")

    }
}

/*function login() {
    // Verify credentials against database
    print("button clicked!")
    // Temporary admin login
    print(login_email)
    print(login_password)


}
*/

// function changeStatus() {
//     console.log('changeStatus being called...');
// }