# -*- coding: utf-8 -*-

import sys
import json
import codecs
from time import time
import traceback

from universe_settings import *
from utils.processpool import ProcessHandler
from utils.processpool import ProcessPool


class ExtractPreprocessHandler(ProcessHandler):

    def __init__(self):
        pass

    def process_function(self, data_item):
        try:
            line = data_item
            if len(line.split('\t')) == 1:
                return None
            json_str = line.strip()
            extracted_data = self.process_json(json_str)
            return extracted_data
        except ValueError:
            sys.stdout.write(line)
            return None
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            traceback.print_exc()
            return None
        pass

    def process_json(self, json_str):
        json_obj = json.loads(json_str, strict=False)
        json_obj = json_obj.get("qa", None)
        if json_obj is not None:
            title = json_obj.get("title", None)
            if title is None:
                return None
        else:
            return None
        return title + '\n'




if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python %s zhihu_data\n" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]

    t0 = time()
    file = codecs.open(filename, encoding='utf-8', errors='ignore')
    pool = ProcessPool(10, handle_queue_size=10000, output_queue_size=10000)
    process_handler = ZhihuPreprocessHandler()
    output_handler = OutputFileHandler('zhihu_title')
    pool.add_handler(process_handler, output_handler)
    pool.startAll()
    for line in file:
        pool.add_process_data(line)
    pool.wait_completion()
    print("done in %fs" % (time() - t0))
    pass
