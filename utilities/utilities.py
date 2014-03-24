#html page encoding
encoding = 'utf-8'
#encoding = None
def getEncoding(content):
    if encoding is None:
        import chardet
        return chardet.detect(content)['encoding']
    else:
        return encoding
