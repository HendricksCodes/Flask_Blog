import json
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


def generate_id():
    counter = 1
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
        if blog_posts:
            ids = [post.get('id', 0) for post in blog_posts]
            counter = max(ids) + 1
    return counter


# Function to fetch the blog posts from the JSON file
def fetch_blog_posts():
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    return blog_posts


# Function to save the updated blog posts to the JSON file
def save_blog_posts(blog_posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file)


@app.route('/')
def index():
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # generate post ID for new posts
        post_id = generate_id()

        # Create a new blog post dictionary
        new_post = {'id': post_id, 'author': author, 'title': title, 'content': content}

        # Load existing blog posts from JSON file
        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)

        # Append the new blog post to the existing list of blog posts
        blog_posts.append(new_post)

        # Save updated blog posts back to the JSON file
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=2)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Find blog post with ID and remove it
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save updated posts to JSON
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=1)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = fetch_blog_posts()

    # Find the blog post with the given post_id
    post = None
    for blog_post in blog_posts:
        if blog_post['id'] == post_id:
            post = blog_post
            break

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save the updated blog posts back to the JSON file
        save_blog_posts(blog_posts)

        # Redirect back to the index page
        return redirect(url_for('index'))

    # If it's a GET request, display the update.html page
    return render_template('update.html', post=post)


@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    # Fetch the blog posts from the JSON file
    blog_posts = fetch_blog_posts()

    # Find the blog post with the given ID
    post = None
    for blog_post in blog_posts:
        if blog_post['id'] == id:
            post = blog_post
            break

    if post is None:
        # Post not found
        return "Post not found", 404

    # Check if 'likes' key exists in the post dictionary
    if 'likes' not in post:
        post['likes'] = 0

    # Increment the likes count
    post['likes'] += 1

    # Save the updated blog posts back to the JSON file
    save_blog_posts(blog_posts)

    # Redirect back to the index page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
