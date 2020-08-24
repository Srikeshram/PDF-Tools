'''
It is Ready-Python program which contains the PDF editing tools in which this tool can be used for extracting the Images and reducing the page
etc.This tools can be mainly used for extracting information which can be used for Machine Learning purposes.The Features of the tools are:
                                      
                                      # Encrypting or Decrypting the PDF. 
                                      # Extracting the Images from the PDF.                            
                                      # Splitting the Pages into the Separate PDF.
                                      # Deleting the pages in the PDF.
                                      # Rotating the pages in the PDF.

Note:Install pikepdf before running script.It can be installed using 'pip install pikepdf'
Note:The Python Script stores all the output in the Current Working Directory of the python script in which it is executed...
'''
import pikepdf
import os
                                                       
def get_path():                                           # The function to get the input path of the PDF file.
    print ('\nEnter the path for the  PDF file:',end=' ')
    path,filename = os.path.split(input())
    
    if (not os.path.isfile (os.path.join(path,filename))):
        raise FileNotFoundError ('The file is not found.') # Exception will be raised if the file not found.
    
    return path,filename

def encrypt_decrypt():                                   #The function to encrypt or decrypt the PDF.
    print('\nEnter Your Option:')
    print('1 - Encrypt')
    print('2 - Decrypt')
    print('\nYour Option:',end=' ')
    n = int(input())
    
    if(n!=1 and n!=2):
        raise ValueError ('Please enter only the above given Numerical Values')
    password=input('\nEnter The Password of the PDF File:')
    
    if(n==1):   
        input_path,filename = get_path()
        out_path = os.path.join(os.getcwd(),'encrypted_'+filename)
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))    
        pdf.save(out_path, encryption=pikepdf.Encryption(owner=password, user=password, R=4)) 
        # you can change the R from 4 to 6 for 256 aes encryption
        pdf.close()
        print('\nFinished........')

    if(n==2):
        input_path,filename = get_path()
        out_path = os.path.join(os.getcwd(),'decrypted_'+filename)
        pdf = pikepdf.open(os.path.join(input_path,filename),password=password)
        pdf.save(out_path)
        pdf.close()
        print('\nFinished.........')

def rotate_pages():                        # The function to rotate the pages in terms of degrees.
    print('\nEnter Your Option:')
    print('1 - Rotating the Specific Pages')
    print('2 - Rotating the Whole Document')
    print('\nYour Option:',end=' ')
    n = int(input())
    
    if(n!=1 and n!=2):
        raise ValueError ('Please enter only mentioned numerical values.')
    
    degrees=int(input('\nEnter the Degrees of Rotation:'))

    input_path,filename = get_path()
    print('\nEnter the Name of the Output File (Ex:output.pdf):',end=' ')
    out_name = input()
    out_path = os.path.join(os.getcwd(),out_name)
    
    if(os.path.isfile(out_path)): 
        raise FileExistsError ('File with specified name already exists.')
    
    if(n==1):
        pages = list(map(int,input('\nEnter the Page Numbers to be Rotated separated by (,):').split(',')))
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
        for page in pages:
            pdf.pages[page-1].Rotate=degrees
        pdf.save(out_path)
        print('\nFinished.........')
        pdf.close()

    else:
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
        for page in pdf.pages:
            page.Rotate=degrees
        pdf.save(out_path)
        print('\nFinished.........')
        pdf.close()

def save_separate_pdf():                              #The Function used to save page in separate pdf
    print('\nEnter Your Option:')
    print('1 - Saving the Specific Pages in Separate PDF')
    print('2 - Saving Every Pages of a Document in Separate PDF')
    print('\nYour Option:',end=' ')
    n = int(input())
    
    if(n!=1 and n!=2):
        raise Exception ('Please enter only the mentioned numerical values.')

    input_path,filename = get_path()

    if(n==1):
        pages = list(map(int,input('\nEnter the Page Numbers to be Splitted:').split(',')))
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))

        for page in pages:
            tmp = pikepdf.Pdf.new()
            tmp.pages.append(pdf.pages[page-1])
            tmp.save(os.path.join(os.getcwd() , str(page) + '_splitted_' + filename))
        print('\nFinished.........')
        pdf.close()

    else:
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
        for page in enumerate(pdf.pages,start=1):
            tmp = pikepdf.Pdf.new()
            tmp.pages.append(page[1])
            tmp.save(os.path.join(os.getcwd() , str(page[0]) + '_splitted_' + filename))
        print('\nFinished.........')
        pdf.close()

def delete_pages():
    input_path,filename=get_path()                    #The function to delete the pages of the PDF
    out_path = os.path.join(os.getcwd(), '_deleted_'+filename)
    page_nums = list(map(int,input('\nEnter the Page Numbers to be Deleted (Separated by Comma(,)):').split(',')))
    pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
    for page in page_nums:
        del pdf.pages[page-1]
    pdf.save(out_path)
    print('\nFinished.........')
    pdf.close()

def img_extract():                    #The function to Extract the images from the Document 
    print('\nEnter Your Option:')
    print('1 - Extracting the Images in Specific Pages.')
    print('2 - Extracting Every Images of a Document.')
    print('\nYour Option:',end=' ')
    n = int(input())
    
    if(n!=1 and n!=2):
        raise Exception ('Please enter only the above given numerical values...')

    input_path,filename = get_path()
    pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
    
    if(n==1):
        page_nums=list(map(int,input('\nEnter the Page Numbers of the Images to be Extracted (Each number should be separated by Comma(,)): ').split(',')))
        for page in page_nums:
            l = list(pdf.pages[page-1].images.keys())
            if len(l)==0:
                raise Exception ('There is No Image present in the Given Page:{}'.format(page))
            else:
                for image in l:
                    raw_image = pdf.pages[page-1].images[image]
                    pdfimage = pikepdf.PdfImage(raw_image)
                    pdfimage.extract_to(fileprefix=os.path.join(os.getcwd(), str(page) + '_' + image[1:] + '_' + filename))
        print('\nFinished.........')
        pdf.close()

    else:
        for page in range(len(pdf.pages)):
            l = list(pdf.pages[page].images.keys())
            
            if len(l) == 0:
                print ('There is No Image present in the Page:{}'.format(page))
            
            else:
                for image in l:
                    raw_image = pdf.pages[page].images[image]
                    pdfimage = pikepdf.PdfImage(raw_image)
                    pdfimage.extract_to(fileprefix=os.path.join(os.getcwd(), str(page) + '_' + image[1:] + '_' + filename))
        print('\nFinished.........')
        pdf.close()

print('PDF Tools -Written in the Python'.center(40))
print('Select any of the Option below:')
print('1 - Encryption or Decryption.')
print('2 - Image Extraction')
print('3 - Rotating the Pages.')
print('4 - Splitting the Pages into Separate PDF.')
print('5 - Removing the pages.')
val = int(input('\nYour Option: '))
if(val==1):
    encrypt_decrypt()
elif(val==2):
    img_extract()
elif(val==3):
    rotate_pages()
elif(val==4):
    save_separate_pdf()
elif(val==5):
    delete_pages()
else:
    raise ValueError('Please enter only mentioned numbers.')
