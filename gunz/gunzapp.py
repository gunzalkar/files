from flask import  Flask, jsonify, render_template, request, send_file,send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime 
import json
import os
import math
import subprocess
import requests
import zipfile
import shutil
import logging
import textstat 
import aspose.words as aw
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import pypdfium2 as pdfium
app = Flask(__name__)
app = Flask(__name__)
UPLOAD_FOLDER = app.root_path+'/Data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#----------sitemap-----------
@app.route('/sitemap.xml')
def map():
    return render_template('sitemap.xml')
#-------ads text------------
@app.route('/ads.txt')
def txt():
    return render_template('ads.txt')
#-------ads text------------
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
#---------robots.txt------
@app.route('/robots.txt')
def robot():
    return render_template('robots.txt')
@app.route('/')
def gunz():
    return render_template('gunz_tools.html')


#------------------------Article Rewriter-----------------    
@app.route('/tools/')
def start():
    return render_template('copy_of_index.html')
    
import aicontent
@app.route('/tools/article-rewriter',methods=['GET'])
def article():
    return render_template('copy_of_article.html', sample_input="", sample_output="")
@app.route('/tools/article-rewriter',methods=['POST'])
def my_form_post():
    sample_input = request.form['text']
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        IP=request.environ['REMOTE_ADDR']
    else:
        IP=request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    x={
      "IP": IP, 
      "Module": "index.html",
      "Content-Typed": sample_input,
      "Timestamp": str(datetime.now())
    }
    if sample_input[-1] !='.':
        sample_input = sample_input + '.'
    sample_output = ''
    s = sample_input.split('.')       
    query = 'Rephrase the following statements and check grammar:'+sample_input
    openAIAnswer =aicontent.openAIQuery(query)
    json_object = json.dumps(x, indent=4)
    with open("log.json", "a") as outfile:
        outfile.write(json_object)
    return openAIAnswer

#------------Grammar.html-----------------------------------------------------------------------------------

@app.route('/tools/grammar-checker',methods=['GET'])
def grammer():
    return render_template('copy_of_grammar.html')

@app.route('/tools/grammar-checker',methods=['POST'])
def my_grammer_post():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        IP=request.environ['REMOTE_ADDR']
    else:
        IP=request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    if request.method == 'POST':
        sample_input = request.form['text']
        x={
        "IP": IP, 
        "Module": "grammar.html",
        "Content-Typed": sample_input,
        "Timestamp": str(datetime.now())
        }
        if sample_input[-1] !='.':
            sample_input = sample_input + '.'
        query = 'Correct grammatical mistakes present in the following statements or words and if the word is correct just give as it is:'+sample_input+'.'
        openAIAnswer =aicontent.openAIQuery(query)
        json_object = json.dumps(x, indent=4)
        with open("log.json", "a") as outfile:
            outfile.write(json_object)
        return openAIAnswer


#---------------------------Content-create.html----------------------------------------------------------------------------------

@app.route('/tools/content-create', methods=["GET", "POST"])
def index():
    return render_template('content_create.html', **locals())


#--------------------essay-ideas.html--------------------------------------------------------------

@app.route('/tools/content-create/essay-ideas', methods=["GET", "POST"])
def essayIdeas():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        IP=request.environ['REMOTE_ADDR']
    else:
        IP=request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    if request.method == 'POST':
        submission = request.form['essayIdeas']
        if submission.strip() == "":
            prompt = "Enter Essay Topic"
            return render_template('essay-ideas.html', **locals())
        x={
        "IP": request.environ.get('HTTP_X_REAL_FOR', request.remote_addr), 
        "Module": "essay-ideas.html",
        "Content-Typed": submission,
        "Timestamp": str(datetime.now())
        }
        query="Generate a detailed essay on: {}".format(submission)
        openAIAnswer = aicontent.openAIQuery(query)
        openAIAnswer = openAIAnswer.replace('\n','<br>')
        prompt = 'AI Suggestions for {} are:'.format(submission)
        json_object = json.dumps(x, indent=4)
        with open("log.json", "a") as outfile:
            outfile.write(json_object)
    return render_template('essay-ideas.html', **locals())

#----------------cold-emails.html----------------------------------------------

@app.route('/tools/content-create/cold-emails', methods=["GET", "POST"])
def coldEmails():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        IP=request.environ['REMOTE_ADDR']
    else:
        IP=request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    
    if request.method == 'POST':
        submission = request.form['coldEmails']
        if submission.strip() == "":
            prompt = "Enter Cold-Email Topic"
            return render_template('cold-emails.html', **locals())
        x={
        "IP": request.environ.get('HTTP_X_REAL_FOR', request.remote_addr), 
        "Module": "cold-emails.html",
        "Content-Typed": submission,
        "Timestamp": str(datetime.now())
        }
        query="Write a cold email to potential clients about: {}".format(submission)
        openAIAnswer = aicontent.openAIQuery(query)
        openAIAnswer = openAIAnswer.replace('\n','<br>')
        prompt = 'AI Suggestions for {} are:'.format(submission)
        json_object = json.dumps(x, indent=4)
        with open("log.json", "a") as outfile:
            outfile.write(json_object)
    return render_template('cold-emails.html', **locals())

#------------tweet-ideas.html----------------------------------------------------------


@app.route('/tools/content-create/tweet-ideas', methods=["GET", "POST"])
def tweetIdeas():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        IP=request.environ['REMOTE_ADDR']
    else:
        IP=request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    
    if request.method == 'POST':
        submission = request.form['tweetIdeas']
        if submission.strip() == "":
            prompt = "Enter Tweet Topic"
            return render_template('tweet-ideas.html', **locals())
        x={
        "IP": request.environ.get('HTTP_X_REAL_FOR', request.remote_addr), 
        "Module": "tweet-ideas.html",
        "Content-Typed": submission,
        "Timestamp": str(datetime.now())
        }
        part1 = aicontent.openAIQuery("Generate tweet on the subject: {}".format(submission))
        part2 = aicontent.openAIQuery("Generate twitter hashtags on the subject: {}".format(submission))
        openAIAnswer = part1 +'<br>'+part2
        openAIAnswer = openAIAnswer.replace('\n','<br>')
        prompt = 'AI Suggestions for {} are:'.format(submission)
        json_object = json.dumps(x, indent=4)
        with open("log.json", "a") as outfile:
            outfile.write(json_object)
    return render_template('tweet-ideas.html', **locals())
#----------blog Post-------------------
@app.route('/tools/blog-creator',methods=['GET'])
def blog():
    if request.method == 'POST':
        submission = request.form['blog']
        print("sub: ", submission)
        if submission.strip() == "":
            prompt = "Enter Blog Topic"
            return render_template('blogpost.html', **locals())
            
        query="Write a blog for my website describing: {}".format(submission)
        openAIAnswer = aicontent.openAIQuery(query)
        openAIAnswer = openAIAnswer.replace('\n','<br>')
        #prompt = 'AI Suggestions for {} are:'.format(submission)
        #print(openAIAnswer)
        return openAIAnswer
    return render_template('create_blogpost.html')


#-----------------Code_generator.html--------------

@app.route('/tools/code-generator',methods=['GET'])
def random_code():
    return render_template('copy_of_code.html')

@app.route('/tools/code-generator',methods=["POST"])
def random_code_post():
    lang = request.form.get('select')
    sample_input = request.form['text']
    print("------language-----: ", lang)
    print("---------sample text-------------:", sample_input)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        IP=request.environ['REMOTE_ADDR']
    else:
        IP=request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    x={
        "IP": IP, 
        "Module": "code_generator.html",
        "Content-Typed": sample_input,
        "Timestamp": str(datetime.now())
      }
    
    query = 'generate '+lang+' code to '+sample_input
    openAIAnswer =aicontent.openAIQuery(query)
    json_object = json.dumps(x, indent=4)
    with open("log.json", "a") as outfile:
        outfile.write(json_object)
    return render_template('copy_of_code.html', select=lang,sample_input=sample_input, sample_output=openAIAnswer)

#----------------wordcounter----------------
@app.route('/tools/word-counter', methods=["GET", "POST"])
def wordcount():
    if request.method == 'POST':
        test_data = request.form['text']
        if test_data.strip() == "":
            return 'N/A'
        print("------test_data: ",test_data)
        score=textstat.dale_chall_readability_score(test_data)
        readscore = readScore(score)
        print("score: ",score," -> ", readscore)
        return readscore
    return render_template('wordcounter.html')

@app.route('/tools/word', methods=["GET", "POST"])
def word():
    if request.method == 'POST':
        test_data = request.form['text']
        if test_data.strip() == "":
            return 'N/A'
        print("------ease: ",test_data)
        ease=textstat.flesch_reading_ease(test_data)
        readease = readEase(ease)
        print("ease: ", readease)
        return readease
    return render_template('wordcounter.html')
def readScore(score):
    readscore = ""
    if score<4.9:
        readscore = "Average 13th to 15th-grade (college) student"
    elif 5.0<=score and score<=5.9:
        readscore = "Average 11th or 12th-grade student"
    elif 6.0<=score and score<=6.9:
        readscore = "Average 9th or 10th-grade student"
    elif 7.0<=score and score<=7.9:
        readscore = "Average 7th or 8th-grade student"
    elif 8.0<=score and score<=8.9:
        readscore = "Average 5th or 6th-grade student"
    elif 9.0<score:
        readscore = "Average 4th-grade student or lower"
    return readscore

def readEase(ease):
    readease=""
    if 90<=ease:
        readease = "Very Easy"
    elif 80<=ease and ease<=89:
        readease = "Easy"
    elif 70<=ease and ease<=79:
        readease = "Fairly Easy"
    elif 60<=ease and ease<=69:
        readease = "Standard"
    elif 50<=ease and ease<=59:
        readease = "Fairly Difficult"
    elif 30<=ease and ease<=49:
        readease = "Difficult"
    elif 0<=ease and ease<=29:
        readease = "Very Confusing"
    return readease

#-----------------text-compare.html--------------

@app.route('/tools/text-compare',methods=['GET'])
def textcompare():
    return render_template('compare-word.html')

#-----------------Code-compare.html--------------

@app.route('/tools/code-compare',methods=['GET'])
def codecompare():
    return render_template('compare-code.html')


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

#------Convert---------------
#--------------------PDF conversion----------------------  
@app.route('/docs/',methods=["GET", "POST"])
def convert():
    return render_template('convert_trial.html')

#-----secure-----------------
@app.route('/docs/secure', methods=["GET", "POST"])
def secure():
    if request.method == 'POST':
        sample_pass = request.form['encrypt']
        sample_input = request.files['myfile']
        
        path = returnPath('encrypted_'+sample_input.filename)
        print("path sample_input = ",path )
        file =  os.path.join(app.config['UPLOAD_FOLDER'],sample_input.filename)
        output_f = os.path.join(app.root_path,'Data',path)
        print("---------------file: ",file)
        sample_input.save(os.path.join(app.config['UPLOAD_FOLDER'], sample_input.filename))
        print("-------------------File saved----------------")
        pdf_in_file = open(file,'rb')
        
        inputpdf = PdfFileReader(pdf_in_file, strict=False)
        pages_no = inputpdf.numPages
        output = PdfFileWriter()
        print("----------------------filename: ",sample_input.filename)
        print("------------------password: ",sample_pass)
        for i in range(pages_no):
            inputpdf = PdfFileReader(pdf_in_file, strict=False)
            
            output.addPage(inputpdf.getPage(i))
            output.encrypt(str(sample_pass))

            with open(output_f, "wb") as outputStream:
                output.write(outputStream)

        pdf_in_file.close()
        os.remove(file)
        return send_file(
         output_f, 
         mimetype="application/pdf", 
         as_attachment=False, 
         download_name=path)
    return render_template('encrypt.html')




#----------------------------------PDF To---------------------------------------------------------------------------

@app.route('/docs/PDFTo', methods=["GET", "POST"])
def pdfTo():
    return render_template('pdfTo.html')

#------------------PDF To word-------
@app.route('/docs/PDFTo/pdftoword', methods=["GET", "POST"])
def pdfToword():
    if request.method == 'POST':
        sample_input = request.files['mywordfile']
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info('PDFtoWORD')
        
        path = returnPath(sample_input.filename)
        logging.info('Path returned %s',path)
        print("path sample_input = ",path )
        file =  os.path.join(app.root_path,'Data',path)
        logging.info('file: %s',file)
        try:    
            sample_input.save(file)
        except Exception as e:
            print("Exception")
        print("Docx: ",sample_input.filename[:-4]) 
        doc = aw.Document(file)
        path = returnPath(sample_input.filename[:-4]+'.docx')
        
        print("path Output = ",path)
        output_f = os.path.join(app.root_path,'Data',path)
        
        doc.save(output_f)
        size = returnSize(output_f)
        
        #os.remove(file)
        print("---------Downloading------------")
        uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        print('Uploads : ', uploads)
        print('Upload[]: ',app.config["UPLOAD_FOLDER"], path)
        return send_from_directory(app.config["UPLOAD_FOLDER"], path, as_attachment=True)
    else:
        return render_template('pdfTo.html')


#----------------rotate.html----------------------------------------------

@app.route('/docs/rotate', methods=["GET"])
def rotate():
    return render_template('rotate.html')
    
@app.route('/docs/rotate', methods=["POST"])
def rotate_pdf():
    sample_input = request.files['myfile']
    degree = int(request.form.get('select'))
    rotation = request.form.get('select2')
    print("Rotation: ",rotation)
    f = PdfFileReader(sample_input)
    pdf_writer = PdfFileWriter()
    
    if rotation == "clock":
        print("--- I'm clockwise -----")
        for pagenum in range(f.numPages):
            page = f.getPage(pagenum)
            page.rotateClockwise(degree)
            pdf_writer.addPage(page)
    elif rotation == "anticlock":
        print("--- I'm Anticlockwise -----")
        for pagenum in range(f.numPages):
            page = f.getPage(pagenum)
            page.rotateCounterClockwise(degree)
            pdf_writer.addPage(page)
    path = returnPath('rotated_'+sample_input.filename)
    print("Path: ",path)
    output_f = os.path.join(app.root_path,'Data',path)
    print("output_f: ",output_f)
    pdf_out = open(output_f, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    size = returnSize(output_f)
    print("Done")
    return send_from_directory(app.config["UPLOAD_FOLDER"], path, as_attachment=True)

#------------read.html----------------------------------------------------------


@app.route('/docs/read', methods=["GET", "POST"])
def read():
    if request.method == 'POST':
        sample_input = request.files['myfile']
        path = returnPath('read_'+sample_input.filename)
        sample_input.save(os.path.join(app.config['UPLOAD_FOLDER'], path))
        return send_file(
         os.path.join(app.config['UPLOAD_FOLDER'], path), 
         mimetype="application/pdf", 
         as_attachment=False, 
         download_name=path)
    return render_template('reader.html')


#-------------Watermark ------------
@app.route('/docs/watermark',methods=["GET", "POST"])
def watermark():
    if request.method == 'POST':
        pdf_file = request.files['myfile']
        watermark = request.files['myWfile']
        input_pdf = PdfFileReader(pdf_file)
        watermark_pdf = PdfFileReader(watermark)
        
        pdf_page = input_pdf.getPage(0)
        watermark_page = watermark_pdf.getPage(0)
        pdf_page.mergePage(watermark_page)
        output = PdfFileWriter()
        output.addPage(pdf_page)
        
        path = './Data/'+returnPath('watermarked_'+pdf_file.filename)
        output.write(path)
        size = returnSize(path)
        print(size)
        return send_file(
         path, 
         mimetype="application/pdf", 
         as_attachment=False, 
         download_name=path)
        
    return render_template('watermark.html')


#---------- pdf To HTML --------------
@app.route('/docs/PDFTo/pdftohtml',methods=["GET", "POST"])
def pdftohtml():
    if request.method == 'POST':
        sample_input = request.files['myhtmlfile']
        filename = secure_filename(sample_input.filename)
        file =  os.path.join(app.config["UPLOAD_FOLDER"],filename)
        sample_input.save(file)
        pathD= returnDir(filename[:-4])
        
        path= imagespdf(filename,pathD) #path for image directory
        print("pathD: ",pathD)
        print("path: ",path)
        DestinationFile =os.path.join(app.root_path,'Data',pathD,pathD+'.html')
        print("DestinationFile: "+DestinationFile)
        img = [im for im in os.listdir(path) if '.png' in im]
        li = makehtml(img,pathD)
        with open(DestinationFile, 'w') as fp:
            for item in li:
                # write each item on a new line
                fp.write("%s\n" % item)
        print('Done')
        size = returnSize(DestinationFile)
        file =  os.path.join(app.root_path,'Data',DestinationFile)
        print("---------Downloading------------")
        pt='./Data/'+pathD
        output_file = zippall(pt)
        shutil.rmtree(path)
        return send_file(output_file,
            mimetype = 'zip',
            download_name= output_file,
            as_attachment = True)
    return render_template('pdfTo.html')
def makehtml(img,path):
    print("img: ",img)
    li=[]
    li.append('''<!doctype html>
       <html lang="en" >
       <head>
        <link rel="canonical" href=""/>
        <meta charset="utf-8">
        <meta content="text/html; charset=UTF-8; X-Content-Type-Options=nosniff" http-equiv="Content-Type" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF</title>
    <style>
    img{
      background-position: center;
      background-repeat: no-repeat;
      background-size: cover;
      border: 2px solid black;
    }
    </style>
    </head>
    <body translate="no"> ''')
    li.append('')
    for i in img:
        li[1]= li[1]+'<img src="'+i+'" style="text-align:center" width="90%" height="90%"/><br>\n'
    li.append('''
    </body>
    </html>''')
    print("li :", li)
    return li

 #---------------------image to pdf------------------------  



@app.route("/docs/imagetopdf", methods=["POST"])
def imagetopdf():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("myfile[]")
        pdf = FPDF()
        for imgd in uploaded_files:
            print("\n")
            print("imgd.filename: ", imgd.filename)
            source =  os.path.join(app.root_path,'Data',returnPath(imgd.filename).strip())
            print(source)
            print("\n")
            imgd.save(source)
            pdf.add_page()         #Unique file number 
            image = source   #inserted image on same page
            pdf.image(image,x=0,y=0,w=210,h=297)
            print("added 1 image")
            print("\n")
        path = './Data/'+returnPath("Output_image.pdf")
        print("path")
        pdf.output(path)

        return send_file(
             path, 
             mimetype="application/pdf", 
             as_attachment=False, 
             download_name=path)
    return render_template('pdfTo.html')

#--------------------------PDF to image------------------------
@app.route("/docs/PDFTo/pdftoimage", methods=["POST"])
def pdftoimage():
    if request.method == 'POST':
        sample_input = request.files['myimagefile']
        
        sample_input.save(os.path.join(app.config['UPLOAD_FOLDER'], sample_input.filename))
        dirname = returnDir(sample_input.filename[:-4])
        path= imagespdf(sample_input.filename,dirname)
        pt = './Data/'+dirname
        print("Path: ",path)
        print("pt: ",pt)
        print("------------------- Lets make a path -----------------\n")
        
        output_file = zippall(pt)
        print("Output: ",output_file)
        shutil.rmtree(path)
        return send_file(output_file,
            mimetype = 'zip',
            download_name= output_file,
            as_attachment = True)
    return render_template('pdfTo.html')

#--------------------folder for images------------------   
def imagespdf(filename,path):
    pdf = pdfium.PdfDocument('./Data/'+filename)
    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],path))
    n_pages = len(pdf)
    
    print("pages in pdf: ", n_pages)
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        pil_image = page.render_topil(
            scale=1,
            rotation=0,
            crop=(0, 0, 0, 0),
            greyscale=False,
            optimise_mode=pdfium.OptimiseMode.NONE,
        )
        name= f"{path}_image_{page_number+1}.png"
        print("name: ",name)
        print("path you've recived: ",path)
        source =  os.path.join(app.root_path,'Data',path,name)
        pil_image.save(source)
    return os.path.join(app.config['UPLOAD_FOLDER'],path)

#--------------------------PDF to text------------------------------
@app.route('/docs/PDFTo/text' ,methods=["GET", "POST"])
def text():
    if request.method == 'POST': 
        input_file = request.files['mytextfile']
        f = PdfFileReader(input_file)
        if f.isEncrypted:
            return render_template('encrypterror.html')
        pfr = PdfFileReader(input_file)
        pgobj = pfr.getPage(0)
        text = pgobj.extractText()
        path = returnPath(input_file.filename[:-4]+'.txt')
        file1 = open(os.path.join(app.root_path,'Data',path),'w+', encoding="utf-8")
        file1.writelines(text)
        file1.close()
        output_f = os.path.join(app.root_path,'Data',path)
        print("---------Downloading------------")
        print('Upload[]: ',app.config["UPLOAD_FOLDER"], path)
        return send_from_directory(app.config["UPLOAD_FOLDER"], path, as_attachment=True)
    return render_template('pdfTo.html')


#---------------zip folder-------------------  
def zippall(path):
    print("----------------------function called!--------------------")
    zipf = zipfile.ZipFile(path+'.zip','w', zipfile.ZIP_DEFLATED)
    for root,dirs, files in os.walk(os.path.join(app.root_path,path)):
        print("------------------inside file-----------------------")
        for file in files:
            print("I'm start-> ",file)
            zipf.write(fr'{path}/'+file)
            print("-----LOOP----------")
    print("done")
    zipf.close()
    print("-----sending value------", path+'_images.zip')
    return path+'.zip'


def returnSize(output_f):
    file_size = int(os.path.getsize(output_f))
    sufixes = ['B', 'kB', 'MB', 'GB', 'TB']
    i = math.floor(math.log(file_size) / math.log(1024))
    byte = round(file_size / math.pow(1024, i),2)
    size= str(byte)+' '+sufixes[i]
    return size

def returnPath(name):
    filename, extension = os.path.splitext(name)
    path = name
    try:
        while os.path.exists(os.path.join(app.root_path,'Data',name)):
            os.remove(path)
    finally:
        return path


def set_page_size(page_setup, width, height):
    page_setup.page_width = width
    page_setup.page_height = height

def returnDir(name):
    path = name.replace(" ", "_")
    while os.path.isdir(os.path.join(app.root_path,'Data',name.replace(" ", "_"))):
        shutil.rmtree(os.path.join(app.root_path,'Data',name.replace(" ", "_")))
    return path

def download(filename):
    print("---------Downloading------------")
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print('Uploads : ', uploads)
    print('Upload[]: ',app.config["UPLOAD_FOLDER"], filename)
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)






#-----------Errors ------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')
import smtplib
@app.errorhandler(500)
def page_not_found(error):    
    return render_template('servererror.html')
    

    
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)