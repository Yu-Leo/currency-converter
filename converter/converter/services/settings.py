import os

# Redis settings
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_DB = int(os.getenv('REDIS_DB', default='0'))

# Exchange rate API:
EXCHANGE_RATE_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD1'
