from fastapi import Depends, APIRouter, HTTPException
from app.api.endpoints.models import PaginationQuery, WalletInfoResponse, WalletInfoRequest
from app.api.dependencies import get_tron_service, get_route_service
from app.services.routes_service.routes_service import RouteService
from app.services.tron_service.tron_service import TronService
from typing import List 
import logging

logger = logging.getLogger("Routes")


router = APIRouter(prefix="/api", tags=["Wallets"])

resp_types = {
    400: {"decription": "Wrong Query Params"},
    404: {"description": "Wallet Not Found"},
    500: {"description": "Internal Server Error"},
    503: {"description": "Tron Service Unavailable"}
}

@router.get("/previousRequests",
            response_model=List[WalletInfoResponse],
            responses=resp_types,
            description="Getting last notes in db")
async def get_wallets(model: PaginationQuery = Depends(),
                      service: RouteService = Depends(get_route_service)):
    try:
        logger.info(f"Received request to get wallets...")

        return await service.get_wallets(
            model=model
        )

    except HTTPException:
        raise 

    except Exception as err:
        logger.error(f"Unexpected error {str(err)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/wallet",
             response_model=WalletInfoResponse,
             responses=resp_types,
             description="Getting wallet from Tron")
async def get_wallet_info(model: WalletInfoRequest,
                          tron_service: TronService = Depends(get_tron_service),
                          route_service: RouteService = Depends(get_route_service)):
    try:
        logger.info(f"Processing wallet info req for address: {model.address}")
        wallet_data: WalletInfoResponse = await tron_service.get_wallet_data(
            address=model.address
        )

        await route_service.save_wallet(
            model = wallet_data
        )

        return wallet_data
    
    except HTTPException:
        raise 

    except Exception as err:
        logger.error(f"Unexpected error {str(err)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )