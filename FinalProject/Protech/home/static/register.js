/**
 * Sends data to backend to register
 */
async function sendDataRegister(){
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    const email = document.getElementById('email').value;

    data_json = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'user_image': picture,
    }
    
    await fetch('http://localhost:8000/%2Fregister/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken")
        },
        credentials: 'same-origin',
        body: JSON.stringify(data_json)
    })
    .then((response) => response.json())
    .then((responseJSON) => {
        document.location.replace("/login_page");
    }).catch(err =>{
        document.location.replace("/error_page");
    });
}

/**
 * 
 * @param {string} name cookie name
 * @returns the csrf token or cookie value
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}