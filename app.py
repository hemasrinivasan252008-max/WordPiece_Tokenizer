import streamlit as st
st.title("🔤 WordPiece Tokenizer From Scratch")

st.write(
    "This mini project demonstrates how WordPiece tokenization "
    "learns subwords using frequency-based scores and converts "
    "words into tokens and token IDs."
)

# Training data
word_freq = {
    "play": 3,
    "player": 2,
    "playing": 1
}

st.subheader("📚 Training Data")
st.caption("These words are used to train our tokenizer.")

for word, frequency in word_freq.items():
    st.write(f"{word} → {frequency}")


# Initial character splits
splits = {
    "play": ["p", "##l", "##a", "##y"],
    "player": ["p", "##l", "##a", "##y", "##e", "##r"],
    "playing": ["p", "##l", "##a", "##y", "##i", "##n", "##g"]
}

st.subheader("Initial Word Splits")

for word, tokens in splits.items():
    st.write(f"{word} → {' '.join(tokens)}")


from collections import Counter

# Count token frequencies
token_freq = Counter()

for word, frequency in word_freq.items():
    for token in splits[word]:
        token_freq[token] += frequency

st.subheader("Token Frequencies")

for token, frequency in token_freq.items():
    st.write(f"{token} → {frequency}")

# Count pair frequencies
pair_freq = Counter()

for word, frequency in word_freq.items():
    tokens = splits[word]

    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        pair_freq[pair] += frequency

st.subheader("Pair Frequencies")

for pair, frequency in pair_freq.items():
    st.write(f"{pair[0]} + {pair[1]} → {frequency}")

    # Calculate WordPiece scores
scores = {}

for pair, frequency in pair_freq.items():
    first = pair[0]
    second = pair[1]

    score = frequency / (
        token_freq[first] * token_freq[second]
    )

    scores[pair] = score

st.subheader("WordPiece Scores")

for pair, score in scores.items():
    st.write(f"{pair[0]} + {pair[1]} → {score:.4f}")

    # Find the highest-scoring pair
best_pair = max(scores, key=scores.get)
best_score = scores[best_pair]

st.subheader("Best Pair")

st.write(f"Pair: {best_pair[0]} + {best_pair[1]}")
st.write(f"Score: {best_score:.4f}")

# Merge the best pair
new_token = best_pair[0] + best_pair[1].replace("##", "")

for word in splits:
    tokens = splits[word]
    new_tokens = []
    i = 0

    while i < len(tokens):

        if i < len(tokens) - 1:
            current_pair = (tokens[i], tokens[i + 1])

            if current_pair == best_pair:
                new_tokens.append(new_token)
                i += 2
                continue

        new_tokens.append(tokens[i])
        i += 1

    splits[word] = new_tokens

st.subheader("After Merging")

st.write(f"Merged Token: {new_token}")

for word, tokens in splits.items():
    st.write(f"{word} → {' '.join(tokens)}")

    # Create the vocabulary
vocab = set()

for tokens in splits.values():
    for token in tokens:
        vocab.add(token)

st.subheader("Updated Vocabulary")

for token in sorted(vocab):
    st.write(token)

# Repeat WordPiece training
num_merges = 4

for step in range(num_merges):

    # Recalculate token frequencies
    token_freq = Counter()

    for word, frequency in word_freq.items():
        for token in splits[word]:
            token_freq[token] += frequency

    # Recalculate pair frequencies
    pair_freq = Counter()

    for word, frequency in word_freq.items():
        tokens = splits[word]

        for i in range(len(tokens) - 1):
            pair = (tokens[i], tokens[i + 1])
            pair_freq[pair] += frequency

    # Calculate scores
    scores = {}

    for pair, frequency in pair_freq.items():
        first = pair[0]
        second = pair[1]

        score = frequency / (
            token_freq[first] * token_freq[second]
        )

        scores[pair] = score

    # Stop if no pairs are available
    if not scores:
        break

    # Find best pair
    best_pair = max(scores, key=scores.get)

    # Create new token
    new_token = best_pair[0] + best_pair[1].replace("##", "")

    # Merge the pair
    for word in splits:
        tokens = splits[word]
        new_tokens = []
        i = 0

        while i < len(tokens):

            if i < len(tokens) - 1:
                current_pair = (tokens[i], tokens[i + 1])

                if current_pair == best_pair:
                    new_tokens.append(new_token)
                    i += 2
                    continue

            new_tokens.append(tokens[i])
            i += 1

        splits[word] = new_tokens


st.subheader("Final Trained Tokens")

for word, tokens in splits.items():
    st.write(f"{word} → {' '.join(tokens)}")
    # Input for a new word
st.subheader("Test the Tokenizer")

input_word = st.text_input("Enter a word:")

if input_word:
    st.write("You entered:", input_word)

# Tokenize the input word
def tokenize_word(word, vocab):
    tokens = []

    while len(word) > 0:
        found = False

        for i in range(len(word), 0, -1):
            part = word[:i]

            if len(tokens) > 0:
                part = "##" + part

            if part in vocab:
                tokens.append(part)
                word = word[i:]
                found = True
                break

        if not found:
            return ["[UNK]"]

    return tokens


# Create vocabulary from trained tokens
vocab = set()

for tokens in splits.values():
    for token in tokens:
        vocab.add(token)


# Show tokenization result
if input_word:
    result = tokenize_word(input_word.lower(), vocab)

    st.subheader("Tokenization Result")
    st.write("Tokens:", result)
# Create Token IDs
token_to_id = {
    "[UNK]": 0
}

for token in sorted(vocab):
    if token not in token_to_id:
        token_to_id[token] = len(token_to_id)


# Convert tokens to IDs
if input_word:
    token_ids = [token_to_id[token] for token in result]

    st.subheader("Token IDs")
    st.write(token_ids)

# Display vocabulary with Token IDs
st.subheader("Final Vocabulary")

for token, token_id in token_to_id.items():
    st.write(f"{token} → {token_id}")
