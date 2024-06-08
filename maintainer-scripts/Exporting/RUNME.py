from modlistCreation import modlistCreation
from prepareExport import prepareExport
from changelogCreation import changelogCreation
import os
import json
import sys


def readSettingsFile(settingsPath: str):
    files = os.listdir(os.path.dirname(os.path.realpath(sys.argv[0])) + os.path.sep + 'scriptData' + os.path.sep)
    json_file_names = [filename for filename in files if
                       filename.endswith('.json') and not filename.endswith('.pythonlist.json')]
    counter = 0
    if len(json_file_names) > 1:
        print('Choose a settings file:')
        for file in json_file_names:
            counter += 1
            print(f'\t{counter}) {file}')
        try:
            chosenFileIndexNr = int(input('file nr: '))
            chosenFileIndex = len(json_file_names) - chosenFileIndexNr
            chosenFile = json_file_names[chosenFileIndex]
        except:
            print(f'{chosenFileIndexNr} is not valid! please try again')
            readSettingsFile(scriptFolderPath)
    else:
        chosenFile = json_file_names[0]
    try:
        with open(f"{settingsPath}{chosenFile}", 'r', encoding='utf-8') as settingsFile:
            df = json.load(settingsFile)
        modrinthCofigPath = df['ModrinthFolderName']
        packType = df['PackType']
        packName = df['PackName']

        useSettingsFile = input(
            f'Would you like to use these settings?\n\tModrinthPath: {modrinthCofigPath}\n\tPackType: {packType}\n\tPackName: {packName}\n [Y]es, [N]o: ')
        if useSettingsFile.lower() in ['y', 'yes']:
            return modrinthCofigPath, packName, packType, True
        elif useSettingsFile.lower() in ['n', 'no']:
            return None, None, None, False

    except:
        print('No settings File found.')
        return None, None, None, False


def saveOptions() -> bool:
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

folderName, packName, packType, usedSettings = readSettingsFile(scriptFolderPath)
version = input('Modpack Version: v. ')

modrinthCofigPath, packType, namesList = modlistCreation(folderName, packType)
folderPath = modrinthCofigPath.split(os.path.sep)[
             :-1]  # Get profile.json path and remove profile.json and turn el in list
modrinthFolderName = folderPath[-1]
if packName != None:
    profileName = packName
else:
    packName = profileName = input('Name of pack: ')

changelogCreation(namesList, profileName, version, scriptFolderPath)

if usedSettings == False:
    save = saveOptions()
    if save:
        settings = {"ModrinthFolderName": profileName, "PackType": packType, "PackName": packName}
        print('Saving settings file ...')
        with open(f'{scriptFolderPath}{modrinthFolderName}ExportScriptSettings.json', 'w') as settingsFile:
            json.dump(settings, settingsFile)

prepareExport(folderPath)

print(f'\n\n{profileName.capitalize()} is ready to export!')
input('')
