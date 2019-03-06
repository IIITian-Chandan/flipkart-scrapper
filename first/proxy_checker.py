# !/usr/bin/env python

import time
from queue import Queue
from threading import Thread

import lxml
import requests
from lxml import html
import asyncio
from proxybroker import Broker


# class ProxyGraberCalss(object):
#     def __init__(self, url, table_selector):
#         self.url = url
#         self.table_selector = table_selector
#         self.start()
#
#     def preparate_result(self, x):
#         return '{}:{}'.format(x.cssselect('td')[0].text, x.cssselect('td')[1].text)
#
#     def start(self):
#         r = requests.get(self.url)
#         htree = lxml.html.fromstring(r.text)
#         all = htree.cssselect(self.table_selector)
#         return [self.preparate_result(x) for x in all]

class ProxyGraberClass():
    def __init__(self,len_proxy_list):
        self.len_proxy_list=len_proxy_list

    proxy_list=[]

    async def save(self,proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            self.proxy_list.append('%s:%d' % ( proxy.host, proxy.port))

    def p_list(self):
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=self.len_proxy_list),
                           self.save(proxies))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)
        print(len(self.proxy_list))
        return self.proxy_list


class ProxyChecker:
    def __init__(self, inlist, threads=200, verbose=False, timeout=25):
        self.inlist = inlist
        # there shouldn't be more threads than there are proxies
        if threads > len(self.inlist):
            self.threads = len(self.inlist)

        else:
            self.threads = threads

        self.verbose = verbose
        self.timeout = timeout

        self.outlist = []
        self.total_scanned = 0
        self.total_working = 0
        self.original_ip = None
        self.threads_done = 0

        # constants
        self.IP_CHECK = "https://api.ipify.org"

    def save_valid_proxy(self, proxy):
        if proxy:
            self.outlist.append(proxy)

    def get_external_ip(self, proxies=None):
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            if proxies:
                r = requests.get(self.IP_CHECK, proxies=proxies, headers=headers, timeout=self.timeout)

            else:
                r = requests.get(self.IP_CHECK, headers=headers)

        except IOError:
            return False

        return str(r.text)

    def check_proxy(self, proxy):
        proxies = {
            "http": "http://" + proxy,
            "https": "https://" + proxy
        }

        # see if the proxy actually works
        ip = self.get_external_ip(proxies=proxies)
        if not ip:
            return False

        if ip != self.original_ip:
            if self.verbose:
                print(ip)

            self.total_working += 1

        return proxy

    def process_proxy(self):
        try:
            while True:
                proxy = self.queue.get()
                self.save_valid_proxy(self.check_proxy(proxy))
                self.queue.task_done()
                self.total_scanned += 1

        except:
            pass

    def start(self):
        if self.verbose:
            print("Running: {} threads...".format(self.threads))

        self.original_ip = self.get_external_ip()

        if self.verbose:
            print("Your original external IP address is: {}".format(self.original_ip))
            print("Checking proxies...")

        self.queue = Queue(self.threads)

        # get all our threads ready for work
        for i in range(0, self.threads):
            thread = Thread(target=self.process_proxy)
            thread.daemon = True
            thread.start()

        self.start = time.time()

        # keep sending threads their jobs
        try:
            for proxy in self.inlist:
                self.queue.put(proxy.strip())

            self.queue.join()

        except KeyboardInterrupt:
            if self.verbose:
                print("Closing down, please let the threads finish.")

        if self.verbose:
            print("Running: {:.2f} seconds".format(time.time() - self.start))

        if self.verbose:
            print("Scanned: {} proxies".format(self.total_scanned))
            print("Working: {} proxies".format(self.total_working))

        return self.outlist
