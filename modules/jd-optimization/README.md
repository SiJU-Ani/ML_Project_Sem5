# Job Description Optimization Module

## Overview

The JD Optimization Module transforms raw job descriptions into high-performing talent magnets by enhancing precision, improving engagement, maximizing visibility, and eliminating bias.

## Value Proposition

### 1. Enhanced Precision
- AI-driven requirement clarification
- Market data-informed role definitions
- Skill taxonomy alignment
- **Result**: Reduce underqualified applications by 30-40%

### 2. Improved Engagement
- Target persona optimization
- Brand voice alignment
- Compelling narrative structure
- **Result**: Increase application rates by 20-35%

### 3. Maximized Visibility
- SEO optimization for job boards
- Keyword density optimization
- Structured data markup
- **Result**: Improve search ranking by 25-50%

### 4. Bias Elimination
- Gender-coded language detection
- Exclusionary jargon identification
- Inclusive alternative suggestions
- **Result**: Increase diverse candidate pool by 15-30%

## Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│              JD Optimization Pipeline                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Input: Raw JD Text                                      │
│     │                                                     │
│     ▼                                                     │
│  ┌──────────────────────────────────────┐               │
│  │  1. Generative AI Engine              │               │
│  │  - GPT-4 / Fine-tuned LLM             │               │
│  │  - Template-based generation          │               │
│  │  - Structure optimization             │               │
│  └──────────┬───────────────────────────┘               │
│             │                                             │
│             ▼                                             │
│  ┌──────────────────────────────────────┐               │
│  │  2. NLP Analysis Engine               │               │
│  │  - Sentiment analysis                 │               │
│  │  - Tone detection                     │               │
│  │  - Readability scoring                │               │
│  │  - Named entity recognition           │               │
│  └──────────┬───────────────────────────┘               │
│             │                                             │
│             ▼                                             │
│  ┌──────────────────────────────────────┐               │
│  │  3. Bias Detection Module             │               │
│  │  - Gender-coded language              │               │
│  │  - Age bias indicators                │               │
│  │  - Cultural exclusivity               │               │
│  │  - Ableist language                   │               │
│  └──────────┬───────────────────────────┘               │
│             │                                             │
│             ▼                                             │
│  ┌──────────────────────────────────────┐               │
│  │  4. SEO Optimization Engine           │               │
│  │  - Keyword extraction                 │               │
│  │  - Competitive analysis               │               │
│  │  - Search intent mapping              │               │
│  └──────────┬───────────────────────────┘               │
│             │                                             │
│             ▼                                             │
│  ┌──────────────────────────────────────┐               │
│  │  5. Market Intelligence Layer         │               │
│  │  - Salary benchmarking                │               │
│  │  - Skills demand trends               │               │
│  │  - Competitive posting analysis       │               │
│  └──────────┬───────────────────────────┘               │
│             │                                             │
│             ▼                                             │
│  Output: Optimized JD + Analytics                        │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Generative AI Engine

**Purpose**: Create high-quality first drafts and improve existing descriptions

**Technology Stack**:
- OpenAI GPT-4 / GPT-4-turbo
- Fine-tuned LLaMA 2 models
- Anthropic Claude for safety-focused generation

**Implementation**:

```python
from openai import OpenAI
from typing import Dict, List
import json

class JDGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"
        
    def generate_jd(
        self,
        job_title: str,
        department: str,
        key_responsibilities: List[str],
        required_skills: List[str],
        company_info: Dict,
        tone: str = "professional"
    ) -> Dict[str, str]:
        """
        Generate optimized job description using GPT-4
        
        Args:
            job_title: Position title
            department: Department/team name
            key_responsibilities: List of main duties
            required_skills: Must-have skills
            company_info: Company description, culture, benefits
            tone: Desired tone (professional, casual, innovative)
            
        Returns:
            Dict with sections: title, summary, responsibilities, 
                              requirements, benefits, company_culture
        """
        
        system_prompt = """You are an expert recruitment copywriter specializing in 
        creating inclusive, engaging, and effective job descriptions. Your writing:
        - Uses clear, accessible language
        - Avoids jargon and buzzwords
        - Is free from gender-coded or biased language
        - Highlights company culture and values
        - Structures content for readability
        - Optimizes for search engines"""
        
        user_prompt = f"""
        Create a compelling job description for:
        
        Job Title: {job_title}
        Department: {department}
        
        Key Responsibilities:
        {self._format_list(key_responsibilities)}
        
        Required Skills:
        {self._format_list(required_skills)}
        
        Company Information:
        {json.dumps(company_info, indent=2)}
        
        Tone: {tone}
        
        Structure the output as JSON with these sections:
        - job_title: Optimized title for search
        - summary: 2-3 sentence compelling overview
        - about_company: Brief, engaging company description
        - responsibilities: List of 5-7 key duties (action-oriented)
        - required_qualifications: Must-have skills/experience
        - preferred_qualifications: Nice-to-have skills
        - benefits: Key perks and benefits
        - dei_statement: Diversity and inclusion commitment
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def improve_existing_jd(self, existing_jd: str) -> Dict[str, any]:
        """
        Analyze and improve existing job description
        
        Returns:
            Dict with improved_jd, suggestions, and changes_made
        """
        
        system_prompt = """You are a job description improvement specialist. 
        Analyze the provided JD and suggest specific improvements for:
        - Clarity and conciseness
        - Inclusive language
        - Proper structure
        - SEO optimization
        - Engagement factors"""
        
        user_prompt = f"""
        Analyze and improve this job description:
        
        {existing_jd}
        
        Return JSON with:
        - improved_jd: Fully rewritten version
        - key_changes: List of major improvements made
        - inclusivity_score: 0-100 rating
        - seo_score: 0-100 rating
        - suggestions: Additional recommendations
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _format_list(self, items: List[str]) -> str:
        return "\n".join([f"- {item}" for item in items])
```

### 2. NLP Analysis Engine

**Purpose**: Deep linguistic analysis for quality and inclusivity

**Technology Stack**:
- spaCy for NLP tasks
- Hugging Face Transformers for sentiment
- Custom models for bias detection

**Implementation**:

```python
import spacy
from transformers import pipeline
from typing import Dict, List, Tuple
import re

class NLPAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        
        # Gender-coded language dictionaries
        self.masculine_coded = {
            'competitive', 'dominant', 'decisive', 'independent',
            'ambitious', 'aggressive', 'assertive', 'analytical',
            'confident', 'defend', 'driven', 'lead', 'outspoken',
            'self-reliant', 'strong', 'ninja', 'rockstar', 'guru'
        }
        
        self.feminine_coded = {
            'collaborative', 'cooperative', 'supportive', 'understand',
            'compassionate', 'nurturing', 'loyal', 'interpersonal',
            'empathetic', 'sensitive', 'sympathetic', 'warm'
        }
        
        # Exclusionary jargon
        self.jargon_terms = {
            'synergy', 'paradigm', 'leverage', 'ninja', 'rockstar',
            'guru', 'wizard', 'unicorn', 'disrupt', 'revolutionary'
        }
        
    def analyze_jd(self, jd_text: str) -> Dict:
        """
        Comprehensive NLP analysis of job description
        
        Returns analysis including:
        - Readability scores
        - Sentiment analysis
        - Bias indicators
        - Tone assessment
        - Structural quality
        """
        
        doc = self.nlp(jd_text)
        
        analysis = {
            'readability': self._calculate_readability(jd_text),
            'sentiment': self._analyze_sentiment(jd_text),
            'bias_indicators': self._detect_bias(jd_text, doc),
            'tone': self._assess_tone(doc),
            'structure': self._analyze_structure(doc),
            'keyword_density': self._calculate_keyword_density(doc),
            'recommendations': []
        }
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _calculate_readability(self, text: str) -> Dict:
        """
        Calculate readability scores (Flesch, Gunning Fog, etc.)
        """
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        syllables = self._count_syllables(text)
        
        # Flesch Reading Ease
        if sentences > 0 and words > 0:
            flesch = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        else:
            flesch = 0
        
        # Gunning Fog Index
        complex_words = self._count_complex_words(text)
        if sentences > 0:
            gunning_fog = 0.4 * ((words / sentences) + 100 * (complex_words / words))
        else:
            gunning_fog = 0
        
        return {
            'flesch_reading_ease': round(flesch, 2),
            'gunning_fog_index': round(gunning_fog, 2),
            'grade_level': self._flesch_to_grade(flesch),
            'interpretation': self._interpret_readability(flesch)
        }
    
    def _detect_bias(self, text: str, doc) -> Dict:
        """
        Detect various forms of bias in language
        """
        text_lower = text.lower()
        words = set([token.text.lower() for token in doc])
        
        masculine_words = words & self.masculine_coded
        feminine_words = words & self.feminine_coded
        jargon_found = words & self.jargon_terms
        
        # Age bias patterns
        age_bias_patterns = [
            r'\bdigital native\b',
            r'\benergy\b',
            r'\byoung\b',
            r'\brecent graduate\b'
        ]
        age_bias = [
            pattern for pattern in age_bias_patterns 
            if re.search(pattern, text_lower)
        ]
        
        # Cultural bias (requiring specific backgrounds)
        cultural_bias = []
        if re.search(r'native (english )?speaker', text_lower):
            cultural_bias.append('native_speaker_requirement')
        
        return {
            'gender_coded': {
                'masculine_words': list(masculine_words),
                'feminine_words': list(feminine_words),
                'balance_score': self._calculate_gender_balance(
                    len(masculine_words), 
                    len(feminine_words)
                ),
                'recommendation': self._gender_balance_recommendation(
                    len(masculine_words), 
                    len(feminine_words)
                )
            },
            'exclusionary_jargon': list(jargon_found),
            'age_bias_indicators': age_bias,
            'cultural_bias': cultural_bias,
            'overall_inclusivity_score': self._calculate_inclusivity_score(
                masculine_words, 
                feminine_words, 
                jargon_found, 
                age_bias, 
                cultural_bias
            )
        }
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze overall sentiment and tone
        """
        # Split into chunks if too long
        max_length = 512
        chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        
        sentiments = [self.sentiment_analyzer(chunk)[0] for chunk in chunks]
        
        # Average sentiment
        avg_score = sum([s['score'] for s in sentiments]) / len(sentiments)
        dominant_sentiment = max(sentiments, key=lambda x: x['score'])
        
        return {
            'overall_sentiment': dominant_sentiment['label'],
            'confidence': round(avg_score, 2),
            'tone_assessment': self._interpret_sentiment(dominant_sentiment['label'])
        }
    
    def _assess_tone(self, doc) -> Dict:
        """
        Assess professional tone and voice
        """
        # Count imperative sentences (commands)
        imperatives = sum([1 for sent in doc.sents if self._is_imperative(sent)])
        
        # Measure formality
        formal_indicators = ['please', 'kindly', 'respectfully']
        informal_indicators = ['awesome', 'cool', 'fun', 'exciting']
        
        formality_score = sum([
            1 for token in doc 
            if token.text.lower() in formal_indicators
        ]) - sum([
            1 for token in doc 
            if token.text.lower() in informal_indicators
        ])
        
        return {
            'formality': 'formal' if formality_score > 0 else 'casual',
            'imperative_ratio': imperatives / len(list(doc.sents)),
            'voice': 'active'  # Simplified; would need deeper analysis
        }
    
    def _analyze_structure(self, doc) -> Dict:
        """
        Analyze document structure and organization
        """
        sentences = list(doc.sents)
        
        return {
            'sentence_count': len(sentences),
            'avg_sentence_length': sum([len(sent) for sent in sentences]) / len(sentences),
            'paragraph_count': len(doc.text.split('\n\n')),
            'has_bullet_points': bool(re.search(r'[•\-\*]\s', doc.text)),
            'structure_score': self._calculate_structure_score(doc)
        }
    
    def _calculate_keyword_density(self, doc) -> Dict:
        """
        Calculate density of important keywords
        """
        # Extract important nouns and skills
        nouns = [
            token.text.lower() 
            for token in doc 
            if token.pos_ == 'NOUN'
        ]
        
        # Count frequencies
        from collections import Counter
        noun_freq = Counter(nouns)
        
        return {
            'top_keywords': noun_freq.most_common(10),
            'unique_keywords': len(set(nouns)),
            'keyword_diversity': len(set(nouns)) / len(nouns) if nouns else 0
        }
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """
        Generate actionable recommendations based on analysis
        """
        recommendations = []
        
        # Readability recommendations
        if analysis['readability']['flesch_reading_ease'] < 50:
            recommendations.append(
                "Consider simplifying language. Current readability is complex. "
                "Aim for Flesch score above 60 for better accessibility."
            )
        
        # Bias recommendations
        bias = analysis['bias_indicators']
        if len(bias['gender_coded']['masculine_words']) > 3:
            recommendations.append(
                f"Reduce masculine-coded language. Found: {', '.join(bias['gender_coded']['masculine_words'])}. "
                "Consider neutral alternatives."
            )
        
        if bias['exclusionary_jargon']:
            recommendations.append(
                f"Replace jargon with clear language: {', '.join(bias['exclusionary_jargon'])}"
            )
        
        # Structure recommendations
        if not analysis['structure']['has_bullet_points']:
            recommendations.append(
                "Add bullet points for responsibilities and requirements to improve scannability."
            )
        
        return recommendations
    
    # Helper methods
    def _count_syllables(self, text: str) -> int:
        # Simplified syllable counting
        words = text.split()
        return sum([self._syllables_in_word(word) for word in words])
    
    def _syllables_in_word(self, word: str) -> int:
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel
        
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
            
        return count
    
    def _count_complex_words(self, text: str) -> int:
        words = text.split()
        return sum([1 for word in words if self._syllables_in_word(word) >= 3])
    
    def _flesch_to_grade(self, flesch: float) -> str:
        if flesch >= 90:
            return "5th grade"
        elif flesch >= 80:
            return "6th grade"
        elif flesch >= 70:
            return "7th grade"
        elif flesch >= 60:
            return "8th-9th grade"
        elif flesch >= 50:
            return "10th-12th grade"
        else:
            return "College level"
    
    def _interpret_readability(self, flesch: float) -> str:
        if flesch >= 60:
            return "Easy to read - accessible to most candidates"
        elif flesch >= 50:
            return "Moderately difficult - readable but could be simplified"
        else:
            return "Difficult to read - consider simplifying language"
    
    def _calculate_gender_balance(self, masculine: int, feminine: int) -> float:
        total = masculine + feminine
        if total == 0:
            return 100.0
        balance = 100 - abs(masculine - feminine) / total * 100
        return round(balance, 2)
    
    def _gender_balance_recommendation(self, masculine: int, feminine: int) -> str:
        if masculine > feminine + 2:
            return "Consider adding more collaborative, team-oriented language"
        elif feminine > masculine + 2:
            return "Balance with some achievement-oriented language"
        else:
            return "Good gender balance in language"
    
    def _calculate_inclusivity_score(
        self, 
        masculine_words, 
        feminine_words, 
        jargon, 
        age_bias, 
        cultural_bias
    ) -> float:
        score = 100
        
        # Deduct for imbalance
        gender_imbalance = abs(len(masculine_words) - len(feminine_words))
        score -= gender_imbalance * 5
        
        # Deduct for jargon
        score -= len(jargon) * 3
        
        # Deduct for age bias
        score -= len(age_bias) * 10
        
        # Deduct for cultural bias
        score -= len(cultural_bias) * 10
        
        return max(0, score)
    
    def _interpret_sentiment(self, label: str) -> str:
        if label == 'POSITIVE':
            return "Enthusiastic and engaging tone"
        else:
            return "Consider adding more positive, welcoming language"
    
    def _is_imperative(self, sent) -> bool:
        # Simplified check for imperative sentences
        if sent[0].pos_ == 'VERB':
            return True
        return False
    
    def _calculate_structure_score(self, doc) -> float:
        # Simplified structure scoring
        score = 50
        
        if bool(re.search(r'[•\-\*]\s', doc.text)):
            score += 20
        
        sentences = list(doc.sents)
        avg_length = sum([len(sent) for sent in sentences]) / len(sentences)
        if 15 <= avg_length <= 25:
            score += 20
        
        if len(doc.text.split('\n\n')) >= 3:
            score += 10
        
        return min(100, score)
```

### 3. SEO Optimization Engine

**Purpose**: Maximize job posting visibility on search engines and job boards

```python
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

class SEOOptimizer:
    def __init__(self):
        self.target_keyword_density = 0.02  # 2%
        
    def optimize_for_search(
        self,
        jd_text: str,
        job_title: str,
        location: str
    ) -> Dict:
        """
        Optimize job description for search engines and job boards
        
        Returns:
            Optimized text and SEO analysis
        """
        
        # Extract key terms
        primary_keywords = self._extract_primary_keywords(job_title)
        secondary_keywords = self._extract_skills_keywords(jd_text)
        
        # Analyze current SEO
        current_seo = self._analyze_seo(jd_text, primary_keywords, secondary_keywords)
        
        # Generate optimized version
        optimized_text = self._inject_keywords(
            jd_text,
            primary_keywords,
            secondary_keywords,
            current_seo
        )
        
        # Generate schema markup
        schema = self._generate_schema_markup(jd_text, job_title, location)
        
        return {
            'optimized_text': optimized_text,
            'seo_score': current_seo['score'],
            'improvements': current_seo['improvements'],
            'primary_keywords': primary_keywords,
            'secondary_keywords': secondary_keywords,
            'schema_markup': schema
        }
    
    def _extract_primary_keywords(self, job_title: str) -> List[str]:
        """Extract primary keywords from job title"""
        # Common job title patterns
        keywords = [job_title.lower()]
        
        # Add variations
        if 'engineer' in job_title.lower():
            keywords.extend(['engineer', 'engineering', 'developer'])
        if 'manager' in job_title.lower():
            keywords.extend(['manager', 'management', 'lead'])
        if 'senior' in job_title.lower():
            keywords.extend(['senior', 'sr', 'experienced'])
            
        return keywords
    
    def _extract_skills_keywords(self, text: str) -> List[str]:
        """Extract technical skills and key terms"""
        # Common tech skills pattern
        tech_pattern = r'\b(Python|Java|JavaScript|React|AWS|Azure|SQL|[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b'
        skills = re.findall(tech_pattern, text)
        
        return list(set(skills))
    
    def _analyze_seo(
        self,
        text: str,
        primary_keywords: List[str],
        secondary_keywords: List[str]
    ) -> Dict:
        """Analyze current SEO quality"""
        text_lower = text.lower()
        word_count = len(text.split())
        
        score = 0
        improvements = []
        
        # Check title in first 100 characters
        if any(keyword in text_lower[:100] for keyword in primary_keywords):
            score += 20
        else:
            improvements.append("Include job title in the first sentence")
        
        # Check keyword density
        keyword_density = sum([
            text_lower.count(keyword) 
            for keyword in primary_keywords
        ]) / word_count
        
        if 0.01 <= keyword_density <= 0.03:
            score += 20
        elif keyword_density < 0.01:
            improvements.append("Increase mention of key terms")
        else:
            improvements.append("Reduce keyword stuffing")
        
        # Check for location
        if word_count > 200:
            score += 20
        else:
            improvements.append("Expand description to 200+ words for better SEO")
        
        # Check for headings/structure
        if '\n\n' in text or '**' in text:
            score += 20
        else:
            improvements.append("Add clear section headings")
        
        # Check for skills/keywords
        if len(secondary_keywords) >= 5:
            score += 20
        else:
            improvements.append("Include more specific technical skills")
        
        return {
            'score': score,
            'improvements': improvements,
            'keyword_density': round(keyword_density, 4)
        }
    
    def _inject_keywords(
        self,
        text: str,
        primary_keywords: List[str],
        secondary_keywords: List[str],
        seo_analysis: Dict
    ) -> str:
        """Intelligently inject keywords to improve SEO"""
        # This is a simplified version - production would be more sophisticated
        optimized = text
        
        # Ensure title appears early
        if primary_keywords[0] not in text[:100].lower():
            optimized = f"We are seeking a {primary_keywords[0]}. " + optimized
        
        return optimized
    
    def _generate_schema_markup(
        self,
        jd_text: str,
        job_title: str,
        location: str
    ) -> Dict:
        """
        Generate JobPosting schema.org markup for rich snippets
        """
        return {
            "@context": "https://schema.org/",
            "@type": "JobPosting",
            "title": job_title,
            "description": jd_text[:500],  # Truncated for snippet
            "datePosted": "2025-01-01",  # Would be dynamic
            "validThrough": "2025-03-01",
            "employmentType": "FULL_TIME",
            "hiringOrganization": {
                "@type": "Organization",
                "name": "Company Name"
            },
            "jobLocation": {
                "@type": "Place",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": location
                }
            }
        }
```

## API Endpoints

### POST /api/v1/jd/optimize
Optimize a job description.

**Request**:
```json
{
  "job_title": "Senior Software Engineer",
  "department": "Engineering",
  "raw_description": "We need a rockstar developer...",
  "responsibilities": ["Build features", "Code review"],
  "required_skills": ["Python", "AWS"],
  "company_info": {
    "name": "TechCorp",
    "industry": "SaaS",
    "size": "200-500"
  },
  "tone": "professional"
}
```

**Response**:
```json
{
  "optimized_jd": {
    "title": "Senior Software Engineer - Python & AWS",
    "summary": "Join our engineering team...",
    "responsibilities": [...],
    "requirements": [...]
  },
  "analysis": {
    "readability_score": 75.5,
    "inclusivity_score": 92,
    "seo_score": 85,
    "bias_indicators": {...}
  },
  "recommendations": [
    "Great inclusivity! Consider adding salary range.",
    "SEO: Add location keywords"
  ]
}
```

### POST /api/v1/jd/analyze
Analyze existing job description without modification.

### GET /api/v1/jd/templates
Get industry-specific JD templates.

## Performance Metrics

### Target KPIs
- **Processing Time**: < 3 seconds per JD
- **Inclusivity Score**: > 85/100
- **SEO Improvement**: +25-50% search visibility
- **Application Rate Increase**: +20-35%

## Competitive Differentiation

vs. **Textio**:
- ✅ Integrated with full recruitment workflow
- ✅ Real-time ATS synchronization
- ⚠️ Need: Equivalent data scale (1B+ documents)

vs. **Built-in ATS Features**:
- ✅ More sophisticated bias detection
- ✅ Deeper NLP analysis
- ✅ Market intelligence integration

## Future Enhancements

1. **A/B Testing Platform**: Test multiple JD versions
2. **Predictive Analytics**: Forecast application volume
3. **Multilingual Support**: Global hiring optimization
4. **Video JD Generation**: Convert to video scripts
