from fastapi import Request
import time

def add_process_time_header(request:Request, call_next):
    start_time = time.time()
    response = call_next(request)
    process_time = time.time() - start_time

    response.headerd['X-Process-Time'] = str(process_time)
    return response