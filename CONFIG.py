import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

drive = logging.FileHandler('logs.log')
drive.setLevel(logging.DEBUG)

stdout = logging.StreamHandler()
stdout.setLevel(logging.INFO)

log.addHandler(drive)
log.addHandler(stdout)

HEADLESS = True
TIMEOUT = 60_000