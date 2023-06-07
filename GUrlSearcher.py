import logging
import os
import sys
from datetime import datetime
from urllib.parse import urlencode, urlparse, parse_qs
from random import randint
from time import sleep

import requests
import bs4
from lxml.html import fromstring
from requests import get
from googlesearch import search

# logging configuration
logger = logging.getLogger('GUrlSearcherLogger')
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
now = datetime.now()
dateTime = now.strftime("%Y-%m-%d_%H_%M_%S")
LOG_FILE_NAME = "GUrlSearcher_" + dateTime + ".log"
fileHandler = logging.FileHandler(LOG_FILE_NAME)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# program parameters
PROXY_HOST = ""
PROXY_PORT = ""
MIN_SECONDS_SLEEP = 0
MAX_SECONDS_SLEEP = 0
NUM_CONSECUTIVE_REQUESTS = 30
MIN_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS = 420
MAX_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS = 420
FIRMS_FILE = ""
OUTPUT_FILE_FOLDER = ""
LOG_FILE_FOLDER = ""
LOG_LEVEL = "INFO"


def main(argv):
    logger.info("****************************************")
    logger.info("**********   GUrlSearcher   *************")
    logger.info("****************************************\n\n")

    now = datetime.now()
    dateTime = now.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Starting datetime: " + dateTime)


    loadExternalConfiguration(argv)
    firmList = loadFirmList(FIRMS_FILE)
    searchUrls(firmList, OUTPUT_FILE_FOLDER)

    now = datetime.now()
    dateTime = now.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Ending datetime: " + dateTime)

def googleSearch(firm):
    ulrList = []
    query = str(firm[1])
    try:
        for linkPos, url in enumerate(search(query, tld="it", lang="it", num=10, start=0, stop=10, pause=2)):
            ulrList.append(url)
        return ulrList
    except Exception as e:
        # delay for 1-2 hours could be a good alternative
        logger.info(e)
    return ulrList


def searchUrls(firmList, OUTPUT_FILE_FOLDER):
    firmListLen = len(firmList)
    now = datetime.now()
    dateTime = now.strftime("%Y-%m-%d_%H_%M_%S")
    outputFileName = "seed_" + dateTime + ".txt"
    outputFile = outputFileName
    if os.path.isdir(OUTPUT_FILE_FOLDER):
        outputFile = OUTPUT_FILE_FOLDER + "/" + outputFileName

    with open(outputFile, 'a+', encoding='utf-8') as f:
        for i, firm in enumerate(firmList[1:]):  # non considera la prima riga del file ovvero l'header
            logger.info(str(i+1) + " / " + str(firmListLen) + " ) Processing " + firm[1] + " having id " + firm[0])

            # wait a random number of seconds between MIN_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS and
            # MAX_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS) after NUM_CONSECUTIVE_REQUESTS requests
            if (i + 1) % NUM_CONSECUTIVE_REQUESTS == 0:
                sleep_seconds = randint(MIN_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS, MAX_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS)
                logger.info(str(NUM_CONSECUTIVE_REQUESTS) + " consecutive requests - sleeping " + str(sleep_seconds) + " before restart")
                sleep(sleep_seconds)
                logger.info("restart !")

            # wait a random number of seconds between MIN_SECONDS_SLEEP and MAX_SECONDS_SLEEP
            # after each request
            sleep(randint(MIN_SECONDS_SLEEP, MAX_SECONDS_SLEEP))

            links = googleSearch(firm)
            logger.info(str(len(links)) + " results retrieved")
            for linkPos, link in enumerate(links):
                #logger.info(str(firm[0]) + "\t" + str(linkPos + 1) + "\t" + links[linkPos])
                f.writelines(str(firm[0]) + "\t" + str(linkPos + 1) + "\t" + links[linkPos] + "\n")
                f.flush()


def loadFirmList(FIRMS_FILE):
    firmList = []

    with open(FIRMS_FILE, "rt", encoding="utf-8") as f:
        for line in f.readlines():
            tokens = line.split("\t")
            if len(tokens) == 2:
                #myTuple = (tokens[0], tokens[1].rstrip(), tokens[2].rstrip())
                myTuple = (tokens[0], tokens[1].rstrip())
                firmList.append(myTuple)
            else:
                logger.warning("the firm having id=" + tokens[0] + " is malformed and will not be considered !")

    return firmList


def loadExternalConfiguration(argv):
    if len(argv) != 1:
        sys.exit("Configuration file invalid or not provided ! \nUSAGE: GUrlSearcher my_path/config.cfg")

    configFile = sys.argv[1]
    external_settings = dict()
    with open(configFile, "rt") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                tokens = line.split("=")
                if len(tokens) == 2:
                    external_settings[tokens[0]] = tokens[1]

    global PROXY_HOST
    global PROXY_PORT
    global MIN_SECONDS_SLEEP
    global MAX_SECONDS_SLEEP
    global NUM_CONSECUTIVE_REQUESTS
    global MIN_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS
    global MAX_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS
    global FIRMS_FILE
    global OUTPUT_FILE_FOLDER
    global LOG_FILE_FOLDER
    global LOG_FILE_NAME
    global LOG_LEVEL
    global consoleHandler
    global fileHandler
    global logger

    PROXY_HOST = str(external_settings.get("PROXY_HOST", "")).rstrip()
    PROXY_PORT = str(external_settings.get("PROXY_PORT", "")).rstrip()

    MIN_SECONDS_SLEEP = int(str(external_settings.get("MIN_SECONDS_SLEEP", "0")).rstrip())
    MAX_SECONDS_SLEEP = int(str(external_settings.get("MAX_SECONDS_SLEEP", "0")).rstrip())

    NUM_CONSECUTIVE_REQUESTS = int(str(external_settings.get("NUM_CONSECUTIVE_REQUESTS", "30")).rstrip())
    MIN_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS = int(str(external_settings.get("MIN_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS", "420")).rstrip())
    MAX_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS = int(str(external_settings.get("MAX_SECONDS_SLEEP_BETWEEN_CONSECUTIVE_REQUESTS", "420")).rstrip())

    FIRMS_FILE = str(external_settings.get("FIRMS_FILE", "")).rstrip()
    if not os.path.isfile(FIRMS_FILE):
        logger.error("Invalid FIRMS_FILE parameter !")
        raise FileNotFoundError("Invalid FIRMS_FILE parameter !")

    OUTPUT_FILE_FOLDER = str(external_settings.get("OUTPUT_FILE_FOLDER", "")).rstrip()
    if not os.path.isdir(OUTPUT_FILE_FOLDER):
        logger.warning("Invalid OUTPUT_FILE_FOLDER parameter, the default location will be used !")
        OUTPUT_FILE_FOLDER = "."

    LOG_FILE_FOLDER = str(external_settings.get("LOG_FILE_FOLDER", "")).rstrip()
    now = datetime.now()
    dateTime = now.strftime("%Y-%m-%d_%H_%M_%S")
    if os.path.isdir(LOG_FILE_FOLDER):
        fileHandler = logging.FileHandler(LOG_FILE_FOLDER + "/" + LOG_FILE_NAME)
    else:
        logger.warning("Invalid LOG_FILE_FOLDER parameter, the default logfile location will be used !")

    LOG_LEVEL = str(external_settings.get("LOG_LEVEL", "INFO")).rstrip()
    consoleHandler.setLevel(LOG_LEVEL)
    fileHandler.setLevel(LOG_LEVEL)
    # logger.addHandler(consoleHandler)
    # logger.addHandler(fileHandler)


if __name__ == "__main__":
    main(sys.argv[1:])