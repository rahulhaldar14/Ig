from fastapi import FastAPI, Query
import instaloader
import os

app = FastAPI()
loader = instaloader.Instaloader(dirname_pattern="downloads")

# Load saved session
try:
    loader.load_session_from_file("yamdipxyz15")
except Exception as e:
    print("Session load failed:", e)
    try:
        loader.login("yamdipxyz15", "@seedhe_maut9880")
        loader.save_session_to_file()
    except Exception as login_error:
        print("Login failed:", login_error)

@app.get("/")
def root():
    return {"status": "API is x running"}

@app.get("/download")
def download_reel(url: str = Query(...)):
    try:
        shortcode = url.strip("/").split("/")[-1]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=post.owner_username)

        return {
            "success": True,
            "caption": post.caption[:120],
            "saved_to": f"downloads/{post.owner_username}/"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
