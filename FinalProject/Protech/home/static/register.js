async function sendData(){
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    const email = document.getElementById('email').value;

    data_json = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'user-image': picture,
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
        return responseJSON;
    }).catch(err =>{
        return err;
    });
}

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