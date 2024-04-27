# Create comment
class Post:
    def __init__(self,content,author):
        self.content = content
        self.author = author
        self.comments = {}

    def add_comment(self,comment):
        self.comments.append(comment)

class Comment:
    def __init__(self,text,author):
        self.text = text
        self.author = author

class Reddit: 
     def __init__(self):
          self.post = {}

     def add_post(self,post):
          self.post.append(Post)

     def display_post(self):
          for idx, post in enumerate(self.post, start=1):
               print(f"Post {idx}:")
               print(f"Author: {post.author}")
               print(f"Content: {post.content}")
               print ("Comment:")
               for comment in post.comment:
                    print(f"- {comment.author}:{comment.text}")
               print()
def main():
        mmu_reddit = Reddit()

        #Create post 
        new_post = Post('This is my 1st post','user1')
        
        #Add comments to the post
        new_post.add_comment(Comment("This is the 1st comment.", 'user2'))

        #Allow users to add comments
        while True:
            new_comment = input("\nEnter your comment(or enter 'exit' to quit to comment):")
            if new_comment.lower() == 'exit':
                break
            Post.add_comment(new_comment)

        # Add post to MMU Reddit
        mmu_reddit.add_post(new_post)

        # Display the post with comments
        mmu_reddit.display_post()
        
if __name__ == "__main__":
        main()

# Add timestamps
import datetime
current_timestamp = datetime.now()
timestamp_str = '27/4/2024 11:05'
timestamp_obj = datetime.datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M')
print(current_timestamp) 
print(timestamp_obj)
# If need to add 1 day to the current timestamp
one_day_delta = datetime.timedelta(days=1)
new_timestamp = current_timestamp + one_day_delta
print(new_timestamp)

# Example of comments
new_comment = Comment(content= 'Amazing!', current_timestamps= datetime.now())
