from time import sleep
import sys
import logging
import snap7

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def mainloop():
    server = snap7.server.Server()
    db_num = 200
    size = 55
    db_data = (snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte] * size)()
    server.register_area(snap7.types.srvAreaDB, db_num, db_data)
    server.start(tcpport=102)

    while True:
        while True:
            event = server.pick_event()
            if event:
                logger.info(server.event_text(event))
            else:
                break
        sleep(1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        snap7.common.load_library(sys.argv[1])
    mainloop()
