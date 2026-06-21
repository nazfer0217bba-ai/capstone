import re

# NLTK setup helper (runs on-demand with robust fallback)
_nltk_initialized = False

def init_nltk():
    global _nltk_initialized
    if _nltk_initialized:
        return True
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        _nltk_initialized = True
        return True
    except Exception:
        # Fallback to pure regex if nltk is not installed or errors
        return False

def parse_user_story(story_text):
    """
    Parses a user story to extract roles, actions, target inputs, and validation constraints.
    
    Args:
        story_text (str): The raw user story description.
        
    Returns:
        dict: Analyzed entities including role, actions, targets, and constraints.
    """
    if not story_text or not story_text.strip():
        return {
            'role': 'User',
            'actions': [],
            'targets': [],
            'constraints': [],
            'scenarios': []
        }
        
    # Standardize whitespace
    story_text = re.sub(r'\s+', ' ', story_text.strip())
    
    # 1. Role extraction
    role = "User"
    role_match = re.search(r'(?i)As a(?:n)?\s+([a-zA-Z0-9_\-\s]+?)(?:,|\s+I want to|\s+I need to)', story_text)
    if role_match:
        role = role_match.group(1).strip()
        
    # 2. Extract actions and target elements
    # Common UI actions
    action_keywords = [
        'login', 'logout', 'sign in', 'sign up', 'register', 'enter', 'input', 'fill', 
        'click', 'press', 'select', 'choose', 'submit', 'delete', 'remove', 'add', 
        'create', 'update', 'edit', 'search', 'view', 'check', 'uncheck', 'toggle'
    ]
    
    actions = []
    targets = []
    
    # Simple regex-based semantic matcher
    # Look for action verbs followed by noun phrases
    # Example: "enter my username", "click the login button", "select the option"
    pattern_actions = r'(?i)\b(' + '|'.join(action_keywords) + r')\b(?:\s+the|\s+a|\s+an|\s+my|\s+their)?\s+([a-zA-Z0-9_\-\s]+?)(?:\b(?:and|or|but|so\s+that|,|to\b)|\.|$)'
    matches = re.finditer(pattern_actions, story_text)
    
    for match in matches:
        act = match.group(1).strip().lower()
        target = match.group(2).strip()
        
        # Clean target noun phrase
        target = re.sub(r'\s+(field|button|input|dropdown|box|form|checkbox|radio)$', '', target, flags=re.IGNORECASE)
        target = target.strip()
        
        if len(target) > 1 and len(target.split()) <= 4:  # Avoid matching entire clauses
            actions.append(act)
            if target not in targets:
                targets.append(target)
                
    # 3. Extract validation constraints
    # e.g., "must be at least 8 characters", "must be a valid email", "cannot be empty"
    constraints = []
    
    constraint_patterns = [
        (r'(?i)(must|should|needs to)\s+be\s+([a-zA-Z0-9_\-\s]+)', r'\1 be \2'),
        (r'(?i)(at least|minimum|min)\s+(\d+)\s+(characters|chars|items|digits)', r'min length of \2'),
        (r'(?i)(maximum|max|no more than)\s+(\d+)\s+(characters|chars|items|digits)', r'max length of \2'),
        (r'(?i)(must be a valid|should match)\s+([a-zA-Z0-9_\-\s]+)', r'format must be \2'),
        (r'(?i)(cannot|must not)\s+be\s+(empty|blank|null)', r'required (cannot be empty)'),
        (r'(?i)(between)\s+(\d+)\s+and\s+(\d+)', r'must be between \2 and \3'),
    ]
    
    for pat, desc in constraint_patterns:
        matches = re.findall(pat, story_text)
        for m in matches:
            if isinstance(m, tuple):
                # Replace placeholders
                res = desc
                for idx, val in enumerate(m):
                    res = res.replace(f'\\{idx+1}', val)
                constraints.append(res.strip())
            else:
                res = desc.replace(r'\1', m)
                constraints.append(res.strip())
                
    # Deduplicate constraints
    constraints = list(set(constraints))
    
    # 4. Generate high-level scenarios based on text structure
    scenarios = []
    clauses = re.split(r'\.|\band\b|, then|\bso that\b', story_text)
    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue
        # Check if clause contains action indicators
        if any(kw in clause.lower() for kw in action_keywords + ['should', 'must', 'can']):
            scenarios.append(clause)
            
    return {
        'role': role,
        'actions': actions,
        'targets': targets,
        'constraints': constraints,
        'scenarios': scenarios
    }
