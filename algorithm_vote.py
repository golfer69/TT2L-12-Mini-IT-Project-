from datetime import datetime, timedelta

def calculate_hidden_votes(posted_time, decay_rate=0.001):
    current_time = datetime.now()
    
    # Calculate the time difference in seconds
    time_difference = (current_time - posted_time).total_seconds()
    
    # Calculate hidden votes and round to the nearest whole number
    hidden_votes = round(time_difference * decay_rate)
    return hidden_votes

def main():
    # Example: Posted time (2 hours ago from now)
    posted_time = datetime.now() - timedelta(hours=2)

    decay_rate = 0.001  # This is the rate at which votes become hidden per second
    
    # Calculate hidden votes
    hidden_votes = calculate_hidden_votes(posted_time, decay_rate)
    
    print(f"Posted Time: {posted_time}")
    print(f"Decay Rate: {decay_rate} votes/second")
    print(f"Hidden Votes: {hidden_votes}")


if __name__ == "__main__":
    main()

