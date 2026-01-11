#!/usr/bin/env python3
"""
Regenerate visualizations with proper Tamil font support
"""

import pickle
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# Load the saved results
print("Loading saved analysis results...")
with open('english_results.pkl', 'rb') as f:
    english_data = pickle.load(f)

with open('tamil_results.pkl', 'rb') as f:
    tamil_data = pickle.load(f)

# Create simple analyzer objects
class SimpleAnalyzer:
    def __init__(self, data):
        self.vocabulary = data['vocabulary']
        self.vocab_size = data['vocab_size']
        self.processed_tokens = data['processed_tokens']
    
    def get_top_words(self, n=20):
        from collections import Counter
        return dict(Counter(self.vocabulary).most_common(n))
    
    def calculate_lexical_diversity(self):
        if len(self.processed_tokens) > 0:
            return self.vocab_size / len(self.processed_tokens)
        return 0

english_analyzer = SimpleAnalyzer(english_data)
tamil_analyzer = SimpleAnalyzer(tamil_data)

print(f"English vocabulary: {english_analyzer.vocab_size}")
print(f"Tamil vocabulary: {tamil_analyzer.vocab_size}")

# Configure matplotlib for Tamil fonts FIRST
print("Configuring Tamil font support...")

# Find Tamil fonts explicitly
import matplotlib.font_manager as fm
tamil_fonts = [f for f in fm.fontManager.ttflist if 'Tamil' in f.name]
tamil_font_dict = {f.name: f.fname for f in tamil_fonts}

print("Available Tamil fonts:")
for name in sorted(tamil_font_dict.keys())[:5]:
    print(f"  - {name}")

# Prefer Noto Sans Tamil (main), then Lohit, then Samyak
preferred_fonts = ['Noto Sans Tamil', 'Lohit Tamil', 'Samyak Tamil']
tamil_font_name = None
for font_name in preferred_fonts:
    if font_name in tamil_font_dict:
        tamil_font_name = font_name
        break

if not tamil_font_name and tamil_fonts:
    tamil_font_name = tamil_fonts[0].name
elif not tamil_font_name:
    tamil_font_name = 'DejaVu Sans'
    print("Warning: No Tamil font found")

print(f"Using Tamil font: {tamil_font_name}")

from matplotlib import font_manager
font_prop = font_manager.FontProperties(family=tamil_font_name)

# Set as default for all text
matplotlib.rcParams['font.family'] = tamil_font_name
matplotlib.rcParams['axes.unicode_minus'] = False

# Set style
sns.set_style("whitegrid")

# Create figure with subplots
print("Creating visualizations...")
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

print("Tamil words to display:", words_ta[:3])  # Debug print

ax3.barh(words_ta, freqs_ta, color='#e74c3c', alpha=0.7, edgecolor='black')
ax3.set_xlabel('Frequency', fontsize=12, fontweight='bold', family='sans-serif')
ax3.set_title('Top 15 Words in Tamil', fontsize=14, fontweight='bold', family='sans-serif')
ax3.invert_yaxis()
ax3.grid(axis='x', alpha=0.3)

# Explicitly set Tamil font for y-axis labels
for label in ax3.get_yticklabels():
    label.set_fontfamily('sans-serif')
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
print("✅ Visualization saved as 'vocabulary_comparison.png'")
print("\nTamil font used:", matplotlib.rcParams['font.sans-serif'][0])
plt.close()

# Create frequency distribution plot
print("Creating frequency distribution plots...")
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# English frequency distribution
from collections import Counter
freq_values_en = sorted(english_analyzer.vocabulary.values(), reverse=True)[:100]
ax1.plot(range(1, len(freq_values_en) + 1), freq_values_en, 'b-', linewidth=2)
ax1.set_xlabel('Rank', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax1.set_title('English Word Frequency Distribution (Top 100)', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')
ax1.set_xscale('log')

# Tamil frequency distribution
freq_values_ta = sorted(tamil_analyzer.vocabulary.values(), reverse=True)[:100]
ax2.plot(range(1, len(freq_values_ta) + 1), freq_values_ta, 'r-', linewidth=2)
ax2.set_xlabel('Rank', fontsize=12, fontweight='bold')
ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax2.set_title('Tamil Word Frequency Distribution (Top 100)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_yscale('log')
ax2.set_xscale('log')

plt.tight_layout()
plt.savefig('frequency_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Frequency distribution saved as 'frequency_distribution.png'")

print("\n✨ All visualizations regenerated successfully!")
