from app.repository.base import BaseAccessor
from sqlalchemy import select, func, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from app.repository.models import WalletModel
from typing import List

class Accessor(BaseAccessor):
    async def save_wallet(self, 
                          address: str, 
                          trx_balance: float,
                          bandwidth: float, 
                          energy: float) -> bool:
        self.logger.info("Creating wallet in database")
        async with self.app.db.session() as session:
            try:
                stmt = (insert(WalletModel)
                        .values(
                            wallet_address = address,
                            trx_balance = trx_balance,
                            bandwidth = bandwidth,
                            energy = energy)
                        .on_conflict_do_update(
                            index_elements=['wallet_address'],  
                            set_={
                                'trx_balance': trx_balance,
                                'bandwidth': bandwidth,
                                'energy': energy,
                                'updated_at': func.now() 
                            }
                    ))
                
                await session.execute(stmt)
                await session.commit()
                self.logger.info("Wallet Successfully Added")
                return True 
            except IntegrityError as err:
                await session.rollback()
                self.logger.error("Database Intergity Error")
                raise

            except Exception as err:
                await session.rollback()
                self.logger.error(f"Unexpected Error {str(err)}", exc_info=True)
                raise 


    async def get_wallets(self, limit: int = 10, offset: int = 1) -> List[WalletModel]:
        self.logger.info(f"Fetching wallets (limit: {limit}, offset: {offset}")
        async with self.app.db.session() as session:
            curr_offset = (offset - 1) * limit 
            try:
                stmt = (select(WalletModel)
                        .order_by(desc(WalletModel.updated_at))
                        .limit(limit)
                        .offset(curr_offset))
                result = await session.execute(stmt)
                wallet_list = result.scalars().all()
                self.logger.info("Wallets Sucessfully Fetched")
                return wallet_list
            
            except SQLAlchemyError as err:
                self.logger.error(f"Database Error {str(err)}", exc_info=True)
                raise 

            except Exception as err:
                self.logger.error(f"Unexpected Error {str(err)}", exc_info=True)
                raise 
    