# This Python file uses the following encoding: utf-8
import os
import codecs
from unicodedata import category
from pyparsing import Word
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
# file_date = open("Results/date.txt", "a", encoding='utf8')
# file_amount=open("Results/amount.txt",'a', encoding='utf8')
# file_amountPro=open("Results/amountPro.txt",'a', encoding='utf8') 
# # Above file contains those numbers that can be correctly pronounced according to as they are written
# file_dateWords=open("Results/dateWords.txt",'a', encoding='utf8')
# # Above file contains the words that are associated with dates, months, years, etc
# file_phone=open("Results/phoneContent.txt",'a', encoding='utf8')
# file_time=open("Results/time.txt",'a', encoding='utf8')
# # Above file contains the words that are associated with dates, months, years, etc
# file_rest=open("Results/rest.txt",'a', encoding='utf8')
# file_num=open("Results/num.txt",'a', encoding='utf8')
# file_ratio=open("Results/ratioContent.txt","a", encoding='utf8')
# # file_share=open("Results/share.txt",'a')
# file_year=open("Results/year.txt",'a', encoding='utf8')
# file_train=open("Results/train.txt",'a', encoding='utf8')


file_results=open("Tagging_Results/results.txt", "a", encoding='utf8')
# Above file results the sentence having words synonyms with share market



# Flushing inner buffer content
# file_date.flush()
# file_amount.flush()
# file_amountPro.flush()
# file_dateWords.flush()
# file_phone.flush()
# file_time.flush()
# file_rest.flush()
# file_num.flush()
# file_ratio.flush()
# # file_share.flush()
# file_year.flush()
# file_train.flush()

file_results.flush()


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
        print(sentence)
        hi_doc = hi_nlp(sentence)
        flag=0
        num=0
        ratio=0
        amountpre=0
        gaadiIndicator=0
        trainIndicator=0
        phoneIndicator=0
        categoryarray=[]
        numarray=[]
        numindex=0
        for i, sent in enumerate(hi_doc.sentences):
            for word in sent.words:
                numindex+=1;
                WordText=word.text
                if WordText.isnumeric() or re.match(pattern_required,WordText):
                    num=1
                    numarray.append(numindex)
                
                if(num==1 and amountpre==1):
                    # file_amount.write(sentence)
                    # file_amount.write("\n\n")
                    amountappend="<amount>"
                    categoryarray.append(amountappend)
                    # file_results.write(sentence)
                    # file_results.write("\n\n")
                    print(sentence)
                    print("amount")
                    amountpre=0
                    flag=1
                    break
                
                if re.match(pattern_time_without_ratio,WordText):
                    if ratio==1:
                        print(sentence)
                        print("time")
                        timeappend="<time>"
                        categoryarray.append(timeappend)
                        # file_time.write(sentence)
                        # file_time.write('\n\n')
                        # file_results.write(sentence)
                        # file_results.write("\n\n")
                        # print(sentence)
                        flag=1
                        ratio=0
                        break
        
                if re.match(pattern_phoneNumber,WordText):
                    if trainIndicator==1:
                        print(sentence)
                        print("train")
                        trainappend="<train>"
                        categoryarray.append(trainappend)
                        # file_train.write(sentence)
                        # file_train.write('\n\n')
                        # file_results.write(sentence)
                        # file_results.write("\n\n")  
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
                            trainappend="<train>"
                            categoryarray.append(trainappend)
                            # file_train.write(sentence)
                            # file_train.write('\n\n')
                            # file_results.write(sentence)
                            # file_results.write("\n\n")
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
                        timeappend="<time>"
                        categoryarray.append(timeappend)
                        # file_time.write(sentence)
                        # file_time.write('\n\n')
                        # file_results.write(sentence)
                        # file_results.write("\n\n")
                        flag=1
                        ratio=0
                        break

                if re.match(pattern_time_with_ratio,WordText):
                    print(sentence)
                    print("Time")
                    timeappend="<time>"
                    categoryarray.append(timeappend)
                    # file_time.write(sentence)
                    # file_time.write('\n\n')
                    # file_results.write(sentence)
                    # file_results.write("\n\n")
                    # print(sentence)
                    flag=1
                    break

                if re.match(pattern_date,WordText):
                    print(sentence)
                    print("Date")
                    dateappend="<date>"
                    categoryarray.append(dateappend)
                    # file_date.write(sentence)
                    # file_date.write('\n\n')
                    # file_results.write(sentence)
                    # file_results.write("\n\n")
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
                        amountappend="<amount>"
                        categoryarray.append(amountappend)
                        # file_amount.write(sentence)
                        # file_amount.write('\n\n')
                        # file_results.write(sentence)
                        # file_results.write("\n\n")
                        phoneIndicator=0
                        flag=1
                        break

                for amountPro in amountPro_words:
                    if amountPro==WordText and num==1:
                        print(sentence)
                        print("AmountPro")
                        amountappend="<amount>"
                        categoryarray.append(amountappend)
                        # file_amountPro.write(sentence)
                        # file_amountPro.write('\n\n')
                        # file_results.write(sentence)
                        # file_results.write("\n\n")
                        flag=1
                        break
                
                for date in date_Words:
                    if date==WordText and num==1:
                        print(sentence)
                        print("Date")
                        dateappend="<date>"
                        categoryarray.append(dateappend)
                        # file_dateWords.write(sentence)
                        # file_dateWords.write('\n\n')
                        # file_results.write(sentence)
                        # file_results.write("\n\n")
                        flag=1
                        break
                
                for time in time_Words:
                    if time==WordText and num==1:
                        print(sentence)
                        print("time")
                        timeappend="<time>"
                        categoryarray.append(timeappend)
                        # file_time.write(sentence)
                        # file_time.write('\n\n')
                        # file_results.write(sentence)
                        # file_results.write("\n\n")
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
                    yearappend="<year>"
                    categoryarray.append(yearappend)
                    # file_year.write(sentence)
                    # file_year.write('\n\n')
                    # file_results.write(sentence)
                    # file_results.write("\n\n")
                    # print(sentence)
                    flag=1
        
            if(phoneIndicator==1):
                print(sentence)
                print("Phone")
                phoneappend="<phone>"
                categoryarray.append(phoneappend)
                # file_phone.write(sentence)
                # file_phone.write('\n\n')
                file_results.write(sentence)
                file_results.write("\n\n")
            elif(ratio==1 and flag==0):
                file_results.write(sentence)
                file_results.write("\n\n")
                ratioappend="<ratio>"
                categoryarray.append(ratioappend)
                # file_ratio.write(sentence)
                # file_ratio.write('\n\n')  
                print("Ratio")    
            elif(flag==0 and num==1):
                # file_num.write(sentence)
                # file_num.write('\n\n')
                # print(sentence)
                numappend="<num>"
                categoryarray.append(numappend)
                print("num")
            elif(flag==0):
                # file_rest.write(sentence)
                # file_rest.write('\n\n')
                print(sentence)
            ratio=0
            amountpre=0

        # idx=0
        # for element in numarray:
        #     print(element,end=' ')
        # print()

            # idx=0
            # resultsent=""
            # for word in sent.words:
            #     WordText=word.text
            #     if WordText.isnumeric() or re.match(pattern_required,WordText):
            #         resultsent+=WordText+" "
            #         resultsent+categoryarray[idx]
            #         idx+=1
            #         print(categoryarray[idx])
            #     else:
            #         resultsent+=WordText
            #         resultsent+=" "
            # file_results.write(resultsent)
        idx=0
        matchindex=0;
        # for element in numarray:
        #     replacetext=sentence[element]+categoryarray[idx]
        #     sentence=sentence.replace(sentence[element],replacetext)
        #     idx+=1;
        # file_results.write(sentence)

        finalsent=""

        # for j in range(0,len(categoryarray)):
        #     print(categoryarray[j],j)

        # for i in range(0,3):
        #     print(numarray[i])
        # print(len(numarray))
        for i, sent in enumerate(hi_doc.sentences):
            for word in sent.words:
                matchindex+=1;
                WordText=word.text
                if idx<len(categoryarray):
                    if matchindex==numarray[idx]:
                        finalsent+=WordText
                        print(idx,len(numarray))
                        finalsent+=categoryarray[idx]
                        finalsent+=" "
                        idx+=1;
                    else:
                        finalsent+=WordText
                        finalsent+=" "
                else:
                    finalsent+=WordText
                    finalsent+=" "
                
        file_results.write(finalsent)
        file_results.write('\n\n')


# जब आप अपने लक्षित खोजशब्दों की पहचान कर सकते हैं और अमेज़ॅन खोज परिणाम पृष्ठ पर आपके उत्पाद कैसे प्रदर्शन कर रहे हैं, तो आप अपने लिस्टिंग अनुकूलन को बेहतर बनाने और मौजूदा त्रुटियों को ठीक करने में सक्षम होंगे। आपको अलग-अलग परीक्षण करना चाहिए और खोजशब्द शोधकर्ताओं को अपनी सूची में सबसे अधिक प्रासंगिक और लक्षित खोज शब्दों को खोजने के लिए प्रदान करना चाहिए। विशिष्ट और लंबी-पूंछ खोज शब्दों के मुकाबले दूसरों की तुलना में अधिक आशय है और छोटे या हाल ही में स्थापित व्यवसायों के लिए रैंकिंग बूस्टर के रूप में सेवा कर सकते हैं। हालांकि, यह उल्लेखनीय है कि व्यापक खोज शब्द कम प्रतिस्पर्धी खोज शब्दों की तुलना में अधिक ट्रैफ़िक को आकर्षित करते हैं।
# इसके लिए जीआईसी और जीजीआईसी के शिक्षकों का ब्यौरा तैयार कराया जाएगा कि कौन कब रिटायर हो रहा है।
# इसके जवाब में वह कहते हैं, “यह बिल्कुल अलग मुद्दा है।
# VIDEO: खाना बनाने के दौरान स्कूल में लगी आग, 4 लाख की संपत्ति स्वाहा
# यूक्रेन के प्रधानमंत्री ओलेक्सी होन्चारुक ने शुक्रवार को राष्ट्रपति वलोडिमिर ज़ेलेंस्की को अपना इस्तीफा सौंप दिया।
# सरकारें राजनीतिक दलों की होती हैं और वे जनता के हित में कोई योजना चलाते हैं, जिनमें वायदे ही तो होते हैं।
# इसके बाद इंटरनेशनल अलर्ट भी जारी कर दिया गया था।
# 'रेस 3' में जहां जैकलीन फर्नांडीज अपने  पोल डांस से अदाओं का तड़का लगाती नजर आएंगी।
# स्‍वदेशी फाइटर जेट तेजस और लाइट कॉम्‍बेट हेलीकॉप्‍टर (एलसीएच) इस एक्‍सरसाइज के स्‍टार परफॉमर्स हैं।
# बलदेव और सूबेदार मेजर ब्रह्मू ने कहा कि सीताराम भारद्वाज हमारे पड़ोसी हैं।
# यहां वर्तमान में 20 हजार पुस्तकें थी जो अभी रैन बसेरा परिसर के कक्ष में रखी हुई है।
# संजय किशन और जोगेन मोहन को राजभवन के दरबार हॉल में एक समारोह में राज्यपाल जगदीश मुखी ने पद और गोपनीयता की शपथ दिलाई।
# राम रहीम विवाद का मामला है जिससे मैं बचना चाहता हूं।
# टॉयलेट एक कथा: बिलासपुर की लड़की ने शादी से इनकार किया तब युवक ने बनवाया टॉयलेट, दिल्ली की टीम ने द  | टॉयलेट एक कथा: बिलासपुर की लड़की ने शादी से इनकार किया तब युवक ने बनवाया टॉयलेट, दिल्ली की टीम ने दिया गिफ्ट - Dainik Bhaskar
# समै समै सुंदर सबै रूपु-कुरूपु न कोइ।
# जबकि दूसरा व्यावहारिक पक्ष यह है कि उक्त आरक्षित पदों पर चयनित होकर आरक्षण का लाभ उठा चुके उच्च पदस्थ, उच्च पदों से सेवानिवृत, सुविधा सम्पन्न एवं धनाढ्य लोगों की संतानें ही वर्तमान में अधिकतर आरक्षित पदों पर नियुक्ति पा रही हैं। जिसके पक्ष में कोई आधिकारिक आंकड़े तो नहीं हैं, लेकिन लोक अवधारणा इस विचार की पुष्टि करती है।
# एयरपोर्ट के अधिकारियों ने बताया कि इंटरनेट भारत-मध्यपूर्व-पश्चिमी यूरोप सबमरीन केबल में आई एक गड़बड़ी की वजह से धीमा हो गया।
# ओवरऑल ग्रोथ अच्‍छी रही है और 7 इंडस्‍ट्री वर्टिकल में से 6 में हमने सालाना आधार पर वृद्धि दर्ज की है।
# इसलिए नियुक्ति प्रक्रिया को आगे बढ़ा दिया गया।
# सावधि जमा से रिटायरमेंट के बाद जिंदगी हो जाती है आसान
# रिपोर्ट की माने तो इस पर एक भारतीय अधिकारी ने कहा सरकार विदेशी मोटरसाइकिलों पर आयात शुल्क अधिक लगाती है क्योंकि घरेलू उद्योग को सुरक्षा देने के लिए यह जरूरी है.
# ऐसे में बोर्ड ने दोबारा परीक्षा कराने का फैसला लिया।
# ज्यादा संभावना मौजूदा जीएसपीए के विस्तार की है।
# काही ठिकाणी पावसाचे पाणी वस्तीत घुसले; तर तुळस येथे घरावर आंब्याचे झाड पडून नुकसान झाले.
# उन्होंने बताया कि एक बार उनकी मम्मी सीढ़ियों से गिर गई थीं और उन्हें 9 फ्रैक्चर आए थे.
# इसी प्रकार पश्चिमी तट और ग़ज़्ज़ा पट्टी के फ़िलिस्तीनियों ने भी भूमि दिवस मनाया।
# जदयू नेता केसी त्यागी ने कहा कि मैं चुनाव आयोग की घोषणा का स्वागत करता हूं लेकिन DA में इस समय बढ़ोतरी करना सवालों के घेरे में है।
# मशहूर अमेरिकी टीवी निर्देशक और अभिनेता का नाम बताइए, जिनका नवम्बर 2017 में 86 वर्ष की आयु में निधन हुआ है?
# अन्य जानकारियों के लिए इस मामले की मूल खबर को पढ़ सकते हैं, जिसका शीर्षक नीचे है…
# फिल्म इंडस्ट्री की एक और अभिनेत्री ने कास्टिंग काउच की सच्चाई को स्वीकार किया है। इस अभिनेत्री ने कहा, “उसने मुझे खुलेआम कहा, देखो तुम मुझे पसंद हो, इसे तुम भी जानती हो, लेकिन मुझे तुम्हारे साथ सेक्सुअल रिलेशन चाहिए, मैंने कहा- नहीं, इसके बाद उसने कहा कि अगर तुम ना कह रही हो तो तुम्हें मैं अपनी फिल्म में रोल नहीं दे रहा हूं, उसने मुझे भला-बुरा कहा और कहा कि तुम्हें कोई रोल नहीं मिलेगा।”
# #  वह राज्य सरकार जिसने स्कूली छात्रों के लिए ‘मधु ऐप’ लांच की- ओडिशा सरकार
# कहा- यह भावनाओं के इजहार का सबसे सस्ता लेकिन सबसे शक्तिशाली संकेत
# विधानसभा चुनाव की दृष्टि से देखे तो यह वही मतदान केन्द्र हैं, जिसमें वर्ष 2013 के विधानसभा चुनाव में भाजपा विधायक केडी देशमुख को पूरे विधानसभा क्षेत्र में सर्वाधिक मत मिले थे। यह मतदान केन्द्र शासकीय कन्या प्राथमिक शाला भवन के अतिरिक्त कक्ष हेटी के बूथ नंबर 3 है। यहां वैसे तो कोई जातीय समीकरण नहीं है। लेकिन ग्रामीणों ने चर्चा में बताया कि इस गांव में जनप्रतिनिधि केवल चुनाव के दौरान ही आते हैं। यहां सड़क की समस्या वर्षों पुरानी है। आज तक गांव के पहुंचने के लिए पक्का रास्ता नहीं बन पाया। इस गांव के लिए एक रास्ता में महकेपार से गोरेघाट होते हुए हेटी और दूसरे रास्ता में महकेपार से कन्हडग़ांव होते हेटी पहुंचा जाता है। लेकिन आज तक दोनों ही मार्ग में पक्की सड़क नहीं बन पाई। बारिश होने पर यह मार्ग कीचड़ में तब्दील हो जाता है। इसी तरह नल-जल योजना नहीं होने से हर समय पेयजल की समस्या बनी रहती है। पेयजल के लिए आधा किमी का सफर तय करना पड़ता है। बिजली तो है लेकिन उसके आने-जाने का कोई समय नहीं है। गांव में आज तक स्ट्रीट लाइट नहीं लग पाई। पंचायत के माध्यम से ग्रामीणों ने अनेक बार माननीय से समस्याओं की गुहार भी लगाई, लेकिन समस्या का अभी तक समाधान नहीं हो पाया।
# यामध्ये, अटक करण्यात आलेले अ‍ॅड.
# कन्वेनर, नेशनल आरटीआई फोरम
# जून महीने में थोक महंगाई दर बढ़कर 5.77 प्रतिशत हो गया है। महंगाई दर में इजाफे की वजह महंगी सब्जियां और पेट्रोल डीजल की कीमतों में इजाफा बताया गया है। बता दें कि पिछले महीने थोक महंगाई दर का आंकड़ा 4.43 प्रतिशत था। जबकि पिछले साल ये आंकड़ा मात्र 0.90 प्रतिशत था। सरकार द्वारा आज जारी आंकड़ों के मुताबिक जून में खाद्य पदार्थों की महंगाई दर 1.80 प्रतिशत थी, जबकि मई में ये आंकड़ा 1.60 प्रतिशत था। महंगाई को आधार बनाकर कांग्रेस समेत विपक्षी पार्टियां मोदी सरकार को 18 जुलाई से शुरू होने जा रहे मॉनसून सत्र में घेरने का प्रयास करेगी। इस वक्त खुदरा महंगाई दर भी पांच महीने के उच्चतम स्तर पर है। लिहाजा विपक्ष के पास सरकार पर हमला करने का मौका है।
# उन्होंने कहा कि निकट भविष्य में डेटिंग एप्स की लोकप्रियता और बढ़ने की सम्भावना है।                    



        

# file_date.close()
# file_rest.close()
# file_time.close()
# file_num.close()
# file_train.close()
# file_phone.close()
# file_amount.close()
# file_amountPro.close()
# file_dateWords.close()
# # file_share.close()
# file_year.close()
# file_dateWords.close()
# file_ratio.close()

file_results.close()