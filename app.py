from flask import Flask, request, jsonify, send_file
import os
import shutil
import subprocess
from flask_cors import CORS  # 导入 CORS

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持

# 定义路径
SOURCE_FOLDER = 'examples/sources'
OUTPUT_FOLDER = 'examples/outputs'

# 清空目录的函数
def clear_directory(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)  # 删除整个目录及其内容
    os.makedirs(folder)  # 重新创建空的目录

# 运行推理任务的函数
def run_inference():
    # 运行你的 main.py 进行推理
    subprocess.run(['python', 'main.py'])

# Flask 路由处理上传和推理
@app.route('/')
def home():
    return "Flask API is running. Go to /upload to upload an image."
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 清空 sources 和 outputs 目录
    clear_directory(SOURCE_FOLDER)
    clear_directory(OUTPUT_FOLDER)

    # 保存上传的图片到 sources 目录
    image_path = os.path.join(SOURCE_FOLDER, file.filename)
    file.save(image_path)

    # 运行推理
    run_inference()

    # 获取 outputs 目录中的推理结果图片
    output_files = os.listdir(OUTPUT_FOLDER)
    if not output_files:
        return jsonify({'error': 'No output generated'}), 500

    result_image_path = os.path.join(OUTPUT_FOLDER, output_files[0])

    # 返回推理结果图片
    return send_file(result_image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 确保 Flask 监听所有 IP 地址
