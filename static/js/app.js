function callGet() {
    fetch("/hello")
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseBox").textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById("responseBox").textContent = "Error: " + error;
        });
}

function callPost() {
    const payload = {
        user_input: document.getElementById("postData").value
    };

    fetch("/hello", {
        method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseBox").textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById("responseBox").textContent = "Error: " + error;
        });
}
