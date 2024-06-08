import json
import os

def changelogCreation(newNamesList, profileName, version, savePath):
    def readNamesList() -> list:
        names = []
        try:
            with open(f'{savePath}{profileName}changelogNamesList.pythonlist.json', 'r') as file:
                names = json.load(file)
                
            if names is None:
                names = []
        except:
            print('No changlog names file found, assuming this is the first time you run this.') 
            names = []   
        return names
    
    def saveNewList(newNames):
        with open(f'{savePath}{profileName}changelogNamesList.pythonlist.json', 'w') as file:
                json.dump(newNames, file)
                
    def readChanglog():
        try:
            with open(f'{profileName} Changlog.md', 'r') as file:
                oldChanglogText = file.read()
        except:
            oldChanglogText = f'## {profileName} Changlog\n'
            
        oldChanglogText = oldChanglogText.split('\n')
        oldChanglogText = oldChanglogText[1:]
        oldChanglogText = '\n'.join(oldChanglogText)
           
        return oldChanglogText        
    
   
    oldNamesSet = set(readNamesList())
    newNamesSet = set(newNamesList)
    
    addedContent = newNamesSet - oldNamesSet
    removedContent = oldNamesSet - newNamesSet
    
    changlogText = f'# {profileName} Changlog\n\n## v{version}\n'
    if len(addedContent) != 0:
        changlogText += '### Added Contents\n'
        for addedItem in addedContent:
            changlogText += f'- {addedItem}\n'
    else:
        changlogText += '### No added content\n'
            
    if len(removedContent) != 0:
        changlogText += '\n### Removed Contents\n'
        for removedItem in removedContent:
            changlogText += f'- {removedItem}\n'
    else:
        changlogText += '### No removed content\n'
            
    oldChanglog = readChanglog()
    newChanglog = changlogText + oldChanglog
    
    changelogSavePathElements = savePath.split(os.path.sep)
    changelogSavePathElements.pop() # remove \\ at the end
    changelogSavePathElements.pop() # remove scriptData
    changelogSavePathElements.pop() # remove export
    changelogSavePathElements.pop() # remove maintainer-scripts
    changelogSavePath = os.path.sep.join(changelogSavePathElements) + os.path.sep
            
    with open(f'{changelogSavePath}{profileName} Changlog.md', 'w', encoding='utf-8') as file:
        file.write(newChanglog)
    
    saveNewList(newNamesList)