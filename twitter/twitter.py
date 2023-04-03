from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        while True:
            username = input("What would youlike your username to be: ")
            user = db_session.query(User).where(User.username == username).first()
            if(user != None):
                print("Username is already taken, try again")
            else:
                break
        
        while True:
            password = input("Please enter your password: ")
            password2 = input("Please re-enter your password to confirm: ") 
            
            if password != password2:
                print("These passwords do not match")
            else:
                break
                
        user = User(password = password, username = username)
        db_session.add(user)
        db_session.commit()
            
        


    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        username = input("Enter username: ")
        input_password = input("Password: ")
        user = db_session.query(User).where((User.username == username) & (User.password == input_password)).first()
        while user == None:
            print("Invalid username or password")
            username = input("Enter username: ")
            input_password = input("Password: ")
        self.current_user = user
        

    
    def logout(self):
        
        self.current_user = None
        self.end

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Welcome to ATCS Twitter\nPlease select a menu option:")
        option = int(input("1.Login \n2. Register User \n3. Exit\n" ))
        if option == 1:
            self.login()
        elif option == 2:
            self.register_user()
        elif option == 3:
            self.end()
        

    def follow(self):
        follow = input("Who would you like to follow? ")
        user = db_session.query(User).where(User.username == follow).first()
        check = db_session.query(Follower).where((Follower.follower_id == self.current_user.username) and (Follower.following_id == user.id)).first()
        if(check == None):
            follower = Follower(follower_id = self.current_user.username, following_id = user.username)
            db_session.add(follower)
            db_session.commit()
            print("You are now following @" + user.username)
        else:
            print("You already follow @" + user.username)


    def unfollow(self):
        unfollow = input("Who would you like to unfollow? ")
        user = db_session.query(Follower).where((Follower.follower_id == self.current_user.username) and (Follower.following_id == unfollow)).first()
        if(user == None):
            print("You don't follow " + user.username)
        else:
            db_session.delete(user)
            db_session.commit()
            print("You are no longer following @" + unfollow)

    
    
    def tweet(self):
        if self.current_user is None:
            print("You must be logged in to create a tweet.")
            return
        tweetContent = input("Create Tweet: ")
        tags = input("Enter your tags separated by spaces: ")
        newTweet = Tweet(content = tweetContent, username = self.current_user.username, timestamp = datetime.now())
        db_session.add(newTweet)
        db_session.commit()
        tweet = db_session.query(Tweet).where(Tweet.content == tweetContent).first()
        tweetID = tweet.id
        tags = tags.split()
        for i in tags:
            if db_session.query(Tag).where(Tag.content == i).first() == None:
                tag = Tag(content=i)
                db_session.add(tag)
                db_session.commit()
            else:
                tag = db_session.query(Tag).where(Tag.content == i).first()
                tweetTag = TweetTag(tag_id = tag.id, tweet_id = tweetID)
                db_session.add(tweetTag)
                db_session.commit()
        

        
    
    def view_my_tweets(self):
        tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username)
        self.print_tweets(tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        tweets = []
        for following in self.current_user.following:
            user_tweets = db_session.query(Tweet).where(Tweet.username == following.username).order_by(Tweet.timestamp.desc()).limit(5)
            tweets.extend(user_tweets)
        tweets.sort(reverse=True, key=lambda tweet: tweet.timestamp)
        self.print_tweets(tweets)


    def search_by_user(self):
        username = input("Enter username to search for: ")
        user = db_session.query(User).where(User.username == username).first()
        if user == None:
            print("There is no user by that name")
        else:
            user_tweets = db_session.query(Tweet).where(Tweet.username == username).all()
            self.print_tweets(user_tweets)


    def search_by_tag(self):
        tag = input("Enter tag to search for: ")
        tag = db_session.query(Tag).filter(Tag.content == tag).first()
        if tag != None:
            tweets_with_tag = db_session.query(Tweet).join(TweetTag).filter(TweetTag.tag_id == tag.id).all()    
            self.print_tweets(tweets_with_tag)
        else:
            print("There is no tag by that name")


    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        self.print_menu()
        option = int(input(""))

        if option == 1:
            self.view_feed()
        elif option == 2:
            self.view_my_tweets()
        elif option == 3:
            self.search_by_tag()
        elif option == 4:
            self.search_by_user()
        elif option == 5:
            self.tweet()
        elif option == 6:
            self.follow()
        elif option == 7:
            self.unfollow()
        else:
            self.logout()
        
        self.end()
