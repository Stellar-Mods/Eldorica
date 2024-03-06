from modlistCreation import modlistCreation
from prepareExport import prepareExport
from changelogCreation import changelogCreation
import os
import json
import sys

def readSettingsFile(settingsPath):
    try:
        with open(f"{settingsPath}ExportScriptSettings.json", 'r', encoding='utf-8') as settingsFile:
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

scriptFolderPath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.path.sep + 'scriptData' + os.path.sep
 
folderName, packType, usedSettings = readSettingsFile(scriptFolderPath)
version = input('Modpack Version: v. ')

modrinthCofigPath, packType, namesList = modlistCreation(folderName, packType)
folderPath = modrinthCofigPath.split(os.path.sep)[:-1]# Get profile.json path and remove profile.json and turn el in list
profileName = folderPath[-1]

changelogCreation(namesList, profileName, version, scriptFolderPath)

if usedSettings == False:
    save = saveOptions()
    if save:
        settings = {"ModrinthFolderName": profileName, "PackType": packType}
        print('Saving settings file ...')
        with open(f'{scriptFolderPath}ExportScriptSettings.json', 'w') as settingsFile:
            json.dump(settings, settingsFile)

prepareExport(folderPath)

print(f'\n\n{profileName.capitalize()} is ready to export!')
input('')