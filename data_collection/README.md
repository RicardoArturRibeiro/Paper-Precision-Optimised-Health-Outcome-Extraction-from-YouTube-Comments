# Data Collection — Corpus Reconstruction

## Why Raw Data Is Not Included

The raw YouTube comment corpus **cannot be redistributed** in accordance with the [YouTube API Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service) (Section III.E.4), which prohibits bulk redistribution of API-sourced data.

However, the corpus can be reconstructed using the YouTube Data API v3 and the channel/video identifiers described below.

## Corpus Description

| Parameter | Value |
|-----------|-------|
| Total comments | 209,661 |
| Channels | 11 |
| Collection period | 2017–2024 |
| Language | English |
| Content domain | Metabolic health / Therapeutic Carbohydrate Restriction |

## Channels

The corpus was collected from the following 11 YouTube channels focused on metabolic health content:

| # | Channel Name | Approximate Comments |
|---|-------------|---------------------|
| 1 | Dr. Eric Berg DC | 20,000 |
| 2 | Dr. Ken D. Berry MD | 20,000 |
| 3 | Thomas DeLauer | 20,000 |
| 4 | Dr. Jason Fung | 20,000 |
| 5 | Dr. Sten Ekberg | 20,000 |
| 6 | Dr. Boz (Annette Bosworth MD) | 20,000 |
| 7 | High Intensity Health | 20,000 |
| 8 | Keto Connect | 19,661 |
| 9 | Diet Doctor | 10,000 |
| 10 | Dr. Pradip Jamnadas MD | 10,000 |
| 11 | What I've Learned | 10,000 |

**Note:** Comment counts are approximate. The actual number of retrievable comments may differ due to deleted comments, channel changes, or API availability.

## Reconstruction Steps

### 1. Obtain YouTube Data API v3 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **YouTube Data API v3**
4. Create an API key under Credentials

### 2. Retrieve Channel Video Lists

For each channel, retrieve all video IDs using the `search.list` or `channels.list` → `playlistItems.list` endpoints:

```python
import googleapiclient.discovery

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def get_channel_videos(channel_id, max_results=500):
    """Retrieve all video IDs for a channel."""
    # Get uploads playlist ID
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    
    uploads_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    videos = []
    next_page = None
    
    while True:
        playlist_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_id,
            maxResults=50,
            pageToken=next_page
        ).execute()
        
        for item in playlist_response["items"]:
            videos.append(item["contentDetails"]["videoId"])
        
        next_page = playlist_response.get("nextPageToken")
        if not next_page or len(videos) >= max_results:
            break
    
    return videos
```

### 3. Retrieve Comments

For each video, retrieve top-level comments using `commentThreads.list`:

```python
def get_video_comments(video_id, max_results=100):
    """Retrieve comments for a single video."""
    comments = []
    next_page = None
    
    while True:
        try:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                order="relevance",
                textFormat="plainText",
                pageToken=next_page
            ).execute()
            
            for item in response["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "video_id": video_id,
                    "comment_id": item["snippet"]["topLevelComment"]["id"],
                    "comment_text": snippet["textDisplay"],
                    "author": snippet["authorDisplayName"],
                    "published_at": snippet["publishedAt"],
                    "like_count": snippet["likeCount"]
                })
            
            next_page = response.get("nextPageToken")
            if not next_page or len(comments) >= max_results:
                break
                
        except Exception as e:
            print(f"Error for video {video_id}: {e}")
            break
    
    return comments
```

### 4. Apply Sampling

The study used a cap of 20,000 comments per channel for the top 8 channels and 10,000 for the remaining 3 channels. If a channel has more comments than the cap, apply random sampling:

```python
import pandas as pd

def apply_channel_caps(df, caps):
    """Apply per-channel comment caps with random sampling."""
    sampled = []
    for channel, cap in caps.items():
        channel_df = df[df["channel_name"] == channel]
        if len(channel_df) > cap:
            channel_df = channel_df.sample(n=cap, random_state=42)
        sampled.append(channel_df)
    return pd.concat(sampled, ignore_index=True)
```

### 5. Expected Output Format

The classification pipeline expects a CSV with (at minimum) these columns:

| Column | Type | Description |
|--------|------|-------------|
| `video_id` | String | YouTube video identifier |
| `channel_name` | String | Channel name |
| `comment_text` | String | Raw comment text |

## API Quota Notes

- The YouTube Data API v3 has a default quota of **10,000 units/day**
- `commentThreads.list` costs **1 unit** per call (100 comments per call)
- `playlistItems.list` costs **1 unit** per call (50 items per call)
- Retrieving ~210,000 comments will require approximately **2,100 API calls** — feasible within a single day's quota
- Consider implementing exponential backoff for rate limiting

## Contact

If you encounter issues reconstructing the corpus, please open a GitHub issue or contact the corresponding author.
