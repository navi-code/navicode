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
                comments_dump[len(corpus)] = str(filename) + '---' + str(comment[1])

                corpus.append(comment[0])

        print(f"\nComputing comment embeddings for {len(corpus)} comments . . .")

        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

        print("\nSaving comment embeddings . . .")

        torch.save(corpus_embeddings, os.path.join(navi_dir, dirname + '_navi.emb'))

        with open(os.path.join(navi_dir, dirname + '_navi.json'), 'w') as file:
            json.dump(comments_dump, file, indent=4)

def navicode_query():
    cur_dir = os.getcwd()
    navi_dir = os.path.join(cur_dir, ".navi")

    if not os.path.exists(navi_dir):
        print("\033[91mError: NaviCode not initialized, use 'navicode --init' to initialize!")
        return

    dirname = os.path.basename(cur_dir)

    print("\nInitializing model . . .")

    embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

    print("\nLoading comment embeddings and lookup JSON . . .")

    corpus_embeddings = torch.load(os.path.join(navi_dir, dirname + '_navi.emb'))

    with open(os.path.join(navi_dir, dirname + '_navi.json'), 'r') as file:
        lookup = json.load(file)

    while True:
        query = input(">>> Enter your query (exit to quit): ")
        if query == "exit":
            break

        query_embedding = embedder.encode(query, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        cos_scores = cos_scores.cpu()

        topk = 3
        scores, idxs = torch.topk(cos_scores, k=topk)

        print(f"\nTop-{topk} matches are:\n")

        for idx in idxs:
            filename, line_num = lookup[str(idx.item())].split("---")
            print(f"Match found in file - {filename} at line number around - {line_num}")

