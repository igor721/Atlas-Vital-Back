import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__) #criando log com modulo atual

logger.setLevel(logging.INFO) #seteando nivel de log.
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') 

streamHandler = logging.StreamHandler()  # Log de msg no console
streamHandler.setFormatter(formatter) 
logger.addHandler(streamHandler) #adicionando ao log

fileHandler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3) #gravando as msg no app.log
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler) #adicionando ao log