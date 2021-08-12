document.addEventListener("DOMContentLoaded", function() {
    // Show all posts page only
    document.querySelector("#all-posts-page").style.display = "block";
    document.querySelector("#profile-page").style.display = "none";
    document.querySelector("#following-page").style.display = "none";

    // Show profile page when link is clicked
    if (document.querySelector("#profile-page-link") != null) {
        username = document.querySelector("#profile-page-link").innerHTML;
        document.querySelector("#profile-page-link").onclick = function()  {
            show_profile_page(username);
        }
    }

    // Show following page when link is clicked
    if (document.querySelector("#following-page-link") != null) {
        username = document.querySelector("#profile-page-link").innerHTML;
        document.querySelector("#following-page-link").onclick = function()  {
            show_following_page(username);
        }
    }

    // Create a new post when user submits new post form
    if (document.querySelector("#new-post-form") != null) {
        document.querySelector("#new-post-form").onsubmit = create_post;
    }

    show_posts("/posts", 1);
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
    document.querySelector("#following-page").style.display = "none";

    // Create a header that displays the user's username
    show_profile_page_header(username);

    // Show follow/unfollow button
    show_follow_or_unfollow_button(username);

    // Show follower/following count
    show_followers_and_following(username);

    // Show posts created by the user
    show_posts(`/posts/user/${username}`, 1);
}

/**
 * Displays the header (the user's username) for a user's profile page
 * @param {string} username the user's username
 */
function show_profile_page_header(username) {
    document.querySelector("#username-container").innerHTML = "";
    
    const h1 = document.createElement("h1");
    h1.className = "section-title";
    h1.innerHTML = username;
    document.querySelector("#username-container").append(h1);
}

/**
 * Displays a button to follow or unfollow a user
 * @param {string} user_to_follow_or_unfollow the user's username
 */
function show_follow_or_unfollow_button(user_to_follow_or_unfollow) {
    // If the user is viewing their own profile page, do not display follow/unfollow button
    const button = document.querySelector("#follow-or-unfollow-button");
    let logged_in_user;

    if (button == null) {
        return;
    } else {
        logged_in_user = button.dataset.user;

        if (user_to_follow_or_unfollow == logged_in_user) {
            button.style.display = "none";
            return;
        }
    }

    // Set button to follow or unfollow depending on if the logged in user is following the user to follow or unfollow
    fetch(`/${logged_in_user}`, {
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

    // Set button value (i.e. what the button displays) to "follow" or "unfollow"
    .then(function(response) {
        const logged_in_user_following_list = response["following"]

        if (following(user_to_follow_or_unfollow, logged_in_user_following_list)) {
            button.innerHTML = "unfollow";
        } else {
            button.innerHTML = "follow";
        }
    })

    // Add functionality to the button so user to follow or unfollow is followed/unfolowed when clicked
    .then(function() {
        button.onclick = function() {
            follow_or_unfollow_user(user_to_follow_or_unfollow, logged_in_user);
        }
    })

    // Catch any errors and log them to console
    .catch(function(err) {
        console.log(err);
    })
}

/**
 * Return true if a username is in users, otherwise return false
 * @param {string} username the username of a user
 * @param {array} users the names of various users
 * @returns {boolean}
 */
function following(username, users) {
    for (let i = 0; i < users.length; i++) {
        user = users[i];
        if (user == username) {
            return true;
        }
    }

    return false;
}

/**
 * Follow or unfollow a user
 * @param {string} user_to_follow_or_unfollow the user's username
 * @param {string} logged_in_user the username of the user that is logged in
 */
function follow_or_unfollow_user(user_to_follow_or_unfollow, logged_in_user) {
    // Determine if user should be followed or unfollowed
    let button = document.querySelector("#follow-or-unfollow-button");
    let follow;

    if (button.innerHTML == "follow") {
        follow = true;
    } else {
        follow = false;
    }

    // Follow/unfollow user
    fetch(`/${logged_in_user}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            follow: follow,
            user: user_to_follow_or_unfollow
        })
    })

    // Convert response to json
    .then(function(response) {
        return response.json();
    })

    // Log response to console
    .then(function(response) {
        console.log(response);
    })

    // Update button name
    .then(function() {
        if (follow) {
            button.innerHTML  = "unfollow";
        } else {
            button.innerHTML  = "follow";
        }
    })

    // Update followers/following count
    .then(function() {
        show_followers_and_following(user_to_follow_or_unfollow);
    })
    
    // Catch any errors and log them to console
    .catch(function(err) {
        console.log(err);
    })

    // Prevent default submission
    return false;
}

/**
 * Displays the number of followers a user has and the number of people a user follows on their profile page
 * @param {string} username the user's username
 */
function show_followers_and_following(username) {
    // Retrieve user info
    fetch(`/${username}`, {
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

    // Clear followers/following count, then add them to the page
    .then(function(response) {
        document.querySelector("#followers-and-following-container").innerHTML = "";
        show_followers_or_following(true, response["followers"].length);
        show_followers_or_following(false, response["following"].length);
    })

    // Catch any errors and log them to console
    .catch(function(err) {
        console.log(err);
    })
}

/**
 * Displays the number of followers a user has or the number of people a user follows on their profile page
 * @param {boolean} whichOne if true, display number of followers; otherwise display number of people a user follows 
 * @param {integer} count the number of people following a user or the number of people a user follows
 */
function show_followers_or_following(whichOne, count) {
    const div = document.createElement("div");
    let header;

    if (whichOne) {
        header = "followers";
    } else {
        header = "following";
    }

    div.id = `${header}-container`;
    div.innerHTML = `
        <h5 class="followers-or-following-header">${header}</h5>
        <p class="followers-or-following-count">${count}</p>
    `;

    document.querySelector("#followers-and-following-container").append(div);
}

/**
 * Displays a page of all the posts made by people a user follows
 * @param {string} username the user's username
 */
function show_following_page(username) {
    // Show following page only
    document.querySelector("#all-posts-page").style.display = "none";
    document.querySelector("#profile-page").style.display = "none";
    document.querySelector("#following-page").style.display = "block";
    
    // Show posts
    show_posts(`/posts/user/${username}/following`, 1)
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
        show_posts("/posts", 1);
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
 * Displays 10 posts
 * @param {string} route the "/posts" API route to use
 * @param {integer} group the group of 10 posts to display (ex. group = 1 = the first 10 posts, group = 2 = the next 10 posts, etc.)
 */
function show_posts(route, group) {
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

        const first = (group - 1) * 10  // index of the first post (in the group) in posts
        for (let i = first; i < posts.length && i < first + 10; i++) {
            show_post(route, group, posts[i]);
        }

        return Math.ceil(posts.length / 10);
    })

    // Display profile page when poster's username is clicked
    .then(function() {
        document.querySelectorAll(".post-poster").forEach(function(poster) {
            poster.onclick = function() {
                show_profile_page(poster.innerHTML);
            }
        })
    })

    // Clear old post navigation bar and display a new one if there is at least one group
    .then(function(num_groups) {
        document.querySelector("#post-navigation-options").innerHTML = "";

        if (num_groups > 0) {
            show_post_navigation_bar(route, num_groups, group);
        }
    })

    // Catch any errors and log them console
    .catch(function(err) {
        console.log(err);
    })
}

/**
 * Displays a post on a page
 * @param {string} route the "/posts" API route that was used to get the post's info
 * @param {integer} group the group of 10 posts that this post belongs to
 * @param {Object} post object that contains info about a post
 */
function show_post(route, group, post) {
    const post_div = document.createElement("div");
    
    post_div.className = "post-container";
    post_div.innerHTML = `
        <a class="post-poster" href="#">${post.poster}</a>
        <p>${post.content}</p>
        <p class="post-timestamp">${post.timestamp}</p>
    `;

    // Add link to the post that allows poster to edit the post 
    add_edit_link_to_post(route, group, post, post_div);

    document.querySelector("#posts").append(post_div);       
}

/**
 * Adds a link to a post that allows the poster to edit the post
 * @param {string} route the "/posts" API route that was used to get the post's info
 * @param {integer} group the group of 10 posts that this post belongs to
 * @param {Object} post object that contains info about a post
 * @param {Element} post_div HTML element that contains the post
 */
function add_edit_link_to_post(route, group, post, post_div) {
    if (document.querySelector("#profile-page-link") != null) {
        const logged_in_user = document.querySelector("#profile-page-link").innerHTML;

        if (logged_in_user == post.poster) {
            const edit_link = document.createElement("a");
            edit_link.id = "post-edit";
            edit_link.href = "#";
            edit_link.innerHTML = "edit";

            post_div.append(edit_link);

            // Add functionality to edit link
            edit_link.onclick = function (e) {
                e.preventDefault(); // Prevents window from scrolling automatically to the top
                edit_post(route, group, post, post_div);
            };
        }
    }
}

/**
 * Allows a user to edit a post
 * @param {string} route the "/posts" API route that was used to get the post's info
 * @param {integer} group the group of 10 posts that this post belongs to
 * @param {Object} post object that contains info about a post
 * @param {Element} post_div HTML element that contains the post
 */
function edit_post(route, group, post, post_div) {
    // Display a form that allows a user to edit a post's content
    post_div.innerHTML = `
        <a class="post-poster" href="#">${post.poster}</a>
        <form id="post-edit-form">
            <textarea id="post-edit-form-content">${post.content}</textarea>
            <input id="post-edit-form-save-button" class="btn btn-primary" type="submit" value="Save">
            <input id="post-edit-form-cancel-button" class="btn btn-secondary" type="submit" value="Cancel">
        </form>
        <p class="post-timestamp">${post.timestamp}</p>
    `

    // Save edits to a post when "save" button is clicked
    document.querySelector("#post-edit-form-save-button").onclick = function() {
        const new_content = document.querySelector("#post-edit-form-content").value;
        update_post_content(route, post.id, new_content);
    }

    // Cancel edits to a post when "cancel" button is clicked
    document.querySelector("#post-edit-form-cancel-button").onclick = function(e) {
        e.preventDefault(); // Prevents window from scrolling automatically to the top
        show_posts(route, group);
    }
}

/**
 * Updates the content of a post
 * @param {string} route the "/posts" API route that was used to get the post's info
 * @param {integer} id the id of the post
 * @param {string} content the post's new content
 */
function update_post_content(route, id, content) {
    // Update post
    fetch(`/posts/${id}/update`, {
        method: "PUT",
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
        show_posts(route, 1);
    })

    // Catch any errors and log them to console
    .catch(function(err) {
        console.log(err);
    })

    // Prevent default submission
    return false;
}

/**
 * Displays navigation bar that allows a user to move between groups of posts
 * @param {string} route the "/posts" API route to use
 * @param {integer} num_groups the number of groups of posts in total
 * @param {integer} group the group of 10 posts being displayed currently
 */
function show_post_navigation_bar(route, num_groups, group) {
    // Create "previous" button, disable if the first group of posts is being displayed
    create_post_navigation_bar_option("post-navigation-previous", "previous");
    if (group == 1) {
        document.querySelector("#post-navigation-previous").className = "page-item disabled";
    }

    // Create "group" buttons, set button of current group being displayed as active
    for (let i = 1; i <= num_groups; i++) {
        create_post_navigation_bar_option(`group-${i}`, `${i}`);

        if (i == group) {
            document.querySelector(`#group-${i}`).className = "page-item active";
        }
    }

    // Create "next" button, disable if the last group of posts is being displayed
    create_post_navigation_bar_option("post-navigation-next", "next");
    if (group == num_groups) {
        document.querySelector("#post-navigation-next").className = "page-item disabled";
    }

    // Add functionality to navigation bar
    document.querySelectorAll(".page-item").forEach(function(option) {
        // If option is "previous" and it is not disabled, show posts from the previous group when clicked
        if (option.id == "post-navigation-previous" && option.className == "page-item") {
            option.firstChild.onclick = function() {
                show_posts(route, group - 1);
            }
        }

        // Else if option is "next" and it is not disabled, show posts from the next group when clicked
        else if (option.id == "post-navigation-next" && option.className == "page-item") {
            option.firstChild.onclick = function() {
                show_posts(route, group + 1);
            }
        }

        // Else show posts from the group that was clicked
        else {
            const group_clicked = parseInt(option.firstChild.innerHTML);
            option.firstChild.onclick = function() {
                show_posts(route, group_clicked);
            }   
        }
    })
}

/**
 * Creates an option for the post navigation bar
 * @param {string} id the CSS id for the option
 * @param {string} name the name of the option
 */
function create_post_navigation_bar_option(id, name) {
    const option = document.createElement("li");

    option.id = id;
    option.className = "page-item";
    option.innerHTML = `<a class="page-link" href="#">${name}</a>`;

    document.querySelector("#post-navigation-options").append(option);
}