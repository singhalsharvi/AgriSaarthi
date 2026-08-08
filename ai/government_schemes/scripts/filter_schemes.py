import os
import json
import re
from typing import List, Optional


def _load_rules():
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, 'eligibility_rules.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _extract_number(text: str) -> Optional[float]:
    if not text:
        return None
    text = text.lower()
    # replace common separators
    text = text.replace(',', '')
    # handle lakhs/crores
    multiplier = 1
    if 'lakh' in text or 'lacs' in text or 'lac' in text:
        multiplier = 1e5
    if 'crore' in text:
        multiplier = 1e7
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    if not m:
        return None
    try:
        return float(m.group(1)) * multiplier
    except Exception:
        return None


def _keywords(text: Optional[str]) -> set:
    if not text:
        return set()
    if isinstance(text, (list, tuple)):
        text = ' '.join(text)
    text = str(text).lower()
    # simple tokenization and stopword removal
    words = re.findall(r"\w+", text)
    stop = {
        'and', 'the', 'of', 'in', 'on', 'for', 'with', 'to', 'all', 'state', 'states',
        'union', 'territories', 'india', 'indian', 'crops', 'crop', 'farmer', 'farmers',
        'category', 'eligible', 'families', 'family', 'scheme', 'schemes', 'minimum', 'maximum'
    }
    return {w for w in words if w not in stop}


def _keyword_score(rule_field, value) -> float:
    """Return a score between 0 and 1 indicating how well rule_field matches value.

    If either side is missing/empty, return 1 (neutral) so that absence of a rule
    does not disqualify the scheme.
    """
    # treat None/empty rule as neutral (do not reject)
    if not rule_field:
        return 1.0
    if not value:
        return 1.0
    # normalize to strings/lists
    rule_kw = _keywords(rule_field)
    val_kw = _keywords(value)
    if not rule_kw or not val_kw:
        return 1.0
    inter = rule_kw & val_kw
    # score proportional to overlap relative to smaller set
    score = len(inter) / max(1, min(len(rule_kw), len(val_kw)))
    return float(score)


def _matches_state(rule_states, state: Optional[str]) -> bool:
    # keep backwards-compatible behavior for 'all' indications
    if not rule_states or not state:
        return True
    # if rule explicitly says all states, accept
    if isinstance(rule_states, (list, tuple)):
        flat = ' '.join(rule_states).lower()
    else:
        flat = str(rule_states).lower()
    if 'all indian states' in flat or flat.strip() == 'all':
        return True
    # use keyword scoring; require at least one keyword overlap
    return _keyword_score(rule_states, state) > 0


def _matches_crop(rule_crops, crop: Optional[str]) -> bool:
    if not rule_crops or not crop:
        return True
    # handle broad allowances
    if isinstance(rule_crops, (list, tuple)):
        flat = ' '.join(rule_crops).lower()
    else:
        flat = str(rule_crops).lower()
    if 'all crops' in flat or 'all agricultural crops' in flat:
        return True
    return _keyword_score(rule_crops, crop) > 0


def _matches_category(rule_categories, farmer_category: Optional[str]) -> bool:
    if not rule_categories or not farmer_category:
        return True
    return _keyword_score(rule_categories, farmer_category) > 0


def _matches_gender(rule_gender, gender: Optional[str]) -> bool:
    # keep permissive: if either side missing, do not reject
    if not rule_gender or not gender:
        return True
    # use keywords to check for explicit gender-specific rules
    rg_kw = _keywords(rule_gender)
    g_kw = _keywords(gender)
    if not rg_kw:
        return True
    # if rule explicitly limits to female/women
    if {'female', 'women', 'woman'} & rg_kw:
        return bool({'female', 'f', 'woman'} & g_kw)
    if {'male', 'men', 'man'} & rg_kw:
        return bool({'male', 'm', 'man'} & g_kw)
    return True


def _matches_income(rule_income, annual_income) -> bool:
    # If rule has no income limit or applicant didn't provide income, don't reject
    if rule_income in (None, '') or annual_income in (None, ''):
        return True
    try:
        max_val = _extract_number(str(rule_income))
        if max_val is None:
            return True
        return float(annual_income) <= max_val
    except Exception:
        return True


def _matches_age(rule_age, age) -> bool:
    if rule_age in (None, '') or age in (None, ''):
        return True
    try:
        num = _extract_number(str(rule_age))
        if num is None:
            return True
        txt = str(rule_age).lower()
        # if rule mentions "eligible age" assume num is minimum required
        if 'above' in txt or 'minimum' in txt or 'at least' in txt:
            return float(age) >= num
        # otherwise treat number as maximum age unless explicitly 'minimum'
        return float(age) <= num
    except Exception:
        return True


def get_eligible_schemes(
    state: Optional[str] = None,
    crop: Optional[str] = None,
    farmer_category: Optional[str] = None,
    annual_income: Optional[float] = None,
    landholding: Optional[float] = None,
    age: Optional[float] = None,
    gender: Optional[str] = None,
    top_n: int = 10,
):
    """Return list of scheme names that are potentially eligible for the given profile.

    Notes:
    - If a rule field is null or not specified, it does not disqualify the applicant.
    - The matching is conservative: schemes are excluded only when the rule explicitly
      contradicts the farmer profile (e.g. scheme limited to certain states or crops).
    """
    rules = _load_rules()
    scored: List[tuple] = []
    for r in rules:
        name = r.get('scheme_name') or 'Unnamed Scheme'
        try:
            # numeric disqualifiers: if rule explicitly contradicts provided profile, skip
            if not _matches_income(r.get('income_limit'), annual_income):
                continue
            if not _matches_age(r.get('age_requirement'), age):
                continue
            if r.get('landholding_requirement'):
                lh = _extract_number(str(r.get('landholding_requirement')))
                if lh is not None and landholding is not None:
                    # if rule indicates a maximum and applicant exceeds it, exclude
                    if float(landholding) > lh:
                        continue

            # keyword-based scoring for state, crop, and farmer category
            s_score = _keyword_score(r.get('states'), state)
            c_score = _keyword_score(r.get('eligible_crops'), crop)
            cat_score = _keyword_score(r.get('farmer_category'), farmer_category)

            # gender: treat as weaker signal
            gender_ok = _matches_gender(r.get('gender_specific'), gender)
            if not gender_ok:
                continue
            g_score = 1.0 if r.get('gender_specific') in (None, '') else _keyword_score(r.get('gender_specific'), gender)

            # aggregate weighted score (higher means more relevant)
            # give higher weight to crop and state matches
            total = (0.4 * c_score) + (0.3 * s_score) + (0.2 * cat_score) + (0.1 * g_score)

            # If rule fields were all empty (neutral), keep but with low score
            scored.append((name, float(total)))
        except Exception:
            # be permissive on parsing errors
            scored.append((name, 0.0))

    # sort by score desc and return top_n scheme names
    scored.sort(key=lambda x: x[1], reverse=True)
    top = [s for s, _ in scored[:top_n]]
    return top


if __name__ == '__main__':
    # quick interactive example
    example = get_eligible_schemes(state='Karnataka', crop='rice', farmer_category='Small and marginal farmer families', annual_income=50000, landholding=1.5, age=40, gender='male')
    print('Potentially eligible schemes (names):')
    for s in example:
        print('-', s)
