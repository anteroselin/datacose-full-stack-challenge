from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import authors, books, auth
from db.session import engine

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def create_app():
    app = FastAPI()

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(authors.router)
    app.include_router(books.router)

    return app


app = create_app()


@app.on_event("startup")
async def startup():
    # Perform database migrations on startup
    from db.base import Base

    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    # Clean up resources on shutdown if necessary
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
