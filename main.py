# This Python file uses the following encoding: utf-8
import os
import codecs
import stanza
import re
from indicnlp.tokenize import sentence_tokenize

path =r"C:\Users\Sanchit Kanda\Desktop\IISc_Internship\Project-1"
os.chdir(path)

def read_files(file_path):
    with codecs.open(file_path, encoding='utf-8') as f:
        return f.read()

stanza.download('hi', verbose=False)
hi_nlp = stanza.Pipeline('hi', processors='tokenize,lemma,pos,depparse', verbose=False, use_gpu=False)

#Regex codes:
pattern_date='[1-2]?\d?\d?\d[-/\.]((0[0-9])|(1[012]))[-/\.][1-2]?\d?\d\d'  

# above pattern only capable for searching 02/05/21
pattern_phoneNumber="^(\+?\d{1,2}\s?)?\d\d\d[-]?\d\d[-]?\d[-]?\d\d\d\d$"
pattern_year="^\d\d\d\d$"
pattern_time_with_ratio="\d*[:]\d*[PpAa][Mm]\D?"
pattern_time_without_ratio="[PpAa][Mm]"
pattern_ratio='\d?\d[:]\d\d?'
pattern_required="\D*\d+[.,:-]?\d*[.,:-]?\d*"



#files name
file_date = open("Results/date.txt", "a", encoding='utf8')
file_amount=open("Results/amount.txt",'a', encoding='utf8')
file_amountPro=open("Results/amountPro.txt",'a', encoding='utf8') 
# Above file contains those numbers that can be correctly pronounced according to as they are written
file_dateWords=open("Results/dateWords.txt",'a', encoding='utf8')
# Above file contains the words that are associated with dates, months, years, etc
file_phone=open("Results/phoneContent.txt",'a', encoding='utf8')
file_time=open("Results/time.txt",'a', encoding='utf8')
# Above file contains the words that are associated with dates, months, years, etc
file_rest=open("Results/rest.txt",'a', encoding='utf8')
file_num=open("Results/num.txt",'a', encoding='utf8')
file_ratio=open("Results/ratioContent.txt","a", encoding='utf8')
# file_share=open("Results/share.txt",'a')
file_year=open("Results/year.txt",'a', encoding='utf8')
file_train=open("Results/train.txt",'a', encoding='utf8')
# Above file results the sentence having words synonyms with share market



# Flushing inner buffer content
file_date.flush()
file_amount.flush()
file_amountPro.flush()
file_dateWords.flush()
file_phone.flush()
file_time.flush()
file_rest.flush()
file_num.flush()
file_ratio.flush()
# file_share.flush()
file_year.flush()
file_train.flush()


# list of words corresponding to each category:
amount_words=["रुपये","डॉलर","डालर","रुपए","पाउंड","येन","यूरो","युआन","$","₹","£","€","/-","रूपये","रूपए","रु.","रुपया"]
amountpre_words=["$","₹","£","€"]
amountPro_words=["करोड़","लाख","हजार","सौ","ट्रिलियन","मिलियन","अरब"]
date_Words=["जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून","जुलाई","अगस्त","सितंबर","सितम्बर","अक्टूबर","नवंबर","दिसंबर","दिनांक","सालों","अक्तूबर","साल","महीने","महीनों","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Sept","Oct","Nov","Dec","January","February","March","April","May","June","July","August","September","October","November","December"]
time_Words=["बजे","घंटे"]
# shareMarket_Words=["स्तर","प्रतिशत"]
time_fileWords=["बजे","IST","घंटे"]
train_words=['एक्सप्रेस']
gaadi="गाड़ी" 
sankhya="संख्या"

path=path+'\Dataset'
os.chdir(path)
for file in os.listdir():
   if file.endswith('.txt'):
    file_path =r'C:\Users\Sanchit Kanda\Desktop\IISc_Internship\Project-1\Dataset\\'+str(file)
    indic_string=read_files(file_path)
    sentences=sentence_tokenize.sentence_split(indic_string, lang='hi')
    for sentence in sentences:
        hi_doc = hi_nlp(sentence)
        flag=0
        num=0
        ratio=0
        amountpre=0
        gaadiIndicator=0
        trainIndicator=0
        phoneIndicator=0
        for i, sent in enumerate(hi_doc.sentences):
            for word in sent.words:
                WordText=word.text
                if WordText.isnumeric() or re.match(pattern_required,WordText):
                    num=1
                
                if(num==1 and amountpre==1):
                    file_amount.write(sentence)
                    file_amount.write("\n\n")
                    print(sentence)
                    print("amount")
                    amountpre=0
                    flag=1
                    break
                
                if re.match(pattern_time_without_ratio,WordText):
                    if ratio==1:
                        print(sentence)
                        print("time")
                        file_time.write(sentence)
                        file_time.write('\n\n')
                        # print(sentence)
                        flag=1
                        ratio=0
                        break
        
                if re.match(pattern_phoneNumber,WordText):
                    if trainIndicator==1:
                        print(sentence)
                        print("train")
                        file_train.write(sentence)
                        file_train.write('\n\n')
                        trainIndicator=0
                        phoneIndicator=0
                        flag=1
                    else:
                        phoneIndicator=1
                        flag=0
                    # # print(sentence)
                    # break

                if WordText==gaadi:
                    gaadiIndicator=1
                if WordText==sankhya and gaadiIndicator==1:
                    trainIndicator=1

                for word in train_words:
                    if word==WordText:
                        if phoneIndicator==1:
                            print(sentence)
                            print("train")
                            file_train.write(sentence)
                            file_train.write('\n\n')
                            phoneIndicator=0
                            flag=1
                            break
                        else:
                            trainIndicator=1;
                            flag=0
                        break

                for word in time_fileWords:
                    if word==WordText and ratio==1:
                        print(sentence)
                        print("time")
                        file_time.write(sentence)
                        file_time.write('\n\n')
                        flag=1
                        ratio=0
                        break

                if re.match(pattern_time_with_ratio,WordText):
                    print(sentence)
                    print("Time")
                    file_time.write(sentence)
                    file_time.write('\n\n')
                    # print(sentence)
                    flag=1
                    break

                if re.match(pattern_date,WordText):
                    print(sentence)
                    print("Date")
                    file_date.write(sentence)
                    file_date.write('\n\n')
                    # print(sentence)
                    flag=1
                    break

                if re.match(pattern_ratio,WordText):
                    ratio=1
                    flag=1
                
                for amount in amount_words:
                    if amount==WordText and (num==1 or phoneIndicator==1):
                        print(sentence)
                        print("amount")
                        file_amount.write(sentence)
                        file_amount.write('\n\n')
                        phoneIndicator=0
                        flag=1
                        break

                for amountPro in amountPro_words:
                    if amountPro==WordText and num==1:
                        print(sentence)
                        print("AmountPro")
                        file_amountPro.write(sentence)
                        file_amountPro.write('\n\n')
                        flag=1
                        break
                
                for date in date_Words:
                    if date==WordText and num==1:
                        print(sentence)
                        print("Date")
                        file_dateWords.write(sentence)
                        file_dateWords.write('\n\n')
                        flag=1
                        break
                
                for time in time_Words:
                    if time==WordText and num==1:
                        print(sentence)
                        print("time")
                        file_time.write(sentence)
                        file_time.write('\n\n')
                        num=0
                        flag=1
                        break
                
                # for share in shareMarket_Words:
                #     if share==WordText and num==1:
                #         print(sentence)
                #         print("Share")
                #         file_share.write(sentence)
                #         file_share.write('\n\n')
                #         flag=1
                #         break

                for amountpr in amountpre_words:
                    if amountpr==WordText:
                        amountpre=1

                if re.match(pattern_year,WordText):
                    print(sentence)
                    print("Year")
                    file_year.write(sentence)
                    file_year.write('\n\n')
                    # print(sentence)
                    flag=1

        if(phoneIndicator==1):
            print(sentence)
            print("Phone")
            file_phone.write(sentence)
            file_phone.write('\n\n')
        elif(ratio==1 and flag==0):
            file_ratio.write(sentence)
            file_ratio.write('\n\n')  
            print("Ratio")    
        elif(flag==0 and num==1):
            file_num.write(sentence)
            file_num.write('\n\n')
            # print(sentence)
            print("num")
        elif(flag==0):
            file_rest.write(sentence)
            file_rest.write('\n\n')
            print(sentence)
        ratio=0
        amountpre=0  

file_date.close()
file_rest.close()
file_time.close()
file_num.close()
file_train.close()
file_phone.close()
file_amount.close()
file_amountPro.close()
file_dateWords.close()
# file_share.close()
file_year.close()
file_dateWords.close()
file_ratio.close()