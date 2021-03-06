#!/usr/bin/env bash
conda create -n tnaggregator-4 python=3.6
source activate tnaggregator-4
conda config --add channels conda-forge
conda install cython
conda install numpy
~/anaconda3/envs/tnaggregator-4/bin/pip install pandas
~/anaconda3/envs/tnaggregator-4/bin/pip install gensim
~/anaconda3/envs/tnaggregator-4/bin/pip install spacy
python -m spacy download en
~/anaconda3/envs/tnaggregator-4/bin/pip install flask scrapy gunicorn
~/anaconda3/envs/tnaggregator-4/bin/pip install pyyaml dataset
<FIX XGBOOST>
~/anaconda3/envs/tnaggregator-4/bin/pip install xgboost
  ~/anaconda3/envs/tnaggregator-4/bin/pip install scikit-learn scipy matplotlib

~/anaconda3/envs/tnaggregator-4/bin/pip install mysqlclient
~/anaconda3/envs/tnaggregator-4/bin/pip install ansible




