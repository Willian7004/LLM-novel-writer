import os
import api

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def read_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    # Step 1: Input outline and number of chapters
    print("Enter summary and number of chapters")
    input_data = input().strip()
    outline, num = input_data.split(maxsplit=1)
    num = int(num)

    ensure_directory_exists('outline')
    ensure_directory_exists('setting')

    save_to_file('outline/outline.txt', outline)
    save_to_file('setting/num.txt', str(num))

    # Step 2: Call setting function
    setting_str = api.setting(outline)
    print(setting_str)
    save_to_file('setting/setting.txt', setting_str)

    # Step 3: Modify setting if needed
    while True:
        print("Enter y to confirm or enter changes")
        user_input = input().strip()
        if user_input.lower() == 'y':
            break
        setting_str = api.modify_setting(outline, setting_str, user_input)
        print(setting_str)
        save_to_file('setting/setting.txt', setting_str)

    # Step 4: Call chapters function
    chapters_str = api.chapters(setting_str, str(num), outline)
    print(chapters_str)
    save_to_file('outline/chapters.txt', chapters_str)

    # Step 5: Modify chapters if needed
    while True:
        print("Enter y to confirm or enter changes")
        user_input = input().strip()
        if user_input.lower() == 'y':
            break
        chapters_str = api.modify_chapters(user_input, str(num), chapters_str)
        print(chapters_str)
        save_to_file('outline/chapters.txt', chapters_str)

    # Step 6: Save chapters to individual files
    chapters_list = chapters_str.split('\n')
    for chapter in chapters_list:
        if chapter:
            chapter_num = chapter.split()[0]
            save_to_file(f'outline/{chapter_num}.txt', chapter)

    # Step 7: Call title function
    title_str = api.title(setting_str, chapters_str)
    print(title_str)
    ensure_directory_exists('title')
    save_to_file('title/title.txt', title_str)

    # Step 8: Modify title if needed
    while True:
        print("Enter y to confirm or enter changes")
        user_input = input().strip()
        if user_input.lower() == 'y':
            break
        title_str = api.modify_title(setting_str, chapters_str, title_str, user_input)
        print(title_str)
        save_to_file('title/title.txt', title_str)

if __name__ == "__main__":
    main()
