import logging
from io import StringIO as StringBuffer

logger = logging.getLogger('basic_logger')
logger.setLevel(logging.DEBUG)

### Setup the console handler with a StringIO object
log_capture_string = StringBuffer()
# log_capture_string.encoding = 'cp1251'
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

### Optionally add a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

### Add the console handler to the logger
logger.addHandler(ch)


### Send log messages.
logger.debug('debug message')
logger.info('info message')
logger.warn(u'warn message')
logger.error('error message')
logger.critical(u'critical message')


### Pull the contents back into a string and close the stream
log_contents = log_capture_string.getvalue()
log_capture_string.close()

### Output as lower case to prove it worked.
print(log_contents.lower())