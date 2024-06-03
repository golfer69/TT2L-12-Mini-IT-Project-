from datetime import datetime, timedelta

# Function to calculate hidden votes
def calculate_hidden_votes(posted_time, decay_rate):
    # Get the current time
    current_time = datetime.now()
    
    # Calculate the time difference in seconds
    time_difference = (current_time - posted_time).total_seconds()
    
    # Calculate hidden votes
    hidden_votes = time_difference * decay_rate
    
    return hidden_votes

# Example usage
# Posted time (for example, 2 hours ago from now)
posted_time = datetime.now() - timedelta(hours=2)

# Decay rate (example value)
decay_rate = 0.001  # This is the rate at which votes become hidden per second

# Calculate hidden votes
hidden_votes = calculate_hidden_votes(posted_time, decay_rate)
print(f"Hidden Votes: {hidden_votes}")
