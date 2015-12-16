Before doing anything, please pip install -r requirements.txt

The .txt files in corruption annotated files/ folder are the original news articles. The .ann files in corruption annotated files/ folder are the human annotations, the gold standard.


Please run python baselineSentenceRecognizer.py for producing the pipelined annotation files. After running, .ann.machine files will show up in corruption annotated data. These are the machine annotations. 

Please run python evaluation for evaluating the precision, recall scores for the machine annotations vs gold standard.

To train the CRF model for NER of certain fields, we need to first produce the training files. This can be done by python trainCrimeTagFile.py.

Then to run the CRF training, do python crf_rec.py test 400 4, the 400 here specifies number of files used for training.

maxent_model.py and features.py were used to produce a logistic classficier for the time_tags.

parse_text.py is how we connect to BosonNLP

Other files are of lesser importance, but we are happy to explain if necessary.

864Final.pptx is our presentation on Thursday.

Best Wishes, 
Shidan & Tingtao

=============================================================
The following are work flows and thought process, please ignore.

NER - 分人名
sentence extraction
classification


关于中文的主语指代
corresponding mapping person v crime
主语在之前的句子里 keep a stack of names？
分词有点不准确 syntactic parsing？
标记不给力 1991-3750 －问下sloan的人

1. 先把新华网数据分词
2a. 分topic － word embedding API
word2vec
2b. 做syntactic parsing
3. 做主语罪名mapping
Coreference resolution
Boson, Jieba, 哈工大


For Friday 11/13
1. Tools and APIs for analyzing. TINGTAO
word embedding - word2vec
segmentation + syntactic parsing - Boson
Coreference - use stanford nlp
2. Build infrastructure SHIDAN
streamline the entire process
input = .txt
output = .ann
have statistics for evaluation
recall, precision, f1 compared to annotated.


3. Record 6.864 lecture SHIDAN



1. 并列关系
2. distance分数在同一句里
3. output合并set	Shidan
4. evaluation模糊	Shidan
5. evaluation score distribution visualization	Shidan
6. 整理extraction contribution
7. summarize problems


Bad annotations
2004 9286