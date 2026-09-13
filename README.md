## WORDPIECE TOKENIZER
# WordPiece Tokenizer From Scratch

A simple educational implementation of a WordPiece tokenizer built from scratch using Python and Streamlit.

This project demonstrates how WordPiece tokenization learns useful subword units from a small training dataset and uses the learned vocabulary to tokenize new words and convert them into token IDs.

## Live Demo

https://wordpiecetokenizer-crkhjwcwt9btcp5hmo6jkm.streamlit.app/

## Project Overview

WordPiece is a subword tokenization technique widely used in modern Natural Language Processing (NLP) systems.

Instead of treating every complete word as a single token, WordPiece can divide a word into smaller meaningful subword units. This allows the tokenizer to handle words that were not directly present in the training vocabulary.

For example:

```text
player → pla ##y ##er
