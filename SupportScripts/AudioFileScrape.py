import sys, os, shutil

SimpleAudioNewText = open('SimpleAudioConfigNew.txt', 'w+')

FileList = []
ApprovedDirectories = ['Alex', 'Daniel', 'Opsal', 'Austin', 'Zak Barker', 'Ernie', 'Dopkins', 'Kumar', 'Kyle' , 'Scott', 'Sheep', 'Ben', 'Holy']

for line in open('SimpleAudioConfig.txt'):
    line = line.split('\t')
    audiofilepath = line[0].replace("'",'')

    audiofilepathsubfolder = ''
    for name in ApprovedDirectories:
        if name in audiofilepath and 'PythonInsert' not in audiofilepath:
            audiofilepathsubfolder = name
            print(os.path.basename(audiofilepath))

    reportline = ''
    if audiofilepathsubfolder == '':
        shutil.copy2(audiofilepath, 'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + os.path.basename(audiofilepath))
        reportline = '\t'.join(["'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/'" + os.path.basename(audiofilepath), line[1], line[2]])
    else:
        if not os.path.exists('G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + audiofilepathsubfolder):
            os.makedirs('G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + audiofilepathsubfolder)
        shutil.copy2(audiofilepath, 'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/' + audiofilepathsubfolder + '/' + os.path.basename(audiofilepath))
        reportline = '\t'.join(["'G:/DiscordBot/ErniesChairPy/sounds/SimpleAudio/'" + audiofilepathsubfolder + '/' + os.path.basename(audiofilepath), line[1], line[2]])

    SimpleAudioNewText.write(reportline)

SimpleAudioNewText.close()