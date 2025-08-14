import typing

if typing.TYPE_CHECKING:
    from app.api.app import Application


class Service:
    def __init__(self, app: "Application"):
        #TODO сделать привязку к сервисам
        from app.services.tron_service.tron_service import TronService
        from app.services.routes_service.routes_service import RouteService


        self.tron_service = TronService(app)
        self.route_service = RouteService(app)


def setup_services(app: "Application") -> None:
    app.service = Service(app)
