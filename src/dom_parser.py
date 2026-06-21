import re
from bs4 import BeautifulSoup

def parse_html_dom(html_content):
    """
    Parses HTML content and extracts form fields, validation attributes, and interactable elements.
    
    Returns:
        list of dict: Extracted elements and their metadata.
    """
    if not html_content or not html_content.strip():
        return []
        
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = []
    
    # Pre-map labels by their 'for' attribute
    labels_by_for = {}
    for label in soup.find_all('label'):
        label_text = label.get_text(strip=True)
        for_id = label.get('for')
        if for_id:
            labels_by_for[for_id] = label_text
            
    # Find all forms or scan the entire DOM if no forms exist
    forms = soup.find_all('form')
    
    # If no forms, parse elements at body/document level
    if not forms:
        elements.extend(_parse_container(soup, None, labels_by_for))
    else:
        for idx, form in enumerate(forms):
            form_id = form.get('id') or form.get('name') or f"form_{idx + 1}"
            elements.extend(_parse_container(form, form_id, labels_by_for))
            
    return elements

def _parse_container(container, form_id, labels_by_for):
    """Helper to parse inputs, select boxes, textareas, and buttons in a container."""
    extracted = []
    
    # Find inputs, selects, textareas, and buttons
    target_elements = container.find_all(['input', 'select', 'textarea', 'button'])
    
    for el in target_elements:
        el_id = el.get('id')
        el_name = el.get('name')
        placeholder = el.get('placeholder') or ""
        
        # Determine label
        label = ""
        if el_id and el_id in labels_by_for:
            label = labels_by_for[el_id]
        else:
            # Check if parent is a label
            parent_label = el.find_parent('label')
            if parent_label:
                # Get label text without the input text itself
                label = parent_label.get_text(strip=True)
                # Remove self text if any
                input_text = el.get_text(strip=True)
                if input_text and input_text in label:
                    label = label.replace(input_text, "").strip()
            else:
                # Use placeholder or name as fallback label
                label = placeholder or el_name or el_id or f"Unnamed {el.name}"
                
        # Clean label (e.g. remove trailing colons)
        label = re.sub(r'[:*]$', '', label).strip()
        
        el_type = el.name
        input_type = el.get('type', '').lower() if el_type == 'input' else None
        
        # Skip hidden inputs
        if input_type == 'hidden':
            continue
            
        # Compile metadata
        meta = {
            'element_type': el_type,
            'input_type': input_type,
            'id': el_id or "",
            'name': el_name or "",
            'label': label,
            'placeholder': placeholder,
            'required': el.has_attr('required'),
            'min_val': el.get('min'),
            'max_val': el.get('max'),
            'min_len': el.get('minlength'),
            'max_len': el.get('maxlength'),
            'pattern': el.get('pattern'),
            'options': [],
            'form_id': form_id or "default_container"
        }
        
        # Handle select options
        if el_type == 'select':
            options = el.find_all('option')
            meta['options'] = [opt.get_text(strip=True) for opt in options if opt.get('value') != ""]
            
        # Button labels
        if el_type == 'button':
            meta['label'] = el.get_text(strip=True) or el.get('value') or label
            
        # Skip generic buttons unless they are submit/reset
        if el_type == 'input' and input_type in ['submit', 'reset', 'button']:
            meta['label'] = el.get('value') or label
            
        extracted.append(meta)
        
    return extracted
