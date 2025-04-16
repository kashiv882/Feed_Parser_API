from fastapi import FastAPI
from database import engine, Base
from routers import auth, feedparser

# from . import auth as auth_route

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.route)
app.include_router(feedparser.route)










































# @app.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     # Check if user already exists
#     existing_user = db.query(User).filter(User.username == user.username).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already taken")

#     # Create new user
#     hashed_pw = hash_password(user.password)
#     new_user = User(username=user.username, hashed_password=hashed_pw)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User registered successfully"}


# @app.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     access_token = create_access_token(data={"sub": str(user.id)})
#     return {"access_token": access_token, "token_type": "bearer"}


# # Pydantic input model
# class FeedInput(BaseModel):
#     urls: List[str]
#     max_items: int = 5

# # Route to fetch and store RSS feeds

# @app.post("/fetch-feeds/")
# def fetch_feeds(feed_input: FeedInput, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     for url in feed_input.urls:
#         parsed_feed = feedparser.parse(url)

#         if not parsed_feed.entries:
#             continue

#         heading = parsed_feed.feed.get("title", "No Title")
#         domain = urlparse(url).netloc

#         # Check if source exists for the current user
#         source = db.query(FeedSource).filter(
#             FeedSource.url == url,
#             FeedSource.user_id == current_user.id
#         ).first()

#         if not source:
#             source = FeedSource(
#                 url=url,
#                 heading=heading,
#                 domain=domain,
#                 user_id=current_user.id  # ✅ assign source to user
#             )
#             db.add(source)
#             db.commit()
#             db.refresh(source)

#         # Add feed items (up to max_items)
#         for entry in parsed_feed.entries[:feed_input.max_items]:
#             title = entry.get("title", "No Title")
#             link = entry.get("link", "")
#             published = entry.get("published", "")

#             # Avoid duplicates
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


# @app.get("/dashboard/")
# def get_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     sources = db.query(FeedSource).filter(FeedSource.user_id == current_user.id).all()
#     dashboard = []

#     for source in sources:
#         # Get stored feed items (from DB)
#         stored_items = db.query(FeedItem).filter(
#             FeedItem.source_id == source.id
#         ).order_by(FeedItem.id.desc()).limit(3).all()

#         stored_data = [{
#             "title": item.title,
#             "link": item.link,
#             "published": item.published
#         } for item in stored_items]

#         # Get latest feed data live (from feedparser)
#         feed = feedparser.parse(source.url)
#         latest_data = []
#         if feed.entries:
#             latest = feed.entries[0]  # Only show latest
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


