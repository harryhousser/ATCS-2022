"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")

    def __repr__(self):
        return "@" + self.username
class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

class Tweet(Base):
    # TODO: Complete the class
    __tablename__ = "tweet"

    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT, nullable=False)
    timestamp = Column('timestamp', DATETIME, nullable=False)
    username = Column('username', TEXT, ForeignKey('users.username'))
    tags = relationship("Tag", secondary="tweettags", back_populates="tags")
    
    def __init__(self, content, timestamp, username):
        self.content = content
        self.timestamp = timestamp
        self.username = username

    def __repr__(self):
        return "@" + self.username + "\n" + self.content + "\n" + self.tags + "\n" + self.timestamp

class Tag(Base):
    # TODO: Complete the class
    __tablename__ = "tag"

    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT)
    
    def __init__(self, content):
        self.content = content
    
    def __repr__(self):
        return "#" + self.content

class TweetTag(Base):
    # TODO: Complete the class
    __tablename__ = "tweettag"

    id = Column("id", INTEGER, primary_key=True)
    tweet_id = Column("tweet_id", INTEGER)
    tag_id = Column('tag_id', INTEGER)
    
    def __init__(self, content):
        self.content = content
    
    def __repr__(self):
        return "#" + self.content
    
