from sqlalchemy.orm import Session


class CRUDBase:
    model = None

    def __init__(self, model):
        self.model = model

    def create(self, db: Session, *args, **kwargs):
        pass


class MagicUlrCRUD(CRUDBase):

    def create(self, db: Session, origin_url: str, id_path: str):
        obj = self.model(origin_url=origin_url, id_path=id_path)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_by_id_path(self, db: Session, id_path: str):
        return db.query(self.model).filter(
            self.model.id_path == id_path).first()

    def get_by_origin_url(self, db: Session, origin_url: str):
        return db.query(self.model).filter(
            self.model.origin_url == origin_url).first()

    def count_plus(self, db, obj, count_index=1):
        obj.count_open += count_index
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
