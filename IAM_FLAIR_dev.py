from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import (FlairEmbeddings, StackedEmbeddings,
                              TransformerWordEmbeddings, WordEmbeddings, ELMoEmbeddings)
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from torch.optim import AdamW
from transformers import LlamaTokenizer

data_folder = 'BIO_FLAIR_FORMAT'
#define the txt columns
columns = {0 : 'text', 1: 'ner'}
dataset = 'rwth_18_all'
corpus : Corpus = ColumnCorpus(
    data_folder, 
    columns, 
    f'iam_train_{dataset}_BIO.txt', 
    f'iam_test_{dataset}_BIO.txt',
    f'iam_valid_{dataset}_BIO.txt'
)

# print(len(corpus.train))
# print(corpus.train[0].to_tagged_string('ner'))

label_type = 'ner'

label_dict = corpus.make_label_dictionary(label_type=label_type, add_unk=False)
# print(label_dict)

# embeddings = TransformerWordEmbeddings(model='chavinlo/gpt4-x-alpaca', layers='-1', subtoken_pooling='first',fine_tune=True,use_context=False)#use_context=True
# tagger = SequenceTagger(hidden_size=256, embeddings=embeddings, tag_dictionary=label_dict, tag_type='ner',use_crf=False,use_rnn=False,reproject_embeddings=False)
# trainer = ModelTrainer(tagger,corpus)
# trainer.fine_tune(f'resources/taggers/iam_ner_alpaca7b_{dataset}', learning_rate=5.0e-6, mini_batch_size=4, mini_batch_chunk_size=1, embeddings_storage_mode='cpu')

embedding_types = [
    WordEmbeddings('glove'),
    FlairEmbeddings('multi-forward'),
    FlairEmbeddings('multi-backward'),
    #TransformerWordEmbeddings(model='elmo-medium', layers='-1', subtoken_pooling='first',fine_tune=True,use_context=False)
]
optim = AdamW
embeddings = StackedEmbeddings(embeddings=embedding_types)

tagger = SequenceTagger(hidden_size=1024, embeddings=embeddings, tag_dictionary=label_dict, tag_type=label_type)
trainer = ModelTrainer(tagger,corpus)
trainer.train(f'resources/taggers/iam_ner_flair_gloves_forward_{dataset}', learning_rate=0.01, mini_batch_size=16, max_epochs=150, embeddings_storage_mode='cpu', optimizer= optim)

#from transformers import LlamaTokenizer
