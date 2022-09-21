import requests
import json
import time
from requests_html import HTMLSession
import os
import csv

category_url = 'https://www.lazada.vn/{}/?ajax=true&page={}&spm=a2o42.searchlistcategory.cate_5.9.46281e22mYNSDT'
review_url = "https://my.lazada.vn/pdp/review/getReviewList?itemId={}&pageSize=50&filter=0&sort=0&pageNo=1"


def get_list_id(url, category, num_page):
    ids = []
    headers = {
        'authority': 'www.lazada.vn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,de;q=0.4',
        'cache-control': 'max-age=0',
        'cookie': '__wpkreporterwid_=2808b1a3-d221-416f-3d15-b09d1b0fd746; miidlaz=miidgg5s0t1g5tikaeobpq; lzd_cid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; t_uid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; t_fv=1655628771333; cna=tcNMGDzACU4CAQE3z2f9D7xO; _gcl_au=1.1.1946339778.1655628782; _fbp=fb.1.1655628793328.1571644443; _bl_uid=I6l6C4vhlyk20Fwy0y1Ca0v17IpR; pdp_sfo=1; _ga=GA1.2.317131772.1655742451; _clck=7nor2h|1|f3a|0; _tb_token_=eed3a0631eaef; AMCVS_126E248D54200F960A4C98C6%40AdobeOrg=1; lzd_uid=200052729661; lzd_uti=%7B%22fpd%22%3A%222020-12-12%22%2C%22lpd%22%3A%222020-12-14%22%2C%22cnt%22%3A%227%22%7D; cto_axid=kZTycV4TYdxOUxlb3NWDg8TqZA4DHh0O; hng=VN|vi|VND|704; userLanguageML=vi; _gcl_aw=GCL.1661147402.Cj0KCQjwr4eYBhDrARIsANPywCgTUJzbtVryq-4AxWtndeL-jltGP1gu-SswE-rro07PPtwGYddEVecaAtM3EALw_wcB; lzd_sid=1f1bf865a88226ebd05f1b150f5462e6; sgcookie=E100VA1qFWzo%2F1%2Fh%2FPpHhcWlSjFQ9uvnj3Z3%2BpHHmaPimczF6YSS154X9TahD%2BDncuqDr6JNsstKBoS%2BruwauPRaUgCNJYDemYHWta9O5XcwnGk%3D; xlly_s=1; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19234%7CMCMID%7C62488878762935670550388505308234942167%7CMCAAMLH-1662393122%7C3%7CMCAAMB-1662393122%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1661795522s%7CNONE%7CvVersion%7C5.2.0; EGG_SESS=S_Gs1wHo9OvRHCMp98md7EhpApcnKJgu3zQUpC022kx8bSrKBVVgkw6kUQSBwNnkHH_LWlEE7TPlJdoTA9OjcltSKgA2U7F51zfVQ3SYXmocjpqwrM5MohZarH5zKMBw0jfZ-VheKH3nAjzGjKAdI5P4B4RFEfLFBqMzsI9nx1E=; exlaz=c_lzd_byr:mm_152831269_51753206_2010753389!vn1296001:clkgg2ntd1gbmgcjr41id2::; lzd_click_id=clkgg2ntd1gbmgcjr41id2; _m_h5_tk=9b81e6e4ae8f2e7150cd875d345d6003_1661841190560; _m_h5_tk_enc=5b2160feda8f221fab0eee848dfb83cc; _uetsid=8591e31027b211edb0bd51f564a4a68a; _uetvid=407f98e0efad11eca64a9f691c90fce5; cto_bundle=GIP49196ZzdtajVONnBFJTJCQmI0dHhZcW9aR3JrMEhUZ0VRJTJGcGtHMDEwRXRvU1hvU3RXc2xFUjFlJTJCZnAwQUVWJTJGYWYxWjRmRWxxdW1oZ0FPUWhnNjFCTDNFZHZVRURkSlN4bEI5T3ZjOWxBelFKMnBpOE51U3JqT1loJTJCRkZ0Q1hFYnBVJTJCbHdHQmxKVHJtT0QlMkJOMnpQaUI3UG9OZyUzRCUzRA; t_sid=d8UDCv6degRzpKwprfDJRnhK1qXuhJk4; utm_channel=NA; x5sec=7b22617365727665722d6c617a6164613b32223a223837646434376236656662643932656566626531333664313966313439373565434b446574706747454f58752b3457736870767741786f4f4d6a41774d4455794e7a49354e6a59784f7a49776e4f484873674e4141773d3d227d; isg=BEJCOzBclRCHpIhysWfa6iq3k0ikE0YtAEFTW4xbC7Vg3-NZdKEWPGUei8Ojj77F; l=eBgBd6DHL_9yMX-xBOfwhurza77tGIRfguPzaNbMiOCP_kCH5gq5W6lC0M8MCnMNnsMpR35Wn1oBByYTsyzh7xv9-eTjpym-zdLh.; tfstk=cKHRBy965EYkUfP_O0d0TbnasExGZKs8-gadpv8IH-5PSuXdiIHiBl_DNkzaynC..; lzd_cid=efc933f8-a785-4148-8a90-6a5da4bde7cb',
        'referer': 'https://www.lazada.vn/dien-thoai-di-dong/?ajax=true&page=0&spm=a2o42.searchlistcategory.cate_5.9.46281e22mYNSDT',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    for page_index in range(num_page):
        session = HTMLSession()
        time.sleep(3)
        page = url.format(category, str(page_index))
        print(page)
        data_item = requests.get(page, headers=headers).json()
        for item in data_item["mods"]["listItems"]:
            ids.append(item["itemId"])

    return list(set(ids))


def get_item_review(category, item_id):
    reviews = []
    session = HTMLSession()
    headers = {
        'authority': 'my.lazada.vn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,de;q=0.4',
        'cache-control': 'max-age=0',
        'cookie': '__wpkreporterwid_=32010a39-b596-49a8-1ba3-b10be94ecd70; client_type=desktop; miidlaz=miidgg5s0t1g5tikaeobpq; lzd_cid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; t_uid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; t_fv=1655628771333; cna=tcNMGDzACU4CAQE3z2f9D7xO; _gcl_au=1.1.1946339778.1655628782; _fbp=fb.1.1655628793328.1571644443; _bl_uid=evlg24znl626b2vURt8C7eFuw036; _ga=GA1.2.317131772.1655742451; _clck=7nor2h|1|f3a|0; _tb_token_=eed3a0631eaef; AMCVS_126E248D54200F960A4C98C6%40AdobeOrg=1; lzd_uid=200052729661; lzd_uti=%7B%22fpd%22%3A%222020-12-12%22%2C%22lpd%22%3A%222020-12-14%22%2C%22cnt%22%3A%227%22%7D; cto_axid=kZTycV4TYdxOUxlb3NWDg8TqZA4DHh0O; hng=VN|vi|VND|704; _gcl_aw=GCL.1661147402.Cj0KCQjwr4eYBhDrARIsANPywCgTUJzbtVryq-4AxWtndeL-jltGP1gu-SswE-rro07PPtwGYddEVecaAtM3EALw_wcB; lzd_sid=1f1bf865a88226ebd05f1b150f5462e6; sgcookie=E100VA1qFWzo%2F1%2Fh%2FPpHhcWlSjFQ9uvnj3Z3%2BpHHmaPimczF6YSS154X9TahD%2BDncuqDr6JNsstKBoS%2BruwauPRaUgCNJYDemYHWta9O5XcwnGk%3D; xlly_s=1; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19234%7CMCMID%7C62488878762935670550388505308234942167%7CMCAAMLH-1662393122%7C3%7CMCAAMB-1662393122%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1661795522s%7CNONE%7CvVersion%7C5.2.0; exlaz=c_lzd_byr:mm_152831269_51753206_2010753389!vn1296001:clkgg2ntd1gbmgcjr41id2::; lzd_click_id=clkgg2ntd1gbmgcjr41id2; _m_h5_tk=9b81e6e4ae8f2e7150cd875d345d6003_1661841190560; _m_h5_tk_enc=5b2160feda8f221fab0eee848dfb83cc; _uetsid=8591e31027b211edb0bd51f564a4a68a; _uetvid=407f98e0efad11eca64a9f691c90fce5; cto_bundle=GIP49196ZzdtajVONnBFJTJCQmI0dHhZcW9aR3JrMEhUZ0VRJTJGcGtHMDEwRXRvU1hvU3RXc2xFUjFlJTJCZnAwQUVWJTJGYWYxWjRmRWxxdW1oZ0FPUWhnNjFCTDNFZHZVRURkSlN4bEI5T3ZjOWxBelFKMnBpOE51U3JqT1loJTJCRkZ0Q1hFYnBVJTJCbHdHQmxKVHJtT0QlMkJOMnpQaUI3UG9OZyUzRCUzRA; t_sid=d8UDCv6degRzpKwprfDJRnhK1qXuhJk4; utm_channel=NA; x5sec=7b22617365727665722d6c617a6164613b32223a223837646434376236656662643932656566626531333664313966313439373565434b446574706747454f58752b3457736870767741786f4f4d6a41774d4455794e7a49354e6a59784f7a49776e4f484873674e4141773d3d227d; tfstk=cr1GBu_WPOJsGxgL-PO_iDXsPm-cCC2wfs5FTPgPmopDNxFp7d50evkr5EUHXuZZh; l=eBgBd6DHL_9yMYbDBO5Bourza77TWIRb8rVzaNbMiInca66PChHN0NCEOiyBAdtjQtfb3etPNKfZAdnH784LRvMDBeYBlvUn2xv9-; isg=BKurafuDTP-G1JGVAPQz1YsUOs-VwL9CwYLq_B0ofOprvMoepZOfkvheEuTSnBc6; client_type=desktop; lzd_cid=efc933f8-a785-4148-8a90-6a5da4bde7cb',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    print(review_url.format(str(item_id)))
    content = requests.get(review_url.format(str(item_id)), headers=headers).json()
    if "rgv587_flag" not in content:
        reviews += [[dt["rating"],dt["reviewContent"]] for dt in content["model"]["items"] if dt["reviewContent"] is not None]
        with open('{}/{}.csv'.format(category, item_id), 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            for review in reviews:
                writer.writerow(review)


if __name__ == '__main__':
    category = "dien-thoai-di-dong"
    num_page = 1
    try:
        os.mkdir(category)
    except:
        pass

    ids = get_list_id(category_url,category, num_page)

    for id in ids:
        time.sleep(3)
        try:
            get_item_review(category, str(id))
        except:
            pass

