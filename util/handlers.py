import requests, logging
from pathlib import Path
import regex, os
from util.helpers import get_filename_from_url

logger = logging.getLogger(__name__)

def text_handler(request, link):
    file_name = get_filename_from_url(link)

    if not Path(file_name).is_file():
        try:
            #https://stackoverflow.com/a/52251488
            request.raise_for_status() # ensure we notice bad responses
            with open(file_name, 'wb') as f:
                file.write(request.text)
        except Exception as e:
            print(link + ": failed with error")
            print(e)
    else:
        print(file_name + ": file already exists on disk")

def binary_downloader(request, link):
    rawfilename = get_filename_from_url(link)
    logger.debug('raw filename: %s', rawfilename)
    filename = ""

    # if this throws a keyerror, we need to redo the robot test
    # try:
    d = request.headers['Content-Disposition']
    logger.debug('Content-Disposition header: %s', d)

    #the old re package was deprecated, this should be compatable but i havent checked.  see https://pypi.org/project/regex/
    filename = regex.findall("filename\*=utf-8''(.+)", d)[0]
    logger.debug('parsed filename: %s', filename)
    # except KeyError:
        # print("KeyError")
        # continue

    if Path(rawfilename).is_file():
        logger.debug('renaming \'%s\' to \'%s\'', rawfilename, filename)
        os.rename(rawfilename, filename)

    if not Path(filename).is_file():
        try:
            if request.status_code == 200:
                with open(filename, 'wb') as f:
                    logger.debug('writing chunks to \'%s\'', filename)
                    for chunk in request.iter_content(chunk_size=1024): 
                        # writing one chunk at a time to pdf file 
                        print('.', end='')
                        if chunk: 
                            f.write(chunk) 
                print()
                logger.debug('done writing chunks to \'%s\'', filename)

            else:
               logger.error('request failed with HTTP status: %s', request.status_code)
        except Exception as e:
            logger.error("%s: failed with error", filename)
            logger.error(e)
    else:
        logger.warning('%s: file already exists on disk', filename)
            