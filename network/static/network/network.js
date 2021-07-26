document.addEventListener("DOMContentLoaded", function() {
    // Create a new post when user submits new post form
    if (document.querySelector("#new-post-form") != null) {
        document.querySelector("#new-post-form").onsubmit = create_post;
    }

    show_posts();
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

    // Catch any errors and log them to console
    .catch(function(err) {
        console.log(err);
    })

    // Reset textarea
    document.querySelector("#new-post-content").value = "";

    // Load posts again so new post appears
    show_posts();

    // Prevent default submission
    return false;
}

/**
 * Displays posts on "all posts" page
 */
function show_posts() {
    // Retrieve posts
    fetch("/posts", {
        method: "GET"
    })

    // Convert response to json
    .then(function(response) {
        return response.json();
    })

    // Log response to console
    .then(function(response) {
        console.log(response);
        return response;
    })

    // Iterate through posts, adding them to the "all posts" page
    .then(function(posts) {
        posts.forEach(function(post) {
            show_post(post);
        })
    })

    // Catch any errors and log them console
    .catch(function(err) {
        console.log(err);
    })
}

/**
 * Displays a post on the "all posts" page
 * @param {object} post object that contains info about a post
 */
function show_post(post) {
    const post_div = document.createElement("div");
    
    post_div.className = "post-container";
    post_div.innerHTML = `
        <h6 class="post-poster">${post.poster}</h6>
        <p>${post.content}</p>
        <p class="post-timestamp">${post.timestamp}</p>
    `;

    document.querySelector("#posts-container").append(post_div);       
}