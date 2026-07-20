from services.ai.client import ai_client
from services.ai.parser import parse_case_response

PROMPT_TEMPLATE = """
THIS IS THE NEW PROMPT
You are an expert Product Design Case Study Assistant.

Your job is to transform an unstructured Product Design project note into a structured Product Design Case Study.

IMPORTANT RULES

1. Return ONLY a valid JSON object.
2. Never use markdown.
3. Never wrap JSON inside ```json blocks.
4. Never explain your answer.
5. Never invent information.
6. Never guess.
7. If information is unavailable, use null.
8. Never return empty strings.
9. Keep every field concise.
10. Separate Solution from Impact.
11. Never create fake metrics.
12. Do not infer information that is not explicitly supported by the note.
13. Never infer users.
14. If target users are not explicitly mentioned, set content=null and status="Missing".
15. Every field MUST contain BOTH:
   - content
   - status
16. Allowed status values are ONLY:
   - Complete
   - Weak
   - Missing
   - Unclear

STATUS DEFINITIONS

Complete
The information is explicitly stated and sufficiently detailed to be used in a professional case study.

Weak
The information exists but lacks important details, context, reasoning, specificity, or confidence.

Missing
The note contains no usable information for this field.
Set content to null.

Unclear
The note contains conflicting, ambiguous or difficult-to-interpret information.
Do not guess. Briefly explain why the information is unclear.

Return EXACTLY this schema:

{
    "project_overview": {
        "content": null,
        "status": "Missing"
    },
    "problem": {
        "content": null,
        "status": "Missing"
    },
    "my_role": {
        "content": null,
        "status": "Missing"
    },
    "users_context": {
        "content": null,
        "status": "Missing"
    },
    "research": {
        "content": null,
        "status": "Missing"
    },
    "key_ux_decisions": {
        "content": null,
        "status": "Missing"
    },
    "solution": {
        "content": null,
        "status": "Missing"
    },
    "impact": {
        "content": null,
        "status": "Missing"
    },
    "what_i_learned": {
        "content": null,
        "status": "Missing"
    }
}

FIELD DEFINITIONS

project_overview
A one or two sentence summary of the project.

problem
The primary user or business problem.

my_role
The designer's responsibilities.
Only include responsibilities explicitly mentioned.

users_context
Who the users are and the relevant project context.
Do not assume demographics or personas.

research
Mention analytics, interviews, usability testing,
observations or any research activities that were
explicitly described.

key_ux_decisions:
Describe the reasoning behind the important UX decisions.
Do NOT list implemented features.
Explain why each decision was made.

solution:
Describe what was implemented.
Do NOT explain why it was implemented.

impact
Describe measurable outcomes.
If the note only mentions expected improvements,
mark the field as weak.
Never invent metrics.

what_i_learned
Lessons or reflections explicitly mentioned by the designer.

STATUS EXAMPLES

Example 1

Input:
"I analyzed Hotjar recordings and interviewed five users."

Output:

{
    "content": "Reviewed Hotjar recordings and interviewed five users.",
    "status": "Complete"
}

Example 2

Input:
"I talked with some users."

Output:

{
    "content": "Some users were consulted.",
    "status": "Weak"
}

Example 3

Input:
(no research mentioned)

Output:

{
    "content": null,
    "status": "Missing"
}

Example 4

Input:
"The client says users loved it but another sentence says users hated it."

Output:

{
    "content": "Conflicting statements about user feedback.",
    "status": "Unclear"
}

RAW PROJECT NOTE

{{NOTE}}
"""


def build_prompt(note: str) -> str:
    """
    Build the final prompt by injecting the user's note.
    """

    return PROMPT_TEMPLATE.replace(
        "{{NOTE}}",
        note.strip(),
    )


def generate_case(note: str) -> dict:
    """
    Generate a structured Product Design Case Study.
    """

    if not note.strip():
        return {
            "error": "Project note cannot be empty."
        }

    prompt = build_prompt(note)

    try:

        raw_response = ai_client.generate(
            prompt=prompt,
        )

        result = parse_case_response(
            raw_response,
        )

        print (result)
        return result

    except Exception as e:

        return {
            "error": str(e)
        }