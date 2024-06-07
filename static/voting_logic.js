
function upvotePost(button) {
    const postId = button.dataset.postId;

    // Check if user has already upvoted
    fetch(`/check_vote/${postId}/upvote`, { method: 'GET' })
      .then(response => response.json())
      .then(data => {
        if (data.voted === true) {
          // User already upvoted, so send unvote request
          fetch(`/unvote/${postId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
              if (data.message === 'Vote removed successfully') {
                // Update vote count in the DOM
                const voteCountElement = document.getElementById(`vote-count-${postId}`);
                voteCountElement.textContent = data.votes;
                button.classList.remove('voted');
              } else {
                console.error('Unvote failed:', data.error);
              }
            })
            .catch(error => console.error('Error:', error));
        } else {
          // Send upvote request as before
          fetch(`/upvote/${postId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
              if (data.message === 'Upvoted successfully') {
                // Update vote count in the DOM
                const voteCountElement = document.getElementById(`vote-count-${postId}`);
                voteCountElement.textContent = data.votes;
                // Get the other button element
                const buttonSelector = `[data-vote-type="downvote"][data-post-id="${postId}"]`;
                const otherButton = document.querySelector(buttonSelector);
              
                // Remove the "voted" class from the downvote button
                otherButton.classList.remove('voted');
                button.classList.add('voted');
              } else {
                console.error('Upvote failed:', data.error);
              }
            })
            .catch(error => console.error('Error:', error));
        }
      })
      .catch(error => console.error('Error:', error));
  }


  function downvotePost(button) {
    const postId = button.dataset.postId;

    // Check if user has already downvoted
    fetch(`/check_vote/${postId}/downvote`, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.voted === true) {
                // User already downvoted, so send unvote request
                fetch(`/unvote/${postId}`, { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message === 'Vote removed successfully') {
                            // Update vote count in the DOM
                            const voteCountElement = document.getElementById(`vote-count-${postId}`);
                            voteCountElement.textContent = data.votes;
                            button.classList.remove('voted');
                        } else {
                            console.error('Unvote failed:', data.error);
                        }
                    })
                    .catch(error => console.error('Error:', error));
            } else {
              // Send downvote request as before
              fetch(`/downvote/${postId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                  if (data.message === 'Downvoted successfully') {
                    // Update vote count in the DOM
                    const voteCountElement = document.getElementById(`vote-count-${postId}`);
                    voteCountElement.textContent = data.votes;
                    const buttonSelector = `[data-vote-type="upvote"][data-post-id="${postId}"]`;
                    const otherButton = document.querySelector(buttonSelector);
              
                    // Remove the "voted" class from the upvote button
                    otherButton.classList.remove('voted');
                    button.classList.add('voted');
                  } else {
                    console.error('Downvote failed:', data.error);
                  }
                })
                .catch(error => console.error('Error:', error));
            }
        })
        .catch(error => console.error('Error:', error));
  }