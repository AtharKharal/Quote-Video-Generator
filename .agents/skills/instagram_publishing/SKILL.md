---
description: Publish videos as Instagram Reels via Facebook Graph API
---

# Instagram Publishing Skill

## Purpose
Upload rendered MP4 videos as Instagram Reels with captions and hashtags. Uses GitHub as a CDN (uploads video to a GitHub repo, then provides the download URL to the Instagram API).

## Module
`execution/vid_publisher.py` — `VideoPublisher` class

## Usage
```python
from execution.vid_publisher import VideoPublisher

publisher = VideoPublisher(caption="Your caption here...", file_path="./output.mp4")
status_code = publisher.publish_video()
```

## Publishing Flow
1. **Upload to GitHub** — Base64-encodes the MP4 and pushes it to a GitHub repo via the GitHub API (acts as a public CDN)
2. **Create IG Container** — Sends the GitHub download URL to the Instagram Graph API to create a Reels media container
3. **Poll Status** — Polls every 5 seconds until the container status is `FINISHED`
4. **Publish** — Publishes the container to the Instagram feed

## Environment Variables
| Variable | Required | Description |
|---|---|---|
| `ACCESS_TOKEN` | **Yes** | Facebook Graph API long-lived access token |
| `BUSINESS_ACC_ID` | **Yes** | Instagram Business Account ID |
| `GITHUB_PAT` | **Yes** | GitHub Personal Access Token (for CDN uploads) |
| `GITHUB_REPO_PATH` | **Yes** | GitHub API path, e.g. `https://api.github.com/repos/USER/REPO/contents` |

## Important Notes
- **Token expiry**: Facebook access tokens expire every ~60 days. Refresh via [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- **Business account required**: The Instagram account must be a Business or Creator account connected to a Facebook Page
- **Video size**: Keep videos under 100MB for reliable uploads
- **GitHub CDN**: Videos are stored permanently in the GitHub repo — consider periodic cleanup
