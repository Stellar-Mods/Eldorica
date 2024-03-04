from modlistCreation import modlistCreation
from prepareExport import prepareExport
import os
import json

def readSettingsFile():
    try:
        with open("settings.json", 'r', encoding='utf-8') as settingsFile:
                df = json.load(settingsFile)      
        modrinthCofigPath = df['ModrinthFolderName']
        packType = df['PackType']
        
        useSettingsFile = input(f'Would you like to use these settings?\n\tModrinthPath: {modrinthCofigPath}\n\tPackType: {packType}\n [Y]es, [N]o: ')
        if useSettingsFile.lower() in ['y', 'yes']:
            return modrinthCofigPath, packType, True
        elif useSettingsFile.lower() in ['n', 'no']:
            return None, None, False
            
    except:
        print('No settings File found.')
        return None, None, False
    
def saveOptions():
    save = input('Would you like to save the settings to a settings file? ([Y]es, [N]o): ')
    if save.lower() in ['y', 'yes']:
        save = True
    elif save.lower() in ['n', 'no']:
        save = False
    else:
        print(f'{save} is not an option choose between: y, yes, n, no')
        saveOptions()
    return save          
    
folderName, packType, usedSettings = readSettingsFile()

modrinthCofigPath, packType = modlistCreation(folderName, packType) 
folderPath = modrinthCofigPath.split(os.path.sep)[:-1]# Get profile.json path and remove profile.json and turn el in list
profileName = folderPath[-1]

if usedSettings == False:
    save = saveOptions()
    if save:
        settings = {"ModrinthFolderName": profileName, "PackType": packType}
        print('Saving settings file ...')
        with open('settings.json', 'w') as settingsFile:
            json.dump(settings, settingsFile)

prepareExport(folderPath)

print(f'\n\n{profileName.capitalize()} is ready to export!')
input('')