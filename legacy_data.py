"""
Data definitions for Living Legacy project scoping.
Contains legacy types, follow-up questions, and audience options.
"""

LEGACY_TYPES = {
    "Full Life Story": {
        "icon": "📖",
        "description": "A comprehensive journey through your entire life — from earliest memories to today. This is the most complete legacy, capturing every chapter.",
        "follow_up_questions": [
            {
                "key": "time_depth",
                "question": "How far back would you like to go?",
                "type": "radio",
                "options": [
                    "As far back as I can remember",
                    "Starting from my teenage years",
                    "Starting from adulthood",
                ],
            },
            {
                "key": "themes",
                "question": "Which life themes are most important to include? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "Family & Relationships",
                    "Career & Professional Life",
                    "Education & Learning",
                    "Travel & Adventures",
                    "Faith & Spirituality",
                    "Health & Overcoming Challenges",
                    "Hobbies & Passions",
                    "Community & Volunteering",
                    "Military Service",
                    "Cultural Heritage & Traditions",
                ],
            },
            {
                "key": "tone",
                "question": "What tone or feel should the story have?",
                "type": "radio",
                "options": [
                    "Warm and conversational — like sitting on the porch together",
                    "Reflective and thoughtful — lessons learned along the way",
                    "Celebratory and uplifting — highlighting the best moments",
                    "Honest and raw — the full truth, good and hard",
                ],
            },
            {
                "key": "estimated_length",
                "question": "How extensive should the final piece be?",
                "type": "radio",
                "options": [
                    "A concise overview (10-20 pages / 30-60 min of audio)",
                    "A detailed narrative (50-100 pages / 2-4 hours of audio)",
                    "A comprehensive memoir (100+ pages / 5+ hours of audio)",
                ],
            },
        ],
    },
    "Words of Wisdom": {
        "icon": "💡",
        "description": "The life lessons, values, and advice you want to pass down. What do you know now that you wish you'd known sooner?",
        "follow_up_questions": [
            {
                "key": "wisdom_topics",
                "question": "What areas of wisdom would you like to share? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "Life lessons & general advice",
                    "Relationship & marriage wisdom",
                    "Parenting insights",
                    "Career & professional guidance",
                    "Financial lessons learned",
                    "Health & wellness advice",
                    "Faith & spiritual guidance",
                    "Dealing with adversity & resilience",
                    "Happiness & finding purpose",
                    "Mistakes I learned from",
                ],
            },
            {
                "key": "format_pref",
                "question": "How would you like the wisdom presented?",
                "type": "radio",
                "options": [
                    "Short, memorable sayings and principles",
                    "Stories that illustrate each lesson",
                    "Letters addressed to specific people",
                    "A mix of stories, advice, and reflections",
                ],
            },
            {
                "key": "tone",
                "question": "What tone feels right?",
                "type": "radio",
                "options": [
                    "Gentle and encouraging",
                    "Direct and no-nonsense",
                    "Humorous and lighthearted",
                    "Deeply personal and heartfelt",
                ],
            },
        ],
    },
    "Growing Up": {
        "icon": "🌱",
        "description": "The story of your childhood and formative years — the people, places, and moments that shaped who you became.",
        "follow_up_questions": [
            {
                "key": "era_focus",
                "question": "Which period would you like to focus on most?",
                "type": "radio",
                "options": [
                    "Early childhood (birth to age 10)",
                    "Pre-teen and teenage years (10-18)",
                    "The full span of growing up (birth through leaving home)",
                ],
            },
            {
                "key": "growing_up_themes",
                "question": "What aspects of growing up are most important to capture? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "Family life & home",
                    "Neighborhood & community",
                    "School days & friendships",
                    "Cultural traditions & holidays",
                    "Pivotal moments & turning points",
                    "Games, toys & entertainment of the era",
                    "Food, meals & family recipes",
                    "Summer vacations & adventures",
                    "Challenges & how I overcame them",
                    "The historical era I grew up in",
                ],
            },
            {
                "key": "setting_detail",
                "question": "How important is it to paint a picture of the time and place?",
                "type": "radio",
                "options": [
                    "Very important — I want readers to feel like they're there",
                    "Somewhat — mention key details but focus on the stories",
                    "Not very — the stories and people matter most",
                ],
            },
        ],
    },
    "Professional Life: My Career": {
        "icon": "💼",
        "description": "Your professional journey — the jobs, mentors, breakthroughs, and lessons from your working life.",
        "follow_up_questions": [
            {
                "key": "career_scope",
                "question": "What part of your career would you like to focus on?",
                "type": "radio",
                "options": [
                    "My entire career arc, start to finish",
                    "A specific role or company that defined me",
                    "A particular industry or field I worked in",
                    "My entrepreneurial journey / business I built",
                ],
            },
            {
                "key": "career_themes",
                "question": "Which professional themes matter most? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "How I got started & early career",
                    "Mentors & people who shaped my path",
                    "Major accomplishments & proud moments",
                    "Failures, setbacks & what I learned",
                    "Leadership philosophy & management style",
                    "Industry changes I witnessed or drove",
                    "Work-life balance & sacrifices",
                    "Advice for the next generation in my field",
                    "The legacy I left at my workplace",
                    "Transition to retirement",
                ],
            },
            {
                "key": "detail_level",
                "question": "How technical or detailed should the career story be?",
                "type": "radio",
                "options": [
                    "Keep it accessible — anyone should be able to enjoy it",
                    "Some industry detail — for people familiar with my field",
                    "In-depth — a record for professionals and colleagues",
                ],
            },
        ],
    },
    "Love & Family": {
        "icon": "❤️",
        "description": "The story of your most important relationships — your partner, your children, your family bonds.",
        "follow_up_questions": [
            {
                "key": "relationship_focus",
                "question": "Which relationships would you like to focus on? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "My love story / marriage",
                    "Being a parent",
                    "Being a grandparent",
                    "My parents & the family I came from",
                    "Siblings & extended family",
                    "Lifelong friendships",
                    "Chosen family & community bonds",
                ],
            },
            {
                "key": "family_themes",
                "question": "What aspects of these relationships matter most? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "How we met / how it all began",
                    "Traditions & rituals we built together",
                    "Challenges we faced & overcame",
                    "Everyday moments that defined us",
                    "Lessons I learned about love & commitment",
                    "Funny stories & inside jokes",
                    "What I want them to know",
                ],
            },
            {
                "key": "tone",
                "question": "What tone feels right for these stories?",
                "type": "radio",
                "options": [
                    "Romantic and sentimental",
                    "Warm and down-to-earth",
                    "Funny and affectionate",
                    "Deeply honest — the real story",
                ],
            },
        ],
    },
    "Military & Service": {
        "icon": "🎖️",
        "description": "Your time in uniform — the service, sacrifice, camaraderie, and experiences that shaped you.",
        "follow_up_questions": [
            {
                "key": "service_scope",
                "question": "What branch and era of service?",
                "type": "text",
                "placeholder": "e.g., US Army, 1968-1972 / Navy, 1990-2010",
            },
            {
                "key": "service_themes",
                "question": "Which aspects of your service are most important to capture? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "Basic training & early days",
                    "Deployments & duty stations",
                    "Combat experiences",
                    "Brotherhood & camaraderie",
                    "Leadership & lessons learned",
                    "Impact on family & home life",
                    "Transition to civilian life",
                    "How service shaped who I am",
                    "Honoring fallen comrades",
                    "Funny stories & lighter moments",
                ],
            },
            {
                "key": "sensitivity",
                "question": "Are there aspects of your service you'd prefer to keep private?",
                "type": "radio",
                "options": [
                    "I'm an open book — capture it all",
                    "Some topics are off-limits — I'll let you know as we go",
                    "I'd like to focus on the positive and skip the difficult parts",
                ],
            },
        ],
    },
    "Faith & Spiritual Journey": {
        "icon": "🙏",
        "description": "Your spiritual path — how faith has guided, challenged, and sustained you through life.",
        "follow_up_questions": [
            {
                "key": "faith_scope",
                "question": "What best describes your spiritual journey?",
                "type": "radio",
                "options": [
                    "Lifelong faith in one tradition",
                    "A journey across different beliefs or denominations",
                    "Coming to faith later in life",
                    "A spiritual but not religious path",
                    "A complex relationship with faith",
                ],
            },
            {
                "key": "faith_themes",
                "question": "What aspects of your faith journey matter most? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "Foundational beliefs & values",
                    "Key moments of spiritual growth",
                    "How faith carried me through hard times",
                    "Community & fellowship",
                    "Doubts, questions & honest wrestling",
                    "Prayers that were answered",
                    "Spiritual mentors & teachers",
                    "Faith traditions I want to pass down",
                    "How my faith evolved over time",
                ],
            },
        ],
    },
    "A Specific Chapter": {
        "icon": "📌",
        "description": "One particular period, event, or experience you want to preserve in detail — a move, an adventure, a challenge overcome.",
        "follow_up_questions": [
            {
                "key": "chapter_description",
                "question": "Briefly describe the chapter or experience you want to capture:",
                "type": "text",
                "placeholder": "e.g., The year we lived in Italy, My battle with cancer, Starting my business from scratch",
            },
            {
                "key": "chapter_timeframe",
                "question": "Roughly how long did this chapter span?",
                "type": "radio",
                "options": [
                    "A single event or moment",
                    "Days to weeks",
                    "Months",
                    "A year or two",
                    "Several years",
                ],
            },
            {
                "key": "chapter_themes",
                "question": "What makes this chapter worth preserving? (Select all that apply)",
                "type": "multiselect",
                "options": [
                    "It changed who I am",
                    "It's a story my family should know",
                    "It involved incredible people",
                    "It was an adventure or unique experience",
                    "I overcame something difficult",
                    "It shaped my values or beliefs",
                    "It's a piece of history",
                    "It's simply a great story",
                ],
            },
        ],
    },
}

AUDIENCE_OPTIONS = [
    {
        "label": "My Children",
        "icon": "👶",
        "description": "Stories and lessons for your sons and daughters",
    },
    {
        "label": "My Grandchildren",
        "icon": "👧",
        "description": "Connecting generations — so they know where they come from",
    },
    {
        "label": "Future Generations",
        "icon": "🌳",
        "description": "A lasting record for descendants you may never meet",
    },
    {
        "label": "My Spouse / Partner",
        "icon": "💑",
        "description": "A gift of memories and love for your life partner",
    },
    {
        "label": "Extended Family",
        "icon": "👨‍👩‍👧‍👦",
        "description": "Siblings, nieces, nephews, cousins — the wider family",
    },
    {
        "label": "Friends & Community",
        "icon": "🤝",
        "description": "People beyond family who are part of your story",
    },
    {
        "label": "Professional Colleagues",
        "icon": "🏢",
        "description": "Mentees, coworkers, and people in your industry",
    },
    {
        "label": "The General Public",
        "icon": "🌍",
        "description": "Your story deserves to be shared widely",
    },
    {
        "label": "Myself",
        "icon": "🪞",
        "description": "A personal reflection — capturing your story for your own sake",
    },
]

DELIVERY_FORMATS = [
    {
        "label": "Written Book / Memoir",
        "icon": "📕",
        "description": "A printed or digital book — a classic, lasting keepsake",
    },
    {
        "label": "Audio Recording",
        "icon": "🎙️",
        "description": "Stories told in your own voice — intimate and personal",
    },
    {
        "label": "Video Documentary",
        "icon": "🎬",
        "description": "Visual storytelling with interviews and imagery",
    },
    {
        "label": "Digital Archive",
        "icon": "💻",
        "description": "An interactive digital collection — stories, photos, and documents",
    },
    {
        "label": "Scrapbook / Photo Essay",
        "icon": "📸",
        "description": "A visual journey pairing photos with narrative",
    },
    {
        "label": "Letters Collection",
        "icon": "✉️",
        "description": "Personal letters to specific people — to be read now or later",
    },
    {
        "label": "Not sure yet",
        "icon": "🤔",
        "description": "We'll help you decide the best format as we go",
    },
]

TIMELINE_OPTIONS = [
    "I'd like to start right away",
    "Within the next month",
    "Within the next few months",
    "No rush — I'm just exploring for now",
]
