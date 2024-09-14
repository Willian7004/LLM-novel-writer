import os
import re
import threading
import time
import api  # 假设api.py文件在当前目录下

# 定义全局变量
seq = 1
num = 0
setting = ""
chapter_current = ""
chapter_last = ""
chapter_next = ""
chapter = ""

# 读取文件内容
def read_file(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 保存文件内容
def save_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 获取文件名中的整数
def get_file_number(file_name):
    match = re.match(r'(\d+)', file_name)
    return int(match.group(1)) if match else 0

# 处理每个seq的线程函数
def process_seq(seq):
    global chapter_current, chapter_last, chapter_next, chapter

    # 读取当前、上一个和下一个章节的内容
    outline_files = [f for f in os.listdir('outline') if f.endswith('.txt')]
    outline_files.sort(key=get_file_number)

    for file_name in outline_files:
        file_number = get_file_number(file_name)
        if file_number == seq:
            chapter_current = read_file(os.path.join('outline', file_name))
        elif file_number == seq - 1:
            chapter_last = read_file(os.path.join('outline', file_name))
        elif file_number == seq + 1:
            chapter_next = read_file(os.path.join('outline', file_name))

    # 调用相应的函数
    if seq == 1:
        chapter = api.chapter_first(chapter_next, chapter_current)
    elif seq > 1 and seq < num:
        chapter = api.chapter_mid(chapter_last, chapter_next, chapter_current)
    elif seq == num:
        chapter = api.chapter_last(chapter_last, chapter_current)

    # 保存标题
    title_content = api.chapter_title(chapter)
    title_folder = 'title'
    if not os.path.exists(title_folder):
        os.makedirs(title_folder)
    save_file(os.path.join(title_folder, f'{seq}.txt'), title_content)

    # 保存章节内容
    chapter_folder = os.path.join('chapter', str(seq))
    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)
    chapter_parts = chapter.split('\n')
    for part in chapter_parts:
        part_number = re.match(r'(\d+)', part)
        if part_number:
            part_number = part_number.group(1)
            save_file(os.path.join(chapter_folder, f'{part_number}.txt'), part)

# 主函数
def main():
    global seq, num, setting

    # 读取setting和num
    setting = read_file(os.path.join('setting', 'setting.txt'))
    num = int(read_file(os.path.join('setting', 'num.txt')))

    # 创建线程并处理每个seq
    threads = []
    while seq <= num:
        if len(threads) >= 64:
            for t in threads:
                t.join()
            threads = []
        thread = threading.Thread(target=process_seq, args=(seq,))
        threads.append(thread)
        thread.start()
        seq += 1
        time.sleep(0.1)

    # 等待所有线程完成
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
