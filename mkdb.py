import os
import argparse
from tqdm import tqdm
from decimal import Decimal
import pandas as pd
import boto3

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('qanda')

parser = argparse.ArgumentParser(description='一問一答のExcelファイルを読み込み、Markdown形式で出力する')

parser.add_argument('file', help='参照するExcelファイル')
parser.add_argument('-t', '--tag', help='指定するタグ')
parser.add_argument('--csv', action='store_true')

args = parser.parse_args()

file_name = args.file
file_ext = os.path.splitext(file_name)[1]
select_tag = args.tag

if file_ext == '.xlsx':
    df = pd.read_excel(file_name).fillna('')
elif file_ext == '.csv':
    df = pd.read_csv(file_name).fillna('')
else:
    exit(1)

items = []
all_tags = set()

test_title = os.path.splitext(os.path.basename(file_name))[0]
questions = []

for idx, row in df.iterrows():
    question_text = row['questions']
    answer_text = row['answers']
    tags = []
    tags_set = set()
    for tag_idx in range(4):
        if f"tag{tag_idx}" in row:
            tag = row[f"tag{tag_idx}"]
            if tag:
                tags += [tag]
                all_tags.add(tag)
                tags_set.add(tag)
    if (not select_tag) or (select_tag in tags):
        questions += [{
            'pname': 'eigo1',
            'qno': Decimal(idx+1),
            'question': question_text,
            'answer': answer_text,
            'tags': tags_set,
        }]

for question in tqdm(questions):
    table.put_item(Item=question)
