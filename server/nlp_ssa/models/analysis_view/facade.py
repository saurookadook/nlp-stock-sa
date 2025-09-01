from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID

from models.analysis_view import AnalysisViewDB
from models.analysis_view.analysis_view import AnalysisView


class AnalysisViewFacade:

    class NoResultFound(Exception):
        pass

    def __init__(self, *, db_session: scoped_session[Session]):
        self.db_session = db_session

    def get_one_by_id(self, id: UUID | str) -> AnalysisView:

        try:
            analysis_view = self.db_session.execute(
                select(AnalysisViewDB).where(AnalysisViewDB.id == id)
            ).scalar_one()
        except NoResultFound:
            raise AnalysisViewFacade.NoResultFound

        return AnalysisView.model_validate(analysis_view)
