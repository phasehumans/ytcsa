## **Project Overview**  
This project is a **YouTube Comment Sentiment Analysis System** that extracts comments from a given YouTube video and classifies them into three sentiment categories:  
- **Positive**  
- **Negative**  
- **Neutral**  

It is built using **Flask**, **Machine Learning**, and the **YouTube Data API**, providing a simple web-based interface to analyze audience reactions.

## **Features**  
- Extracts comments from any **YouTube video** using its URL.  
- Performs **sentiment analysis** (Positive, Negative, Neutral) using a **Machine Learning model**.  
- Displays **sentiment distribution** in a graphical format.  
- Provides a **user-friendly web interface** built with Flask.  

## **Phases of the Project**
1. **Data Collection**   
   - Using a pre-labeled dataset (**CSV file**)  

2. **Data Processing**  
   - Removing URLs, special characters, and emojis  
   - Converting text to lowercase for consistency  
   - Removing stopwords to improve model accuracy  
   - Tokenization to split text into meaningful units  
   - Lemmatization / Stemming to get the root form of words  

3. **Feature Extraction**  
- Used TF-IDF Vectorizer to convert textual data into numerical form.
- Captures important keywords while reducing the impact of common words.
- Produces a sparse matrix representation used for training the ML model.
   
4. **Model Training**  
- Trained a Multinomial Naive Bayes classifier on the preprocessed data
- Achieved reliable accuracy on test data
  
5. **Web Application Development**  
- Users input YouTube video URL
- Backend fetches top comments using YouTube Data API
- Preprocesses and vectorizes comments
- Predicts sentiment for each comment
- Displays result as:
   - Text list with sentiment tags
   - Pie chart for sentiment distribution

6. **Deployment**  
- Can be run locally via Flask
- Ready for deployment to platforms like Heroku, Render, or Streamlit Cloud


## **Technologies Used**  
| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Flask** | Web framework for UI & API |
| **YouTube Data API** | Fetching comments from YouTube videos |
| **Scikit-learn** | Machine learning model for sentiment analysis |
| **NLTK & Text Processing** | Preprocessing text data |
| **Pandas & NumPy** | Data manipulation and processing |
| **HTML, CSS, Bootstrap** | Frontend design |


## **Screenshots**
<img width="1914" height="966" alt="image" src="https://github.com/user-attachments/assets/5be294cb-9a96-4680-b338-045f6a1a38f5" />
<img width="1919" height="1021" alt="image" src="https://github.com/user-attachments/assets/ac60782b-82ed-4ca4-b28e-eb20722d1e3b" />





