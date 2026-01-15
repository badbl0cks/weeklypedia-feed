# Weeklypedia RSS Feed

An RSS feed generated from the [Weeklypedia](https://weekly.hatnote.com/) email archive.

Weeklypedia is "a list of the most edited Wikipedia articles and discussions from the last week" delivered every Friday.

## Setup

1. Create a new GitHub repository
2. Push this code to the repo
3. Enable GitHub Pages:
   - Go to Settings > Pages
   - Source: "Deploy from a branch"
   - Branch: `main`, folder: `/ (root)`
4. Run the workflow once manually (Actions > Update RSS Feed > Run workflow)

## Feed URL

Once deployed, your feed will be available at:

```
https://YOUR_USERNAME.github.io/REPO_NAME/feed.xml
```

## How it works

- `generate_feed.py` scrapes the Weeklypedia archive index
- Generates a standard RSS 2.0 `feed.xml`
- GitHub Actions runs weekly (Saturday 06:00 UTC) to catch Friday's release
- GitHub Pages serves the static XML file

## Manual update

Run locally:

```bash
python generate_feed.py
```

Or trigger the GitHub Action manually from the Actions tab.
