from cStringIO import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

'''
Takes in PDF files and converts to Python human-readable Python data.

Input: path -> full path to PDF file
Output: String representation of parsed data
'''


def getPDFText(path):
    retstr = StringIO()
    parser = PDFParser(open(path, 'r'))

    try:
        document = PDFDocument(parser)

    except Exception:
        print path + 'is not a readable pdf'
        return ''

    if document.is_extractable:
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, retstr, codec='ascii',
                               laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
        return retstr.getvalue()

    else:
        print path, "Warning: could not extract text from PDF file."
        return ''


'''
Function to directly test file as a standalone
Input: None
Output: Textfile of parsed data
'''

#def test():
 #   from os.path import abspath, dirname, join

#    BASEDIR = dirname(abspath(__file__))
#    path = join(BASEDIR, "samples", raw_input("Enter file path: "))

#    try:
 #       words = getPDFText(str(path) + ".pdf")
#        if words != '':
#            with open("samples/parsed.txt", "wb") as result:
#                result.write(words)
#            print "Text is extracted and saved as 'parsed.txt'."
#
#    except IOError:
#        exit("Invalid file name.")
#
#test()
#
# def test():
#     from os.path import abspath, dirname, join
#
#     BASEDIR = dirname(abspath(__file__))
#     path = join(BASEDIR, "samples", raw_input("Enter file path: "))
#
#     try:
#         words = getPDFText(str(path) + ".pdf")
#         if words != '':
#             with open("samples/parsed.txt", "wb") as result:
#                 result.write(words)
#             print "Text is extracted and saved as 'parsed.txt'."
#
#     except IOError:
#         exit("Invalid file name.")

# test()