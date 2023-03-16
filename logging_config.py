import logging

# Create a logger object
logger = logging.getLogger(__name__)

# Set the logging level to INFO
logger.setLevel(logging.INFO)

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('bot.log')

# Create a console handler to output logs to the console
console_handler = logging.StreamHandler()

# Set the logging format for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
