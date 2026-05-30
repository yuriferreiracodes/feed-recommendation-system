from fastapi import FastAPI

app = FastAPI(
    title="Feed Recommendation System",
    description="A personalized feed recommendation system.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
