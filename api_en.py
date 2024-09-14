#This procedure contains prompt words for each task, called by other procedures within the project, before using the send function you need to fill in the api address and api key of the model you use.
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

#Overall setting
def setting(outline):
    output=send("You are writing a full-length novel, and based on the following outline, write the general setting of the novel:",outline)
    return(output)

def modify_setting(outline,setting,text):
    output=send("You are writing a full-length novel, outlined as:"+outline+"Overall setting as:"+setting+"Revise the setting of the novel according to the following requirements:",text)
    return(output)

#Summary of all chapters
def chapters(setting,num,outline):
    output=send("You are writing a full-length novel with the overall setting:"+setting+"the novel contains"+num+"chapters,Based on the following summary, write a summary of each section without headings, precede each section summary with a serial number, and do not break lines within each section summary:",outline)
    return(output)

def modify_chapters(text,num,chapters):
    output=send("You are writing a full-length novel,the novel contains"+num+"chapters，below is a summary of each chapter:"+chapters+"Make changes to the synopsis according to the following requirements; do not change the typography:",text)
    return(output)

#Confirm the title of the novel
def title(setting,chapters):
    output=send("You are writing a full-length novel with the overall setting:"+setting+"The chapters are summarised as:"+chapters,"Determine the title of the novel based on the above, and the answer should contain only the title and nothing else.")
    return(output)

def modify_title(setting,chapters,title,text):
    output=send("You are writing a full-length novel with the overall setting:"+setting+"The chapters are summarised as:"+chapters+"the title of the novel is:"+title+"Determine the title of the novel based on the above, and the answer should contain only the title and nothing else.",text)
    return(output)


#Write outlines of chapters
def chapter_first(chapter_next,chapter_current):
    output=send("You're writing a full-length novel and the next chapter is outlined as:"+chapter_next+"The current chapter summary is:"+chapter_current,"The current chapter is the first chapter of the novel. Based on the above information, divide the current chapter into five parts and write outlines for each according to the order of content. The outline for each part should contain information about characters, places, events, etc. The outline for each part should be preceded by a serial number, and there should be no line breaks within each part of the outline:")
    return(output)

def chapter_mid(chapter_last,chapter_next,chapter_current):
    output=send("You're writing a full-length novel and the last chapter is outlined as:"+chapter_last+"The outline of the next chapter is:"+chapter_next+"The current chapter summary is:"+chapter_current,"Based on the above information, divide the current chapter into five parts and write outlines for each according to the order of content. The outline for each part should contain information about characters, places, events, etc. The outline for each part should be preceded by a serial number, and there should be no line breaks within each part of the outline:")
    return(output)

def chapter_last(chapter_last,chapter_current):
    output=send("You're writing a full-length novel and the last chapter is outlined as:"+chapter_last+"The current chapter summary is:"+chapter_current,"The current chapter is the last chapter of the novel. Based on the above information, divide the current chapter into five parts and write outlines for each according to the order of content. The outline for each part should contain information about characters, places, events, etc. The outline for each part should be preceded by a serial number, and there should be no line breaks within each part of the outline:")
    return(output)

#Write the body of the chapters
def context_first(outline_next,outline_current):
    output=send("You are writing the first part of a chapter of a long novel, and the next part is outlined as:"+outline_next+"Based on the following outline, write the current section and ensure that the content is articulated:",outline_current)
    return(output)

def context_mid(last,outline_next,outline_current):
    output=send("You are writing one part of a chapter of a long novel, and the previous part reads:"+last+"The next section is outlined as:"+outline_next+"Based on the following outline, write the current section and ensure that the content is articulated:",outline_current)
    return(output)

def context_last(last,outline_current):
    output=send("You are writing the last part of a chapter of a long novel, and the previous part reads:"+last+"Based on the following outline, write the current section and ensure that the content is articulated:",outline_current)
    return(output)

#Confirm the section headings
def chapter_title(chapter):
    output=send("You are writing a full-length novel, write the current chapter title based on the current chapter outline. The answer should contain only the title and nothing else:",chapter)
    return(output)
