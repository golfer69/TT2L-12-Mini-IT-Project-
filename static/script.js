document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.upvote').forEach(button => {
        button.addEventListener('click', () => {
            const postElement = button.closest('.post');
            const postId = postElement.dataset.id;
            vote(postId, 'upvote', postElement);
        });
    });

    document.querySelectorAll('.downvote').forEach(button => {
        button.addEventListener('click', () => {
            const postElement = button.closest('.post');
            const postId = postElement.dataset.id;
            vote(postId, 'downvote', postElement);
        });
    });

    function vote(postId, voteType, postElement) {
        fetch('/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ post_id: postId, vote_type: voteType })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                postElement.querySelector('.upvotes').textContent = data.post.upvotes;
                postElement.querySelector('.downvotes').textContent = data.post.downvotes;
            }
        });
    }
});
