import asyncio
from proxybroker import Broker

proxy_l=[]
async def save(proxies):


    """Save proxies to a file."""
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        proto = 'https' if 'HTTPS' in proxy.types else 'http'
        proxy_l.append('%s:%d' % ( proxy.host, proxy.port))





def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=5000),
                           save(proxies))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    print(proxy_l)
    print(len(proxy_l))


if __name__ == '__main__':
    main()
