


from aip import AipOcr
import time
import requests
import os
import pandas as pd


APP_ID = '11667470'
API_KEY = 'SFT15tT0Mc1VSNhHefTRxzXQ'
SECRET_KEY = 'yCHr7bcLZM9I53n4U4Z9oPwHvR2X7BcE'



client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def ocr_general(image_path):
    #image_path = '../upload/p1.jpg'
    beginTime = time.time()
    [dirname, filename] = os.path.split(image_path)
    ext = filename.rsplit('.', 1)[1]  # 获取文件后缀
    name_ = filename.rsplit('.', 1)[0]  # name
    to_path = dirname + '/excel/' + name_ + '.xls'
    ##to_pathz = dirname + '/excel_down/' + name_ + '.xls'
    #to_pathz = '/static/download/' + name_ + '.xls'
    #pathx = os.path.dirname(os.path.dirname(dirname))
    #to_pathz = pathx + '//static//abc.xls'
    to_pathz =  'static/download/' + name_ + '.xls'
    info = {}
    info['name'] = name_
    info['dir'] = to_pathz
    #print(info)

    result = img_to_str(image_path)  ##############################
    # for i in result["result"]["result_data"]:
    #     print(i)
    # print(result["result"]["result_data"])
    #print(result)
    #resultx = result
    requestId = result["result"]["request_id"] ###########################
    print(requestId)
    #time.sleep(2)
    #requestId =  '11667470_493393'  #####################
    ########
    # requestId = "23454320-23255"
    # requestId = result["result"]["request_id"]
    # client.getTableRecognitionResult(requestId);
    # options = {}
    # options["result_type"] = "json"
    # client.getTableRecognitionResult(requestId, options)
    ###########

    result2 = client.getTableRecognitionResult(requestId)
    # result2 = client.getTableRecognitionResult('11667470_432287')
    #print(result2)
    Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 1')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 2')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 3')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 4')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 5')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 6')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 7')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    if Url == '':
        print('if get id 8')
        time.sleep(2)
        result2 = client.getTableRecognitionResult(requestId)
        Url = result2["result"]["result_data"]
    print('----------------------------')
    print(Url)
    print('----------------------------')
    endTime = time.time()
    # print('# MAPPINFG: '+str(round(endTime - beginTime,4))+'s' )
    print('# ocr Done ', end='')
    print(str(round(endTime - beginTime, 4)) + 's')

    #print('----------------')
    r = requests.get(Url)
    with open(to_path, "wb") as f:
        f.write(r.content)
    f.close()
    zendTime = time.time()
    print('# to_excel Done  ', end='')
    print(str(round(zendTime - endTime, 4)) + 's')

    #### 转换excel
    data_header = pd.read_excel(to_path, 'header')
    data_body = pd.read_excel(to_path, 'body')
    data_footer = pd.read_excel(to_path, 'footer')

    # data_header2 = pd.read_excel(to_path,sheetname = 'header')

    # 处理表头
    # 字符串进行合并，去重，再比较
    def Qc(s):
        ss = set(s)
        ss = list(set(s))
        ss.sort(key=s.index)
        return ''.join(ss)

    yhead = list(data_body.columns)
    if len(yhead) == 6 or len(yhead) == 8:
        cz = int(len(yhead) / 2)
        bhead = list(range(len(yhead)))
        for i in range(cz):
            stt = yhead[i] + yhead[i + cz]
            Stt = Qc(stt)
            # print(Stt)
            if '项目' in Stt or '目' in Stt or '项' in Stt:
                bhead[i] = '项目'
            elif '科目' in Stt or '科' in Stt:
                bhead[i] = '科目'
            elif '行次' in Stt or '行' in Stt or '次' in Stt:
                bhead[i] = '行次'
            elif '本期余额' in Stt:
                bhead[i] = '本期余额'
            elif '本期金额' in Stt:
                bhead[i] = '本期金额'
            elif '年初余额' in Stt:
                bhead[i] = '年初余额'
            elif '期末余额' in Stt:
                bhead[i] = '期末余额'
            elif '上期金额' in Stt:
                bhead[i] = '上期金额'
            elif '累计' in Stt:
                bhead[i] = '累计金额'
            else:
                bhead[i] = Stt
            bhead[i + cz] = bhead[i]

        data_body.columns = bhead

    writer = pd.ExcelWriter(to_pathz)
    data_body.to_excel(writer, sheet_name='body', index=False)
    data_header.to_excel(writer, sheet_name='header', index=False)
    data_footer.to_excel(writer, sheet_name='footer', index=False)
    writer.save()

    #print("Done!!!")
    #print(info)
    return info





def img_to_str(image_path):
    #print('# begin.. ', end='')
    image = get_file_content(image_path)
    # result = client.basicGeneral(image)

    options = {}
    # options["result_type"] = "json"
    result = client.tableRecognition(image, options)
    # result = client.form(image);
    # if 'words_result' in result:
    #    return '\n'.join([w['words'] for w in result['words_result']])
    return result


# image_path = 'D:\\ocr_test\\IMAGE\\bb\\5.png'
# to_path = "D:\ocr_test\ceshi\\OCR_TEST_5.xls"
