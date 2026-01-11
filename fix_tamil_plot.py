#!/usr/bin/env python3
"""
Fixed Tamil font rendering for matplotlib
"""

import pickle
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import seaborn as sns

# Load results
print("Loading analysis results...")
with open('english_results.pkl', 'rb') as f:
    english_data = pickle.load(f)
with open('tamil_results.pkl', 'rb') as f:
    tamil_data = pickle.load(f)

class SimpleAnalyzer:
    def __init__(self, data):
        self.vocabulary = data['vocabulary']
        self.vocab_size = data['vocab_size']
        self.processed_tokens = data['processed_tokens']
    
    def get_top_words(self, n=20):
        from collections import Counter
        return dict(Counter(self.vocabulary).most_common(n))
    
    def calculate_lexical_diversity(self):
        return self.vocab_size / len(self.processed_tokens) if self.processed_tokens else 0

english_analyzer = SimpleAnalyzer(english_data)
tamil_analyzer = SimpleAnalyzer(tamil_data)

print(f"English vocab: {english_analyzer.vocab_size}, Tamil vocab: {tamil_analyzer.vocab_size}")

# Find Tamil font
print("\nFinding Tamil fonts...")
tamil_font = None
for font in font_manager.fontManager.ttflist:
    if 'Tamil' in font.name and 'Noto Sans Tamil' == font.name:
        tamil_font = font_manager.FontProperties(fname=font.fname)
        print(f"✓ Using: {font.name} ({font.fname})")
        break

if not tamil_font:
    # Try any Tamil font
    for font in font_manager.fontManager.ttflist:
        if 'Tamil' in font.name and 'Supplement' not in font.name:
            tamil_font = font_manager.FontProperties(fname=font.fname)
            print(f"✓ Using fallback: {font.name}")
            break

if not tamil_font:
    print("⚠ No Tamil font found!")
    tamil_font = font_manager.FontProperties()

# Create visualization
print("\nGenerating plots...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
sns.set_style("whitegrid")

# 1. Vocabulary Size
ax1 = axes[0, 0]
languages = ['English', 'Tamil']
vocab_sizes = [english_analyzer.vocab_size, tamil_analyzer.vocab_size]
colors = ['#3498db', '#e74c3c']
bars = ax1.bar(languages, vocab_sizes, color=colors, alpha=0.7, edgecolor='black')
ax1.set_ylabel('Vocabulary Size', fontsize=12, fontweight='bold')
ax1.set_title('Vocabulary Size Comparison', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
for i, v in enumerate(vocab_sizes):
    ax1.text(i, v + 100, str(v), ha='center', va='bottom', fontweight='bold')

# 2. Top 15 English Words
ax2 = axes[0, 1]
top_english = english_analyzer.get_top_words(15)
words_en = list(top_english.keys())
freqs_en = list(top_english.values())
ax2.barh(words_en, freqs_en, color='#3498db', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Frequency', fontsize=12, fontweight='bold')
ax2.set_title('Top 15 Words in English', fontsize=14, fontweight='bold')
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

# 3. Top 15 Tamil Words - WITH EXPLICIT FONT
ax3 = axes[1, 0]
top_tamil = tamil_analyzer.get_top_words(15)
words_ta = list(top_tamil.keys())
freqs_ta = list(top_tamil.values())

ax3.barh(words_ta, freqs_ta, color='#e74c3c', alpha=0.7, edgecolor='black')
ax3.set_xlabel('Frequency', fontsize=12, fontweight='bold')
ax3.set_title('Top 15 Words in Tamil', fontsize=14, fontweight='bold')
ax3.invert_yaxis()
ax3.grid(axis='x', alpha=0.3)

# Apply Tamil font to y-tick labels
for label in ax3.get_yticklabels():
    label.set_fontproperties(tamil_font)
    label.set_fontsize(11)

# 4. Lexical Diversity
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
print("✅ Saved: vocabulary_comparison.png")
plt.close()

# Frequency distribution
print("Creating frequency distributions...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

freq_en = sorted(english_analyzer.vocabulary.values(), reverse=True)[:100]
ax1.plot(range(1, len(freq_en) + 1), freq_en, 'b-', linewidth=2)
ax1.set_xlabel('Rank', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax1.set_title('English Word Frequency (Top 100)', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')
ax1.set_xscale('log')

freq_ta = sorted(tamil_analyzer.vocabulary.values(), reverse=True)[:100]
ax2.plot(range(1, len(freq_ta) + 1), freq_ta, 'r-', linewidth=2)
ax2.set_xlabel('Rank', fontsize=12, fontweight='bold')
ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax2.set_title('Tamil Word Frequency (Top 100)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_yscale('log')
ax2.set_xscale('log')

plt.tight_layout()
plt.savefig('frequency_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Saved: frequency_distribution.png")

print("\n✨ Done! Tamil characters should now render correctly.")
