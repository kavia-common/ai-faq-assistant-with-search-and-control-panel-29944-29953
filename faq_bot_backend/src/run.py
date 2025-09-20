import uvicorn

if __name__ == "__main__":
    # Use default host/port; can be overridden via CLI in deployments
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)
