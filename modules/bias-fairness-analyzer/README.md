# Bias & Fairness Analyzer Module

## Overview

The crown jewel of the enhancement microservice. Provides continuous algorithmic auditing, bias detection, and compliance reporting to ensure ethical, fair, and legally defensible AI-powered hiring.

## Strategic Importance

**Market Differentiator**: While competitors offer bias features, a dedicated, transparent, auditable fairness analyzer is a significant gap.

**Value Proposition**:
- **Risk Mitigation**: Protect against discrimination lawsuits
- **Regulatory Compliance**: EEOC, GDPR, EU AI Act readiness
- **Brand Protection**: Demonstrate commitment to DEI
- **Legal Defensibility**: Audit trails and compliance reports

## Regulatory Landscape

### Key Regulations

| Regulation | Jurisdiction | Key Requirements | Impact |
|------------|--------------|------------------|---------|
| **EEOC Guidelines** | USA | No disparate impact (4/5 rule) | High |
| **GDPR** | EU | Right to explanation for automated decisions | High |
| **EU AI Act** | EU | HR systems classified as "high-risk" | Critical |
| **CCPA** | California | Data transparency and privacy | Medium |
| **NYC Local Law 144** | New York City | Bias audits for automated hiring tools | High |

### Compliance Timeline

- **2024**: EU AI Act enforcement begins
- **2025**: Increased EEOC enforcement of AI discrimination
- **Ongoing**: State-level regulations expanding

## Technical Architecture

```
┌───────────────────────────────────────────────────────────┐
│          Bias & Fairness Analysis Pipeline                 │
├───────────────────────────────────────────────────────────┤
│                                                             │
│  Input: Model Outputs + Candidate Data                    │
│     │                                                       │
│     ▼                                                       │
│  ┌──────────────────────────────────────┐                 │
│  │  1. Algorithmic Auditing Engine       │                 │
│  │  - Disparate Impact Analysis          │                 │
│  │  - Four-Fifths Rule Testing           │                 │
│  │  - Statistical Significance Tests     │                 │
│  │  - Demographic Parity Checks          │                 │
│  └──────────┬───────────────────────────┘                 │
│             │                                               │
│             ▼                                               │
│  ┌──────────────────────────────────────┐                 │
│  │  2. Proxy Detection Module            │                 │
│  │  - Name-based inference               │                 │
│  │  - Geographic proxies                 │                 │
│  │  - Educational institution proxies    │                 │
│  │  - Implicit bias identification       │                 │
│  └──────────┬───────────────────────────┘                 │
│             │                                               │
│             ▼                                               │
│  ┌──────────────────────────────────────┐                 │
│  │  3. Debiasing Engine                  │                 │
│  │  - Word embedding correction          │                 │
│  │  - Adversarial debiasing              │                 │
│  │  - Data augmentation                  │                 │
│  │  - Fairness constraints               │                 │
│  └──────────┬───────────────────────────┘                 │
│             │                                               │
│             ▼                                               │
│  ┌──────────────────────────────────────┐                 │
│  │  4. Language Bias Detector            │                 │
│  │  - Job description analysis           │                 │
│  │  - Gender-coded language              │                 │
│  │  - Age bias indicators                │                 │
│  │  - Cultural exclusivity               │                 │
│  └──────────┬───────────────────────────┘                 │
│             │                                               │
│             ▼                                               │
│  ┌──────────────────────────────────────┐                 │
│  │  5. Compliance Reporting Engine       │                 │
│  │  - Audit trail generation             │                 │
│  │  - Fairness metrics dashboard         │                 │
│  │  - Regulatory reports                 │                 │
│  │  - Historical trend analysis          │                 │
│  └──────────┬───────────────────────────┘                 │
│             │                                               │
│             ▼                                               │
│  Output: Bias Alerts + Compliance Reports                  │
│                                                             │
└───────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Disparate Impact Analyzer

**Purpose**: Detect if AI systems disproportionately impact protected groups

**Implementation**:

```python
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
import pandas as pd

class DisparateImpactAnalyzer:
    def __init__(self):
        self.protected_groups = [
            'gender', 'race', 'age_group', 'disability_status'
        ]
        self.four_fifths_threshold = 0.8
    
    def analyze_disparate_impact(
        self,
        candidates: List[Dict],
        scoring_results: List[Dict],
        threshold_score: float = 70.0
    ) -> Dict:
        """
        Perform comprehensive disparate impact analysis
        
        Args:
            candidates: List of candidate demographic data
            scoring_results: AI-generated scores for each candidate
            threshold_score: Cutoff score for "passing" candidates
            
        Returns:
            Analysis with disparate impact metrics, violations, and recommendations
        """
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([
            {
                'candidate_id': c['id'],
                'score': next(
                    (s['score'] for s in scoring_results if s['candidate_id'] == c['id']),
                    None
                ),
                **{group: c.get(group, 'Unknown') for group in self.protected_groups}
            }
            for c in candidates
        ])
        
        analysis_results = {
            'overall_compliance': True,
            'violations': [],
            'metrics': {},
            'recommendations': []
        }
        
        # Analyze each protected characteristic
        for group in self.protected_groups:
            group_analysis = self._analyze_group(
                df,
                group,
                threshold_score
            )
            
            analysis_results['metrics'][group] = group_analysis
            
            if not group_analysis['compliant']:
                analysis_results['overall_compliance'] = False
                analysis_results['violations'].append({
                    'protected_characteristic': group,
                    'issue': group_analysis['issue'],
                    'impact_ratio': group_analysis['impact_ratio'],
                    'severity': group_analysis['severity']
                })
        
        # Generate recommendations
        analysis_results['recommendations'] = self._generate_recommendations(
            analysis_results['violations']
        )
        
        return analysis_results
    
    def _analyze_group(
        self,
        df: pd.DataFrame,
        group_column: str,
        threshold_score: float
    ) -> Dict:
        """
        Analyze disparate impact for a specific protected group
        Using the Four-Fifths (80%) Rule
        """
        
        # Filter out unknown values
        df_known = df[df[group_column] != 'Unknown'].copy()
        
        if len(df_known) == 0:
            return {
                'compliant': True,
                'note': 'No demographic data available'
            }
        
        # Calculate selection rates for each subgroup
        selection_rates = {}
        group_counts = {}
        
        for subgroup in df_known[group_column].unique():
            subgroup_df = df_known[df_known[group_column] == subgroup]
            total = len(subgroup_df)
            selected = len(subgroup_df[subgroup_df['score'] >= threshold_score])
            
            selection_rates[subgroup] = selected / total if total > 0 else 0
            group_counts[subgroup] = {
                'total': total,
                'selected': selected,
                'selection_rate': selection_rates[subgroup]
            }
        
        # Find highest selection rate (reference group)
        max_rate = max(selection_rates.values())
        reference_group = [
            k for k, v in selection_rates.items() 
            if v == max_rate
        ][0]
        
        # Calculate impact ratios (Four-Fifths Rule)
        impact_ratios = {
            subgroup: rate / max_rate if max_rate > 0 else 1.0
            for subgroup, rate in selection_rates.items()
        }
        
        # Check for violations
        violations = {
            subgroup: ratio 
            for subgroup, ratio in impact_ratios.items() 
            if ratio < self.four_fifths_threshold
        }
        
        # Statistical significance test (Chi-square)
        chi_square_result = self._chi_square_test(df_known, group_column, threshold_score)
        
        compliant = len(violations) == 0
        
        result = {
            'compliant': compliant,
            'group_counts': group_counts,
            'selection_rates': selection_rates,
            'reference_group': reference_group,
            'impact_ratios': impact_ratios,
            'statistical_significance': chi_square_result,
            'violations': violations if violations else None
        }
        
        if not compliant:
            # Identify most severe violation
            min_ratio = min(violations.values())
            affected_group = [k for k, v in violations.items() if v == min_ratio][0]
            
            result['issue'] = (
                f"{affected_group} has selection rate {min_ratio:.2%} of {reference_group} "
                f"(below 80% threshold)"
            )
            result['impact_ratio'] = min_ratio
            result['severity'] = self._calculate_severity(min_ratio)
        
        return result
    
    def _chi_square_test(
        self,
        df: pd.DataFrame,
        group_column: str,
        threshold_score: float
    ) -> Dict:
        """
        Perform chi-square test for statistical significance
        """
        # Create contingency table
        df['selected'] = df['score'] >= threshold_score
        contingency_table = pd.crosstab(df[group_column], df['selected'])
        
        # Perform chi-square test
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        return {
            'chi_square': chi2,
            'p_value': p_value,
            'statistically_significant': p_value < 0.05,
            'interpretation': (
                'Statistically significant disparity detected' 
                if p_value < 0.05 
                else 'No statistically significant disparity'
            )
        }
    
    def _calculate_severity(self, impact_ratio: float) -> str:
        """Calculate severity of disparate impact"""
        if impact_ratio < 0.5:
            return 'CRITICAL'
        elif impact_ratio < 0.65:
            return 'HIGH'
        elif impact_ratio < 0.8:
            return 'MODERATE'
        else:
            return 'LOW'
    
    def _generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generate actionable recommendations to address violations"""
        recommendations = []
        
        if not violations:
            return ["No disparate impact detected. Continue monitoring."]
        
        for violation in violations:
            group = violation['protected_characteristic']
            severity = violation['severity']
            
            if severity == 'CRITICAL':
                recommendations.append(
                    f"URGENT: Immediately review and potentially disable AI scoring for {group}. "
                    "Conduct manual review of affected candidates. Consult legal counsel."
                )
            elif severity == 'HIGH':
                recommendations.append(
                    f"HIGH PRIORITY: Review training data and feature engineering for {group} bias. "
                    "Consider retraining model with fairness constraints."
                )
            elif severity == 'MODERATE':
                recommendations.append(
                    f"Monitor {group} metrics closely. Consider data augmentation to balance "
                    "representation in training data."
                )
            
            # Specific remediation strategies
            recommendations.append(
                f"For {group}: Analyze feature importance to identify biased features. "
                "Consider removing proxy variables or applying fairness post-processing."
            )
        
        return recommendations
```

### 2. Proxy Variable Detector

**Purpose**: Identify indirect proxies for protected characteristics

```python
import re
from typing import Dict, List, Set
import gender_guesser.detector as gender
from geopy.geocoders import Nominatim

class ProxyDetector:
    def __init__(self):
        self.gender_detector = gender.Detector()
        self.geolocator = Nominatim(user_agent="bias_analyzer")
        
        # Historically privileged institutions (proxy for socioeconomic status)
        self.elite_institutions = {
            'Harvard', 'Yale', 'Princeton', 'Stanford', 'MIT',
            'Oxford', 'Cambridge', 'Caltech', 'Columbia', 'UPenn'
        }
        
        # Geographic areas that may serve as proxies
        self.geographic_patterns = {
            'zip_code': r'\b\d{5}\b',
            'city_state': r'[A-Z][a-z]+,\s*[A-Z]{2}'
        }
    
    def detect_proxies(
        self,
        candidate_data: Dict,
        features_used: List[str]
    ) -> Dict:
        """
        Detect potential proxy variables for protected characteristics
        
        Args:
            candidate_data: Candidate information
            features_used: List of features used in scoring model
            
        Returns:
            Dictionary of detected proxies and recommendations
        """
        
        proxies_detected = {
            'gender_proxies': [],
            'race_ethnicity_proxies': [],
            'age_proxies': [],
            'socioeconomic_proxies': [],
            'recommendations': []
        }
        
        # Name-based gender inference
        if 'name' in features_used or 'first_name' in features_used:
            proxies_detected['gender_proxies'].append({
                'feature': 'name',
                'risk': 'HIGH',
                'explanation': 'Names can reveal gender, creating indirect bias',
                'recommendation': 'Remove name from scoring features or anonymize'
            })
        
        # Educational institution as socioeconomic proxy
        if 'education' in features_used or 'university' in features_used:
            institutions = self._extract_institutions(candidate_data)
            elite_found = [
                inst for inst in institutions 
                if any(elite in inst for elite in self.elite_institutions)
            ]
            
            if elite_found:
                proxies_detected['socioeconomic_proxies'].append({
                    'feature': 'university',
                    'risk': 'MODERATE',
                    'explanation': (
                        'Elite universities may serve as proxy for socioeconomic status, '
                        'which correlates with race'
                    ),
                    'recommendation': (
                        'Consider focusing on skills/experience rather than institution prestige'
                    )
                })
        
        # Geographic location as race/ethnicity proxy
        if 'address' in features_used or 'location' in features_used:
            proxies_detected['race_ethnicity_proxies'].append({
                'feature': 'location',
                'risk': 'HIGH',
                'explanation': (
                    'Zip codes and neighborhoods correlate strongly with race/ethnicity '
                    'due to historical segregation'
                ),
                'recommendation': 'Use only broad region (state/country), not specific addresses'
            })
        
        # Age-related proxies
        age_proxy_features = ['graduation_year', 'years_of_experience', 'career_start_year']
        age_features_found = [f for f in features_used if f in age_proxy_features]
        
        if age_features_found:
            proxies_detected['age_proxies'].append({
                'feature': ', '.join(age_features_found),
                'risk': 'MODERATE',
                'explanation': 'These features correlate with age',
                'recommendation': (
                    'Ensure age is genuinely relevant to job requirements. '
                    'Avoid arbitrary experience thresholds.'
                )
            })
        
        # Generate overall recommendations
        proxies_detected['recommendations'] = self._generate_proxy_recommendations(
            proxies_detected
        )
        
        # Calculate overall risk score
        proxies_detected['overall_risk'] = self._calculate_risk_score(proxies_detected)
        
        return proxies_detected
    
    def _extract_institutions(self, candidate_data: Dict) -> List[str]:
        """Extract educational institutions from candidate data"""
        institutions = []
        
        education = candidate_data.get('education', [])
        for edu in education:
            if 'institution' in edu and edu['institution']:
                institutions.append(edu['institution'])
        
        return institutions
    
    def _generate_proxy_recommendations(self, proxies: Dict) -> List[str]:
        """Generate recommendations for proxy mitigation"""
        recommendations = []
        
        high_risk_count = sum([
            len([p for p in proxies[category] if p.get('risk') == 'HIGH'])
            for category in ['gender_proxies', 'race_ethnicity_proxies', 
                           'age_proxies', 'socioeconomic_proxies']
        ])
        
        if high_risk_count > 0:
            recommendations.append(
                f"PRIORITY: {high_risk_count} HIGH-RISK proxy variables detected. "
                "Immediate feature engineering review required."
            )
        
        # Specific recommendations
        if proxies['gender_proxies']:
            recommendations.append(
                "Implement name anonymization or remove names from model inputs"
            )
        
        if proxies['race_ethnicity_proxies']:
            recommendations.append(
                "Replace specific location data with broader geographic regions"
            )
        
        if proxies['socioeconomic_proxies']:
            recommendations.append(
                "Consider skill-based assessment over credential-based evaluation"
            )
        
        return recommendations
    
    def _calculate_risk_score(self, proxies: Dict) -> str:
        """Calculate overall proxy risk score"""
        risk_weights = {'HIGH': 3, 'MODERATE': 2, 'LOW': 1}
        
        total_risk = 0
        for category in ['gender_proxies', 'race_ethnicity_proxies', 
                        'age_proxies', 'socioeconomic_proxies']:
            for proxy in proxies[category]:
                total_risk += risk_weights.get(proxy.get('risk', 'LOW'), 1)
        
        if total_risk >= 6:
            return 'HIGH'
        elif total_risk >= 3:
            return 'MODERATE'
        else:
            return 'LOW'
```

### 3. Word Embedding Debiasing

**Purpose**: Remove bias from word embeddings used in semantic matching

```python
import numpy as np
from typing import List, Dict, Tuple

class EmbeddingDebiaser:
    def __init__(self):
        # Gender direction pairs for debiasing
        self.gender_pairs = [
            ('he', 'she'),
            ('man', 'woman'),
            ('male', 'female'),
            ('boy', 'girl'),
            ('father', 'mother'),
            ('husband', 'wife'),
            ('son', 'daughter'),
            ('brother', 'sister')
        ]
    
    def debias_embeddings(
        self,
        embeddings: Dict[str, np.ndarray],
        method: str = 'hard'
    ) -> Dict[str, np.ndarray]:
        """
        Remove bias from word embeddings
        
        Args:
            embeddings: Dictionary mapping words to embedding vectors
            method: 'hard' (full neutralization) or 'soft' (partial reduction)
            
        Returns:
            Debiased embeddings
        """
        
        # 1. Identify gender subspace
        gender_direction = self._identify_bias_direction(
            embeddings,
            self.gender_pairs
        )
        
        # 2. Identify gender-specific and neutral words
        specific_words = self._get_gender_specific_words()
        neutral_words = [
            word for word in embeddings.keys() 
            if word not in specific_words
        ]
        
        # 3. Debias neutral words
        debiased = embeddings.copy()
        
        if method == 'hard':
            # Hard debiasing: completely remove gender component
            for word in neutral_words:
                debiased[word] = self._neutralize(
                    embeddings[word],
                    gender_direction
                )
        elif method == 'soft':
            # Soft debiasing: reduce gender component by 50%
            for word in neutral_words:
                debiased[word] = self._soft_neutralize(
                    embeddings[word],
                    gender_direction,
                    reduction_factor=0.5
                )
        
        # 4. Equalize gender-specific pairs
        for word1, word2 in self.gender_pairs:
            if word1 in debiased and word2 in debiased:
                debiased[word1], debiased[word2] = self._equalize_pair(
                    debiased[word1],
                    debiased[word2],
                    gender_direction
                )
        
        return debiased
    
    def _identify_bias_direction(
        self,
        embeddings: Dict[str, np.ndarray],
        defining_pairs: List[Tuple[str, str]]
    ) -> np.ndarray:
        """
        Identify the bias direction in embedding space
        using defining pairs (e.g., he-she, man-woman)
        """
        
        differences = []
        
        for word1, word2 in defining_pairs:
            if word1 in embeddings and word2 in embeddings:
                diff = embeddings[word1] - embeddings[word2]
                differences.append(diff)
        
        if not differences:
            # Return zero vector if no pairs found
            return np.zeros(len(next(iter(embeddings.values()))))
        
        # Average differences to get bias direction
        bias_direction = np.mean(differences, axis=0)
        
        # Normalize
        bias_direction = bias_direction / np.linalg.norm(bias_direction)
        
        return bias_direction
    
    def _neutralize(
        self,
        vector: np.ndarray,
        bias_direction: np.ndarray
    ) -> np.ndarray:
        """
        Remove component of vector along bias direction
        """
        # Project onto bias direction
        projection = np.dot(vector, bias_direction) * bias_direction
        
        # Remove projection
        neutralized = vector - projection
        
        return neutralized
    
    def _soft_neutralize(
        self,
        vector: np.ndarray,
        bias_direction: np.ndarray,
        reduction_factor: float = 0.5
    ) -> np.ndarray:
        """
        Partially remove bias component
        """
        projection = np.dot(vector, bias_direction) * bias_direction
        
        # Only remove portion of projection
        neutralized = vector - (reduction_factor * projection)
        
        return neutralized
    
    def _equalize_pair(
        self,
        vector1: np.ndarray,
        vector2: np.ndarray,
        bias_direction: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Equalize a pair of gendered words to be equidistant
        from neutral space
        """
        # Find their mean (neutral point)
        mean = (vector1 + vector2) / 2
        
        # Remove bias from mean
        neutral_mean = self._neutralize(mean, bias_direction)
        
        # Project original difference onto bias direction
        diff = vector1 - vector2
        bias_component = np.dot(diff, bias_direction) * bias_direction
        
        # Create equalized pair
        equalized1 = neutral_mean + (bias_component / 2)
        equalized2 = neutral_mean - (bias_component / 2)
        
        return equalized1, equalized2
    
    def _get_gender_specific_words(self) -> List[str]:
        """
        Get list of inherently gendered words that should NOT be neutralized
        """
        specific_words = []
        
        for word1, word2 in self.gender_pairs:
            specific_words.extend([word1, word2])
        
        # Add more specific terms
        specific_words.extend([
            'king', 'queen', 'prince', 'princess',
            'mr', 'mrs', 'ms', 'sir', 'madam',
            'gentleman', 'lady', 'actor', 'actress',
            'waiter', 'waitress', 'steward', 'stewardess'
        ])
        
        return specific_words
```

### 4. Compliance Report Generator

```python
from datetime import datetime, timedelta
from typing import Dict, List
import json

class ComplianceReporter:
    def __init__(self):
        self.report_templates = {
            'EEOC': self._generate_eeoc_report,
            'GDPR': self._generate_gdpr_report,
            'EU_AI_ACT': self._generate_eu_ai_act_report,
            'NYC_LOCAL_LAW_144': self._generate_nyc_report
        }
    
    def generate_report(
        self,
        regulation: str,
        analysis_results: Dict,
        time_period: str = '30_days'
    ) -> Dict:
        """
        Generate compliance report for specific regulation
        
        Args:
            regulation: Which regulation ('EEOC', 'GDPR', 'EU_AI_ACT', 'NYC_LOCAL_LAW_144')
            analysis_results: Results from bias analysis
            time_period: Reporting period
            
        Returns:
            Formatted compliance report
        """
        
        if regulation not in self.report_templates:
            raise ValueError(f"Unknown regulation: {regulation}")
        
        report_generator = self.report_templates[regulation]
        report = report_generator(analysis_results, time_period)
        
        # Add metadata
        report['metadata'] = {
            'report_type': regulation,
            'generated_at': datetime.now().isoformat(),
            'reporting_period': time_period,
            'compliance_version': '1.0'
        }
        
        return report
    
    def _generate_eeoc_report(self, analysis: Dict, period: str) -> Dict:
        """EEOC Compliance Report (Four-Fifths Rule)"""
        
        return {
            'title': 'EEOC Uniform Guidelines Compliance Report',
            'summary': {
                'overall_compliance': analysis.get('overall_compliance', False),
                'violations_count': len(analysis.get('violations', [])),
                'period': period
            },
            'disparate_impact_analysis': analysis.get('metrics', {}),
            'violations': analysis.get('violations', []),
            'remediation_plan': analysis.get('recommendations', []),
            'attestation': (
                'This report documents compliance with EEOC Uniform Guidelines '
                'on Employee Selection Procedures (29 CFR Part 1607)'
            )
        }
    
    def _generate_gdpr_report(self, analysis: Dict, period: str) -> Dict:
        """GDPR Right to Explanation Report"""
        
        return {
            'title': 'GDPR Article 22 Compliance Report',
            'summary': {
                'automated_decision_making': True,
                'human_oversight': True,
                'explanation_provided': True
            },
            'transparency_measures': {
                'explainable_ai_implemented': True,
                'feature_importance_available': True,
                'decision_rationale_documented': True
            },
            'data_protection': {
                'purpose_limitation': 'Hiring decisions only',
                'data_minimization': 'Only relevant features used',
                'storage_limitation': 'Deleted after 90 days if not hired'
            },
            'individual_rights': {
                'right_to_explanation': 'Provided via XAI module',
                'right_to_contest': 'Human review process in place',
                'right_to_deletion': 'Automated after retention period'
            }
        }
    
    def _generate_eu_ai_act_report(self, analysis: Dict, period: str) -> Dict:
        """EU AI Act High-Risk System Report"""
        
        return {
            'title': 'EU AI Act Compliance Report - High-Risk HR System',
            'classification': 'High-Risk AI System (Annex III, Category 4)',
            'risk_management': {
                'risk_assessment_conducted': True,
                'bias_testing_frequency': 'Continuous',
                'mitigation_measures': analysis.get('recommendations', [])
            },
            'data_governance': {
                'training_data_quality': 'Documented and audited',
                'bias_in_training_data': 'Tested and mitigated',
                'data_representativeness': 'Monitored'
            },
            'transparency_requirements': {
                'technical_documentation': 'Maintained',
                'user_information': 'Provided to recruiters',
                'human_oversight': 'Required for final decisions'
            },
            'accuracy_metrics': {
                'model_performance': 'Monitored continuously',
                'bias_metrics': analysis.get('metrics', {}),
                'validation_frequency': 'Monthly'
            },
            'conformity_assessment': {
                'ce_marking': 'Pending',
                'third_party_audit': 'Scheduled annually'
            }
        }
    
    def _generate_nyc_report(self, analysis: Dict, period: str) -> Dict:
        """NYC Local Law 144 Bias Audit Report"""
        
        return {
            'title': 'NYC Local Law 144 Bias Audit Report',
            'audit_summary': {
                'audit_date': datetime.now().isoformat(),
                'auditor': 'Internal Compliance Team',
                'tool_name': 'AI Enhancement Microservice',
                'tool_version': '1.0'
            },
            'selection_rates': {
                category: metrics.get('selection_rates', {})
                for category, metrics in analysis.get('metrics', {}).items()
            },
            'impact_ratios': {
                category: metrics.get('impact_ratios', {})
                for category, metrics in analysis.get('metrics', {}).items()
            },
            'compliance_status': {
                'meets_bias_audit_requirement': analysis.get('overall_compliance', False),
                'results_published': True,
                'notice_provided_to_candidates': True
            },
            'next_audit_date': (
                datetime.now() + timedelta(days=365)
            ).isoformat()
        }
```

## API Endpoints

### POST /api/v1/bias/analyze

**Request**:
```json
{
  "candidates": [...],
  "scoring_results": [...],
  "features_used": ["skills", "experience"],
  "threshold_score": 70
}
```

**Response**:
```json
{
  "overall_compliance": false,
  "violations": [
    {
      "protected_characteristic": "gender",
      "issue": "Female candidates selected at 65% rate of male candidates",
      "impact_ratio": 0.65,
      "severity": "HIGH"
    }
  ],
  "metrics": {...},
  "proxy_detection": {...},
  "recommendations": [...]
}
```

### GET /api/v1/bias/report

Generate compliance report for specific regulation.

### GET /api/v1/bias/dashboard

Real-time fairness metrics dashboard.

## Competitive Advantage

| Feature | This Module | Eightfold | SeekOut | ATS Built-in |
|---------|-------------|-----------|---------|--------------|
| Continuous Auditing | ✅ | ✅ | ⚠️ | ❌ |
| Four-Fifths Rule | ✅ | ✅ | ❌ | ❌ |
| Proxy Detection | ✅ | ⚠️ | ⚠️ | ❌ |
| Embedding Debiasing | ✅ | ❌ | ❌ | ❌ |
| Multi-Regulation Reports | ✅ | ⚠️ | ❌ | ❌ |
| Audit Trail | ✅ | ✅ | ⚠️ | ⚠️ |

**Legend**: ✅ = Full Support | ⚠️ = Partial | ❌ = Not Available

## ROI for Customers

### Risk Mitigation Value

**Average discrimination lawsuit cost**: $200K - $500K  
**Our pricing**: $25K/year  
**ROI**: If module prevents 1 lawsuit every 10 years = 80-200% ROI

### Brand Protection

Demonstrate DEI commitment publicly through:
- Published bias audit reports
- Transparent hiring metrics
- Third-party certifications

### Regulatory Readiness

Avoid penalties:
- EU AI Act fines: Up to 6% of global revenue
- EEOC settlements: $50K-$500K typical range
- NYC Local Law 144: $500-$1,500 per violation
