from fastapi import Depends, Request
from app.services.tron_service.tron_service import TronService
from app.services.routes_service.routes_service import RouteService

async def get_tron_service(request: Request) -> TronService:
    return request.app.state.service.tron_service

async def get_route_service(request: Request) -> RouteService:
    return request.app.state.service.route_service