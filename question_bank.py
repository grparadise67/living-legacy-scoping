"""
Interview Question Bank for Living Legacy.

Questions are organized by CATEGORY (theme). Each legacy type maps to a set
of relevant categories, and user scoping selections further refine which
categories and bonus questions are included.

The generator function `generate_questions()` accepts the full project-data
dict (from build_project_data) and returns an ordered dict:
    { "Category Name": [ "question text", ... ], ... }
"""

from collections import OrderedDict

# ═══════════════════════════════════════════════════════════════════════════
# Master question pool — organised by thematic category
# ═══════════════════════════════════════════════════════════════════════════

QUESTIONS_BY_CATEGORY = {
    # ── Childhood & Growing Up ──────────────────────────────────────────
    "Childhood & Growing Up": [
        "What is your earliest memory?",
        "Where did you grow up, and what was your neighborhood like?",
        "Describe the home you grew up in — what did it look like, smell like, sound like?",
        "Who were the most important people in your childhood?",
        "What were your favorite games, toys, or ways to spend time as a kid?",
        "What was school like for you? Did you have a favorite teacher?",
        "What got you in trouble as a kid?",
        "What was dinnertime like in your family?",
        "What holidays or traditions did your family celebrate, and how?",
        "Was there a moment in your childhood that changed the direction of your life?",
        "What was the best summer you remember as a kid?",
        "What did you want to be when you grew up?",
        "What were your parents like when you were young?",
        "What music, TV shows, or movies do you remember from growing up?",
        "What was the hardest thing about being a kid in that era?",
    ],

    # ── Family & Relationships ──────────────────────────────────────────
    "Family & Relationships": [
        "How did you meet your spouse or life partner?",
        "What was your wedding day like?",
        "What's the secret to a lasting relationship, in your experience?",
        "What was it like becoming a parent for the first time?",
        "What's a favorite memory with each of your children?",
        "How would you describe your parenting style?",
        "What traditions have you created with your own family?",
        "What do you admire most about your parents?",
        "Tell me about a family challenge you overcame together.",
        "What do you most want your children or grandchildren to know about you?",
        "Is there a family recipe, song, or saying that's been passed down?",
        "What has being a grandparent meant to you?",
        "Describe a perfect ordinary day with your family.",
        "What's the funniest thing that ever happened in your family?",
        "Who in your extended family had the biggest impact on you?",
    ],

    # ── Career & Professional Life ──────────────────────────────────────
    "Career & Professional Life": [
        "What was your very first job?",
        "How did you end up in the career or industry you spent your life in?",
        "Who was the most influential mentor in your professional life?",
        "What accomplishment are you most proud of professionally?",
        "Tell me about a time you failed at work and what you learned from it.",
        "How did your career change you as a person?",
        "What was the biggest risk you took professionally?",
        "What was the hardest decision you ever made at work?",
        "What leadership lesson took you the longest to learn?",
        "If you could give one piece of career advice to a young person, what would it be?",
        "How did you handle the balance between work and family?",
        "What do you think your colleagues would say about you?",
        "What industry changes did you witness during your career?",
        "Describe the moment you knew it was time to retire or move on.",
        "What legacy did you leave at the place you worked the longest?",
    ],

    # ── Values & Life Lessons ───────────────────────────────────────────
    "Values & Life Lessons": [
        "What values were you raised with that you still hold today?",
        "What's the most important lesson life has taught you?",
        "What do you know now that you wish you'd known at 20?",
        "What does 'success' mean to you — has that definition changed?",
        "What advice would you give about handling money?",
        "How do you define a good life?",
        "What's the best advice anyone ever gave you?",
        "What's a mistake you made that taught you something valuable?",
        "How do you handle disagreements or conflict?",
        "What does courage mean to you? When have you had to be courageous?",
        "How do you decide what's right when the answer isn't clear?",
        "What's worth fighting for?",
        "If you could write a letter to your younger self, what would it say?",
        "What keeps you going when life gets hard?",
        "What do you hope people learn from your life?",
    ],

    # ── Faith & Spirituality ────────────────────────────────────────────
    "Faith & Spirituality": [
        "How would you describe your relationship with faith or spirituality?",
        "Were you raised in a religious tradition? How did that shape you?",
        "Was there a defining moment in your spiritual life?",
        "How has your faith helped you through difficult times?",
        "Have you ever had doubts? How did you work through them?",
        "What spiritual practices are most meaningful to you?",
        "Is there a scripture, prayer, or saying that guides your life?",
        "Who has been a spiritual mentor or model for you?",
        "How has your faith changed or deepened over the years?",
        "What do you hope to pass down about your faith?",
        "Describe a moment you felt truly at peace.",
        "How does your faith community matter to you?",
    ],

    # ── Military & Service ──────────────────────────────────────────────
    "Military & Service": [
        "Why did you join the military / enter service?",
        "What was basic training like?",
        "Where were you stationed, and what was life like there?",
        "Tell me about the people you served with — who stands out?",
        "What was your most meaningful experience during your service?",
        "How did military life affect your family?",
        "Was there a moment that tested everything you had?",
        "What did you learn about leadership in the military?",
        "How did you transition back to civilian life?",
        "Is there a fallen comrade you'd like to honor or remember?",
        "What do civilians most misunderstand about military life?",
        "How did your service shape the person you became?",
        "What's the funniest thing that happened during your service?",
        "If you could talk to a young person considering enlisting, what would you say?",
    ],

    # ── Adventures & Experiences ────────────────────────────────────────
    "Adventures & Experiences": [
        "What's the greatest adventure you've ever had?",
        "Where is the most memorable place you've ever traveled?",
        "Tell me about a time you stepped completely outside your comfort zone.",
        "What's the most spontaneous thing you've ever done?",
        "Is there an experience that fundamentally changed how you see the world?",
        "What's a hobby or passion that has brought you the most joy?",
        "Describe a perfect day doing something you love.",
        "What's a risk you took that paid off — or didn't?",
        "Tell me about a time you were truly awestruck.",
        "What's on your bucket list that you still hope to do?",
    ],

    # ── Health & Resilience ─────────────────────────────────────────────
    "Health & Resilience": [
        "Have you faced a serious health challenge? How did you cope?",
        "What kept you strong during the hardest period of your life?",
        "How did your family support you through a difficult time?",
        "What did you learn about yourself through adversity?",
        "Has a loss or hardship changed your perspective on life?",
        "What advice would you give someone going through something similar?",
        "How do you take care of your mental and emotional health?",
        "Who or what gave you hope when things looked dark?",
    ],

    # ── Cultural Heritage & Traditions ──────────────────────────────────
    "Cultural Heritage & Traditions": [
        "What is your cultural or ethnic heritage?",
        "What traditions from your culture are most important to you?",
        "Are there family customs you'd like to see continue?",
        "What language(s) were spoken in your home growing up?",
        "Tell me about a food or recipe that connects you to your heritage.",
        "What cultural values were instilled in you?",
        "How has your heritage shaped your identity?",
        "Is there a family history or origin story that's been passed down?",
    ],

    # ── Reflection & Legacy ─────────────────────────────────────────────
    "Reflection & Legacy": [
        "When you look back on your life, what are you most grateful for?",
        "What are you most proud of?",
        "Is there anything you wish you'd done differently?",
        "What do you want people to remember about you?",
        "If you could live one day over again, which would it be and why?",
        "What brings you the most joy right now?",
        "What does the word 'legacy' mean to you?",
        "What message would you like to leave for future generations?",
        "How would you like to be remembered by those who knew you best?",
        "If you had one more thing to say to the people you love, what would it be?",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════
# Mapping: legacy type → default categories to include
# ═══════════════════════════════════════════════════════════════════════════

LEGACY_TYPE_CATEGORIES = {
    "Full Life Story": [
        "Childhood & Growing Up",
        "Family & Relationships",
        "Career & Professional Life",
        "Values & Life Lessons",
        "Adventures & Experiences",
        "Reflection & Legacy",
    ],
    "Words of Wisdom": [
        "Values & Life Lessons",
        "Reflection & Legacy",
    ],
    "Growing Up": [
        "Childhood & Growing Up",
        "Cultural Heritage & Traditions",
    ],
    "Professional Life: My Career": [
        "Career & Professional Life",
        "Values & Life Lessons",
    ],
    "Love & Family": [
        "Family & Relationships",
        "Reflection & Legacy",
    ],
    "Military & Service": [
        "Military & Service",
        "Values & Life Lessons",
        "Reflection & Legacy",
    ],
    "Faith & Spiritual Journey": [
        "Faith & Spirituality",
        "Values & Life Lessons",
        "Reflection & Legacy",
    ],
    "A Specific Chapter": [
        "Adventures & Experiences",
        "Health & Resilience",
        "Reflection & Legacy",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════
# Mapping: scoping theme selections → extra categories to pull in
# These keys match the multiselect option strings from legacy_data.py
# ═══════════════════════════════════════════════════════════════════════════

THEME_TO_CATEGORY = {
    # Full Life Story themes
    "Family & Relationships": "Family & Relationships",
    "Career & Professional Life": "Career & Professional Life",
    "Education & Learning": "Childhood & Growing Up",
    "Travel & Adventures": "Adventures & Experiences",
    "Faith & Spirituality": "Faith & Spirituality",
    "Health & Overcoming Challenges": "Health & Resilience",
    "Hobbies & Passions": "Adventures & Experiences",
    "Community & Volunteering": "Cultural Heritage & Traditions",
    "Military Service": "Military & Service",
    "Cultural Heritage & Traditions": "Cultural Heritage & Traditions",

    # Words of Wisdom topics
    "Life lessons & general advice": "Values & Life Lessons",
    "Relationship & marriage wisdom": "Family & Relationships",
    "Parenting insights": "Family & Relationships",
    "Career & professional guidance": "Career & Professional Life",
    "Financial lessons learned": "Values & Life Lessons",
    "Health & wellness advice": "Health & Resilience",
    "Faith & spiritual guidance": "Faith & Spirituality",
    "Dealing with adversity & resilience": "Health & Resilience",
    "Happiness & finding purpose": "Values & Life Lessons",
    "Mistakes I learned from": "Values & Life Lessons",

    # Growing Up themes
    "Family life & home": "Family & Relationships",
    "Neighborhood & community": "Cultural Heritage & Traditions",
    "School days & friendships": "Childhood & Growing Up",
    "Cultural traditions & holidays": "Cultural Heritage & Traditions",
    "Pivotal moments & turning points": "Values & Life Lessons",
    "Games, toys & entertainment of the era": "Childhood & Growing Up",
    "Food, meals & family recipes": "Cultural Heritage & Traditions",
    "Summer vacations & adventures": "Adventures & Experiences",
    "Challenges & how I overcame them": "Health & Resilience",
    "The historical era I grew up in": "Cultural Heritage & Traditions",

    # Career themes
    "How I got started & early career": "Career & Professional Life",
    "Mentors & people who shaped my path": "Career & Professional Life",
    "Major accomplishments & proud moments": "Career & Professional Life",
    "Failures, setbacks & what I learned": "Health & Resilience",
    "Leadership philosophy & management style": "Career & Professional Life",
    "Industry changes I witnessed or drove": "Career & Professional Life",
    "Work-life balance & sacrifices": "Family & Relationships",
    "Advice for the next generation in my field": "Values & Life Lessons",
    "The legacy I left at my workplace": "Reflection & Legacy",
    "Transition to retirement": "Reflection & Legacy",

    # Love & Family — relationship focus
    "My love story / marriage": "Family & Relationships",
    "Being a parent": "Family & Relationships",
    "Being a grandparent": "Family & Relationships",
    "My parents & the family I came from": "Family & Relationships",
    "Siblings & extended family": "Family & Relationships",
    "Lifelong friendships": "Family & Relationships",
    "Chosen family & community bonds": "Cultural Heritage & Traditions",

    # Love & Family — family themes
    "How we met / how it all began": "Family & Relationships",
    "Traditions & rituals we built together": "Cultural Heritage & Traditions",
    "Challenges we faced & overcame": "Health & Resilience",
    "Everyday moments that defined us": "Family & Relationships",
    "Lessons I learned about love & commitment": "Values & Life Lessons",
    "Funny stories & inside jokes": "Family & Relationships",
    "What I want them to know": "Reflection & Legacy",

    # Military themes
    "Basic training & early days": "Military & Service",
    "Deployments & duty stations": "Military & Service",
    "Combat experiences": "Military & Service",
    "Brotherhood & camaraderie": "Military & Service",
    "Leadership & lessons learned": "Values & Life Lessons",
    "Impact on family & home life": "Family & Relationships",
    "Transition to civilian life": "Military & Service",
    "How service shaped who I am": "Reflection & Legacy",
    "Honoring fallen comrades": "Military & Service",
    "Funny stories & lighter moments": "Military & Service",

    # Faith themes
    "Foundational beliefs & values": "Faith & Spirituality",
    "Key moments of spiritual growth": "Faith & Spirituality",
    "How faith carried me through hard times": "Faith & Spirituality",
    "Community & fellowship": "Cultural Heritage & Traditions",
    "Doubts, questions & honest wrestling": "Faith & Spirituality",
    "Prayers that were answered": "Faith & Spirituality",
    "Spiritual mentors & teachers": "Faith & Spirituality",
    "Faith traditions I want to pass down": "Faith & Spirituality",
    "How my faith evolved over time": "Faith & Spirituality",

    # Specific Chapter themes
    "It changed who I am": "Reflection & Legacy",
    "It's a story my family should know": "Family & Relationships",
    "It involved incredible people": "Family & Relationships",
    "It was an adventure or unique experience": "Adventures & Experiences",
    "I overcame something difficult": "Health & Resilience",
    "It shaped my values or beliefs": "Values & Life Lessons",
    "It's a piece of history": "Cultural Heritage & Traditions",
    "It's simply a great story": "Adventures & Experiences",
}


# ═══════════════════════════════════════════════════════════════════════════
# Generator
# ═══════════════════════════════════════════════════════════════════════════

def generate_questions(project_data: dict) -> OrderedDict:
    """
    Given a project_data dict (from build_project_data), return an
    OrderedDict of { category_name: [question, ...] } tailored to
    the user's legacy type and scoping selections.
    """
    legacy_type = project_data["legacy_type"]

    # Start with the base categories for this legacy type
    categories = list(LEGACY_TYPE_CATEGORIES.get(legacy_type, []))

    # Expand categories based on scoping theme selections
    scoping = project_data.get("scoping_details", {})
    for _question_text, answer in scoping.items():
        if isinstance(answer, list):
            for theme in answer:
                mapped = THEME_TO_CATEGORY.get(theme)
                if mapped and mapped not in categories:
                    categories.append(mapped)
        elif isinstance(answer, str):
            mapped = THEME_TO_CATEGORY.get(answer)
            if mapped and mapped not in categories:
                categories.append(mapped)

    # Always end with Reflection & Legacy if not already present
    if "Reflection & Legacy" not in categories:
        categories.append("Reflection & Legacy")

    # Assemble questions
    result = OrderedDict()
    for cat in categories:
        questions = QUESTIONS_BY_CATEGORY.get(cat, [])
        if questions:
            result[cat] = list(questions)  # copy so we don't mutate master

    return result
