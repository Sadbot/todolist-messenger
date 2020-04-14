import logging

from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session, logger: logging.Logger = None):
        self.db: Session = db
        self.logger = logger or logging.getLogger()
