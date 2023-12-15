# Sabichão
Escola de Artes, Ciências e Humanidades da Universidade de São Paulo (EACH-USP)

Bacharelado em Sistemas de Informação

Disciplina de Resolução de Problemas 2

Orientadora: Profª Drª Patrícia Rufino

### Grupo
Lizandro Raposo, Lucas Gigante, Miguel Puga, Natalia Augusto e Pietro Zalla

### Overview
Sabichão é uma plataforma desenvolvida como projeto para suportar os estudos do grupo nos campos de aprendizado de máquina e processamento de dados. O sistema incorpora um modelo de análise de sentimentos e é capaz de realizar classificações qualitativas de avaliações coletadas do marketplace da Amazon. 

A inspiração de concepção do projeto foram os experimentos de análise de sentimentos em avaliações de produtos. Este tipo de texto confere grande carga semântica e emocional e se apresenta como um excelente caso de estudo, uma vez que a classificação em polaridades (positivo, negativo e neutro) é um conceito fundamental da área.

Há uma recente movimentação na academia pelo estudo computacional de textos avaliatórios, e a seção de trabalhos relacionados destaca trabalhos exitosos nesse sentido. Dentre os algoritmos de classificação abordados na literatura, destacam-se a Floresta Aleatória (ou Random Forest) e as Redes Neurais Convolucionais (CNNs).

A metodologia adotada para o desenvolvimento do projeto é estruturada em três grandes etapas: (i) coleta e processamento dos dados; (ii) experimento comparativo de algoritmos de aprendizado de máquina para a análise de sentimento; e (iii) implementação de um sistema integrado com um modelo de análise de sentimentos e conectado ao marketplace da Amazon.

Na primeira etapa, são coletadas extensas avaliações de produtos online, de modo a garantir uma base de dados para treinamento abrangente e representativa. Depois, os dados passam por uma meticulosa etapa de pré-processamento, o que inclui a limpeza de textos, tokenização e vetorização, visando prepará-los para uma análise de sentimentos mais precisa. 

Em seguida, são observados os resultados de medidas de avaliação dos algoritmos de RF e CNN, tais como F1-score e acurácia, discutidos na próxima seção, e é realizada a escolha de implementar a CNN no modelo do Sabichão. Por fim, é feita a construção e implementação da plataforma, com apoio da linguagem Python e diversos frameworks de integração.

Como resulado dos experimentos, a comparação entre o desempenho do Random Forest e da CNN revelou nuances
importantes, destacando as áreas em que cada modelo se sobressai. A precisão da CNN, por exemplo, mostrou sua eficácia em classificar corretamente as avaliações, além disso, a CNN exibiu também um recall, acurácia e F1-score superiores à Random Forest, evidenciando sua habilidade em capturar nuances e padrões mais complexos.

Cada etapa contou com a utilização de ferramentas específicas de apoio. Na primeira, o processamento de dados contou com os frameworks NLTK e TF-IDF, responsáveis pela remoção de stopwords, lematização, tokenização e vetorização dos textos coletados. A plataforma Kaggle ofereceu um ambiente de desenvolvimento ideal para a criação e treinamento dos algoritmos de machine learning, onde foi possível acessar bibliotecas como o Keras e o Scikit-learn, indispensáveis para a configuração dos hiperparâmetros e indicação de medidas de desempenho. 

A criação do sistema se deu com o suporte do Flask, framework que possibilita o desenho de interfaces no ambiente Python, e de ferramentas de web scraping, como o Scrapy e o ScrapeOps.
