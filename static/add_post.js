function addPost() {
    const container = document.getElementById('posts-container');

    const newPost = document.createElement('div');
    newPost.classList.add('post-entry');

    newPost.innerHTML = `
        <label><p></p></label>
        <label for="username">Username:</label>
        <input type="text" name="username[]" required><br>

        <label for="social_media">Social Media Platform:</label>
        <input type="text" name="social_media[]" required><br>

        <label for="time_posted">Time Posted:</label>
        <input type="datetime-local" name="time_posted[]" required>
        <br><br>

        <button type="button" onclick="removePost(this)">Remove</button><br><br>
    `;

    container.appendChild(newPost);
    renumberPosts();
}

function renumberPosts() {
    const posts = document.querySelectorAll('.post-entry');
    posts.forEach((post, index) => {
      const label = post.querySelector('label p');
      label.textContent = `Post ${index + 1}`;
    });
  }

function removePost(button) {
    button.parentElement.remove();
    renumberPosts();
}

window.onload = function() {
    addPost();
};