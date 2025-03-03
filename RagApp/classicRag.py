from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data listing wonders of the world
documents = [
    "The Great Wall of China is an ancient wall in China.",
    "Christ the Redeemer is a large statue in Rio de Janeiro, Brazil.",
    "Machu Picchu is an ancient Incan city in Peru.",
    "The Taj Mahal is a white marble mausoleum in India.",
    "The Colosseum is an ancient amphitheater in Rome, Italy.",
    "Petra is a historical and archaeological city in Jordan.",
    "Chichen Itza is a large pre-Columbian archaeological site in Mexico."
]
query = ["Tell me wonder from China"] # This is query that should be searched in given documents
vectorizer = TfidfVectorizer() # This useful but now almost forgot it seems
tfidf_matrix = vectorizer.fit_transform(documents) # Storing document vectors
query_vector = vectorizer.transform(query) # Convert the query to vector form
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten() #We use cosine similarity here
most_relevant_doc_index = cosine_similarities.argmax() # This is Retrieval
print(f"Most relevant document: {documents[most_relevant_doc_index]}")
