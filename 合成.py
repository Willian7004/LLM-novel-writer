import os
import re
import glob
import api

# 步骤1：初始化变量
seq = 1
part = 1
result = ""

# 读取setting文件夹中的num.txt文件
setting_folder = "setting"
num_file = os.path.join(setting_folder, "num.txt")
if not os.path.exists(setting_folder):
    os.makedirs(setting_folder)
if not os.path.exists(num_file):
    with open(num_file, 'w', encoding='utf-8') as f:
        f.write("0")

with open(num_file, 'r', encoding='utf-8') as f:
    num = int(f.read().strip())

# 步骤2：处理title文件夹中的txt文件
title_folder = "title"
if not os.path.exists(title_folder):
    os.makedirs(title_folder)

for title_file in glob.glob(os.path.join(title_folder, "*.txt")):
    with open(title_file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^"|"$|^《|》$', '', content)
    with open(title_file, 'w', encoding='utf-8') as f:
        f.write(content)

# 步骤3：处理context文件夹中的txt文件
context_folder = "context"
if not os.path.exists(context_folder):
    os.makedirs(context_folder)

for folder in glob.glob(os.path.join(context_folder, "[0-9]*")):
    if os.path.isdir(folder):
        folder_name = os.path.basename(folder)
        combined_content = ""
        for txt_file in sorted(glob.glob(os.path.join(folder, "*.txt")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0])):
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            content = re.sub(r'^#.*\n.*\n', '', content)
            content = re.sub(r'\n{2,}', '\n', content)
            combined_content += content
        output_file = os.path.join(context_folder, f"{folder_name}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(combined_content)

# 步骤4：重复执行第5到第7步，直到seq=num
while seq <= num:
    # 步骤5：读取title文件夹中文件名=seq的txt文件
    title_file = os.path.join(title_folder, f"{seq}.txt")
    if os.path.exists(title_file):
        with open(title_file, 'r', encoding='utf-8') as f:
            title = f.read().strip()
        chapter_title = f"第{seq}章 {title}"
    else:
        chapter_title = f"第{seq}章 无标题"

    # 步骤6：读取context文件夹中文件名=seq的txt文件
    context_file = os.path.join(context_folder, f"{seq}.txt")
    if os.path.exists(context_file):
        with open(context_file, 'r', encoding='utf-8') as f:
            context = f.read().strip()
    else:
        context = "无内容"

    # 步骤7：连接chapter_title和context到result字符串
    result += chapter_title + "\n" + context + "\n\n"

    # 增加seq的值
    seq += 1

# 步骤8：将result字符串写入以title.txt内容命名的txt文件
title_file = os.path.join(title_folder, "title.txt")
if os.path.exists(title_file):
    with open(title_file, 'r', encoding='utf-8') as f:
        file_name = f.read().strip()
else:
    file_name = "output"

output_file = f"{file_name}.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"结果已保存到 {output_file}")
