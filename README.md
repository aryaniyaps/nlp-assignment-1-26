# NLP Assignment: Comparative Vocabulary Analysis

## Project Structure

This project analyzes "War and Peace" by Leo Tolstoy in English and Tamil to compare vocabulary characteristics across languages.

## Files

- `nlp_vocabulary_analysis.py` - Main Python script for analysis
- `requirements.txt` - Python dependencies
- `ASSIGNMENT_DOCUMENTATION.md` - Complete documentation and video scripts
- `README.md` - This file

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Analysis

```bash
python nlp_vocabulary_analysis.py
```

### 3. Expected Runtime

- First run: 20-40 minutes (includes translation)
- Subsequent runs: 5-10 minutes (uses cached translation)

## Output Files

After running the script, you'll get:

1. **vocabulary_comparison.png** - Visual comparison charts
   - Vocabulary size comparison
   - Top 15 words in English
   - Top 15 words in Tamil
   - Lexical diversity (Type-Token Ratio)

2. **frequency_distribution.png** - Word frequency plots
   - English frequency distribution (Zipf's Law)
   - Tamil frequency distribution (Zipf's Law)

3. **analysis_report.txt** - Detailed statistical report
   - Basic statistics
   - Top 20 frequent words for each language
   - Comparative analysis

4. **english_results.pkl** - Serialized English analysis results

5. **tamil_results.pkl** - Serialized Tamil analysis results

6. **tamil_text.txt** - Cached Tamil translation (for faster reruns)

## Key Features

- **Automatic Text Download** from Project Gutenberg
- **Comprehensive Preprocessing** including tokenization, normalization, stopword removal, and lemmatization
- **Language-Specific Handling** for English and Tamil (Tamil script)
- **Translation Support** using Google Translate API
- **Statistical Analysis** including vocabulary size, frequency distribution, and lexical diversity
- **Visualizations** with publication-quality plots
- **Caching** for faster subsequent runs

## Assignment Requirements

This project fulfills all assignment requirements:

✅ Fictional text of ~100 pages (War and Peace: 560,000 words)  
✅ Digital form from Project Gutenberg  
✅ NLP preprocessing and vocabulary construction  
✅ Translation to Indian regional language (Tamil)  
✅ Same algorithm applied to both languages  
✅ Comparative analysis of vocabulary characteristics  
✅ Quantitative results and visualizations  
✅ Technical documentation  
✅ Video scripts provided in documentation

## Video Recording Guide

The complete documentation includes two detailed video scripts:

1. **English Text Video** (2-3 minutes)
   - Dataset and algorithm explanation
   - Preprocessing pipeline demonstration
   - Results presentation

2. **Tamil Text Video** (2-3 minutes)
   - Translation process
   - Tamil-specific preprocessing
   - Comparative analysis

See [ASSIGNMENT_DOCUMENTATION.md](ASSIGNMENT_DOCUMENTATION.md) for complete scripts.

## Expected Results

**English:**
- Vocabulary: ~15,000-20,000 unique words
- Tokens: ~130,000-150,000
- Type-Token Ratio: ~0.12-0.15

**Tamil:**
- Vocabulary: ~18,000-25,000 unique words (15-30% more)
- Tokens: ~130,000-160,000
- Type-Token Ratio: ~0.14-0.18 (higher lexical diversity)

**Key Finding:** Tamil shows larger vocabulary and higher lexical diversity due to morphological richness.

## Algorithm Used

**Frequency-Based Vocabulary Construction with TF Analysis**

- Counts word occurrences
- Calculates term frequencies
- Simple, interpretable, and effective for comparison
- Industry standard baseline approach

## Preprocessing Steps

### English:
1. Tokenization (NLTK)
2. Lowercasing
3. Remove punctuation/numbers
4. Stopword removal
5. Lemmatization

### Tamil:
1. Whitespace tokenization
2. Tamil character filtering
3. Remove punctuation/numbers
4. Preserve vocabulary integrity (no stopword removal)

## Dependencies

- Python 3.8+
- requests - Download text from web
- matplotlib - Create visualizations
- seaborn - Enhanced plotting
- googletrans - Translation API
- nltk - Natural language processing
- pandas - Data manipulation
- numpy - Numerical operations
- scikit-learn - TF-IDF analysis

## Troubleshooting

### googletrans issues:
```bash
pip install googletrans==4.0.0rc1
```

### NLTK data missing:
```python
import nltk
nltk.download('all')
```

### Hindi fonts not displaying:
- Install Tamil fonts on your system
- Ubuntu: `sudo apt-get install fonts-taml fonts-lohit-taml`

## Learning Outcomes

This project demonstrates:

- ✅ CO1: Fundamental concepts of language processing
- ✅ CO2: Language models and NLP application development
- Understanding of tokenization and vocabulary construction
- Language-specific preprocessing techniques
- Comparative linguistic analysis
- Data visualization and interpretation

## Documentation

For complete details, methodology, analysis, and video scripts, see:

**[ASSIGNMENT_DOCUMENTATION.md](ASSIGNMENT_DOCUMENTATION.md)**

This includes:
- Detailed methodology
- Algorithm justification
- Complete preprocessing pipeline
- Video scripts (word-by-word)
- Expected results interpretation
- Comparative analysis
- Technical insights
- Submission checklist

## Academic Integrity

This code is provided as a learning tool. Understand the concepts, modify as needed, and properly cite any sources used in your submission.

## Support

For questions:
1. Review ASSIGNMENT_DOCUMENTATION.md
2. Check console output for errors
3. Verify dependencies are installed
4. Ensure Python 3.8+ is being used

---

**Good luck with your assignment!** 🎓

Remember to:
1. Run the code and generate outputs
2. Record your videos using the provided scripts
3. Upload videos to Google Drive
4. Include shareable links in submission
5. Submit all required files

---

*Project created for NLP Assignment - Vocabulary Construction and Comparative Analysis*
