import requests
import uuid
import pathlib
import json
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import configparser

config = configparser.ConfigParser()
config.read("config.conf")

mime_types = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "bmp": "image/bmp",
    "webp": "image/webp"
}

photo_uuid = None
file_path = None
fileext = None
mime_type = None

def func1():
    url = "https://miniapp.wps.cn/api/v1/file/get-photo-url?open_id=o0T4b0UCKHuLPcXVSKlLruDyZfpQ"
    headers = {
        "Host": "miniapp.wps.cn",
        "Connection": "keep-alive",
        "xweb_xhr": "1",
        "cookie": f"wps_sid={config['Account']['wps_sid']};",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxe66629a225dbd0ef/130/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    with open(file_path, "rb") as file:
        files = {
            "file": (f"{photo_uuid}.{fileext}", file, mime_type)
        }
        response = requests.post(url, headers=headers, files=files)
    return response.json()["data"]["photoUrl"]

def func2(photourl):
    url = "https://miniapp.wps.cn/api/v1/wx/commit"
    headers = {
        "Host": "miniapp.wps.cn",
        "Connection": "keep-alive",
        "sid": config['Account']['wps_sid'],
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275",
        "Client-Ver": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "xweb_xhr": "1",
        "Client-Chan": "1",
        "Client-Type": "wps-wxapp",
        "Client-Lang": "zh-CN",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxe66629a225dbd0ef/130/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    task_params = {
        "size": pathlib.Path(file_path).stat().st_size,
        "sourcefileurl": photourl,
        "uploadadd": ["应用", "图片转表格"],
        "sourcefileext": "png",
        "filename": str(photo_uuid)
    }
    data = {
        "service": "pic2xlsx",
        "formid": "undefined",
        "task_params": json.dumps(task_params),
        "file_urls": json.dumps([photourl])
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()['data']['id']

def func3(xlsx_id):
    url = f"https://dcapi3.wps.cn/api/v4/query/{xlsx_id}"
    headers = {
        "Host": "dcapi3.wps.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275",
        "Client-Ver": "1",
        "Content-Type": "application/json",
        "xweb_xhr": "1",
        "Cookie": f"wps_sid={config['Account']['wps_sid']}",
        "Client-Chan": "1",
        "Client-Type": "wps-wxapp",
        "Client-Lang": "zh-CN",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxe66629a225dbd0ef/130/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    response = requests.get(url, headers=headers)
    while response.json()['progress'] != 100:
        sleep(1)
        response = requests.get(url, headers=headers)
    return response.json()['resp']['files']['files'][0]['fileInfo']['fileid']

def func4(fileid):
    url = f"https://www.kdocs.cn/api/v3/office/file/{fileid}/download"
    headers = {
        "Host": "www.kdocs.cn",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.kdocs.cn/latest",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": config["Account"]["kdocs_cookie"]
    }
    response = requests.get(url, headers=headers)
    return response.json()['download_url']

def func5(download_url):
    response = requests.get(download_url)
    if not pathlib.Path(config["Directory"]["xlsx_dir"]).exists():
        pathlib.Path(config["Directory"]["xlsx_dir"]).mkdir()
    with open(f'{config["Directory"]["xlsx_dir"]}/{photo_uuid}.xlsx', "wb") as file:
        file.write(response.content)

def pic_to_xlsx(fp):
    global photo_uuid, file_path, fileext, mime_type
    photo_uuid = uuid.uuid4()
    file_path = fp
    fileext = pathlib.Path(file_path).suffix.lstrip(".").lower()
    mime_type = mime_types.get(fileext, "image/png")
    pic = func1()
    xlsx_id = func2(pic)
    fileid = func3(xlsx_id)
    download_url = func4(fileid)
    func5(download_url)
    return f"{config['Directory']['xlsx_dir']}/{photo_uuid}.xlsx"

if __name__ == "__main__":
    photo_uuid = uuid.uuid4()
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(initialdir=os.path.dirname(__file__), title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")])
    root.destroy()
    if not file_path:
        print("No file selected. Exiting...")
        exit()
    fileext = pathlib.Path(file_path).suffix.lstrip(".").lower()
    mime_type = mime_types.get(fileext, "image/png")
    pic = func1()
    # pic = "769918db307b49a8aca2d7a5be3c52ba"
    print("pic:", pic)
    xlsx_id = func2(pic)
    # xlsx_id = "673ac2490712c1001fd5245dwl"
    print("xlsx_id:", xlsx_id)
    fileid = func3(xlsx_id)
    print("fileid:", fileid)
    download_url = func4(fileid)
    print("download_url:", download_url)
    func5(download_url)