import pandas as pd
import nltk
from nltk.corpus import stopwords
import spacy

def preprocess(file_path):
    # Carregue o modelo spaCy para o idioma português
    nlp = spacy.load("pt_core_news_sm")

    # Faça o download das stopwords em português
    nltk.download("stopwords")
    stop_words = set(stopwords.words("portuguese"))
    stop_words.remove('não')

    # Leia o arquivo CSV
    df = pd.read_csv(file_path)

    # Função para remover stopwords e lematizar um texto
    def preprocess_text(row):
        if isinstance(row["opinion"], str):
            # Tokenize o texto com spaCy
            doc = nlp(row["opinion"])

            # Remova stopwords e lematize
            lemmatized_tokens = [token.lemma_ for token in doc if token.text.lower() not in stop_words]

            # Junte os tokens em um texto novamente
            processed_text = " ".join(lemmatized_tokens)

            return processed_text
        else:
            print(f"Ignorando valor não string: {row['opinion']}")
            # Se não for uma string, retorne vazio ou outra ação apropriada
            return ""

    # Aplique a função de pré-processamento à coluna de reviews
    df["reviews_processadas"] = df.apply(preprocess_text, axis=1)

    # Salve o DataFrame de volta em um novo arquivo CSV
    df.to_csv(file_path, index=False)

