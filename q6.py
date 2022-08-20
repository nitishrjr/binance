from prometheus_client import start_http_server, Summary, Info
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import time, datetime
from submission import q4

# 6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.

def show(prev, curr):
    c_time = datetime.datetime.now().strftime('%H:%M:%S:%f')
    
    for res in curr:
        i = Info(res+'_'+str(c_time), 'Price Spread/Abs Delta')
        i.info({'price_spread': str(curr[res]), 'abs_delta': str(curr[res]-prev[res])})

if __name__ == '__main__':
    start_http_server(8080)
    prev = q4()
    curr = prev
    while True:
        show(prev, curr)
        time.sleep(10)
        prev = curr
        curr = q4()