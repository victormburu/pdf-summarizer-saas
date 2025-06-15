import os

desc_dir = os.path.join(os.getcwd(), "test1") #create a path to the directory
if not os.path.exists(desc_dir): #check if the directory exists
    os.mkdir(desc_dir) #create the directory if it does not exist

src_file = os.path.join(os.getcwd(), "test1", "README.md") #create a path to the file source
desc_file = os.path.join(os.getcwd(), "test2", "README.md") #create a path to the file destination

if not os.path.exists(src_file): #check if the file exists in the source directory
    print("File not moved from source to destination") #print a message if the file still exists in the source directory
else:
    print("File moved from source to destination") #print a message if the file has been moved to the destination

os.rename(src_file, desc_file) #move the file to the destination directory




