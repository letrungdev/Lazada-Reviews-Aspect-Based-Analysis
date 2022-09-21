import requests
import json
import time
from requests_html import HTMLSession
from kafka import KafkaProducer


# api lay thong tin danh sach san pham cua 1 danh muc theo trang
category_url = 'https://www.lazada.vn/{}/?ajax=true&page={}&spm=a2o42.searchlistcategory.cate_5.9.46281e22mYNSDT'
# API lay review cua san pham
review_url = "https://my.lazada.vn/pdp/review/getReviewList?itemId={}&pageSize=50&filter=0&sort=0&pageNo=1"


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def get_list_id(url, category, num_page):
    ids = []
    headers = {
        'authority': 'www.lazada.vn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,de;q=0.4',
        'cache-control': 'max-age=0',
        'cookie': '__wpkreporterwid_=2808b1a3-d221-416f-3d15-b09d1b0fd746; miidlaz=miidgg5s0t1g5tikaeobpq; lzd_cid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; t_uid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; t_fv=1655628771333; cna=tcNMGDzACU4CAQE3z2f9D7xO; _fbp=fb.1.1655628793328.1571644443; _bl_uid=I6l6C4vhlyk20Fwy0y1Ca0v17IpR; pdp_sfo=1; _ga=GA1.2.317131772.1655742451; _tb_token_=eed3a0631eaef; AMCVS_126E248D54200F960A4C98C6%40AdobeOrg=1; lzd_uid=200052729661; lzd_uti=%7B%22fpd%22%3A%222020-12-12%22%2C%22lpd%22%3A%222020-12-14%22%2C%22cnt%22%3A%227%22%7D; cto_axid=kZTycV4TYdxOUxlb3NWDg8TqZA4DHh0O; _gcl_aw=GCL.1661147402.Cj0KCQjwr4eYBhDrARIsANPywCgTUJzbtVryq-4AxWtndeL-jltGP1gu-SswE-rro07PPtwGYddEVecaAtM3EALw_wcB; lzd_sid=1f1bf865a88226ebd05f1b150f5462e6; sgcookie=E100VA1qFWzo%2F1%2Fh%2FPpHhcWlSjFQ9uvnj3Z3%2BpHHmaPimczF6YSS154X9TahD%2BDncuqDr6JNsstKBoS%2BruwauPRaUgCNJYDemYHWta9O5XcwnGk%3D; exlaz=c_lzd_byr:mm_152831269_51753206_2010753389!vn1296001:clkgg2ntd1gbmgcjr41id2::; lzd_click_id=clkgg2ntd1gbmgcjr41id2; _uetvid=407f98e0efad11eca64a9f691c90fce5; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19246%7CMCMID%7C62488878762935670550388505308234942167%7CMCAAMLH-1663386510%7C3%7CMCAAMB-1663386510%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1662788910s%7CNONE%7CvVersion%7C5.2.0; cto_bundle=52MZlF96ZzdtajVONnBFJTJCQmI0dHhZcW9aR21XVjhnNlZ2eW1lNjVKdXUxZyUyRk1lOXJndmo2ZGYwSDBOSjhjMGdBSnZkbFdVdnFwVEJZUXlyVU85U0FrQWdDMTZYMlZPcVRtMkJ4ejRibGRiUDJQQTREUThEcjY5ZSUyRldVM3JHVjhyaGE0aG01ZERVJTJCSDVXRiUyRllrdXJQVUdnSE13JTNEJTNE; _clck=7nor2h|1|f4r|0; hng=VN|vi|VND|704; userLanguageML=vi; _m_h5_tk=1ed1607f490dd7d298cecabdda2ad81c_1663690698559; _m_h5_tk_enc=7af78b08a564cdfccdfa51f8bb555d21; _gcl_au=1.1.1426747026.1663680259; xlly_s=1; EGG_SESS=S_Gs1wHo9OvRHCMp98md7KXPtE6h1HIm4jBCspoSvxQ1WfYjCxkHuoLgowJpj5VhE8P6uASAkrBc4WUEDXDhKYX1-v2BlN0W3a5dsb-IdkGZcuzRDN5se9MndOK_yKoPmEEVuT1AndUOuTGfN2pfd_svkpp7BTVbRclix01bIXc=; __wpkreporterwid_=c39c1d10-d363-4a6e-bd03-0a6bf185657c; tfstk=cOxVBdZTxmnVg4x_hgSw4mpgD_sfCfCGOuWFoXCOX2E3-cHCTK50W5BuPsBPQ8PGo; l=eBgBd6DHL_9yMSNzBO5CFurza77TqIRbzsPzaNbMiInca66FpFMCPNCEfFL9XdtjQtCfJetz5Tzfvdpa03Ud9xDDBe020surnxvO.; isg=BBgYpQUUz9JfIOJMD1VQDAwl6UaqAXyL2ooOhFIJr9MH7brX-hFpGjGFIT1dfTRj; lzd_cid=efc933f8-a785-4148-8a90-6a5da4bde7cb',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    for page_index in range(num_page):
        session = HTMLSession()
        time.sleep(1)
        page = url.format(category, str(page_index))
        data_item = requests.get(page, headers=headers).json()
        for item in data_item["mods"]["listItems"]:
            ids.append(item["itemId"])
    return list(set(ids))


def public_item_review(category, item_id):
    session = HTMLSession()
    headers = {
        'authority': 'my.lazada.vn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,de;q=0.4',
        'cache-control': 'max-age=0',
        'cookie': '__wpkreporterwid_=32010a39-b596-49a8-1ba3-b10be94ecd70; client_type=desktop; miidlaz=miidgg5s0t1g5tikaeobpq; t_uid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; lzd_cid=31df296a-4bea-4ce8-d0e4-215a0a15c4a7; t_fv=1655628771333; cna=tcNMGDzACU4CAQE3z2f9D7xO; _fbp=fb.1.1655628793328.1571644443; _bl_uid=evlg24znl626b2vURt8C7eFuw036; _ga=GA1.2.317131772.1655742451; _tb_token_=eed3a0631eaef; AMCVS_126E248D54200F960A4C98C6%40AdobeOrg=1; lzd_uid=200052729661; lzd_uti=%7B%22fpd%22%3A%222020-12-12%22%2C%22lpd%22%3A%222020-12-14%22%2C%22cnt%22%3A%227%22%7D; cto_axid=kZTycV4TYdxOUxlb3NWDg8TqZA4DHh0O; _gcl_aw=GCL.1661147402.Cj0KCQjwr4eYBhDrARIsANPywCgTUJzbtVryq-4AxWtndeL-jltGP1gu-SswE-rro07PPtwGYddEVecaAtM3EALw_wcB; lzd_sid=1f1bf865a88226ebd05f1b150f5462e6; sgcookie=E100VA1qFWzo%2F1%2Fh%2FPpHhcWlSjFQ9uvnj3Z3%2BpHHmaPimczF6YSS154X9TahD%2BDncuqDr6JNsstKBoS%2BruwauPRaUgCNJYDemYHWta9O5XcwnGk%3D; exlaz=c_lzd_byr:mm_152831269_51753206_2010753389!vn1296001:clkgg2ntd1gbmgcjr41id2::; lzd_click_id=clkgg2ntd1gbmgcjr41id2; _uetvid=407f98e0efad11eca64a9f691c90fce5; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19246%7CMCMID%7C62488878762935670550388505308234942167%7CMCAAMLH-1663386510%7C3%7CMCAAMB-1663386510%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1662788910s%7CNONE%7CvVersion%7C5.2.0; cto_bundle=52MZlF96ZzdtajVONnBFJTJCQmI0dHhZcW9aR21XVjhnNlZ2eW1lNjVKdXUxZyUyRk1lOXJndmo2ZGYwSDBOSjhjMGdBSnZkbFdVdnFwVEJZUXlyVU85U0FrQWdDMTZYMlZPcVRtMkJ4ejRibGRiUDJQQTREUThEcjY5ZSUyRldVM3JHVjhyaGE0aG01ZERVJTJCSDVXRiUyRllrdXJQVUdnSE13JTNEJTNE; _clck=7nor2h|1|f4r|0; hng=VN|vi|VND|704; _m_h5_tk=1ed1607f490dd7d298cecabdda2ad81c_1663690698559; _m_h5_tk_enc=7af78b08a564cdfccdfa51f8bb555d21; _gcl_au=1.1.1426747026.1663680259; xlly_s=1; tfstk=cOxVBdZTxmnVg4x_hgSw4mpgD_sfCfCGOuWFoXCOX2E3-cHCTK50W5BuPsBPQ8PGo; l=eBgBd6DHL_9yMSNzBO5CFurza77TqIRbzsPzaNbMiInca66FpFMCPNCEfFL9XdtjQtCfJetz5Tzfvdpa03Ud9xDDBe020surnxvO.; isg=BBgYpQUUz9JfIOJMD1VQDAwl6UaqAXyL2ooOhFIJr9MH7brX-hFpGjGFIT1dfTRj; lzd_cid=efc933f8-a785-4148-8a90-6a5da4bde7cb',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    print(review_url.format(str(item_id)))
    content = requests.get(review_url.format(str(item_id)), headers=headers).json()
    if "rgv587_flag" not in content:
        for item in content["model"]["items"]:
            if item["reviewContent"] is not None:
                review = item["reviewContent"]
                publish_message(kafka_producer, category, item_id, review)


if __name__ == '__main__':
    category = 'dien-thoai-di-dong'
    num_page = 50
    kafka_producer = connect_kafka_producer()
    ids = get_list_id(category_url,category, num_page)
    for id in ids:
        time.sleep(1)
        try:
            public_item_review(category, str(id))
        except:
            pass


