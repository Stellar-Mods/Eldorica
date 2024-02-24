import json
import humanfriendly as hf
import os
import sys

modrinthConfig_path = input("Modrinth profile path: ") + "\profile.json"
header = ['', 'Project Name', 'Authors', 'Desciption', 'Downloads', 'Project Type']

class Content:
    def __init__(self, name, description, authors, downloads, slug, pr_type):
        self.name = name
        self.desc = description
        self.authors = authors
        self.downloadCount = downloads
        self.link = 'https://modrinth.com/' + pr_type + '/' + slug
        self.project_type = pr_type
        
    def printInfo(self):
        print(f"{self.name}, {self.desc}, {self.authors}, {self.downloadCount}, {self.link}, {self.project_type}")

def getInfo(project_value, wantedInfo):
    try:
        return project_value["metadata"]["project"][wantedInfo].replace("\n", "")
    except:
        try:
            return project_value["metadata"][wantedInfo].replace("\n", "")
        except:
            return '/'
        
def extractInfo(data):
    contents = []
    
    for project_key, project_value in data["projects"].items():
        authors = []
        try:
            for member in project_value['metadata']['members']:
                authors.append(member['user']['username'])
        except:
            authors = getInfo(project_value, 'authors')
            
        name = getInfo(project_value, 'title')
        desc = getInfo(project_value, 'description')
        downs = getInfo(project_value, 'downloads')
        try:
            downs = hf.format_number(downs)
        except:
            downs = downs
            
        slug = getInfo(project_value, 'slug')
        prType = getInfo(project_value, 'project_type')
        
        content = Content(name, desc, authors, downs, slug, prType)
        contents.append(content)
        
    return contents

def mdHeader(header):
    mod_type = input('Are these server mods or client mods? (Enter "server" or "client"): ')
    # Check if the input is valid
    if mod_type.lower() == 'server':
        mod_type = mod_type.upper()
        md_hd = '# Server Mods'
    elif mod_type.lower() == 'client':
        mod_type = mod_type.upper()
        md_hd = '# Client Mods'
    else:
        raise Exception('Unknown type', mod_type)
    
    markdownHeader = md_hd + '\n'
    markdownHeader += '| ' + ' | '.join(header) + ' |\n'
    markdownHeader += '|---' * len(header) + '|\n'
    
    return markdownHeader, mod_type

def mdConversion(header, contents):
    markdown = header
    counter = 0
    for content in contents:
        counter += 1
        markdown += f'| {counter} | {content.name} | {content.authors} | {content.desc} | {content.downloadCount} | {content.project_type} |\n'
        
    return markdown

def outputPath():
    output_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    path_components = output_path.split(os.path.sep)
    path_components.pop()
    output_path = os.path.sep.join(path_components)
    # Check if the output path exists
    if not os.path.exists(output_path):
        raise Exception(f'Output path:{output_path} does not exist')
    
    return output_path

with open(modrinthConfig_path, encoding='utf-8') as config:
    data = json.load(config)

mdHeader, contentType = mdHeader(header)
contents = extractInfo(data)
markdown = mdConversion(mdHeader, contents)
outputPath = outputPath()

with open(f'{outputPath}{os.path.sep}{contentType}MODS.md', 'w', encoding='utf-8') as f:
    f.write(markdown)