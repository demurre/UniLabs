def count_words(text):
    if not text:
        return 0

    spaces = text.count(' ')

    return spaces + 1

text = "Sample text for counting"
word_count = count_words(text)
print(f"Number of words: {word_count}")