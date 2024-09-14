#本程序包含用于各项任务的提示词，由项目内其它程序调用，使用前需要在send函数填写自己使用的模型的api地址和api key。
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI

def send(system,user):
    client = OpenAI(api_key=" ", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content":system},
            {"role": "user", "content":user},
        ],
        stream=False
    )

    return(response.choices[0].message.content)

#总体设定
def setting(outline):
    output=send("你正在写一部长篇小说，根据以下概要，写出小说的总体设定：",outline)
    return(output)

def modify_setting(outline,setting,text):
    output=send("你正在写一部长篇小说，概要为："+outline+"总体设定为："+setting+"根据以下要求，对小说的设定进行修改：",text)
    return(output)

#所有章节的概要
def chapters(setting,num,outline):
    output=send("你正在写一部长篇小说，总体设定为："+setting+"小说分为"+num+"章，根据以下概要，写出每个章节的概要，不用写标题，每个章节的概要之前加序号，每个章节的概要内不要换行：",outline)
    return(output)

def modify_chapters(text,num,chapters):
    output=send("你正在写一部长篇小说，小说分为"+num+"章，以下为每个章节的概要："+chapters+"根据以下要求，对概要进行修改，不要更改排版：",text)
    return(output)

#确定小说标题
def title(setting,chapters):
    output=send("你正在写一部长篇小说，总体设定为："+setting+"各章节的概要为："+chapters,"根据以上内容确定小说标题回答的内容应当只包含标题，不包含其它内容。")
    return(output)

def modify_title(setting,chapters,title,text):
    output=send("你正在写一部长篇小说，总体设定为："+setting+"各章节的概要为："+chapters+"小说标题为："+title+"根据以下要求修改小说标题回答的内容应当只包含标题，不包含其它内容：",text)
    return(output)


#写各章节的提纲
def chapter_first(chapter_next,chapter_current):
    output=send("你正在写一部长篇小说，下一章概要为："+chapter_next+"当前章节概要为："+chapter_current,"当前章节为小说的第一章，根据以上信息，把当前章节分为5个部分，根据内容先后顺序分别写出提纲。每个部分的提纲应包含人物、地点、事件等信息，每个部分的提纲前加序号，每个部分的提纲内不要换行：")
    return(output)

def chapter_mid(chapter_last,chapter_next,chapter_current):
    output=send("你正在写一部长篇小说，上一章概要为："+chapter_last+"下一章概要为："+chapter_next+"当前章节概要为："+chapter_current,"当前章节为小说的第一章，根据以上信息，把当前章节分为5个部分，根据内容先后顺序分别写出提纲。每个部分的提纲应包含人物、地点、事件等信息，每个部分的提纲前加序号，每个部分的提纲内不要换行：")
    return(output)

def chapter_last(chapter_last,chapter_current):
    output=send("你正在写一部长篇小说，上一章概要为："+chapter_last+"当前章节概要为："+chapter_current,"当前章节为小说的最后一章，根据以上信息，把当前章节分为5个部分，根据内容先后顺序分别写出提纲。每个部分的提纲应包含人物、地点、事件等信息，每个部分的提纲前加序号，每个部分的提纲内不要换行：")
    return(output)

#写各章节正文
def context_first(outline_next,outline_current):
    output=send("你正在写一部长篇小说的一个章节的第一个部分，下一个部分概要为："+outline_next+"根据以下概要，写当前部分的内容并确保内容衔接：",outline_current)
    return(output)

def context_mid(last,outline_next,outline_current):
    output=send("你正在写一部长篇小说的一个章节的一个部分，上一个部分内容为："+last+"下一个部分概要为："+outline_next+"根据以下概要，写当前部分的内容并确保内容衔接：",outline_current)
    return(output)

def context_last(last,outline_current):
    output=send("你正在写一部长篇小说的一个章节的最后一个部分，上一个部分内容为："+last+"根据以下概要，写当前部分的内容并确保内容衔接：",outline_current)
    return(output)

#确定章节标题
def chapter_title(chapter):
    output=send("你正在写一部长篇小说，根据当前章节提纲，写出当前章节标题。回答的内容应当只包含标题，不包含其它内容：",chapter)
    return(output)
