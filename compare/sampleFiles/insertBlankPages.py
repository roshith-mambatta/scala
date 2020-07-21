# !/usr/bin/python

import fitz

original_pdf_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//sample.pdf"
output_file_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//example-extended.pdf"


original_pdf = fitz.open(original_pdf_path)
if len(original_pdf)%2:
    evenPagesFlag=0
else:
    evenPagesFlag=1
print("evenPagesFlag ="+str(evenPagesFlag))
extraPages=0
page_list=range(len(original_pdf))
for i in page_list:
    extraPages+=1
    if i==page_list[-1] and evenPagesFlag ==0:
        print("evenPagesFlag")
    else:
        original_pdf.newPage(i+extraPages,width = 595.44, height = 841.68)


# create a list

original_pdf.save(output_file_path)

