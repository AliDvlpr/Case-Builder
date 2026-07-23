from services.ai.client import ai_client
from services.ai.parser import parse_case_response

PROMPT_TEMPLATE = """
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
14. Every field MUST contain BOTH:
    - content
    - status
15. Allowed status values are ONLY:
    - Complete
    - Weak
    - Missing
    - Unclear

EXTRACTION RULE (applies to every field)

Do not paraphrase, summarize, or rewrite the note in your own words.
For "content", extract the relevant sentence(s) from the note as close to the
original wording as possible. You may lightly trim a sentence to remove parts
that belong to a different field, but you must not change word choice, tone,
or phrasing. If nothing in the note relates to a field, content is null.

STATUS DEFINITIONS (apply identically to every field, including users_context)

Complete
The information is explicitly stated and sufficiently detailed to be used in a professional case study.

Weak
The information exists but lacks important details, context, reasoning, specificity, or confidence.

Missing
The note contains no usable information for this field at all.
Set content to null.

Unclear
The note contains information related to this field, but it is conflicting,
ambiguous, or too difficult to interpret with confidence.
Do not guess what it means. Set "content" to the relevant original text from
the note, and briefly append the reason it's unclear in parentheses at the end.

Rule of thumb: if the note says NOTHING related to the field → Missing.
If the note says SOMETHING related to the field but you can't confidently
interpret or trust it → Unclear. Never force Missing just because a field is
usually hard to fill in (e.g. users_context) — judge it the same way as every
other field, based only on whether the note contains relevant text.

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
A one or two sentence summary of the project, taken from the note.

problem
The primary user or business problem, as described in the note.

my_role
The designer's responsibilities.
Only include responsibilities explicitly mentioned.

users_context
Who the users are and the relevant project context, as stated in the note.
Do not assume demographics or personas.

research
Mention analytics, interviews, usability testing,
observations or any research activities that were
explicitly described.

key_ux_decisions
Describe the reasoning behind the important UX decisions.
Do NOT list implemented features.
Extract the reasoning as written, not a summary of it.

solution
Describe what was implemented, as written in the note.
Do NOT explain why it was implemented.

impact
Describe measurable outcomes, as stated in the note.
If the note only mentions expected improvements,
mark the field as Weak.
Never invent metrics.

what_i_learned
Lessons or reflections explicitly mentioned by the designer.

STATUS EXAMPLES

Example 1

Input:
"I analyzed Hotjar recordings and interviewed five users."

Output:

{
    "content": "Analyzed Hotjar recordings and interviewed five users.",
    "status": "Complete"
}

Example 2

Input:
"I talked with some users."

Output:

{
    "content": "Talked with some users.",
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
    "content": "The client says users loved it, but another part of the note says users hated it. (Conflicting user feedback)",
    "status": "Unclear"
}

Example 5

Input:
"We built it mainly for our internal sales team, though a couple of external partners might use parts of it too."

Output:

{
    "content": "Built mainly for the internal sales team, though a couple of external partners might use parts of it too. (Mix of internal and external users, not clearly defined)",
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