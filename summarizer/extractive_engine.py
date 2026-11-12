import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from summarizer.nlp_preprocessor import LegalNLPPreprocessor
from summarizer.legal_knowledge import LegalKnowledgeEngine
from summarizer.metrics import LegalSummaryMetrics
from config import Config

class HybridExtractiveSummarizer:
    def __init__(self):
        self.nlp = LegalNLPPreprocessor()
        self.knowledge = LegalKnowledgeEngine()
        self.metrics = LegalSummaryMetrics()

    def summarize(self, raw_text, ratio=Config.DEFAULT_SUMMARY_RATIO, target_sentences=None, algorithm='hybrid'):
        """
        Executes extractive summarization on input legal document text.
        
        Args:
            raw_text (str): Full text of legal agreement/statute/petition
            ratio (float): Ratio of sentences to extract (0.10 to 0.50)
            target_sentences (int, optional): Exact number of sentences to extract
            algorithm (str): 'hybrid', 'textrank', or 'tfidf'
            
        Returns:
            dict containing summary, sentences, metrics, clauses, legalese, accuracy.
        """
        if not raw_text or len(raw_text.strip()) == 0:
            return {
                "summary": "No text provided for analysis.",
                "sentences": [],
                "metrics": {},
                "clauses": {},
                "legalese": [],
                "risk_analysis": {}
            }

        # 1. NLP Preprocessing and Sentence Segmentation
        sentences = self.nlp.segment_sentences(raw_text)
        total_sentences = len(sentences)

        if total_sentences <= 3:
            # If document is extremely short, return original sentences
            summary_text = " ".join(sentences)
            return self._build_result_package(raw_text, summary_text, sentences, sentences, [1.0]*total_sentences)

        # 2. Determine target count
        if target_sentences and target_sentences > 0:
            k = min(target_sentences, total_sentences)
        else:
            k = max(Config.MIN_SUMMARY_SENTENCES, int(round(total_sentences * ratio)))
            k = min(k, Config.MAX_SUMMARY_SENTENCES, total_sentences)

        # 3. Calculate sentence representations and algorithm scores
        textrank_scores = self._compute_textrank_scores(sentences)
        tfidf_scores = self._compute_tfidf_scores(sentences)
        legal_cue_scores = self._compute_legal_cue_scores(sentences)

        # 4. Combine into final scores according to selected algorithm
        final_scores = np.zeros(total_sentences)
        if algorithm == 'textrank':
            final_scores = textrank_scores
        elif algorithm == 'tfidf':
            final_scores = tfidf_scores
        else: # 'hybrid' ensemble
            final_scores = (0.45 * textrank_scores) + (0.35 * tfidf_scores) + (0.20 * legal_cue_scores)

        # 5. Select Top-K sentences with Maximal Marginal Relevance (MMR)
        selected_indices = self._select_diverse_sentences(sentences, final_scores, k)

        # 6. Sort selected indices chronologically to preserve legal narrative logic
        selected_indices.sort()
        summary_sentences = [sentences[idx] for idx in selected_indices]
        summary_text = " ".join(summary_sentences)

        return self._build_result_package(raw_text, summary_text, sentences, summary_sentences, final_scores[selected_indices])

    def _compute_textrank_scores(self, sentences):
        """Constructs sentence similarity graph and executes PageRank."""
        n = len(sentences)
        if n == 0:
            return np.array([])
        if n == 1:
            return np.array([1.0])

        try:
            # Vectorize sentences using TF-IDF
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_mat = vectorizer.fit_transform(sentences)
            
            # Sentence-to-sentence cosine similarity matrix
            sim_matrix = cosine_similarity(tfidf_mat, tfidf_mat)
            np.fill_diagonal(sim_matrix, 0)  # remove self-loops
            
            # Build NetworkX weighted graph
            graph = nx.from_numpy_array(sim_matrix)
            scores_dict = nx.pagerank(
                graph,
                alpha=Config.TEXTRANK_DAMPING,
                max_iter=Config.TEXTRANK_MAX_ITER,
                tol=Config.TEXTRANK_CONVERGENCE
            )
            scores = np.array([scores_dict.get(i, 0.0) for i in range(n)])
            
            # Min-Max normalize
            s_min, s_max = scores.min(), scores.max()
            if s_max > s_min:
                scores = (scores - s_min) / (s_max - s_min)
            else:
                scores = np.ones(n) / n
            return scores
        except Exception:
            # Fallback uniform
            return np.ones(n) / n

    def _compute_tfidf_scores(self, sentences):
        """Computes TF-IDF sentence centroid saliency scores."""
        n = len(sentences)
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_mat = vectorizer.fit_transform(sentences)
            
            # Mean document centroid vector
            centroid = np.asarray(tfidf_mat.mean(axis=0))
            
            # Cosine similarity between each sentence and the document centroid
            sims = cosine_similarity(tfidf_mat, centroid).flatten()
            
            s_min, s_max = sims.min(), sims.max()
            if s_max > s_min:
                return (sims - s_min) / (s_max - s_min)
            return np.ones(n) / n
        except Exception:
            return np.ones(n) / n

    def _compute_legal_cue_scores(self, sentences):
        """
        Calculates domain-specific legal heuristics:
        - Position bias (Preamble clauses and Execution sections)
        - Legal modal verbs ('shall', 'hereby', 'warrants', 'indemnifies', 'covenants')
        - Quantitative terms ($ amounts, dates, penalty percentages)
        """
        n = len(sentences)
        cue_scores = np.zeros(n)
        
        legal_keywords = re.compile(
            r'(?i)\b(shall\s+be|hereby\s+agrees|indemnif\w*|liable|liability|covenant|warrant\w*|'
            r'breach|terminat\w*|confidential\w*|arbitrat\w*|governed\s+by|jurisdiction|default)\b'
        )
        numerical_facts = re.compile(r'(\$[\d,]+|Rs\.?\s*[\d,]+|\d+%\s*|\b\d+\s+days\b|\b\d+\s+months\b)')

        for i, sent in enumerate(sentences):
            score = 0.0
            
            # 1. Positional heuristic: Recitals and Final Terms hold key bounds
            if i < int(n * 0.15) or i > int(n * 0.85):
                score += 0.25
                
            # 2. Strong legal operative phrasing
            matches = len(legal_keywords.findall(sent))
            score += min(matches * 0.20, 0.50)
            
            # 3. Specific legal quantities, timelines, or penalty figures
            if numerical_facts.search(sent):
                score += 0.25
                
            cue_scores[i] = score

        s_max = cue_scores.max()
        if s_max > 0:
            cue_scores = cue_scores / s_max
        return cue_scores

    def _select_diverse_sentences(self, sentences, scores, k):
        """
        Maximal Marginal Relevance (MMR) selection to avoid picking redundant repetitive clauses.
        """
        n = len(sentences)
        if k >= n:
            return list(range(n))

        # Precompute similarity matrix
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_mat = vectorizer.fit_transform(sentences)
            sim_mat = cosine_similarity(tfidf_mat, tfidf_mat)
        except Exception:
            # Just take top scored
            return np.argsort(scores)[::-1][:k].tolist()

        selected = []
        candidates = list(range(n))
        
        # Pick the highest scoring sentence first
        best_first = int(np.argmax(scores))
        selected.append(best_first)
        candidates.remove(best_first)

        lambda_param = 0.7  # Tradeoff between relevance (0.7) and novelty (0.3)
        
        while len(selected) < k and candidates:
            best_score = -float('inf')
            best_candidate = candidates[0]
            
            for cand in candidates:
                relevance = scores[cand]
                redundancy = max([sim_mat[cand][sel] for sel in selected]) if selected else 0
                mmr_val = (lambda_param * relevance) - ((1 - lambda_param) * redundancy)
                
                if mmr_val > best_score:
                    best_score = mmr_val
                    best_candidate = cand
                    
            selected.append(best_candidate)
            candidates.remove(best_candidate)

        return selected

    def _build_result_package(self, original_text, summary_text, all_sentences, summary_sentences, sent_scores):
        """Assembles metrics, clause mappings, legalese translations, and accuracy scores."""
        orig_words = self.nlp.get_word_count(original_text)
        sum_words = self.nlp.get_word_count(summary_text)

        # Accuracy & Metrics
        accuracy_score = self.metrics.calculate_extractive_accuracy(original_text, summary_text)
        compression_ratio, time_saved = self.metrics.calculate_compression(orig_words, sum_words)
        readability_orig = self.metrics.calculate_readability(original_text)
        readability_sum = self.metrics.calculate_readability(summary_text)

        # Legal Knowledge extraction
        detected_legalese = self.knowledge.detect_legalese(original_text)
        important_clauses = self.knowledge.extract_important_clauses(all_sentences)
        risk_analysis = self.knowledge.assess_legal_risks(original_text, important_clauses, detected_legalese)

        return {
            "summary_text": summary_text,
            "summary_sentences": summary_sentences,
            "all_sentence_count": len(all_sentences),
            "summary_sentence_count": len(summary_sentences),
            "original_words": orig_words,
            "summary_words": sum_words,
            "accuracy_score": accuracy_score,
            "compression_ratio": compression_ratio,
            "time_saved_minutes": time_saved,
            "readability_original": readability_orig,
            "readability_summary": readability_sum,
            "legalese": detected_legalese,
            "clauses": important_clauses,
            "risk_analysis": risk_analysis
        }
