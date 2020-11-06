import os
import json
from sentence_transformers import SentenceTransformer, util
import torch

from navicode.parsers.python.parse_comments import comment_parser

def navicode_init():
    print("\nInitializing model . . .")

    embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

    cur_dir = os.getcwd()

    python_files = []

    for dirpath, _, files in os.walk(cur_dir):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith('.py'):
                python_files.append(fname)

    print(f"\nFound {len(python_files)} python sources\n")

    if len(python_files) > 0:
        dirname = os.path.basename(cur_dir)

        navi_dir = os.path.join(cur_dir, ".navi")
        if not os.path.exists(navi_dir):
            os.mkdir(navi_dir)

        corpus = []

        comments_dump = {}
        for i, python_file in enumerate(python_files):
            print(f"[{i+1}/{len(python_files)}] Scanning {python_file}")
            comments = comment_parser(python_file)
            filename = python_file[python_file.index(dirname):]
            for comment in comments:
                if filename in comments_dump.keys():
                    comments_dump[filename].append(len(corpus))
                else:
                    comments_dump[filename] = [len(corpus)]

                corpus.append(comment)

        print(f"\nComputing comment embeddings for {len(corpus)} comments . . .")

        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

        print("\nSaving comment embeddings . . .")

        torch.save(corpus_embeddings, os.path.join(navi_dir, dirname + '_navi.emb'))

        with open(os.path.join(navi_dir, dirname + '_navi.json'), 'w') as file:
            json.dump(comments_dump, file, indent=4)