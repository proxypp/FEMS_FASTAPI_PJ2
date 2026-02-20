import uvicorn

from fems_fastApi.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    ssl_kwargs: dict = {}
    if settings.ssl_certfile and settings.ssl_keyfile:
        ssl_kwargs["ssl_certfile"] = settings.ssl_certfile
        ssl_kwargs["ssl_keyfile"] = settings.ssl_keyfile

    uvicorn.run(
        "fems_fastApi.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
        **ssl_kwargs,
    )


if __name__ == "__main__":
    main()
