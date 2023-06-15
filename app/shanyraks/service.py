from app.config import database, here_api_key

from .repository.repository import ShanyrakRepository
from .adapters.s3_service import S3Service
from .adapters.here_service import HereService


class Service:
    def __init__(
        self,
        repository: ShanyrakRepository,
        s3_service: S3Service,
        here_service: HereService,
    ):
        self.repository = repository
        self.s3_service = s3_service
        self.here_service = here_service


def get_service():
    repository = ShanyrakRepository(database)
    s3_service = S3Service()
    here_service = HereService(here_api_key)
    print(here_api_key)
    svc = Service(repository, s3_service, here_service)
    return svc
