from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from models.analysis_view import AnalysisView, AnalysisViewDB


class AnalysisViewFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session):
        self.db_session = db_session

    def get_one_by_id(self, id):

        try:
            analysis_view = self.db_session.execute(
                select(AnalysisViewDB).where(AnalysisViewDB.id == id)
            ).scalar_one()
        except NoResultFound:
            raise AnalysisViewFacade.NoResultFound

        return AnalysisView.model_validate(analysis_view)
