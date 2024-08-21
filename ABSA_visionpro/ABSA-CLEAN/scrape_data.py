import praw
import pandas as pd

# Reddit API credentials
client_id = 'P-srExWsH5G50JyBvf-edQ'
client_secret = 'AQ0ntp3mH8TbvTPf0OC19bbgkz0j7Q'
user_agent = 'sentiment-analysis:v1.0 (by u/Longjumping_Ad3881)'

# Initialize PRAW
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Keywords list
keywords = [
    "Apple Vision Pro", "Vision Pro", "Apple AR headset", "Apple VR technology",
    "Vision Pro features", "Vision Pro AR", "Vision Pro VR", "Vision Pro gaming",
    "Vision Pro entertainment", "Vision Pro productivity", "Vision Pro augmented reality",
    "Vision Pro virtual reality", "Vision Pro vs Meta Quest", "Vision Pro vs Hololens",
    "Apple Vision Pro comparison", "best AR headset", "best VR headset", "Vision Pro release",
    "Vision Pro launch", "Apple Vision Pro announcement", "Vision Pro specifications",
    "Vision Pro battery life", "Vision Pro display technology", "Apple Vision Pro review",
    "Vision Pro first impressions", "Vision Pro hands-on", "Apple Vision Pro unboxing"
]

# Function to scrape Reddit globally
def scrape_reddit(query, limit_per_query):
    posts = reddit.subreddit('all').search(query, limit=limit_per_query)

    posts_list = []
    for post in posts:
        if post.selftext:  # Ensure the text field is not empty
            posts_list.append(
                [post.title, post.selftext, post.score, post.id, post.subreddit, post.url, post.num_comments, post.created])

    return pd.DataFrame(posts_list,
                        columns=['Title', 'Text', 'Score', 'ID', 'Subreddit', 'URL', 'Num_Comments', 'Created'])

# Initialize an empty DataFrame to store all results
all_posts = pd.DataFrame()

# Define the initial limit per keyword
limit_per_keyword = 500

# Scrape data for each keyword
for keyword in keywords:
    df = scrape_reddit(keyword, limit_per_keyword)
    all_posts = pd.concat([all_posts, df], ignore_index=True)

    # If collected posts are still under the desired count, increase the limit dynamically
    if len(all_posts) < 10000 and len(df) < limit_per_keyword:
        additional_df = scrape_reddit(keyword, limit_per_keyword)  # Re-fetch with the same limit
        all_posts = pd.concat([all_posts, additional_df], ignore_index=True)
        if len(all_posts) >= 10000:
            break  # Break the loop if we have collected enough data

# Check if minimum row requirement is met
if len(all_posts) < 10000:
    print(f"Warning: Only {len(all_posts)} posts scraped, which is less than the desired 10,000 rows.")

# Save to CSV
all_posts.to_csv('reddit_global_vision_pro_reviews_with_text.csv', index=False)

print("Scraped data saved to reddit_global_vision_pro_reviews_with_text.csv")
