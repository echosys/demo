from PyPDF2 import PdfFileReader, PdfFileWriter
import os 


def decrypt_pdf(input_path, output_path, password):
    with open(input_path, 'rb') as input_file, \
        open(output_path, 'wb') as output_file:
        reader = PdfFileReader(input_file)
        reader.decrypt(password)

        writer = PdfFileWriter()
        
        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))
        
        writer.write(output_file)

def mirrorfolderstructure(rootpath, targetfolder, newfoldername):
    inputpath = os.path.join(rootpath, targetfolder)
    outputpath = os.path.join(rootpath, newfoldername)
    
    for dirpath, dirnames, filenames in os.walk(inputpath):
        structure = os.path.join(outputpath, os.path.relpath(dirpath, inputpath))
        if not os.path.isdir(structure):
            os.mkdir(structure)
            print(structure)
        else:
            print("Folder already exits!")

def loopallfile(rootdir, outputroot):
    password = 'birds'
    folders = os.listdir(rootdir)
    for eachfolder in folders:
        print(eachfolder)
        folder_path = os.path.join(rootdir, eachfolder)
        files = os.listdir(folder_path)
        for eachfile in files:
            #print(eachfile)
            file_path = os.path.join(rootdir, eachfolder, eachfile)
            input_path = os.path.join(rootdir, eachfolder, eachfile)
            output_path = os.path.join(outputroot, eachfolder, eachfile)
            exists = os.path.isfile(output_path)
            if exists:
                # Store configuration file values
                print("File already exits!" + eachfile)
            else:
                # Keep presets
                decrypt_pdf(input_path, output_path, password)

#no easy way to parse existing bookmarks 
def mergepdf(rootdir, outputroot): # no nested bookmark, but all depth of folder
    output = PdfFileWriter()
    count = 0
    
    for path, subdirs, files in os.walk(rootdir):
        for filename in files:
            input_path = os.path.join(path, filename)
            print(os.path.join(path, filename) )
            input1 = PdfFileReader(open(input_path, 'rb'))
            output.addPage(input1.getPage(0))
            filename_only, file_extension = os.path.splitext(filename)
            bookmarkname = os.path.basename(path) + ' ' + filename_only
            parent = output.addBookmark(bookmarkname, count) # add parent bookmark
            count = count + 1
    
    output.setPageMode("/UseOutlines") #This is what tells the PDF to open to bookmarks
    outputStream = open('ADSol_v1.pdf','wb') #creating result pdf JCT
    output.write(outputStream) #writing to result pdf JCT
    outputStream.close() #closing result JCT

def mergepdf2(rootdir, outputroot): # no nested bookmark, but all depth of folder
    output = PdfFileWriter()
    count = 0
    parentList = []
    
    for path, subdirs, files in os.walk(rootdir):
        for filename in files:
            input_path = os.path.join(path, filename)
            print(os.path.join(path, filename) )
            input1 = PdfFileReader(open(input_path, 'rb'))
            output.addPage(input1.getPage(0))
            filename_only, file_extension = os.path.splitext(filename)
            foldername = os.path.basename(path)
            bookmarkname = foldername + ' ' + filename_only
            if foldername in parentList: 
                output.addBookmark(filename_only, count, parent) # add child bookmark
            else: 
                parentList.append(foldername)
                parent = output.addBookmark(foldername, count) # add parent bookmark
                output.addBookmark(filename_only, count, parent) # add child bookmark
            count = count + 1
            
    output.setPageMode("/UseOutlines") #This is what tells the PDF to open to bookmarks
    outputStream = open('ADSol_v2.pdf','wb') #creating result pdf JCT
    output.write(outputStream) #writing to result pdf JCT
    outputStream.close() #closing result JCT


def main():
    targetfolder = 'ADSol'
    newfoldername = 'ADSol_v1'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    rootdir = os.path.join(dir_path, targetfolder)
    outputroot = os.path.join(dir_path, newfoldername)
    
    #mirrorfolderstructure(dir_path, targetfolder, newfoldername)
    #loopallfile(rootdir, outputroot)
    mergepdf(outputroot, outputroot)
    mergepdf2(outputroot, outputroot)
    #output_path  =  os.path.join(dir_path, 'test1.pdf')
    #password = 'birds'
    #decrypt_pdf(input_path, output_path, password)

if __name__ == '__main__':
    main()
