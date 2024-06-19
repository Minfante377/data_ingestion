from typing import List

from sqlalchemy.orm import Session


def batch_insert(db: Session, batch: List) -> None:
    """
    Batch insert a set of records on the database
    """
    db.add_all(batch)
    db.commit()
