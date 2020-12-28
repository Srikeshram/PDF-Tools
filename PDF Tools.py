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
from colorama import Fore,Back,Style,init

banner = '''  
  _____    _____    ______     _______                   _       
 |  __ \  |  __ \  |  ____|   |__   __|                 | |      
 | |__) | | |  | | | |__         | |      ___     ___   | |  ___ 
 |  ___/  | |  | | |  __|        | |     / _ \   / _ \  | | / __|
 | |      | |__| | | |           | |    | (_) | | (_) | | | \__ |
 |_|      |_____/  |_|           |_|     \___/   \___/  |_| |___/
 '''


def get_path():                                           # The function to get the input path of the PDF file.
    print (Style.BRIGHT+Fore.CYAN + '\nEnter the Path for the  PDF file:',end=' ')
    path,filename = os.path.split(input())
    
    if (not os.path.isfile (os.path.join(path,filename))):
        raise FileNotFoundError ('File not Found...') # Exception will be raised if the file not found.
    
    return path,filename

def encrypt_decrypt():                                   #The function to encrypt or decrypt the PDF.
    print(Style.BRIGHT+Fore.CYAN + '\nEnter Your Option:\n')
    print(Style.BRIGHT+Fore.YELLOW + '1 - Encrypt')
    print(Style.BRIGHT+Fore.YELLOW + '2 - Decrypt')
    print(Style.BRIGHT+Fore.RED + '\nYour Option >>>',end=' ')
    n = int(input())

    if(n!=1 and n!=2):
        raise ValueError ('Please enter only the above given Numerical Values')
    
    print(Style.BRIGHT+Fore.BLUE + '\nEnter the Password for the PDF File:',end =" ")
    password = input()
    
    if(n==1):   
        input_path,filename = get_path()
        out_path = os.path.join(os.getcwd(),'encrypted_'+filename)
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))    
        pdf.save(out_path, encryption=pikepdf.Encryption(owner=password, user=password, R=4)) 
        # you can change the R from 4 to 6 for 256 aes encryption
        pdf.close()
        print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')

    if(n==2):
        input_path,filename = get_path()
        out_path = os.path.join(os.getcwd(),'decrypted_'+filename)
        pdf = pikepdf.open(os.path.join(input_path,filename),password=password)
        pdf.save(out_path)
        pdf.close()
        print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')

def rotate_pages():                        # The function to rotate the pages in terms of degrees.
    print(Style.BRIGHT+Fore.CYAN + '\nEnter Your Option:\n')
    print(Style.BRIGHT+Fore.YELLOW + '1 - Rotating the Specific Pages')
    print(Style.BRIGHT+Fore.YELLOW + '2 - Rotating the Whole Document')
    print(Style.BRIGHT+Fore.YELLOW + '\nYour Option >>>',end=' ')
    n = int(input())
    
    if(n!=1 and n!=2):
        raise ValueError ('Please enter only emntioned Numerical Values.')
    
    print(Style.BRIGHT+Fore.BLUE + "\nEnter the Degrees of Rotation:")
    degrees=int(input())

    input_path,filename = get_path()

    print(Style.BRIGHT+Fore.BLUE + '\nEnter the Name of the Output File (Ex:output.pdf):',end=' ')
    out_name = input()
    
    if('.pdf' not in out_name):
        out_name+='.pdf'
    out_path = os.path.join(os.getcwd(),out_name)
    
    if(os.path.isfile(out_path)): 
        raise FileExistsError ('File with specified name already exists.')
    
    if(n==1):
        print(Style.BRIGHT+Fore.BLUE + "\nEnter the Page Numbers to be Rotated separated by (,):")
        
        pages = list(map(int,input().split(',')))
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
        
        for page in pages:
            pdf.pages[page-1].Rotate=degrees
        
        pdf.save(out_path)
        print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')
        pdf.close()

    else:
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
        
        for page in pdf.pages:
            page.Rotate=degrees
        
        pdf.save(out_path)
        print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')
        pdf.close()

def save_separate_pdf():                              #The Function used to save page in separate pdf
    print(Style.BRIGHT+Fore.CYAN + '\nEnter Your Option:\n')
    print(Style.BRIGHT+Fore.YELLOW +'1 - Saving the Specific Pages in Separate PDF')
    print(Style.BRIGHT+Fore.YELLOW +'2 - Saving Every Pages of a Document in Separate PDF')
    print(Style.BRIGHT+Fore.RED +'\nYour Option >>>',end=' ')
    n = int(input())
    
    if(n!=1 and n!=2):
        raise Exception ('Please enter only the mentioned numerical values.')

    input_path,filename = get_path()

    if(n==1):
        print(Style.BRIGHT+Fore.BLUE + '\nEnter the Page Numbers to be Splitted:')
        pages = list(map(int,input().split(',')))
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))

        for page in pages:
            tmp = pikepdf.Pdf.new()
            tmp.pages.append(pdf.pages[page-1])
            tmp.save(os.path.join(os.getcwd() , str(page) + '_splitted_' + filename))
        
        print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')
        pdf.close()

    else:
        pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
        
        for page in enumerate(pdf.pages,start=1):
            tmp = pikepdf.Pdf.new()
            tmp.pages.append(page[1])
            tmp.save(os.path.join(os.getcwd() , str(page[0]) + '_splitted_' + filename))
        
        print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')
        pdf.close()

def delete_pages():
    input_path,filename=get_path()                    #The function to delete the pages of the PDF
    out_path = os.path.join(os.getcwd(), '_deleted_'+filename)
    
    print(Style.BRIGHT+Fore.BLUE + "\nEnter the Page Numbers to be Deleted (Separated by Comma(,)):",end = " ")
    page_nums = list(map(int,input().split(',')))
    
    pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
    
    for i,page in enumerate(page_nums):
        del pdf.pages[page-1-i]
    
    pdf.save(out_path)
    print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')
    pdf.close()

def img_extract():                    #The function to Extract the images from the Document 
    print(Style.BRIGHT+Fore.CYAN + '\nEnter Your Option:\n')
    print(Style.BRIGHT+Fore.YELLOW + '1 - Extracting the Images in Specific Pages.')
    print(Style.BRIGHT+Fore.YELLOW +'2 - Extracting Every Images of a Document.')
    print(Style.BRIGHT+Fore.RED +'\nYour Option >>>',end=' ')
    n = int(input())
    
    if(n!=1 and n!=2):
        raise Exception ('Please enter only the above given numerical values...')

    input_path,filename = get_path()
    pdf = pikepdf.Pdf.open(os.path.join(input_path,filename))
    
    if(n==1):
        print(Style.BRIGHT+Fore.BLUE + '\nEnter the Page Numbers of the Images to be Extracted (Each number should be separated by Comma(,)): ',end = '')
        page_nums=list(map(int,input().split(',')))
        
        for page in page_nums:
            l = list(pdf.pages[page-1].images.keys())
            
            if len(l)==0:
                print(Style.DIM+Fore.LIGHTRED_EX + 'There is No Image present in the Given Page:{}'.format(page))
            
            else:
                for image in l:
                    raw_image = pdf.pages[page-1].images[image]
                    pdfimage = pikepdf.PdfImage(raw_image)
                    pdfimage.extract_to(fileprefix=os.path.join(os.getcwd(), str(page) + '_' + image[1:] + '_' + filename))
        print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')
        pdf.close()

    else:
        for page in range(len(pdf.pages)):
            l = list(pdf.pages[page].images.keys())
            
            if len(l) == 0:
                print (Style.DIM+Fore.LIGHTRED_EX + 'There is No Image present in the Page:{}'.format(page))
            
            else:
                for image in l:
                    raw_image = pdf.pages[page].images[image]
                    pdfimage = pikepdf.PdfImage(raw_image)
                    pdfimage.extract_to(fileprefix=os.path.join(os.getcwd(), str(page) + '_' + image[1:] + '_' + filename))
                print(Style.BRIGHT+Fore.RED + '\n----------FINISHED------------')
        pdf.close()

def main():
    init()
    print(Fore.RED+Style.BRIGHT+"\n\n",banner.center(300))
    init(autoreset=True)
    print("------------------Coded in Python by Srikesh---------------------\n\n\n")
    print(Style.BRIGHT+Fore.CYAN+'Select any of the Option below:\n'+Fore.RESET)
    print(Style.BRIGHT+Fore.GREEN+'1 - Encryption or Decryption.')
    print(Style.BRIGHT+Fore.GREEN+'2 - Image Extraction')
    print(Style.BRIGHT+Fore.GREEN+'3 - Rotating the Pages.')
    print(Style.BRIGHT+Fore.GREEN+'4 - Splitting the Pages into Separate PDF.')
    print(Style.BRIGHT+Fore.GREEN+'5 - Removing the pages.')
    print(Style.BRIGHT+Fore.GREEN+'6 - Exit')
    print(Style.BRIGHT+Fore.RED+'\nYour Option >>>'+Fore.RESET,end = ' ')
    val = int(input())
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
    elif(val==6):
        exit()
    else:
        raise ValueError('Please enter only mentioned numbers.')
if(__name__=="__main__"):
    main()
