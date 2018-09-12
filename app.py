#encoding:utf8
from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request,send_from_directory
import time
import os
import base64
import datetime
import ocr.ocr_image as ocr_te

app = Flask(__name__)
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png','jpg','JPG','PNG','HEIF','heif','JPEG','jpeg','RAW','raw','DNG','dng','BMP','bmp'])

from aip import AipOcr
APP_ID = '11693548'
API_KEY = 'DXeZodLasHpoK6pSLhrow4Lt'
SECRET_KEY = '6xc52me6D1P5sS9WeeZauG6xjedWVSPw'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def ocr_general(image_path):
    #image_path = '../upload/p1.jpg'
    image = get_file_content(image_path)
    # result = client.basicGeneral(image)
    # result = client.basicAccurate(image)  # 调用通用文字识别（高精度版）
    result = client.general(image)# 调用通用文字识别（含位置信息版）
    return result

def array_txt(result):
    arr_txt = []
    for item in result['words_result']:
        arr_txt.append(item['words'])
    return  arr_txt

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

# 用于测试上传，稍后用到
@app.route('/',methods=['GET'],strict_slashes=False)
def indexpage():
    # return render_template('index.html')
    return render_template('index.html')


# 上传文件
@app.route('/',methods=['POST'],strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        #print(fname)
        print((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' --> '+fname))
        ext = fname.rsplit('.',1)[1]  # 获取文件后缀
        name_ = fname.rsplit('.', 1)[0]  # name
        unix_time = int(time.time())
        new_filename = str(unix_time) + '_' +name_+'.'+ext  # 修改了上传的文件名
        #new_filename = '12'+'.'+ ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir,new_filename))  #保存文件到upload目录
        # f.save(os.path.join(file_dir, fname))
        #encodestr = base64.b64encode(new_filename.encode('utf-8'))
        #token = str(encodestr,'utf-8')
        # print(str(base64.b64decode(encodestr), 'utf-8'))
        #print(new_filename+' --> '+token)

        image_path = 'upload/' + new_filename
        #result = ocr_general(image_path)
        result = ocr_te.ocr_general(image_path)
        #info = array_txt(result)
        print('Done!!!')
        # return jsonify({"errno":0, "msg":"succeed ","token":token})
        #return '找不到用户信息'
        #return jsonify({"errno": 0, "msg": "succeed "})

        return render_template('Result.html', info=result)
    else:
        return jsonify({"errno": 1001, "errmsg": u"failed: Only supports image format"})


if __name__ == '__main__':
    app.run(debug=True, port=8999)