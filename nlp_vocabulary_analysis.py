"""
NLP Vocabulary Analysis: War and Peace (English vs Tamil)
Comparative study of vocabulary construction and language characteristics
"""

import requests
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import pickle
import os

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass


class VocabularyAnalyzer:
    """
    A class to analyze and compare vocabulary characteristics across languages
    """
    
    def __init__(self, language='english'):
        self.language = language
        self.lemmatizer = WordNetLemmatizer()
        self.raw_text = ""
        self.processed_tokens = []
        self.vocabulary = {}
        self.vocab_size = 0
        self.tfidf_scores = {}
        
    def download_text(self, url):
        """Download text from Project Gutenberg"""
        print(f"Downloading text from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            self.raw_text = response.text
            print(f"Downloaded {len(self.raw_text)} characters")
            return True
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return False
    
    def clean_gutenberg_text(self):
        """Remove Project Gutenberg header and footer"""
        start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
        end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
        
        start_idx = self.raw_text.find(start_marker)
        end_idx = self.raw_text.find(end_marker)
        
        if start_idx != -1:
            start_idx = self.raw_text.find('\n', start_idx) + 1
        else:
            start_idx = 0
            
        if end_idx != -1:
            self.raw_text = self.raw_text[start_idx:end_idx]
        else:
            self.raw_text = self.raw_text[start_idx:]
        
        print(f"Cleaned text: {len(self.raw_text)} characters")
    
    def preprocess_english(self):
        """
        Preprocess English text:
        1. Tokenization
        2. Lowercasing
        3. Remove punctuation and numbers
        4. Remove stopwords
        5. Lemmatization
        """
        print("Preprocessing English text...")
        
        # Convert to lowercase
        text = self.raw_text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        print(f"Total tokens after tokenization: {len(tokens)}")
        
        # Remove punctuation, numbers, and short words
        tokens = [token for token in tokens if token.isalpha() and len(token) > 2]
        print(f"Tokens after removing punctuation/numbers: {len(tokens)}")
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        print(f"Tokens after stopword removal: {len(tokens)}")
        
        # Lemmatization
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        self.processed_tokens = tokens
        print(f"Final processed tokens: {len(tokens)}")
        
        return tokens
    
    def preprocess_tamil(self):
        """
        Preprocess Tamil text:
        1. Tokenization (word-based)
        2. Remove English characters
        3. Remove punctuation and numbers
        4. Remove very short tokens
        """
        print("Preprocessing Tamil text...")
        
        # Simple tokenization by whitespace
        tokens = self.raw_text.split()
        print(f"Total tokens after tokenization: {len(tokens)}")
        
        # Remove punctuation and numbers
        cleaned_tokens = []
        for token in tokens:
            # Keep only Tamil characters (Unicode range: U+0B80 to U+0BFF)
            cleaned_token = re.sub(r'[^\u0B80-\u0BFF]+', '', token)
            if len(cleaned_token) > 1:  # Keep tokens with at least 2 characters
                cleaned_tokens.append(cleaned_token)
        
        print(f"Tokens after cleaning: {len(cleaned_tokens)}")
        
        # Note: Tamil stopword removal is optional as the library support varies
        # For this assignment, we'll keep all Tamil words
        
        self.processed_tokens = cleaned_tokens
        print(f"Final processed tokens: {len(cleaned_tokens)}")
        
        return cleaned_tokens
    
    def build_vocabulary(self):
        """
        Build vocabulary using frequency-based approach
        Calculate TF (Term Frequency) scores
        """
        print("Building vocabulary...")
        
        # Count word frequencies
        word_freq = Counter(self.processed_tokens)
        self.vocabulary = dict(word_freq)
        self.vocab_size = len(self.vocabulary)
        
        print(f"Vocabulary size: {self.vocab_size}")
        
        # Calculate term frequencies (TF)
        total_words = len(self.processed_tokens)
        self.tfidf_scores = {word: freq/total_words for word, freq in self.vocabulary.items()}
        
        return self.vocabulary
    
    def get_top_words(self, n=20):
        """Get top N frequent words"""
        return dict(Counter(self.vocabulary).most_common(n))
    
    def calculate_lexical_diversity(self):
        """Calculate Type-Token Ratio (TTR)"""
        if len(self.processed_tokens) > 0:
            ttr = self.vocab_size / len(self.processed_tokens)
            return ttr
        return 0
    
    def save_results(self, filename):
        """Save analysis results to file"""
        with open(filename, 'wb') as f:
            pickle.dump({
                'vocabulary': self.vocabulary,
                'processed_tokens': self.processed_tokens,
                'vocab_size': self.vocab_size,
                'tfidf_scores': self.tfidf_scores
            }, f)
        print(f"Results saved to {filename}")


class TextTranslator:
    """
    Class to handle translation from English to Tamil
    """
    
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='ta')
    
    def translate_text(self, text, chunk_size=4500, max_chunks=100):
        """
        Translate text in chunks to avoid API limitations
        Note: For full book translation, consider using Google Cloud Translation API
        For this assignment, we'll translate a significant portion
        """
        print("Translating text to Tamil...")
        print(f"Text length: {len(text)} characters")
        
        # Split text into chunks (deep-translator has a 5000 char limit)
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        total_chunks = min(len(chunks), max_chunks)
        
        print(f"Translating {total_chunks} chunks...")
        
        translated_chunks = []
        for i, chunk in enumerate(chunks[:max_chunks]):
            try:
                print(f"Translating chunk {i+1}/{total_chunks}...")
                translation = self.translator.translate(chunk)
                translated_chunks.append(translation)
                time.sleep(0.5)  # Avoid rate limiting
            except Exception as e:
                print(f"Error translating chunk {i+1}: {e}")
                # Continue with available translations
                break
        
        translated_text = ' '.join(translated_chunks)
        print(f"Translation complete: {len(translated_text)} characters")
        
        return translated_text


def create_visualizations(english_analyzer, tamil_analyzer):
    """
    Create comprehensive visualizations comparing English and Tamil vocabularies
    """
    print("\nCreating visualizations...")
    
    # Configure matplotlib to support Tamil fonts
    import matplotlib
    from matplotlib import font_manager
    
    # Find Tamil font explicitly
    tamil_font = None
    for font in font_manager.fontManager.ttflist:
        if 'Tamil' in font.name and 'Noto Sans Tamil' == font.name:
            tamil_font = font_manager.FontProperties(fname=font.fname)
            print(f"Using Tamil font: {font.name}")
            break
    
    if not tamil_font:
        # Fallback to any Tamil font
        for font in font_manager.fontManager.ttflist:
            if 'Tamil' in font.name and 'Supplement' not in font.name:
                tamil_font = font_manager.FontProperties(fname=font.fname)
                print(f"Using Tamil font: {font.name}")
                break
    
    if not tamil_font:
        print("Warning: No Tamil font found")
        tamil_font = font_manager.FontProperties()
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (15, 10)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Vocabulary Size Comparison
    ax1 = axes[0, 0]
    languages = ['English', 'Tamil']
    vocab_sizes = [english_analyzer.vocab_size, tamil_analyzer.vocab_size]
    colors = ['#3498db', '#e74c3c']
    ax1.bar(languages, vocab_sizes, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Vocabulary Size', fontsize=12, fontweight='bold')
    ax1.set_title('Vocabulary Size Comparison', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    for i, v in enumerate(vocab_sizes):
        ax1.text(i, v + 100, str(v), ha='center', va='bottom', fontweight='bold')
    
    # 2. Top 15 Words - English
    ax2 = axes[0, 1]
    top_english = english_analyzer.get_top_words(15)
    words_en = list(top_english.keys())
    freqs_en = list(top_english.values())
    ax2.barh(words_en, freqs_en, color='#3498db', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Frequency', fontsize=12, fontweight='bold')
    ax2.set_title('Top 15 Words in English', fontsize=14, fontweight='bold')
    ax2.invert_yaxis()
    ax2.grid(axis='x', alpha=0.3)
    
    # 3. Top 15 Words - Tamil
    ax3 = axes[1, 0]
    top_tamil = tamil_analyzer.get_top_words(15)
    words_ta = list(top_tamil.keys())
    freqs_ta = list(top_tamil.values())
    
    ax3.barh(words_ta, freqs_ta, color='#e74c3c', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Frequency', fontsize=12, fontweight='bold')
    ax3.set_title('Top 15 Words in Tamil', fontsize=14, fontweight='bold')
    ax3.invert_yaxis()
    ax3.grid(axis='x', alpha=0.3)
    
    # Apply Tamil font to y-axis labels
    for label in ax3.get_yticklabels():
        label.set_fontproperties(tamil_font)
        label.set_fontsize(11)
    
    # 4. Lexical Diversity Comparison
    ax4 = axes[1, 1]
    ttr_english = english_analyzer.calculate_lexical_diversity()
    ttr_tamil = tamil_analyzer.calculate_lexical_diversity()
    ttr_values = [ttr_english, ttr_tamil]
    ax4.bar(languages, ttr_values, color=colors, alpha=0.7, edgecolor='black')
    ax4.set_ylabel('Type-Token Ratio', fontsize=12, fontweight='bold')
    ax4.set_title('Lexical Diversity (TTR)', fontsize=14, fontweight='bold')
    ax4.set_ylim(0, max(ttr_values) * 1.2)
    ax4.grid(axis='y', alpha=0.3)
    for i, v in enumerate(ttr_values):
        ax4.text(i, v + 0.001, f'{v:.4f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('vocabulary_comparison.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as 'vocabulary_comparison.png'")
    
    # Create frequency distribution plot
    plt.figure(figsize=(14, 6))
    
    # English frequency distribution
    plt.subplot(1, 2, 1)
    freq_values_en = sorted(english_analyzer.vocabulary.values(), reverse=True)[:100]
    plt.plot(range(1, len(freq_values_en) + 1), freq_values_en, 'b-', linewidth=2)
    plt.xlabel('Rank', fontsize=12, fontweight='bold')
    plt.ylabel('Frequency', fontsize=12, fontweight='bold')
    plt.title('English Word Frequency Distribution (Top 100)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xscale('log')
    
    # Tamil frequency distribution
    plt.subplot(1, 2, 2)
    freq_values_ta = sorted(tamil_analyzer.vocabulary.values(), reverse=True)[:100]
    plt.plot(range(1, len(freq_values_ta) + 1), freq_values_ta, 'r-', linewidth=2)
    plt.xlabel('Rank', fontsize=12, fontweight='bold')
    plt.ylabel('Frequency', fontsize=12, fontweight='bold')
    plt.title('Tamil Word Frequency Distribution (Top 100)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xscale('log')
    
    plt.tight_layout()
    plt.savefig('frequency_distribution.png', dpi=300, bbox_inches='tight')
    print("Frequency distribution saved as 'frequency_distribution.png'")


def generate_report(english_analyzer, tamil_analyzer):
    """
    Generate comprehensive comparison report
    """
    report = []
    report.append("="*80)
    report.append("COMPARATIVE VOCABULARY ANALYSIS: WAR AND PEACE")
    report.append("English vs Tamil Translation")
    report.append("="*80)
    report.append("")
    
    # Basic Statistics
    report.append("1. BASIC STATISTICS")
    report.append("-" * 80)
    report.append(f"{'Metric':<40} {'English':>15} {'Tamil':>15}")
    report.append("-" * 80)
    report.append(f"{'Total Tokens (after preprocessing)':<40} {len(english_analyzer.processed_tokens):>15,} {len(tamil_analyzer.processed_tokens):>15,}")
    report.append(f"{'Vocabulary Size (Unique Words)':<40} {english_analyzer.vocab_size:>15,} {tamil_analyzer.vocab_size:>15,}")
    report.append(f"{'Type-Token Ratio (Lexical Diversity)':<40} {english_analyzer.calculate_lexical_diversity():>15.4f} {tamil_analyzer.calculate_lexical_diversity():>15.4f}")
    report.append("")
    
    # Top Words
    report.append("2. TOP 20 MOST FREQUENT WORDS")
    report.append("-" * 80)
    report.append(f"{'English Words':<25} {'Frequency':>12} | {'Tamil Words':<25} {'Frequency':>12}")
    report.append("-" * 80)
    
    top_en = list(english_analyzer.get_top_words(20).items())
    top_ta = list(tamil_analyzer.get_top_words(20).items())
    
    for i in range(20):
        en_word, en_freq = top_en[i] if i < len(top_en) else ("", 0)
        ta_word, ta_freq = top_ta[i] if i < len(top_ta) else ("", 0)
        report.append(f"{en_word:<25} {en_freq:>12,} | {ta_word:<25} {ta_freq:>12,}")
    
    report.append("")
    
    # Analysis
    report.append("3. COMPARATIVE ANALYSIS")
    report.append("-" * 80)
    
    vocab_diff = abs(english_analyzer.vocab_size - tamil_analyzer.vocab_size)
    vocab_diff_pct = (vocab_diff / english_analyzer.vocab_size) * 100
    
    report.append(f"• Vocabulary Size Difference: {vocab_diff:,} words ({vocab_diff_pct:.2f}%)")
    
    if tamil_analyzer.vocab_size > english_analyzer.vocab_size:
        report.append(f"  Tamil has a larger vocabulary, indicating potential morphological richness")
    else:
        report.append(f"  English has a larger vocabulary in this processed form")
    
    report.append("")
    
    ttr_en = english_analyzer.calculate_lexical_diversity()
    ttr_ta = tamil_analyzer.calculate_lexical_diversity()
    
    report.append(f"• Lexical Diversity (Type-Token Ratio):")
    report.append(f"  English TTR: {ttr_en:.4f}")
    report.append(f"  Tamil TTR: {ttr_ta:.4f}")
    
    if ttr_ta > ttr_en:
        report.append(f"  Tamil shows higher lexical diversity, likely due to morphological variations")
    else:
        report.append(f"  English shows higher lexical diversity in this analysis")
    
    report.append("")
    report.append("="*80)
    
    # Save and print report
    report_text = '\n'.join(report)
    print("\n" + report_text)
    
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print("\nReport saved to 'analysis_report.txt'")


def main():
    """
    Main execution function
    """
    print("="*80)
    print("NLP VOCABULARY ANALYSIS: WAR AND PEACE")
    print("Comparative Study of English and Tamil")
    print("="*80)
    print()
    
    # URL for War and Peace
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    
    # Check if we have cached translations
    use_cached = os.path.exists('tamil_text.txt')
    
    # ENGLISH ANALYSIS
    print("\n" + "="*80)
    print("PART 1: ENGLISH TEXT ANALYSIS")
    print("="*80)
    
    english_analyzer = VocabularyAnalyzer(language='english')
    
    # Download and process English text
    if english_analyzer.download_text(url):
        english_analyzer.clean_gutenberg_text()
        english_analyzer.preprocess_english()
        english_analyzer.build_vocabulary()
        english_analyzer.save_results('english_results.pkl')
    
    # TRANSLATION
    print("\n" + "="*80)
    print("PART 2: TRANSLATION TO TAMIL")
    print("="*80)
    
    if use_cached:
        print("Loading cached Tamil translation...")
        with open('tamil_text.txt', 'r', encoding='utf-8') as f:
            tamil_text = f.read()
        print(f"Loaded {len(tamil_text)} characters")
    else:
        translator = TextTranslator()
        # For the assignment, translate a significant portion (first ~50 pages worth)
        # Full translation may take very long due to API limitations
        sample_text = english_analyzer.raw_text[:100000]  # Approx 50 pages
        tamil_text = translator.translate_text(sample_text)
        
        # Save translated text
        with open('tamil_text.txt', 'w', encoding='utf-8') as f:
            f.write(tamil_text)
        print("Tamil translation saved to 'tamil_text.txt'")
    
    # TAMIL ANALYSIS
    print("\n" + "="*80)
    print("PART 3: TAMIL TEXT ANALYSIS")
    print("="*80)
    
    tamil_analyzer = VocabularyAnalyzer(language='tamil')
    tamil_analyzer.raw_text = tamil_text
    tamil_analyzer.preprocess_tamil()
    tamil_analyzer.build_vocabulary()
    tamil_analyzer.save_results('tamil_results.pkl')
    
    # COMPARISON AND VISUALIZATION
    print("\n" + "="*80)
    print("PART 4: COMPARATIVE ANALYSIS")
    print("="*80)
    
    create_visualizations(english_analyzer, tamil_analyzer)
    generate_report(english_analyzer, tamil_analyzer)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  • vocabulary_comparison.png - Comparative visualizations")
    print("  • frequency_distribution.png - Word frequency plots")
    print("  • analysis_report.txt - Detailed comparison report")
    print("  • english_results.pkl - English analysis results")
    print("  • tamil_results.pkl - Tamil analysis results")
    print("  • tamil_text.txt - Translated Tamil text")
    print()


if __name__ == "__main__":
    main()
