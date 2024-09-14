import os
import re
import glob
import api

# Step 1: Initialise variables
seq = 1
part = 1
result = ""

# Read the num.txt file in the setting folder
setting_folder = "setting"
num_file = os.path.join(setting_folder, "num.txt")
if not os.path.exists(setting_folder):
    os.makedirs(setting_folder)
if not os.path.exists(num_file):
    with open(num_file, 'w', encoding='utf-8') as f:
        f.write("0")

with open(num_file, 'r', encoding='utf-8') as f:
    num = int(f.read().strip())

# Step 2: Process the txt file in the title folder
title_folder = "title"
if not os.path.exists(title_folder):
    os.makedirs(title_folder)

for title_file in glob.glob(os.path.join(title_folder, "*.txt")):
    with open(title_file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^"|"$|^《|》$', '', content)
    with open(title_file, 'w', encoding='utf-8') as f:
        f.write(content)

# Step 3: Process the txt file in the context folder
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

# Step 4: Repeat steps 5 to 7 until seq=num
while seq <= num:
    # Step 5: Read the txt file with filename=seq in the title folder
    title_file = os.path.join(title_folder, f"{seq}.txt")
    if os.path.exists(title_file):
        with open(title_file, 'r', encoding='utf-8') as f:
            title = f.read().strip()
        chapter_title = f"chapter{seq} {title}"
    else:
        chapter_title = f"chapter{seq} no title"

    # Step 6: Read the txt file with filename=seq in the context folder
    context_file = os.path.join(context_folder, f"{seq}.txt")
    if os.path.exists(context_file):
        with open(context_file, 'r', encoding='utf-8') as f:
            context = f.read().strip()
    else:
        context = "no context"

    # Step 7: Connect chapter_title and context to result string
    result += chapter_title + "\n" + context + "\n\n"

    # Increase the value of seq
    seq += 1

# Step 8: Write the result string to a txt file named after the title.txt content.
title_file = os.path.join(title_folder, "title.txt")
if os.path.exists(title_file):
    with open(title_file, 'r', encoding='utf-8') as f:
        file_name = f.read().strip()
else:
    file_name = "output"

output_file = f"{file_name}.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"The results have been saved to {output_file}")