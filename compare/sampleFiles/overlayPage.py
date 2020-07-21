#https://github.com/pymupdf/PyMuPDF/wiki/How-to-Insert-new-PDF-Pages,-Images-and-Text

import fitz
from fitz.utils import getColor ,getColorInfoList
original_pdf_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//After.pdf"
output_file_path = "C://Users//Roshith\Desktop//In progress//BIRTsamples//overlayPage.pdf"

doc = fitz.open(original_pdf_path)    # or new: fitz.open(), followed by insertPage()
page1 = doc[0]                         # choose some page
page2 = doc[0]
rect = fitz.Rect(50, 100, 300, 400)   # rectangle (left, top, right, bottom) in pixels
"""
text = """"Sômé tèxt wìth nöñ-Lâtîn characterßThis text will only appear in the rectangle. Depending on width, new lines are generated as required.\n<- This forced line break will also appear.\tNow a very long word: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.\nIt will be broken into pieces."""
"""
from fitz.utils import getColor ,getColorInfoList         # function delivers RGB triple for a color name
white = getColor("gold")                  # one of the 540+ pre-installed colors ...
black = getColor("black")                  # one of the 540+ pre-installed colors ...
grey=getColor("GAINSBORO") #('GAINSBORO', 220, 220, 220)

il = getColorInfoList()
print(il)
rc = page1.insertTextbox(rect, text, fontsize = 6,color = white, # choose fontsize (float)
                   fontname = "Times-Roman",       # a PDF standard font
                   fontfile = None,                # could be a file on your system
                   align = 0)                      # 0 = left, 1 = center, 2 = right

print("unused rectangle height: %g" % rc)          # just demo (should display "44.2")

r1 = fitz.IRect(-1, -1, 300, 300) # a 50x50 rectangle # rectangle (left, top, right, bottom) in pixels



doc[0].drawRect(r1,  fill = grey,overlay=True)
rectImage = fitz.Rect(-1, -1, 100, 100)
text = "some text containing line breaks and\na prettier mono-spaced font."
where = fitz.Point(50, 100)  # text starts here
# this inserts 2 lines of text using font `DejaVu Sans Mono`
doc[0].insertText(where, text,
                fontname="Times-Roman",  # arbitrary if fontfile given
                #fontfile=ffile,  # any file containing a font
                fontsize=11,  # default
                rotate=0,  # rotate text
                color=(0, 0, 1),  # some color (blue)
                overlay=True)  # text in foreground
                """
grey=getColor("GAINSBORO")
footer = fitz.Rect(50, 900, 300, 400) #rectangle (left, top, right, bottom) in pixels
doc[0].drawRect(footer,  fill = grey,overlay=True)
doc.save(output_file_path)
#doc.saveIncr()   # update file. Save to new instead by doc.save("new.pdf",...)