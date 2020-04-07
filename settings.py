DBMS = ''
DBUSER = ''
DBPASS = ''
DBHOST = ''
DBPORT = ''
DBNAME = 'hltv'
TABLENAME = 'hltv_results'

crawler_settings = {
    'ITEM_PIPELINES': {
       'db.pipeline.HltvPipeline': 300, # enabling pipeline for saving data into DB
    },
    'CONCURRENT_REQUESTS': 1,
    'DOWNLOAD_DELAY': 2, # 1 page per 2 seconds  
#     'CLOSESPIDER_ITEMCOUNT': 1000,
    'LOG_ENABLED': False # Disable scrapy logging
}