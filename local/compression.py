import subprocess

def video():
    pass

def image():
    pass

def gif():
    pass

def text(textList):
    text = textList[0]
    textList.clear()

    while len(text) > 1900:
        textList.append(text[0:1900])
        text = text[1900:]

    textList.append(text)