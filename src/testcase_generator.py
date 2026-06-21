import re
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Define synthetic training corpus for the ML Classifier
SYNTHETIC_TRAINING_DATA = [
    # (Name/Description, Type, ElementType, InputType, Label)
    ("Verify password complexity validation", "Boundary", "input", "password", "Critical"),
    ("Ensure session token is invalidated on logout", "Functional", "button", None, "Critical"),
    ("Submit payment form with valid credit card", "Functional", "form", None, "Critical"),
    ("Verify payment transaction fails with expired card", "Negative", "input", "text", "Critical"),
    ("Verify user is redirected to dashboard after login", "Functional", "form", None, "Critical"),
    ("Verify login fails with wrong password", "Negative", "input", "password", "Critical"),
    ("Ensure empty password field displays error", "Negative", "input", "password", "Critical"),
    ("Ensure user can delete account permanently", "Functional", "button", None, "Critical"),
    
    ("Submit registration form with valid data", "Functional", "form", None, "High"),
    ("Submit search query with valid term", "Functional", "input", "text", "High"),
    ("Ensure email input matches valid format regex", "Boundary", "input", "email", "High"),
    ("Verify search fails when inputs exceed maximum characters", "Boundary", "input", "text", "High"),
    ("Verify submission of profile photo", "Functional", "input", "file", "High"),
    ("Ensure delete product action displays confirmation prompt", "Functional", "button", None, "High"),
    ("Ensure form cannot be submitted with empty required fields", "Negative", "form", None, "High"),
    ("Verify validation warning for blank username", "Negative", "input", "text", "High"),
    
    ("Verify text area accepts multi-line input", "Functional", "textarea", None, "Medium"),
    ("Verify search returns zero results for gibberish terms", "Negative", "input", "text", "Medium"),
    ("Verify dropdown select updates value", "Functional", "select", None, "Medium"),
    ("Verify check/uncheck status of checkbox", "Functional", "input", "checkbox", "Medium"),
    ("Verify radio button selection logic", "Functional", "input", "radio", "Medium"),
    ("Ensure phone number field allows optional formatting", "Functional", "input", "tel", "Medium"),
    ("Verify reset button clears all fields in the form", "Functional", "input", "reset", "Medium"),
    ("Verify numeric input matches range rules", "Boundary", "input", "number", "Medium"),
    
    ("Verify layout does not break when label text wraps", "Functional", "label", None, "Low"),
    ("Verify placeholder text is grayed out", "Functional", "input", "text", "Low"),
    ("Verify hover effects on cancel button", "Functional", "button", None, "Low"),
    ("Verify help icon displays tooltip on hover", "Functional", "button", None, "Low"),
    ("Verify reset form inputs works as intended", "Functional", "button", None, "Low"),
    ("Verify input element has correct placeholder", "Functional", "input", "text", "Low"),
]

class TestPriorityClassifier:
    """
    ML Classifier that predicts the priority (Critical, High, Medium, Low) of a test case
    using Scikit-Learn's RandomForestClassifier trained on text & structural features.
    """
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.classes = ["Critical", "High", "Medium", "Low"]
        self._train()
        
    def _extract_features(self, name_desc, tc_type, el_type, input_type):
        """Extracts numerical features from test case descriptions and metadata."""
        text = name_desc.lower()
        
        # 1. Keywords related to security/auth
        sec_keywords = ["login", "password", "auth", "credential", "session", "logout", "token", "security"]
        f_security = 1.0 if any(k in text for k in sec_keywords) else 0.0
        
        # 2. Keywords related to billing/payment/critical actions
        pay_keywords = ["pay", "card", "billing", "checkout", "transaction", "checkout", "buy", "purchase"]
        f_payment = 1.0 if any(k in text for k in pay_keywords) else 0.0
        
        # 3. Keywords related to destructive/critical actions
        del_keywords = ["delete", "remove", "cancel", "drop", "terminate", "destroy"]
        f_deletion = 1.0 if any(k in text for k in del_keywords) else 0.0
        
        # 4. Input types
        f_is_pw = 1.0 if input_type == "password" else 0.0
        f_is_email = 1.0 if input_type == "email" else 0.0
        f_is_number = 1.0 if input_type == "number" else 0.0
        
        # 5. Test Case Type
        f_is_negative = 1.0 if tc_type == "Negative" else 0.0
        f_is_boundary = 1.0 if tc_type == "Boundary" else 0.0
        f_is_functional = 1.0 if tc_type == "Functional" else 0.0
        
        # 6. Element Type
        f_is_button = 1.0 if el_type == "button" or (el_type == "input" and input_type in ["submit", "button"]) else 0.0
        f_is_form = 1.0 if el_type == "form" else 0.0
        
        # 7. Word lengths
        f_length = float(len(text.split()))
        
        return [
            f_security, f_payment, f_deletion, f_is_pw, f_is_email, f_is_number,
            f_is_negative, f_is_boundary, f_is_functional, f_is_button, f_is_form, f_length
        ]
        
    def _train(self):
        X = []
        y = []
        for name_desc, tc_type, el_type, input_type, label in SYNTHETIC_TRAINING_DATA:
            features = self._extract_features(name_desc, tc_type, el_type, input_type)
            X.append(features)
            y.append(self.classes.index(label))
            
        self.model.fit(np.array(X), np.array(y))
        
    def predict(self, name_desc, tc_type, el_type, input_type):
        """Predicts the priority class for a test case."""
        features = self._extract_features(name_desc, tc_type, el_type, input_type)
        idx = self.model.predict([features])[0]
        return self.classes[idx]


# Initialize classifier
classifier = TestPriorityClassifier()


def generate_test_cases(dom_elements, nlp_data, include_negative=True, include_boundary=True):
    """
    Generates test cases by combining DOM element inputs with NLP user stories.
    
    Args:
        dom_elements (list of dict): Elements extracted from HTML DOM.
        nlp_data (dict): Data parsed from user story.
        include_negative (bool): Whether to generate negative scenarios.
        include_boundary (bool): Whether to generate boundary/limit scenarios.
        
    Returns:
        list of dict: Generated test cases.
    """
    test_cases = []
    tc_counter = 1
    
    def add_tc(element_label, tc_type, name, description, steps, expected, el_type, in_type):
        nonlocal tc_counter
        prio = classifier.predict(name + " " + description, tc_type, el_type, in_type)
        test_cases.append({
            'id': f"TC_{tc_counter:03d}",
            'element': element_label,
            'type': tc_type,
            'name': name,
            'description': description,
            'steps': steps,
            'expected_result': expected,
            'priority': prio
        })
        tc_counter += 1

    # Apply NLP context to existing DOM elements
    # e.g., if user story mentions a field, mark it as high priority or update constraints
    nlp_targets = [t.lower() for t in nlp_data.get('targets', [])]
    nlp_constraints = nlp_data.get('constraints', [])
    
    # 1. PROCESS EACH DOM ELEMENT
    for el in dom_elements:
        label = el['label']
        el_type = el['element_type']
        in_type = el['input_type']
        form_id = el['form_id']
        required = el['required']
        
        # Check if NLP requirements target this field
        is_nlp_targeted = any(t in label.lower() or (el['name'] and t in el['name'].lower()) for t in nlp_targets)
        
        # Determine constraints based on DOM or NLP rules
        min_len = el['min_len']
        max_len = el['max_len']
        min_val = el['min_val']
        max_val = el['max_val']
        pattern = el['pattern']
        
        # NLP constraints override if applicable
        for constraint in nlp_constraints:
            constraint_lower = constraint.lower()
            if label.lower() in constraint_lower or (el['name'] and el['name'].lower() in constraint_lower):
                # Attempt to extract limits
                len_match = re.search(r'min length of (\d+)', constraint_lower)
                if len_match:
                    min_len = int(len_match.group(1))
                max_len_match = re.search(r'max length of (\d+)', constraint_lower)
                if max_len_match:
                    max_len = int(max_len_match.group(1))
                if 'required' in constraint_lower:
                    required = True
                    
        # --- A. Functional Test Cases ---
        # Basic interactive test case
        if el_type == 'button' or in_type in ['submit', 'button']:
            add_tc(
                element_label=label,
                tc_type="Functional",
                name=f"Verify {label} click action",
                description=f"Ensure clicking '{label}' triggers the associated event or submits the form.",
                steps=f"1. Navigate to the form containing '{label}'.\n2. Fill in any other required inputs.\n3. Click the '{label}' button.",
                expected=f"The application performs the action or redirects/submits successfully.",
                el_type=el_type,
                in_type=in_type
            )
        elif el_type == 'select':
            opts_str = ", ".join(el['options'][:3])
            add_tc(
                element_label=label,
                tc_type="Functional",
                name=f"Verify selection from {label} dropdown",
                description=f"Ensure a user can select options from the '{label}' dropdown.",
                steps=f"1. Click the '{label}' dropdown.\n2. Select an option (e.g., '{el['options'][0] if el['options'] else 'Option 1'}').\n3. Observe the change.",
                expected=f"The selected option is highlighted and active.",
                el_type=el_type,
                in_type=in_type
            )
        elif in_type in ['checkbox', 'radio']:
            add_tc(
                element_label=label,
                tc_type="Functional",
                name=f"Verify toggling of {label}",
                description=f"Ensure the '{label}' option can be selected and deselected.",
                steps=f"1. Locate the '{label}' selection.\n2. Click/Toggle the element.",
                expected=f"The element changes state (checked/unchecked).",
                el_type=el_type,
                in_type=in_type
            )
        else:
            # Standard Text/Number/Email/Textarea inputs
            placeholder = el['placeholder'] or label
            sample_value = "Test Input"
            if in_type == 'email':
                sample_value = "user@example.com"
            elif in_type == 'password':
                sample_value = "P@ssw0rd123"
            elif in_type == 'number':
                sample_value = str(min_val) if min_val else "10"
                
            add_tc(
                element_label=label,
                tc_type="Functional",
                name=f"Verify valid input in {label} field",
                description=f"Ensure the user can input standard characters into the '{label}' field.",
                steps=f"1. Click on the '{label}' input field.\n2. Type a valid value (e.g. '{sample_value}').\n3. Unfocus or submit.",
                expected=f"The text is successfully inputted and no error is raised.",
                el_type=el_type,
                in_type=in_type
            )
            
        # --- B. Negative Test Cases ---
        if include_negative:
            # Required field validation
            if required:
                add_tc(
                    element_label=label,
                    tc_type="Negative",
                    name=f"Verify error for blank required field: {label}",
                    description=f"Verify validation triggers when '{label}' is left empty.",
                    steps=f"1. Leave the '{label}' field blank.\n2. Complete other fields if necessary.\n3. Click Submit.",
                    expected=f"A validation error is shown indicating '{label}' is required.",
                    el_type=el_type,
                    in_type=in_type
                )
            
            # Format validation (Email)
            if in_type == 'email':
                invalid_emails = ["user@", "user@domain", "user.domain.com"]
                for ie in invalid_emails:
                    add_tc(
                        element_label=label,
                        tc_type="Negative",
                        name=f"Verify invalid email format: {ie}",
                        description=f"Ensure inputting an invalid email syntax '{ie}' displays a format error.",
                        steps=f"1. Enter '{ie}' into the '{label}' field.\n2. Try to submit the form.",
                        expected=f"Browser or form validation flags '{ie}' as an invalid email address.",
                        el_type=el_type,
                        in_type=in_type
                    )
                    
            # Script injection testing (Text/Textarea inputs)
            if el_type in ['textarea'] or (el_type == 'input' and in_type in ['text', 'search']):
                add_tc(
                    element_label=label,
                    tc_type="Negative",
                    name=f"Verify script injection prevention on {label}",
                    description=f"Ensure inputting malicious HTML/JS scripts is sanitized.",
                    steps=f"1. Input '<script>alert(1)</script>' in the '{label}' field.\n2. Submit the form.",
                    expected=f"The application encodes, sanitizes, or rejects the script input safely without executing code.",
                    el_type=el_type,
                    in_type=in_type
                )
                
        # --- C. Boundary Value Test Cases ---
        if include_boundary:
            # Length bounds
            if min_len:
                short_val = "A" * (int(min_len) - 1)
                add_tc(
                    element_label=label,
                    tc_type="Boundary",
                    name=f"Verify minlength boundary for {label}",
                    description=f"Ensure inputting less than the minimum length of {min_len} characters is blocked.",
                    steps=f"1. Enter '{short_val}' (length {len(short_val)}) into the '{label}' field.\n2. Click Submit.",
                    expected=f"Form fails to submit and displays a minimum length error.",
                    el_type=el_type,
                    in_type=in_type
                )
            if max_len:
                long_val = "B" * (int(max_len) + 1)
                add_tc(
                    element_label=label,
                    tc_type="Boundary",
                    name=f"Verify maxlength boundary for {label}",
                    description=f"Ensure inputs exceeding the maximum length of {max_len} are either truncated or blocked.",
                    steps=f"1. Try to enter '{long_val}' (length {len(long_val)}) into the '{label}' field.\n2. Observe input limits.",
                    expected=f"Input is truncated to {max_len} characters or submission triggers an error.",
                    el_type=el_type,
                    in_type=in_type
                )
            # Numeric bounds
            if in_type == 'number':
                if min_val is not None:
                    below_min = float(min_val) - 1
                    add_tc(
                        element_label=label,
                        tc_type="Boundary",
                        name=f"Verify minimum value bound for {label}",
                        description=f"Ensure values below the minimum limit of {min_val} are rejected.",
                        steps=f"1. Input '{below_min}' in '{label}'.\n2. Click submit.",
                        expected=f"Error message indicates value must be greater than or equal to {min_val}.",
                        el_type=el_type,
                        in_type=in_type
                    )
                if max_val is not None:
                    above_max = float(max_val) + 1
                    add_tc(
                        element_label=label,
                        tc_type="Boundary",
                        name=f"Verify maximum value bound for {label}",
                        description=f"Ensure values above the maximum limit of {max_val} are rejected.",
                        steps=f"1. Input '{above_max}' in '{label}'.\n2. Click submit.",
                        expected=f"Error message indicates value must be less than or equal to {max_val}.",
                        el_type=el_type,
                        in_type=in_type
                    )
                    
    # 2. PROCESS ABSTRACT NLP SCENARIOS NOT MAPPED TO DOM
    # If the user story has actions/scenarios that weren't captured by DOM elements, generate workflow test cases
    for scenario in nlp_data.get('scenarios', []):
        # Check if this scenario is already covered by DOM elements
        is_covered = False
        for tc in test_cases:
            # Simple keyword matching to see if scenario maps to an existing test case
            words = scenario.lower().split()
            matched_words = sum(1 for w in words if w in tc['name'].lower() or w in tc['description'].lower())
            if matched_words >= 3:
                is_covered = True
                break
                
        if not is_covered:
            # Create a workflow level test case
            action_verb = "execute"
            for act in nlp_data.get('actions', []):
                if act in scenario.lower():
                    action_verb = act
                    break
                    
            add_tc(
                element_label="User Story Flow",
                tc_type="Functional",
                name=f"Verify story action: {scenario[:40]}...",
                description=f"Execute workflow: {scenario}",
                steps=f"1. Initiate workflow corresponding to '{scenario}'.\n2. Perform required NLP steps.\n3. Verify results.",
                expected=f"System responds correctly to action and transitions states.",
                el_type="workflow",
                in_type=None
            )
            
    return test_cases
