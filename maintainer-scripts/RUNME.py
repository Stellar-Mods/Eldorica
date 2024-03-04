from modlistCreation import modlistCreation
from prepareExport import prepareExport
import os
import json

def readSettingsFile():
    try:
        with open("settings.json", encoding='utf-8') as settingsFile:
                df = json.load(settingsFile)
                
        modrinthCofigPath = df['ModrinthFolderName']
        packType = df['PackType']
        return modrinthCofigPath, packType, 'n'
    except:
        print('No settings File found.')
        save = input('Would you like to save the settings to a settings file? ([Y]es, [N]o)')
        if save.lower() in ['y', 'yes']:
            save = 'y'
        elif save.lower() in ['n', 'no']:
            save = 'n'
        else:
            readSettingsFile()
        return None, None, save
            
    
folderName, packType, save = readSettingsFile()
print(folderName, packType)
'''
modrinthCofigPath = modlistCreation(folderName, packType).split(os.path.sep)[:-1] # Get profile.json path and remove profile.json and turn el in list
prepareExport(modrinthCofigPath)

profileName = modrinthCofigPath[-1]
print(f'\n\n{profileName.capitalize()} is ready to export!')
input('')
'''