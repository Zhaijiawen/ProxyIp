from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import urllib.parse

baseUrl = "http://www.xicidaili.com/"
ipType = ("nn", "nt", "wn", "wt")
pageNum = 5

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}

print("0:国内高匿代理")
print("1:国内普通代理")
print("2:国内HTTPS代理")
print("3:国内HTTP代理")
try:
    type = input("输入获取ip类型:")
    baseUrl += str(ipType[int(type)])
    num = input("输入爬取页数：")
    pageNum = int(num)
except:
    print("出错了，请保持参数的正确性！")

# ip存放位置
proxyIp = []


def requestIp(num, baseUrl, header):
    # 获取网页
    for i in range(num):
        url = baseUrl + "/" + str(i + 1)
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response.read(), "lxml")
        parseHtml(soup)


def parseHtml(beautifulSoup):
    # 解析网页
    trList = beautifulSoup.find_all("tr")
    for trSoup in trList:
        tdList = trSoup.find_all("td")
        if (len(tdList) == 0):
            continue
        ipAddress = tdList[1]
        ipPort = tdList[2]

        # 结果加入到list中
        proxyIp.append(ipAddress.get_text() + ":" + ipPort.get_text())


def visitIp(url, timeout):
    # 过滤可用ip
    for i in range(len(proxyIp)):
        # 防止越界
        if (i >= len(proxyIp)):
            break
        request = urllib.request.ProxyHandler({'http': proxyIp[i]})
        opener = urllib.request.build_opener(request, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        try:
           urllib.request.urlopen(url, timeout=timeout).read().decode('utf8')
        except:
            proxyIp.pop(i)
            continue


if __name__ == '__main__':
    print("开始获取数据...")
    requestIp(pageNum, baseUrl, header)
    print("解析完成！")
    print("过滤可用ip...")
    visitIp("http://ip.chinaz.com/", 1)
    print("过滤完成！可用ip为" + str(len(proxyIp)) + "个")

    targetUrl = input("输入目标url:")
    print("开始访问...")
    visitIp(targetUrl, 5)
    print("结束访问,成功访问ip为" + str(len(proxyIp)) + "个")
