# -*- coding: utf-8 -*-
import word_extractor.word_parser as parser
import link_processor.data_miner as miner
import semantic_similituder.sentence_comparator as similar_op

def truth_check(sentence,vocab_file,model_file, file_types=["html"], search_engine="https://www.google.com/search",
                keyword_num=3, synonym_num=2,batch_size = 64, eval_file = "result.txt" ) :

    print("\nToken extracting ...")

    wordParser = parser.WordParser(sentence,keyword_num,synonym_num)
    querys = wordParser.query_generator(file_types)
    search_words = wordParser.searching_word_generator()

    print("\n\nLink mining ...")

    sentence_miners = [None] * len(querys)
    for i in range(len(querys)) :
        sentence_miners[i] = miner.LinkMiner(search_engine,querys[i])


    print("\n\nsentence extracting ...")
    link_dic = dict()
    url_chunk = []
    for sen_miner in sentence_miners :
        url_chunk.append(sen_miner.url_list)

    ref_sentences = miner.sentence_crawling(search_words,url_chunk,link_dic,file_types)

    ref_sentences = list(set(ref_sentences))
    miner.learningFormatting(sentence,ref_sentences,eval_file)

    print("\n\nsentence comparing ...")


    result_list = similar_op.comparator(batch_size, eval_file, vocab_file, model_file)
    # result_dic = dict(zip(ref_sentences,result_list))
    #
    # for ref_sentence,result in result_dic :
    #     print("sentence : {key} \n- {value}".format(key = ref_sentence,value=result))

    for ref_sentence,url in link_dic.items() :
        print("sentence : {key} \nurl : {value}".format(key=ref_sentence,value=url))


sentence = "According to the report, the results of an EDA survey in China complied by analyst Nancy Wu, consumer electronics applications were the primary design market in China in 2005, replacing telecommunications/data communications, which fell to third place behind industrial controls."
vocab_file = "/Users/jisung/Documents/cse/DataSet/deepSiamese/runs/1546678177/checkpoints/vocab"
model_file = "/Users/jisung/Documents/cse/DataSet/deepSiamese/runs/1546678177/checkpoints/model-506000"
truth_check(sentence,vocab_file,model_file)

