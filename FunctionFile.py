def checkVoiceChannelFromMsg(msg, client):
    if (msg.author.id != client.user.id) and (msg.author.voice_channel):
        return True
    else:
        return False


def ConvertMsg(messagestring):
    replacedict = {'[':'',
                   ']': '',
                   '(': '',
                   ')': '',
                   '"': '',
                   "'": '',
                   ' ': '',
                   '{': '',
                   '}': '',
                   ',': '',
    }
    for i, j in replacedict.items():
        messagestring = messagestring.replace(i, j)
    messagestring = messagestring.lower()
    return messagestring


def cleantextList(listasstring):
    output = listasstring.replace("'",'').replace("]",'').replace("[",'').replace('"','')
    return output


def getSimpleAudioDict():
    SIMPLEAUDIOCONFIGFILE = open('sounds\SimpleAudio\SimpleAudioConfig.txt','r')
    SimpleAudioDict = {}
    SimpleAudioDict['audiofile'] = {}
    SimpleAudioDict['logword'] = {}
    SimpleAudioDict['chatresponse'] = {}

    for line in SIMPLEAUDIOCONFIGFILE:
        line = line.rstrip().split('\t')
        audiofilepath = line[0].replace("'",'')
        keywordlist = line[1].split(',')
        try:
            logword = line[2]
        except IndexError:
            print("Caution!!!!!!!!! - [" + audiofilepath + '\t' + str(keywordlist) + '] have no logword.\n')
        try:
            chatresponse = line[3]
        except:
            pass

        for keyword in keywordlist:
            keyword = ConvertMsg(keyword)
            SimpleAudioDict['audiofile'][keyword] = audiofilepath
            SimpleAudioDict['logword'][keyword] = logword
            try:
                SimpleAudioDict['chatresponse'][keyword] = chatresponse
            except:
                pass

    return SimpleAudioDict


def getSimpleAudioList():
    SIMPLEAUDIOCONFIGFILE = open('sounds\SimpleAudio\SimpleAudioConfig.txt','r')
    SimpleAudioList = []
    for line in SIMPLEAUDIOCONFIGFILE:
        line = line.rstrip().split('\t')
        keywordlist = line[1].split(',')

        for keyword in keywordlist:
            keyword = ConvertMsg(keyword)
            SimpleAudioList.append(keyword)

    return SimpleAudioList


def getrngAudioDict():
    RNGAUDIOCONFIGFILE = open('sounds\RNGAudio\RNGAudioConfig.txt','r')
    RngAudioDict = {}
    RngAudioDict['audiofile'] = {}
    RngAudioDict['logword'] = {}
    RngAudioDict['chatresponse'] = {}
    RngAudioDict['kicktable'] = {}

    for line in RNGAUDIOCONFIGFILE:
        line = line.rstrip().split('\t')
        audiofilepath = cleantextList(line[0]).split(',')
        keywordlist = line[1].split(',')
        try:
            logword = line[2]
        except IndexError:
            print("Caution!!!!!!!!! - [" + '\t' + str(keywordlist) + '] has no logword.\n')
        try:
            chatresponse = cleantextList(line[3]).split(',')
        except:
            print("Caution!!!!!!!!! - [" + '\t' + str(keywordlist) + '] has no chatresponse.\n')
        try:
            kicktable =  cleantextList(line[4]).split(',')
        except:
            print("Caution!!!!!!!!! - [" + '\t' + str(keywordlist) + '] has no KickTable.\n')

        if len(audiofilepath) != len(chatresponse):
            print("!!!!WARNING!!!\taudiofilepath length != chatresponse length")
        if len(audiofilepath) != len(kicktable):
            print("!!!!WARNING!!!\taudiofilepath length != kicktable length")

        for keyword in (keywordlist):
            keyword = ConvertMsg(keyword)
            RngAudioDict['audiofile'][keyword] = audiofilepath
            RngAudioDict['logword'][keyword] = logword
            RngAudioDict['chatresponse'][keyword] = chatresponse
            RngAudioDict['kicktable'][keyword] = kicktable

    return RngAudioDict


def getRngAudioList():
    RNGAUDIOCONFIGFILE = open('sounds\RNGAudio\RNGAudioConfig.txt', 'r')
    RngAudioList = []
    for line in RNGAUDIOCONFIGFILE:
        line = line.rstrip().split('\t')
        keywordlist = line[1].split(',')

        for keyword in keywordlist:
            keyword = ConvertMsg(keyword)
            RngAudioList.append(keyword)

    return RngAudioList

#def checkSimpleAudioFiles: