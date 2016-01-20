#************************************************************************************
#                                 PDF Text Extractor
#************************************************************************************
#====================================================================================
#                                  Include stuff
#====================================================================================
import io
from pdfminer.converter import TextConverter
from pdfminer.layout    import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
#====================================================================================
#                                    Actual Code
#====================================================================================
#------------------------------------------------------------------------------------
#                                     Extractor
#------------------------------------------------------------------------------------
def pdf2txt(infp):
    '''
    PDF Text Extractor
    Takes a file objects, and returns a string stream object.
    Implementation is based on the pdfminer3k package.
    '''
    infp.open()
    #Settings
    caching = True #If set to False, it reduces memory consumption, but also slows down the processing
    #Open Output Stream
    outfp   = io.StringIO('')
    #Convert PDF into text
    rsrcmgr = PDFResourceManager(caching=caching)
    device  = TextConverter(rsrcmgr, outfp, laparams=LAParams())
    process_pdf(rsrcmgr, device, infp, caching = caching)
    device.close()
    #Close Input Stream
    infp.close()
    #Reset Output Stream Position
    outfp.seek(0)
    return outfp