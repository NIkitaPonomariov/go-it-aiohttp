import sys
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
from priv_bank_api import PrivatBankAPI
from logger import Logger

async def main(days: int, currencies: List[str]) -> None:
    if days < 1 or days > 10:
        print("Error: Days should be between 1 and 10.")
        return
    
    logger = Logger("exchange_log.txt")
    privat_bank_api = PrivatBankAPI()
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]

    tasks = [privat_bank_api.get_exchange_rates(date, currencies) for date in dates]
    results = await asyncio.gather(*tasks)
    
    exchange_data = [{date: result} for date, result in zip(dates, results)]
    
    await logger.log(f"Command executed for {days} days with currencies: {currencies}")
    
    print(exchange_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <days> <currency1> <currency2> ...")
        sys.exit(1)

    days = int(sys.argv[1])
    currencies = sys.argv[2:] if len(sys.argv) > 2 else ['EUR', 'USD']
    
    asyncio.run(main(days, currencies))
