from app.repository.base import BaseService
from fastapi import HTTPException
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound
from app.api.endpoints.models import WalletInfoResponse
import typing 

if typing.TYPE_CHECKING:
    from app.api.app import Application

class TronService(BaseService):
    def __init__(self, app: "Application"):
        super().__init__(app=app)
        self._client = None 

    
    @property
    def client(self) -> AsyncTron:
        if self._client is None:
            self._client = AsyncTron(network=self.app.settings.TRON_NETWORK)
            self.logger.info("Tron Sevice Initialized")
        return self._client
    

    async def get_wallet_data(self, address: str):
        try:
            self.logger.info("Processing wallet address...")

            self._validate_tron_address(
                address=address
            )
                
            
            account = await self._get_account_data(
                address=address
            )

            return WalletInfoResponse(
                address=address,
                trx_balance=account.balance,
                bandwidth=getattr(account, 'bandwidth_remaining', 0),
                energy=getattr(account, 'energy_remaining', 0)
            )
        
        except AddressNotFound:
            self.logger.error("Wallet Not Found")
            raise HTTPException(
                status_code=404,
                detail="Wallet Not Found"
            )
        
        except HTTPException as err:
            self.logger.error(f"{str(err.detail)}", exc_info=True)
            raise

        except Exception as err:
            self.logger.error(f"Unexpected error {str(err)}", exc_info= True)
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error"
            )
        
    
    async def _get_account_data(self, address: str):
        account = await self.client.get_account(address)
        self.logger.info(f"Received account {account}")
        if not account:
            raise HTTPException(
                status_code=404,
                detail="Wallet exists but has no transactions (inactive)"
            )
        account_data = {
            'address': address,
            'trx_balance': account.get('balance', 0) / 1_000_000,
            'bandwidth': account.get('net_window_size', 0),  
            'energy': account.get('energy_window_size', 0),   
            }
        
        return type('AccountObject', (), account_data)
    

    def _validate_tron_address(self, address: str) -> bool:
        if not address.startswith('T') and len(address) == 34:
            raise HTTPException(
                status_code=422, 
                detail="Invalid TRON address format"
            )
        return True 