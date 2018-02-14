import sys, os, shutil

RngAudioNewText = open('RNGAudioConfigNew.txt', 'w+')

FileList = []

for line in open('RNGAudioConfig.txt'):
    line = line.split('\t')
    audiofilepathList = line[0].replace("'",'').replace("]",'').replace("[",'').split(',')
    RNGFolder = line[2].replace(' ','').replace("'",'')

    if not os.path.exists('G:/DiscordBot/ErniesChairPy/sounds/RNGAudio/' + RNGFolder):
        os.makedirs('G:/DiscordBot/ErniesChairPy/sounds/RNGAudio/' + RNGFolder)

    reportline = ''
    newaudiofilepathList = []
    for audiofilepath in audiofilepathList:
        newaudiofilepathList.append('G:/DiscordBot/ErniesChairPy/sounds/RNGAudio/' + RNGFolder + "/" + os.path.basename(audiofilepath))
        shutil.copy2(audiofilepath, 'G:/DiscordBot/ErniesChairPy/sounds/RNGAudio/' + RNGFolder + "/" + os.path.basename(audiofilepath))


    reportline = '\t'.join([str(newaudiofilepathList), line[1], line[2], line[3], line[4]])
    RngAudioNewText.write(reportline)
#    reportline = ''
#    if audiofilepathsubfolder == '':
#        shutil.copy2(audiofilepath, 'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + os.path.basename(audiofilepath))
#        reportline = '\t'.join(["'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/'" + os.path.basename(audiofilepath), line[1], line[2]])
#    else:
#        if not os.path.exists('G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + audiofilepathsubfolder):
#            os.makedirs('G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + audiofilepathsubfolder)
#        shutil.copy2(audiofilepath, 'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + audiofilepathsubfolder + '/' + os.path.basename(audiofilepath))
#        reportline = '\t'.join(["'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/'" + audiofilepathsubfolder + '/' + os.path.basename(audiofilepath), line[1], line[2]])
#
#    SimpleAudioNewText.write(reportline)
#
RngAudioNewText.close()