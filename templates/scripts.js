// scripts.js
let voteCount = 0;

function vote(type) {
    if (type === 'upvote') {
        voteCount++;
    } else if (type === 'downvote') {
        voteCount--;
    }
    document.getElementById('voteCount').textContent = voteCount;
}
