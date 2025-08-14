import typing

if typing.TYPE_CHECKING:
    from app.api.app import Application



class Store:
    def __init__(self, app: "Application"):
        from app.repository.accessors.dbase_accessor import Accessor

        self.dbase_accessor = Accessor(app)

    
def setup_store(app: "Application") -> None:
    app.store = Store(app)