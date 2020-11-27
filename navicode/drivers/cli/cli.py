import os
import json
import re

from sentence_transformers import SentenceTransformer, util
import torch
import faiss
import numpy as np

from navicode.parsers.python.parse_comments import comment_parser

def navicode_init():
    print("\nInitializing model . . .")

    embedder = SentenceTransformer('distilbert-base-nli-mean-tokens')

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
                comments_dump[len(corpus)] = str(filename) + '---' + str(comment[1]) + "---" + re.sub(r'[^a-zA-Z0-9]+', ' ', comment[0])

                corpus.append(re.sub(r'[^a-zA-Z0-9]+', ' ', comment[0]))

        print(f"\nComputing comment embeddings for {len(corpus)} comments . . .")

        corpus_embeddings = embedder.encode(corpus, show_progress_bar=True)

        print("\nIndexing comment embeddings . . .")
    
        index = faiss.IndexIDMap(faiss.IndexFlatIP(768))
        index.add_with_ids(corpus_embeddings, np.array(range(0, len(corpus))))
        faiss.write_index(index, os.path.join(navi_dir, dirname + '_navi'))

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

    print("\nLoading comment indexes and lookup JSON . . .")

    index = faiss.read_index(os.path.join(navi_dir, dirname + "_navi"))

    with open(os.path.join(navi_dir, dirname + '_navi.json'), 'r') as file:
        lookup = json.load(file)

    while True:
        query = input(">>> Enter your query (exit to quit): ")
        if query == "exit":
            break

        query_embedding = embedder.encode([query])
        
        k = 3
        top_k = index.search(query_embedding, k)

        for _id in top_k[1].tolist()[0]:
            print(lookup[str(_id)])

