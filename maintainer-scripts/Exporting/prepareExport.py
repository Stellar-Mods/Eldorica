import os
import shutil
import glob

def prepareExport(basePath):
    def moveConfigFiles(basePath):
        print('Moving files to the yosbr/config folder... ')
        src_dir = os.path.sep.join(basePath) + os.path.sep + 'config' 
        dest_dir = src_dir + os.path.sep + 'yosbr' + os.path.sep + 'config'
        
        print('Removing old config files')
        for file in os.listdir(dest_dir):
            filePath = os.path.join(dest_dir, file)
            try:
                if os.path.isdir(filePath):
                    # If it's a directory, attempt to delete its contents first
                    for subitem in os.listdir(filePath):
                        subitemPath = os.path.join(filePath, subitem)
                        os.remove(subitemPath) # This will delete files
                    os.rmdir(filePath) # This will delete the directory if it's empty
                else:
                    # If it's a file, attempt to delete it directly
                    os.remove(filePath)
            except PermissionError:
                print(f"Permission denied for {filePath} Skipping this item, It's suggested to manually move these config files from {src_dir} to {dest_dir}")
        
        
        for config in os.listdir(src_dir):
            source_file = os.path.join(src_dir, config)
            dest_file = os.path.join(dest_dir, config)
            
            if config != 'yosbr':
                try:
                    shutil.move(source_file, dest_file)
                except IOError as e:
                    print("Unable to copy because of:", str(e))

    
    moveConfigFiles(basePath)