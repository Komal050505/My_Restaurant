import logging as log

# Configure logging
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filemode='a', filename='main.log')
