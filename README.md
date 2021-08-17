# Network
A social media platform that allows users to upload posts and interact with other users.

## Features
- Upload posts for others to see
- Explore a user's profile page and follow them to stay updated on all of their posts
- Like content from other users

## API Documentation
**`GET /posts`**: Get all posts

**`GET /posts/user/{username}`**: Get all posts from a user  
Path Parameters:
- **username** (required)
    - Type: string
    - Description: the user's username

**`GET /posts/user/{username}/following`**: Get all posts from the people a user follows  
Path Parameters:
- **username** (required)
    - Type: string
    - Description: the user's username

**`PUT /posts/{post_id}/update`**: Update a post  
Path Parameters:
- **post_id** (required)
    - Type: integer
    - Description: ID of the post  

Body Parameters:
- **content** (optional)
    - Type: string
    - Description: the post’s new content
- **like** (optional)
    - Type: boolean
    - Description: true = increment likes on post by 1, false = decrement likes on post by 1

**`POST /posts`**: Create a new post  
Body Parameters:
- **content** (required)
    - Type: string
    - Description: content of the post

**`GET /{username}`**: Get info about a user  
Path Parameters:
- **username** (required)
    - Type: string
    - Description: the user’s username

**`PUT /{username}`**: Update follow/following count for a user  
Path Parameters:
- **follow** (required)
    - Type: boolean
    - Description: true = follow user, false = unfollow user
- **user** (required)
    - Type: string
    - Description: the username of the user to follow/unfollow

## Inspiration
I created this project for CS50's Web Programming with Python and Javascript offered on edX. The premise behind this project was to develop a Twitter-like social network website for making posts and following users. (the full specifications for this project can be found [here](https://cs50.harvard.edu/web/2020/projects/4/network/)). From this project, I learned how to develop my own API.

## License
> You can check out the full license [here](https://github.com/TylerWon/network/blob/master/LICENSE)

This project is licensed under the terms of the MIT license. 
