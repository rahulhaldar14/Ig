from fastapi import FastAPI, Query
import instaloader
import os

app = FastAPI()
loader = instaloader.Instaloader(dirname_pattern="downloads")

@app.get("/")
def root():
    return {"status": "Instaloader API Running"}

@app.get("/download")
def download_reel(url: str = Query(...)):
    try:
        shortcode = url.strip("/").split("/")[-1]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=post.owner_username)

        return {
            "success": True,
            "video_description": post.caption[:100] if post.caption else "No caption",
            "saved_to": f"downloads/{post.owner_username}/"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
