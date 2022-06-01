import re
import requests


# 去除文件名中的特殊字符
def fixname(filename):
    character = r'[?*/\|:><]'
    filename = re.sub(character, "", filename)  # 用正则表达式去除windows下的特殊字符，这些字符不能用在文件名
    return filename


# 爬取主程序
def crawl_main():
    while 1:
        number = input('-------请在此粘贴您的分享链接------\n')

        # 请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; ''Nexus 5 Build/MRA58N) AppleWebKit/537.36 ('
                                 'KHTML, '
                                 'like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
                   'referer': 'https://www.douyin.com/'}
        try:
            number_ = re.findall('douyin.com/(.*?)/', number)[0]  # 匹配粘贴目标包含的抖音视频id
        except Exception as e:
            print('粘贴链接错误,未匹配!!!\n', e)
            continue

        url = f'https://v.douyin.com/{number_}/'

        response = requests.head(url=url, headers=headers)
        url_1 = response.headers['location']  # 获取真实的视频源地址
        uid = re.findall('video/(.*?)/', url_1)[0]  # 获得抖音视频对应的唯一视频id
        src_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={uid}'

        response_src = requests.get(url=src_url, headers=headers).json()

        if response_src["item_list"][0]["images"] is None:
            print('您粘贴的是抖音视频资源')
            video_content = response_src["item_list"][0]["video"]["play_addr"]["url_list"][0]  # 获取抖音视频的直接地址
            video_name = response_src["item_list"][0]["desc"]  # 获取视频名称
            video_name_fix = fixname(video_name)  # 修复(去除)windows下非法的字符

            video_content_rmwm = video_content.replace("playwm", "play", 1)  # 链接去水印
            print('下载中.......')
            video_response = requests.get(url=video_content_rmwm, headers=headers, stream=True)  # 获取视频的数据流

            with open(f'{video_name_fix}.mp4', 'wb') as f:  # 存入当前目录
                for i in video_response.iter_content(10000):  # 边下边存入硬盘
                    f.write(i)
            print('下载完成!!!\n')
        else:
            print('您粘贴的是抖音图集资源')
            list_url = []  # 图片的url列表
            list_src = response_src["item_list"][0]["images"]  # 图片的信息列表
            for i in list_src:
                url_l = i['url_list'][3]
                list_url.append(url_l)
            count = 0
            for i in list_url:

                images_response = requests.get(url=i, headers=headers, stream=True)  # 获取图集的数据流
                with open(f'{count}.jpeg', 'wb') as f:
                    for b in images_response.iter_content(10000):
                        f.write(b)
                count = count + 1
                print(f'图{count}下载完成!')
            print('图集下载完毕')


if __name__ == '__main__':
    try:
        crawl_main()
    except KeyboardInterrupt:
        print('程序异常\n')
    else:
        print('程序运行正常.....\n')
