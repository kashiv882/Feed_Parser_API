
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from urllib.parse import urlparse
import feedparser
from database import get_db
from models import FeedSource, FeedItem, User
from schemas import UserClaims
from routers.auth import validate_token

route = APIRouter()

class FeedInput(BaseModel):
    urls: List[str]
    max_items: int = 5

def get_or_create_user(
    current_user: UserClaims = Depends(validate_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.sub).first()

    if not user:
        user = User(id=current_user.sub)
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


@route.post("/fetch/")
def fetch_feeds(
    feed_input: FeedInput,
    db: Session = Depends(get_db),
    user: User = Depends(get_or_create_user)
):
    for url in feed_input.urls:
        parsed_feed = feedparser.parse(url)
        if not parsed_feed.entries:
            continue

        heading = parsed_feed.feed.get("title", "No Title")
        domain = urlparse(url).netloc

        source = db.query(FeedSource).filter(
            FeedSource.url == url,
            FeedSource.user_id == user.id
        ).first()

        if not source:
            source = FeedSource(
                url=url,
                heading=heading,
                domain=domain,
                user_id=user.id
            )
            db.add(source)
            db.commit()
            db.refresh(source)

        for entry in parsed_feed.entries[:feed_input.max_items]:
            title = entry.get("title", "No Title")
            link = entry.get("link", "")
            published = entry.get("published", "")

            exists = db.query(FeedItem).filter(
                FeedItem.link == link,
                FeedItem.source_id == source.id
            ).first()
            if exists:
                continue

            feed_item = FeedItem(
                title=title,
                link=link,
                published=published,
                source_id=source.id
            )
            db.add(feed_item)

        db.commit()

    return {"message": "Feeds fetched and stored successfully."}




@route.get("/dashboard/")
def get_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(get_or_create_user)
):
    sources = db.query(FeedSource).filter(FeedSource.user_id == user.id).all()
    dashboard = []

    for source in sources:
        stored_items = db.query(FeedItem).filter(
            FeedItem.source_id == source.id
        ).order_by(FeedItem.id.desc()).limit(3).all()

        stored_data = [{
            "title": item.title,
            "link": item.link,
            "published": item.published
        } for item in stored_items]

        feed = feedparser.parse(source.url)
        latest_data = []
        if feed.entries:
            latest = feed.entries[0]
            latest_data.append({
                "title": latest.get("title", "No Title"),
                "link": latest.get("link", ""),
                "published": latest.get("published", "Unknown")
            })

        dashboard.append({
            "source": {
                "heading": source.heading,
                "domain": source.domain,
                "url": source.url,
            },
            "stored_data": stored_data,
            "latest_data": latest_data
        })

    return dashboard





# @route.post("/fetch/")
# def fetch_feeds(
#     feed_input: FeedInput,
#     db: Session = Depends(get_db),
#     current_user: UserClaims = Depends(validate_token)
# ):
#     for url in feed_input.urls:
#         parsed_feed = feedparser.parse(url)
#         if not parsed_feed.entries:
#             continue

#         heading = parsed_feed.feed.get("title", "No Title")
#         domain = urlparse(url).netloc

#         source = db.query(FeedSource).filter(
#             FeedSource.url == url,
#             FeedSource.user_id == current_user.sub
#         ).first()

#         if not source:
#             source = FeedSource(
#                 url=url,
#                 heading=heading,
#                 domain=domain,
#                 user_id=current_user.sub
#             )
#             db.add(source)
#             db.commit()
#             db.refresh(source)

#         for entry in parsed_feed.entries[:feed_input.max_items]:
#             title = entry.get("title", "No Title")
#             link = entry.get("link", "")
#             published = entry.get("published", "")

#             exists = db.query(FeedItem).filter(
#                 FeedItem.link == link,
#                 FeedItem.source_id == source.id
#             ).first()
#             if exists:
#                 continue

#             feed_item = FeedItem(
#                 title=title,
#                 link=link,
#                 published=published,
#                 source_id=source.id
#             )
#             db.add(feed_item)

#         db.commit()

#     return {"message": "Feeds fetched and stored successfully."}


























# @route.get("/dashboard/")
# def get_dashboard(
#     db: Session = Depends(get_db),
#     current_user: UserClaims = Depends(validate_token)
# ):
#     sources = db.query(FeedSource).filter(FeedSource.user_id == current_user.sub).all()
#     dashboard = []

#     for source in sources:
#         stored_items = db.query(FeedItem).filter(
#             FeedItem.source_id == source.id
#         ).order_by(FeedItem.id.desc()).limit(3).all()

#         stored_data = [{
#             "title": item.title,
#             "link": item.link,
#             "published": item.published
#         } for item in stored_items]

#         feed = feedparser.parse(source.url)
#         latest_data = []
#         if feed.entries:
#             latest = feed.entries[0]
#             latest_data.append({
#                 "title": latest.get("title", "No Title"),
#                 "link": latest.get("link", ""),
#                 "published": latest.get("published", "Unknown")
#             })

#         dashboard.append({
#             "source": {
#                 "heading": source.heading,
#                 "domain": source.domain,
#                 "url": source.url,
#             },
#             "stored_data": stored_data,
#             "latest_data": latest_data
#         })

#     return dashboard
