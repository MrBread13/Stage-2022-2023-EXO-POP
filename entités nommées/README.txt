Named Entity (NE) Annotations for the George Washington Dataset(gw) and the IAM Database (iam) 


IAM Dataset: https://fki.tic.heia-fr.ch/databases/iam-handwriting-database

An empty row indicates a new sentence
The Information are comma separated

Data format:		
	iam:	word_img_id ne_tag

iam two formats: 
	perfect: only word images used in the rwth split are considered
	all: all word images from the pages are considered (with segmentation errors!)
	
iam two splits: 
	rwth: Data split proposed by RWTH Aachen
	custom: Specifically designed data split for the task of Named Entity Recognition
	
iam two NE tag sets: 
	6: Self designed tag set with 6 categories: Location (FAC, GPE, Location), Time (Date,Time), Cardinal (Cardinal, Ordinal, Percent, Quantity, Money), NORP, Person and Organization
	18: Tag set of Ontonotes with 18 categories: Cardinal, Date, Event, FAC, GPE, Language, Law, Location, Money, NORP, Ordinal, Organization, Person, Percent, Product, Quantity, Time and Work_of_art
