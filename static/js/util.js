function validateForm() {
    var username = document.forms["RegisterForm"]["username"].value;
    var password1 = document.forms["RegisterForm"]["password1"].value;
    var password2 = document.forms["RegisterForm"]["password2"].value;
    var first_name = document.forms["RegisterForm"]["first_name"].value;
    var last_name = document.forms["RegisterForm"]["last_name"].value;
    var phone_number = document.forms["RegisterForm"]["phone_number"].value;
    var message = "";
    var isError = false;
    if (username == null || username == "") {
        message += "Username is blank, please fill in all required fields\n";
        isError = true;
    }
    if (password1 == null || password1 == "") {
        message += "Password is blank, please fill in all required fields\n";
        isError = true;
    }
    if (password2 == null || password2 == "") {
        message += "Confirm password is blank, please fill in all required fields\n";
        isError = true;
    }
    if (first_name == null || first_name == "") {
        message += "First name is blank, please fill in all required fields\n";
        isError = true;
    }
    if (last_name == null || last_name == "") {
        message += "Last name is blank, please fill in all required fields\n";
        isError = true;
    }
    if (phone_number == null || phone_number == "") {
        message += "Phone number is blank, please fill in all required fields\n";
        isError = true;
    }
    if (isError) {
        alert(message);
    }
    return !isError;
}

function validateRideRequest() {
    var dst_addr = document.forms["RideRequestForm"]["dst_addr"].value;
    var owner_desired_arrival_time = document.forms["RideRequestForm"]["owner_desired_arrival_time"].value;
    var num_passengers_owner_party = document.forms["RideRequestForm"]["num_passengers_owner_party"].value;
    console.log("here")
    console.log(num_passengers_owner_party)
    var message = "";
    var isError = false;
    if (dst_addr == null || dst_addr === "") {
        message += "Destination address is blank, please fill in all required fields\n";
        isError = true;
    }
    if (owner_desired_arrival_time == null || owner_desired_arrival_time === "") {
        message += "Desired arrival time is blank, please fill in all required fields\n";
        isError = true;
    }
    if (num_passengers_owner_party == null || num_passengers_owner_party === "") {
        message += "Number of passengers is blank, please fill in all required fields\n";
        isError = true;
    }
    if (isError) {
        alert(message)
    }
    return !isError;
}