from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)  # Auth0 'sub' value (e.g., "auth0|abc123")
    feeds = relationship("FeedSource", back_populates="user", cascade="all, delete-orphan")


class FeedSource(Base):
    __tablename__ = "feed_sources"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)  # not unique anymore, same feed may be saved by multiple users
    heading = Column(String)
    domain = Column(String)

    user_id = Column(String, ForeignKey("users.id"))  # Link to Auth0 user
    user = relationship("User", back_populates="feeds")

    feeds = relationship("FeedItem", back_populates="source", cascade="all, delete-orphan")


class FeedItem(Base):
    __tablename__ = "feed_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    link = Column(String)  # not globally unique anymore
    published = Column(String)

    source_id = Column(Integer, ForeignKey("feed_sources.id"))
    source = relationship("FeedSource", back_populates="feeds")
