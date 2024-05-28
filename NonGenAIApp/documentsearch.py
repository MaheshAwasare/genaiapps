import spacy


def search_document(question, document_path):
    nlp = spacy.load("en_core_web_sm")

    with open(document_path, 'r') as file:
        document = file.read()

    doc = nlp(document)

    # Search for sentences containing the question
    for sentence in doc.sents:
        if question.lower() in sentence.text.lower():
            return sentence.text

    # If the question is not found in any sentence
    return "Sorry, the answer to the question was not found in the document."


# Example usage:
question = "What is the capital of France?"
document_path = "document.txt"  # Replace with the path to your document
answer = search_document(question, document_path)
print(answer)
