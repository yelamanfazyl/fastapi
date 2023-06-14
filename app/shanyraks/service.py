from app.config import database

from .repository.repository import ShanyrakRepository
from .adapters.s3_service import S3Service


class Service:
    def __init__(
        self,
        repository: ShanyrakRepository,
        s3_service: S3Service,
    ):
        self.repository = repository
        self.s3_service = s3_service


def get_service():
    repository = ShanyrakRepository(database)
    s3_service = S3Service()
    svc = Service(repository, s3_service)
    return svc
