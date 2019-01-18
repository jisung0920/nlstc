import word_extractor.word_parser as parser
import link_processor.data_miner as miner
import semantic_similituder.sentence_comparator as similar_op



def truth_check(sentence,vocab_file,model_file, file_types=["html","pdf"], search_engine="https://www.google.com/search",
                keyword_num=3, synonym_num=2,batch_size = 64, eval_file = "result.txt" ) :

    print("\nToken extracting ...")

    wordParser = parser.WordParser(sentence,keyword_num,synonym_num)
    querys = wordParser.query_generator(file_types)
    search_words = wordParser.searching_word_generator()

    print "\n\nLink mining ..."

    sentence_miners = [None] * len(querys)
    for i in range(len(querys)) :
        sentence_miners[i] = miner.LinkMiner(search_engine,querys[i])

    print("\n\nsentence extracting ...")

    url_chunk = []
    for sen_miner in sentence_miners :
        url_chunk.append(sen_miner.url_list)

    ref_sentences = miner.sentence_crawling(search_words,url_chunk,file_types)

    ref_sentences = list(set(ref_sentences))
    miner.learningFormatting(sentence,ref_sentences,eval_file)

    print("\n\nsentence comparing ...")
    result_list = similar_op.comparator(batch_size, eval_file, vocab_file, model_file)

    for i in result_list :
        print(i)


sentence = "According to the Report, the most common form of human trafficking (79%) is sexual exploitation"
vocab_file = "/Users/jisung/Documents/cse/DataSet/deepSiamese/runs/1546678177/checkpoints/vocab"
model_file = "/Users/jisung/Documents/cse/DataSet/deepSiamese/runs/1546678177/checkpoints/model-506000"
truth_check(sentence,vocab_file,model_file)

