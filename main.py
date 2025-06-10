import uvicorn

if __name__ == "__main__":
    # This command tells uvicorn:
    # "Look for a package named 'app' (the app/ folder), and inside its
    # __init__.py file, find the variable named 'app' (our FastAPI instance)."
    # reload=True is great for development as it restarts the server on code changes.
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)