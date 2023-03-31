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
    'iam_train_rwth_6_all_BIO.txt', 
    'iam_test_rwth_6_all_BIO.txt',
    'iam_valid_rwth_6_all_BIO.txt'
)

print(len(corpus.train))
print(corpus.train[0].to_tagged_string('ner'))

label_type = 'ner'

label_dict = corpus.make_label_dictionary(label_type=label_type, add_unk=False)
print(label_dict)

# embeddings = TransformerWordEmbeddings(model='xlm-roberta-large', layers='-1', subtoken_pooling='first',fine_tune=True,use_context=True)
# tagger = SequenceTagger(hidden_size=256, embeddings=embeddings, tag_dictionary=label_dict, tag_type='ner',use_crf=False,use_rnn=False,reproject_embeddings=False)
# trainer = ModelTrainer(tagger,corpus)
# trainer.fine_tune('resources/taggers/iam_ner_flert_fine_tuning', learning_rate=5.0e-6, mini_batch_size=8, mini_batch_chunk_size=1)

embedding_types = [
    WordEmbeddings('glove'),
    FlairEmbeddings('news-forward'),
    FlairEmbeddings('news-backward')
]

embeddings = StackedEmbeddings(embeddings=embedding_types)

tagger = SequenceTagger(hidden_size=256, embeddings=embeddings, tag_dictionary=label_dict, tag_type=label_type)
trainer = ModelTrainer(tagger,corpus)
trainer.train('resources/taggers/iam_ner_flair_gloves', learning_rate=0.01, mini_batch_size=64, max_epochs=150)
