"""
validators.py — Server-Side Validation for Opportunity Data
=============================================================
Contains functions to validate request data before it reaches
the database. Returns a list of human-readable error messages.
"""

from datetime import datetime


def validate_opportunity(data, is_update=False):
    """
    Validate opportunity data from a request body.

    Args:
        data (dict): The parsed JSON request body.
        is_update (bool): If True, fields are optional (partial update).

    Returns:
        list: A list of error message strings. Empty list = valid.
    """
    errors = []

    # Define required string fields and their max lengths
    string_fields = {
        'title': 200,
        'description': None,       # TEXT — no practical max
        'research_area': 100,
        'faculty_name': 100,
        'department': 100,
        'required_skills': 500,
    }

    # --- Validate string fields ---
    for field, max_len in string_fields.items():
        value = data.get(field)

        # On CREATE, all fields are required
        if not is_update and value is None:
            errors.append(f"'{field}' is required")
            continue

        # On UPDATE, skip fields that are not provided
        if is_update and value is None:
            continue

        # Check type
        if not isinstance(value, str):
            errors.append(f"'{field}' must be a string")
            continue

        # Check not empty after trimming
        if value.strip() == '':
            errors.append(f"'{field}' cannot be empty")
            continue

        # Check max length
        if max_len and len(value.strip()) > max_len:
            errors.append(f"'{field}' must be at most {max_len} characters")

    # --- Validate positions_available ---
    positions = data.get('positions_available')
    if not is_update and positions is None:
        errors.append("'positions_available' is required")
    elif positions is not None:
        if not isinstance(positions, int) or isinstance(positions, bool):
            errors.append("'positions_available' must be a non-negative integer")
        elif positions < 0:
            errors.append("'positions_available' must be a non-negative integer")

    # --- Validate application_deadline ---
    deadline = data.get('application_deadline')
    if not is_update and deadline is None:
        errors.append("'application_deadline' is required")
    elif deadline is not None:
        if not isinstance(deadline, str):
            errors.append("'application_deadline' must be a date string in YYYY-MM-DD format")
        else:
            try:
                datetime.strptime(deadline.strip(), '%Y-%m-%d')
            except ValueError:
                errors.append("'application_deadline' must be a valid date in YYYY-MM-DD format")

    # --- Validate status (only on update) ---
    status = data.get('status')
    if status is not None:
        if status not in ('Open', 'Closed'):
            errors.append("'status' must be either 'Open' or 'Closed'")

    return errors
