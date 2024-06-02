// Example data structure
let posts = [
    { id: 1, title: "Post 1", upvotes: 0, downvotes: 0, score: 0 },
    { id: 2, title: "Post 2", upvotes: 0, downvotes: 0, score: 0 }
  ];
  
  let userVotes = {
    user1: { 1: 0, 2: 0 },  // 0 = no vote, 1 = upvote, -1 = downvote
    user2: { 1: 0, 2: 0 }
  };

  
  function castVote(userId, postId, vote) {
    if (!userVotes[userId] || !posts.find(post => post.id === postId)) {
      console.log("Invalid user or post");
      return;
    }
  
    let post = posts.find(post => post.id === postId);
    let currentVote = userVotes[userId][postId];
  
    if (vote === 1) {  // upvote
      if (currentVote === 1) {
        console.log("User already upvoted this post");
        return;
      } else if (currentVote === -1) {
        post.downvotes--;
      }
      post.upvotes++;
    } else if (vote === -1) {  // downvote
      if (currentVote === -1) {
        console.log("User already downvoted this post");
        return;
      } else if (currentVote === 1) {
        post.upvotes--;
      }
      post.downvotes++;
    } else {
      console.log("Invalid vote");
      return;
    }
  
    userVotes[userId][postId] = vote;
    post.score = post.upvotes - post.downvotes;
    console.log(`User ${userId} voted on post ${postId}. New score: ${post.score}`);
  }

  
// Simulating votes
castVote('user1', 1, 1);  // user1 upvotes post 1
castVote('user1', 2, -1); // user1 downvotes post 2
castVote('user2', 1, 1);  // user2 upvotes post 1
castVote('user1', 1, -1); // user1 changes vote to downvote post 1
castVote('user2', 2, 1);  // user2 upvotes post 2
castVote('user1', 2, 1);  // user1 changes vote to upvote post 2

// Display final post scores
console.log(posts);
