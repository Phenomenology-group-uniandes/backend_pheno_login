from app import get_app

app = get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("__main__:app", port=8080, reload=True)
