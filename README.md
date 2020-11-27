# NaviCode

Navigate through large codebases with ease. NaviCode is a command line tool which uses "Sentence Transformers" to search for relevant filename along with line number which might be relevant to your problem, just query whatever change you want to make and it will point out which files and sections of codebase to look into.

## Installation

```bash
user@programmer~:$ pip install git+https://github.com/navi-code/navicode
```

## Steps to run

1) Before starting to use navicode you have to initialize your project with navicode, navigate to your project directory and call --init inside it:- (This is a one time operation)

```bash
user@programmer~:$ navicode --init
```

2) Once initialized you can start querying:-

```bash
user@programmer~:$ navicode --query
```