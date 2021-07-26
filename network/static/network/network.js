document.addEventListener("DOMContentLoaded", function() {
    // Create a new post when user submits new post form
    if (document.querySelector("#new-post-form") != null) {
        document.querySelector("#new-post-form").onsubmit = create_post;
    }
})

const csrftoken = getCookie("csrftoken");

/**
 * Get a cookie (implementation from: https://docs.djangoproject.com/en/3.2/ref/csrf/)
 * @param {string} name name of the cookie
 * @returns the cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Creates a new post
 */
function create_post() {
    const content = document.querySelector("#new-post-content").value;

    // Create post
    fetch("/posts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            content: content
        })
    })

    // Convert response to json
    .then(function(response) {
        return response.json();
    })

    // Log response to console
    .then(function(response) {
        window.alert(response.message);
        console.log(response);
    })

    // Reset textarea
    .then(function() {
        document.querySelector("#new-post-content").value = "";
    })

    // Catch any errors and log them to console
    .catch(function(err) {
        console.log(err);
    })

    // Prevent default submission
    return false;
}