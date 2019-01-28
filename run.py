import sys
import nlstc

try :
    sentence = sys.argv[1]
    vocab_file = sys.argv[2]
    model_file = sys.argv[3]
    nlstc.truth_check(sentence,vocab_file,model_file)
    exit()
except :
    print "you can use this form - python nlstc.py 'sentence' 'vocabulary file path' 'model file path'"

sentence = raw_input("sentence : ")
vocab_file = raw_input("vocabulary path : ")
model_file = raw_input("model path : ")
nlstc.truth_check(sentence,vocab_file,model_file)
exit()


# sentence = "According to the report, the results of an EDA survey in China complied by analyst Nancy Wu, consumer electronics applications were the primary design market in China in 2005, replacing telecommunications/data communications, which fell to third place behind industrial controls."
# vocab_file = "/Users/jisung/Documents/cse/DataSet/deepSiamese/runs/1546678177/checkpoints/vocab"
# model_file = "/Users/jisung/Documents/cse/DataSet/deepSiamese/runs/1546678177/checkpoints/model-506000"
