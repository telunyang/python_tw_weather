import matplotlib
import matplotlib.pyplot as plt
import requests, sys, urllib3
from requests.exceptions import ConnectionError

matplotlib.matplotlib_fname()

# 取消錯誤訊息
urllib3.disable_warnings()

# 標題中文字型問題
# 請參考 https://www.zhihu.com/question/25404709

# 取得天氣資料
def getWeatherData(data_id, district):
    dict_headers = {
        'Authorization': 'your-authorization-key-from-cwb',
        'Content-type': 'application/json',
    }
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/' + data_id + '?locationName=' + district + '&elementName=T&format=json&sort=time'
    response = requests.get(url, headers = dict_headers, stream = True, allow_redirects = True, verify = False)
    response.encoding = 'utf-8'
    return response.json()

# 繪製圖表
def drawChart():
    # x 軸文字集合
    list_xticks = []
    
    # x 軸資料集合
    list_x = []
    
    # y 軸資料集合
    list_y = []
    
    # 參數設定(用在 Request 的 URL 字串)
    # 請參考 http://opendata.cwb.gov.tw/usages 網頁
    # 但其實看中央氣象局給的文件最快: http://opendata.cwb.gov.tw/opendatadoc/CWB_Opendata_API_V1.2.pdf
    city_data_id = 'F-D0047-067' # 市代號 eg.F-D0047-063
    district = '六龜區' # 區代號 (這裡中央氣象局用中文當作代號，我就不予置評了…)
    
    # 取得天氣資料
    obj = getWeatherData(city_data_id, district)
    
    # 市
    print(obj['records']['locations'][0]['locationsName'])
    city = obj['records']['locations'][0]['locationsName']
    
    # 區
    print(obj['records']['locations'][0]['location'][0]['locationName'])
    
    # 類別(這個要再了解一下，有 T, PoP ... 等)
    type = obj['records']['locations'][0]['location'][0]['weatherElement'][0]['elementName']
    
    # 溫度單位(預設 C)
    unit = obj['records']['locations'][0]['location'][0]['weatherElement'][0]['elementMeasure']
    
    # 圖表標籤
    label = obj['records']['locations'][0]['datasetDescription']
    
    # 計算 time 元素的數量
    count_time = len(obj['records']['locations'][0]['location'][0]['weatherElement'][0]['time'])
    
    print('時間數量: ' + str(count_time))
    
    for index, t in enumerate(obj['records']['locations'][0]['location'][0]['weatherElement'][0]['time']):
        print('row number: ' + str(index))
        print('起始時間: ' + t['startTime'])
        print('結束時間: ' + t['endTime'])
        print('溫度 (單位:' + unit + '): ' + t['elementValue'])
        print()
        
        # 用迴圈來累計 x 軸的值，以便繪線
        list_x.append(index)
        
        # 對應 y 軸的溫度數值
        list_y.append(t['elementValue'])
        
        # 設定 x 軸要顯示的文字，來取代數值
        list_xticks.append(t['startTime'] + '\n' + t['endTime'])
    
    # 圖片輸出大小
    fig_size = (16, 13)
    plt.rcParams["figure.figsize"] = fig_size
    
    # 讓圖表有格子
    plt.grid(True)
    
    # 設置圖片
    plt.plot(list_x, list_y, label = district)
    
    # 限定 y 軸數值範圍
    plt.ylim(0, 50)
    
    # 讓 label 顯示
    plt.legend()
    
    # x 軸標題
    plt.xlabel('時間週期 (年-月-日 時:分:秒)')
    
    # x 軸文字 (取代數字)
    plt.xticks(list_x, list_xticks)
    
    # x 軸文字旋轉 90 度
    plt.xticks(rotation = 90, fontsize = 8)

    # y 軸標題
    plt.ylabel('溫度 (單位:C)')
    
    # 圖片主要標題(Title)
    plt.title(label)
    
    # 輸出圖片
    #plt.show()
    
    # 儲存圖片到 images 資料夾
    plt.savefig('images/' + city + district + '.png', dpi = 150)
    

try:
    # 繪製圖表
    drawChart()
    
except ConnectionError:
    print('ConnectionError: \n', sys.exc_info())