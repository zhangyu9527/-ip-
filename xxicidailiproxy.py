import requests
from lxml import etree
from multiprocessing import Pool


class GetProxy(object):

    def get_all_proxy(self):
        assert(0)

    def validate_proxy(self, proxy_str):
        url = 'http://www.baidu.com'
        proxy = {
            'http': proxy_str,
            'https': proxy_str
        }
        try:
            response = requests.get(url, timeout=5, proxies=proxy)
            print('这个proxy好用,牛: ', proxy)
            return proxy
        except Exception as e:
            print('啥呀, 你这破ip, ', proxy)
            print(e)
            return None
    def validate_proxy_concurrent(self):
        # 进程池
        # 1. 能够重用进程
        # 2. 能够限制进程的数量

        # 1. 生成进程池的类
        pool = Pool(15)
        # 2. 将任务设置进入进程池
        # for task in task_list:
        #   pool.apply_async(func=)
        # 可以接收进程池的返回值
        res_list = []
        for proxy in self.get_all_proxy():
            res = pool.apply_async(func=self.validate_proxy, args=(proxy,))
            res_list.append(res)

        good_proxy_list = []
        # 获取返回值
        for res in res_list:
            good_proxy = res.get()
            if good_proxy:
                good_proxy_list.append(good_proxy)
        # 3. 进程池关闭
        pool.close()

        # 4. 等待所有进程结束
        pool.join()

        # good_proxy_list = []
        # for proxy in get_all_proxy():
        #     if validate_proxy(proxy):
        #         good_proxy_list.append(proxy)

        return good_proxy_list
#247s

class GetXicidailiProxy(GetProxy):
    def get_all_proxy(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
        url = 'https://www.xicidaili.com/nn'
        # 爬虫的第三步
        response = requests.get(url, headers=headers)

        # 爬虫的第四步
        html_ele = etree.HTML(response.text)

        tr_ele_list = html_ele.xpath('//table[@id="ip_list"]/tr')
        tr_ele_list = tr_ele_list[1:]

        for tr_ele in tr_ele_list:
            ip = tr_ele.xpath('./td[2]/text()')[0]
            port = tr_ele.xpath('./td[3]/text()')[0]
            proxy_str = 'http://' + ip + ':' + port
            yield proxy_str


class GetKuaiProxy(GetProxy):
    def get_all_proxy(self):
        pass

if __name__ == '__main__':
    import time
    start_time = time.time()

    xici_proxy = GetXicidailiProxy()
    good_proxy_list = xici_proxy.validate_proxy_concurrent()


    print('所有的好用的proxy是:')
    print(good_proxy_list)
    end_time = time.time()
    print('总的时间是:', str(end_time - start_time))
