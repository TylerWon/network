document.addEventListener("DOMContentLoaded", function() {
    // Show all posts page only initially
    document.querySelector("#all-posts-page").style.display = "block";
    document.querySelector("#profile-page").style.display = "none";

    // Show profile page when link is clicked
    if (document.querySelector("#profile-page-link") != null) {
        username = document.querySelector("#profile-page-link").innerHTML;
        document.querySelector("#profile-page-link").onclick = function()  {
            show_profile_page(username);
        }
    }

    // Create a new post when user submits new post form
    if (document.querySelector("#new-post-form") != null) {
        document.querySelector("#new-post-form").onsubmit = create_post;
    }

    show_posts("/posts");
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
 * Displays a user's profile page
 * @param {string} username the user's username 
 */
function show_profile_page(username) {
    // Show profile page only
    document.querySelector("#all-posts-page").style.display = "none";
    document.querySelector("#profile-page").style.display = "block";

    // Create header that displays the user's username
    const h1 = document.createElement("h1");
    h1.innerHTML = `<h1 class="section-title">${username}</h1>`;
    document.querySelector("#profile-page").append(h1);

    // Show follower/following count


    // Show posts created by the user
    show_posts(`/posts/${username}`);
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

    // Load posts again so new post appears
    .then(function() {
        show_posts("/posts");
    })

    // Catch any errors and log them to console
    .catch(function(err) {
        console.log(err);
    })

    // Reset textarea
    document.querySelector("#new-post-content").value = "";

    // Prevent default submission
    return false;
}

/**
 * Displays posts on a page
 * @param {string} route the API route to use
 */
function show_posts(route) {
    // Retrieve posts
    fetch(route, {
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

    // Clear posts that are being displayed then iterate through posts, adding them to the page
    .then(function(posts) {
        document.querySelector("#posts").innerHTML = "";
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
 * Displays a post on a page
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

    document.querySelector("#posts").append(post_div);       
}