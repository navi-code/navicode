import tokenize

def comment_parser(py_source_file):
    comments = []

    with open(py_source_file, "r") as file:
        tokens = tokenize.generate_tokens(file.readline)
        for token in tokens:
            if token.type == 55:
                comments.append(token.string.strip())
            elif token.type == 3 and token.string.startswith('"""'):
                comments.append(token.string.strip())

    return comments