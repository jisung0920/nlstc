# -*- coding: utf-8 -*-
import word_extractor.word_parser as parser
import link_processor.data_miner as miner
import semantic_similituder.sentence_comparator as similar_op
import nltk

"""
truth_check is composed of functions 

It makes you can use module easily in sequence
"""

def truth_check(sentence,vocab_file,model_file, file_types=["html","pdf"], search_engine="https://www.google.com/search",
                keyword_num=3, synonym_num=2,batch_size = 64, eval_file = "result.txt",
                accuracy_threshold = 0.4, process_debug = False, key_num_option = False ) :

    if key_num_option :
        keyword_num = keywordNumOptimer(sentence)

    if process_debug:
        print("INPUT : "+sentence)

        print("\nToken extracting ...")
    """
    Word extraction 
     1. Make query (google search form) 
     2. Get keywords and synonyms from sentence 
    """
    wordParser = parser.WordParser(sentence,keyword_num,synonym_num)
    querys = wordParser.query_generator(file_types)
    search_words = wordParser.searching_word_generator()
    keywords = wordParser.keywords


    ###
    if process_debug:
        print("\tkeyword :")
        keywords_str = "\t\t"
        for k in keywords :
            keywords_str = keywords_str+k +" | "
        print keywords_str

        print("\tquery :")
        for q in querys :
            print("\t\t"+q)
    ###


        print("\n\nLink mining ...")
        """
        Link finder
         1. Find url on the internet
        """
    sentence_miners = [None] * len(querys)
    for i in range(len(querys)) :
        sentence_miners[i] = miner.LinkMiner(search_engine,querys[i])


    ###
    if process_debug:
        print("\turl")
        for sen_miner in sentence_miners :
            for link in sen_miner.url_list :
                print("\t\t"+link)
    ###


        print("\n\nsentence extracting ...")
        """
        Sentence extraction
         1. Extract sentences from url (including search_words)
         2. Save sentences in result.txt file
        """

        ###
        print("\tToken :")
        token_str = "\t\t"
        for t in search_words :
            token_str= token_str+t+" | "
        print token_str
    ###


    link_dic = dict()
    url_chunk = []
    for sen_miner in sentence_miners :
        url_chunk.append(sen_miner.url_list)

    ref_sentences = miner.sentence_crawling(search_words,url_chunk,link_dic,file_types)

    ref_sentences = list(set(ref_sentences))
    miner.learningFormatting(sentence,ref_sentences,eval_file)


    if process_debug:

    ###
        print("\tOUTPUT FILE(sentences) : "+eval_file)
        ###

        print("\n\nsentence comparing ...")
    """
    Sentence comparing
     1. Compare input sentence with ref sentence
     2. Score semantic simility  
    """
    result_list,pred_list = similar_op.comparator(batch_size, eval_file, vocab_file, model_file)
    
#     result_dic = dict(zip(ref_sentences,result_list))
    
    print("\n\n[Result]\n")

    """
    output format : JSON (sentence , url, accuracy)
    filter value =1, pred
    """

    print('{result : [')
    for i in range(len(result_list)) :
        if result_list[i]==1 and pred_list[i]> accuracy_threshold :
            print(' \n {{ \"sentence\" : \"{key}\" \n \"url\" : \"{url}\" \n  \"accuracy\" : \"{value}\" }},'.format(key = ref_sentences[i],url=link_dic[ref_sentences[i]],value=pred_list[i]))
    print(']}')
#     for ref_sentence,result in result_dic :
#         print("sentence : {key} \n- {value}".format(key = ref_sentence,value=result))

#     for ref_sentence,url in link_dic.items() :
#         print("sentence : {key} \nurl : {value}".format(key=ref_sentence,value=url))



def keywordNumOptimer(sentence) :
    keyNum =0
    sen_tokens = nltk.sent_tokenize(sentence)
    num_sen = len(sen_tokens)
    keyNum += num_sen

    word_tokens = nltk.word_tokenize(sentence)
    num_word = len(word_tokens)
    keyNum += num_word/10

    return keyNum
