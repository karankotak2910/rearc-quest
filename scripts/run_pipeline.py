from src.ingest import run as ingest
from src.analytics import run as analytics


def main():
    ingest()
    analytics()


if __name__ == "__main__":
    main()