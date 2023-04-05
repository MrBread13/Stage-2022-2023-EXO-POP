from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from flair.embeddings import TransformerWordEmbeddings, WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from flair.trainers import ModelTrainer

data_folder = 'BIO_FLAIR_FORMAT'
#define the txt columns
columns = {0 : 'text', 1: 'ner'}
corpus : Corpus = ColumnCorpus(
    data_folder, 
    columns, 
    'iam_train_custom_6_perfect_BIO.txt', 
    'iam_test_custom_6_perfect_BIO.txt',
    'iam_valid_custom_6_perfect_BIO.txt'
)

print(len(corpus.train))
print(corpus.train[0].to_tagged_string('ner'))

label_type = 'ner'

label_dict = corpus.make_label_dictionary(label_type=label_type, add_unk=False)
print(label_dict)

embeddings = TransformerWordEmbeddings(model='bert-base-uncased', layers='-1', subtoken_pooling='first',fine_tune=True,use_context=False)#use_context=True
tagger = SequenceTagger(hidden_size=256, embeddings=embeddings, tag_dictionary=label_dict, tag_type='ner',use_crf=False,use_rnn=False,reproject_embeddings=False)
trainer = ModelTrainer(tagger,corpus)
trainer.fine_tune('resources/taggers/iam_ner_bert_custom_6_perfect_nocontext', learning_rate=5.0e-6, mini_batch_size=4, mini_batch_chunk_size=1, embeddings_storage_mode='cpu')

# embedding_types = [
#     WordEmbeddings('glove'),
#     FlairEmbeddings('news-forward'),
#     FlairEmbeddings('news-backward')
# ]

# embeddings = StackedEmbeddings(embeddings=embedding_types)

# tagger = SequenceTagger(hidden_size=256, embeddings=embeddings, tag_dictionary=label_dict, tag_type=label_type)
# trainer = ModelTrainer(tagger,corpus)
# trainer.train('resources/taggers/iam_ner_flair_gloves_18_custom_perfect', learning_rate=0.01, mini_batch_size=64, max_epochs=150, embeddings_storage_mode='none')
