from app.repository.base import BaseService
import typing 
from app.api.endpoints.models import WalletInfoResponse, PaginationQuery
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from typing import List 

if typing.TYPE_CHECKING:
    from app.api.app import Application


class RouteService(BaseService):
    def __init__(self, app: "Application"):
        super().__init__(app=app)
        self._accessor = None 

    @property
    def accessor(self):
        if self._accessor is None:
            self._accessor = self.app.store.dbase_accessor
            self.logger.info("Database Accessor Initialized")

        return self._accessor
    

    async def save_wallet(self, model: WalletInfoResponse) -> bool:
        try:
            self.logger.info(f"Saving wallet {model.address}")

            result = await self.accessor.save_wallet(
                address = model.address,
                trx_balance = model.trx_balance,
                bandwidth=model.bandwidth,
                energy=model.energy
            )
            return result
        
        except IntegrityError:
            self.logger.error("Database Integrity Error")
            raise HTTPException(
                status_code=409, 
                detail="Wallet data conflict"
            )
        except SQLAlchemyError as e:
            self.logger.error(f"Database error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=503,
                detail="Database service unavailable"
            )
        
        except Exception as err:
            self.logger.error("Unexpected error in accessor")
            raise HTTPException(
                status_code=500,
                detail=str(err)
            )
        
    
    async def get_wallets(self, model: PaginationQuery) -> List[WalletInfoResponse]:
        try:
            self.logger.info("Fetching wallets...")

            result = await self.accessor.get_wallets(
                limit=model.limit,
                offset=model.offset
            )
            if not result:
                self.logger.warning("Result list is empty")
                raise HTTPException(
                    status_code=404,
                    detail="Wallets Not Found"
                )
            
            formatted_res = [
                WalletInfoResponse(
                    address=w.address,
                    trx_balance=w.trx_balance,
                    bandwidth=w.bandwidth,
                    energy=w.energy,
                    updated_at=w.updated_at
                )
                for w in result
            ]

            return formatted_res
        
        except HTTPException:
            raise 

        except SQLAlchemyError as e:
            self.logger.error(f"Database error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=503,
                detail="Database service unavailable"
            )
        
        except Exception as err:
            self.logger.error("Unexpected error in accessor")
            raise HTTPException(
                status_code=500,
                detail=str(err)
            )
        