import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

cpu_count = cpu_count()

log = logging
log.basicConfig(format='%(asctime)s %(threadName)s %(message)s', level=log.INFO)
log.getLogger('requests').setLevel(log.ERROR)
log.getLogger('socketio').setLevel(log.ERROR)
log.getLogger('engineio').setLevel(log.ERROR)

cpu_pool = ThreadPoolExecutor(max_workers=cpu_count, thread_name_prefix='c')
loop = asyncio.get_event_loop()
