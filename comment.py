Post_Comment:
def __init__(self,text,author):
    self.text = text 
    self.author = author
    self.reply = []

def add_reply(self,reply):
    """Add a reply to this comment.""" 
    self.reply.append(reply)

def display(self,indent=0):
    """Display the comment and reply."""
    print(""*indent + f"{self.author}:{self.text}")
    for reply in self.reply:
        reply.display(indent + 1)

# Example usage in comments:
top_comment = Post_Comment("This is the top comment.","user1")
reply1 = Post_Comment("Reply to top comment.", "user2")
reply2 = Post_Comment("Another reply to top comment.", "user 3")
reply3 = Post_Comment("A reply to the first reply.", "user4")

top_comment.add.reply(reply1)
top_comment.add_reply(reply2)
reply1.add_reply(reply3)

print("Comments:")
top_comment.display()


# Create vote
# Create reply 
# Create share
# Add timestamps
# Add user authentication 