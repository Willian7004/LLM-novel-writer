import os
import threading
import time
import api

# 创建文件夹的函数
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# 读取文件内容
def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    return ""

# 保存文件内容
def save_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 线程执行的函数
def thread_function(seq):
    part = 1
    last = ""
    while part <= 5:
        chapter_folder = os.path.join("chapter", str(seq))
        create_folder_if_not_exists(chapter_folder)
        
        outline_current_file = os.path.join(chapter_folder, f"{part}.txt")
        outline_current = read_file(outline_current_file)
        
        outline_next = ""
        if part < 5:
            outline_next_file = os.path.join(chapter_folder, f"{part + 1}.txt")
            outline_next = read_file(outline_next_file)
        
        if part == 1:
            last = api.context_first(outline_next, outline_current)
        elif 1 < part < 5:
            last = api.context_mid(last, outline_next, outline_current)
        elif part == 5:
            last = api.context_last(last, outline_current)
        
        context_folder = os.path.join("context", str(seq))
        create_folder_if_not_exists(context_folder)
        
        context_file = os.path.join(context_folder, f"{part}.txt")
        save_file(context_file, last)
        
        part += 1

# 主程序
def main():
    setting_folder = "setting"
    create_folder_if_not_exists(setting_folder)
    
    num_file = os.path.join(setting_folder, "num.txt")
    num_str = read_file(num_file)
    num = int(num_str) if num_str.isdigit() else 1
    
    seq = 1
    threads = []
    
    while seq <= num:
        thread = threading.Thread(target=thread_function, args=(seq,))
        threads.append(thread)
        thread.start()
        seq += 1
        time.sleep(0.1)
        
        if len(threads) >= 64:
            for thread in threads:
                thread.join()
            threads = []
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
