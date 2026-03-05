"""
domains.py — The Twelve Domains of Human Flourishing

Every person is the centerpiece of an architecture far more vast than any single
government program or social service. The Dome is not a safety net — it is a cathedral.
These twelve domains represent the full spectrum of what it means for a human being
to flourish: not merely to survive, not merely to be comfortable, but to become
fully alive in every dimension of existence.

The domains are organized into three layers:
  - Foundation: The bedrock conditions without which flourishing cannot begin
  - Aspiration: The dimensions that elevate life from adequate to magnificent
  - Transcendence: The realms where human experience touches something beyond itself
"""

from typing import Any


FLOURISHING_DOMAINS: list[dict[str, Any]] = [
    {
        "id": "health_vitality",
        "name": "Health & Vitality",
        "color": "#1A6B3C",
        "icon": "heart-pulse",
        "layer": "foundation",
        "description": (
            "Health is not merely the absence of disease. It is the felt experience of "
            "aliveness — the capacity to wake each morning with energy sufficient for the day's "
            "purposes, to move through the world without the constant friction of pain or limitation, "
            "to trust that the body and mind will carry one forward. Vitality is health in its "
            "affirmative dimension: not just surviving but thriving, not just functioning but "
            "flourishing in the most literal, biological sense."
        ),
        "flourishing_looks_like": (
            "A person flourishing in health and vitality sleeps deeply and wakes restored. They "
            "have access to nutritious food that they enjoy eating, to clean water, to air that "
            "does not slowly poison them. They can see a doctor when something is wrong, but more "
            "importantly, their daily environment — their neighborhood, their workplace, their home — "
            "actively supports their wellbeing rather than degrading it. They move their body not "
            "out of guilt but out of joy. They understand their own health not as a mystery managed "
            "by experts but as a felt reality they participate in shaping. Mental health is not "
            "separated from physical health; the wholeness of the person is honored. Chronic stress "
            "does not define their baseline. They age with dignity, and when illness comes, they "
            "are not abandoned to navigate it alone."
        ),
        "threats": [
            "Food deserts and nutritional poverty that make healthy eating a privilege",
            "Environmental toxins concentrated in communities of least political power",
            "Healthcare systems designed around profit extraction rather than healing",
            "Chronic stress from economic precarity that erodes the body over decades",
            "Mental health stigma that isolates people from the help they need",
            "Sedentary built environments that engineer movement out of daily life"
        ],
        "de_risked_by": [
            "Universal healthcare access decoupled from employment status",
            "Community health infrastructure embedded in neighborhoods",
            "Food sovereignty — the right and ability to grow, choose, and access real food",
            "Environmental justice that distributes clean air and water equitably",
            "Preventive and holistic health models that treat the whole person",
            "Mental health support normalized and accessible at every life stage"
        ]
    },
    {
        "id": "economic_prosperity",
        "name": "Economic Prosperity",
        "color": "#6B5A1A",
        "icon": "landmark",
        "layer": "foundation",
        "description": (
            "Economic prosperity is not wealth accumulation. It is economic sufficiency — the "
            "condition in which a person has enough material resources to participate fully in "
            "their society, to make meaningful choices about their life, and to weather setbacks "
            "without catastrophe. Prosperity means the absence of economic terror: the knowledge "
            "that one will not be destroyed by a medical bill, a job loss, or a broken appliance."
        ),
        "flourishing_looks_like": (
            "A person flourishing economically is not necessarily rich. They have stable housing "
            "they can afford. They have work that compensates them fairly and does not consume "
            "every waking hour. They can save — not heroically, but naturally, because their "
            "income exceeds their basic needs by enough to plan ahead. They have access to credit "
            "that does not exploit them. They can invest in their children's futures, take a "
            "vacation, replace worn-out shoes without agonizing. Economic flourishing means "
            "having enough slack in the system that a person can make decisions based on what "
            "matters to them rather than what desperation demands. They own assets — a home, "
            "savings, perhaps a small business — that compound over time rather than debts that "
            "compound against them. Economic security is the floor beneath all other aspirations."
        ),
        "threats": [
            "Wage stagnation that disconnects productivity from compensation",
            "Predatory financial instruments designed to extract wealth from the vulnerable",
            "Housing costs that consume the majority of income and prevent wealth-building",
            "Lack of intergenerational wealth transfer in historically excluded communities",
            "Automation without redistribution, concentrating gains among capital owners",
            "The gig economy's erosion of stable employment with benefits and protections"
        ],
        "de_risked_by": [
            "Living wage floors indexed to actual cost of living in each geography",
            "Universal basic services that reduce the cost of a dignified life",
            "Community-owned financial institutions and cooperative economics",
            "Progressive asset-building programs that close the racial wealth gap",
            "Worker ownership models that distribute profits to those who create them",
            "Financial literacy and empowerment integrated into public education"
        ]
    },
    {
        "id": "creative_expression",
        "name": "Creative Expression",
        "color": "#8B1A6B",
        "icon": "palette",
        "layer": "aspiration",
        "description": (
            "Every human being is born creative. Not in the narrow sense of artistic talent, "
            "but in the fundamental sense of being a maker — of meaning, of beauty, of order, "
            "of surprise. Creative expression is the domain where a person discovers that they "
            "have something to say that has never been said before, something to make that has "
            "never existed. It is the antidote to the lie that some people are creative and "
            "others are merely consumers."
        ),
        "flourishing_looks_like": (
            "A person flourishing in creative expression has regular access to the tools, "
            "spaces, and time needed to make things. They might paint, or code, or cook "
            "elaborate meals, or arrange flowers, or write poetry, or build furniture, or "
            "design games. The specific medium matters less than the experience of creative "
            "agency — the knowledge that one can shape the world, however modestly. They have "
            "been exposed to enough art, music, literature, and craft to have developed their "
            "own aesthetic sensibility. They have spaces — physical and temporal — where creative "
            "work is possible: a workshop, a kitchen, a studio, even a corner of a room. "
            "They are not so exhausted by survival that imagination has been extinguished. "
            "Their creativity is witnessed: someone sees what they make, responds to it, is "
            "moved or challenged or delighted by it. Creation is not solitary indulgence but "
            "a form of communication with the world."
        ),
        "threats": [
            "Arts education eliminated from schools as a 'non-essential' expense",
            "Economic precarity that leaves no time or energy for creative work",
            "Cultural industries that concentrate creative opportunity in elite institutions",
            "Digital platforms that reduce creators to content producers optimizing for engagement",
            "Lack of affordable studio, workshop, and performance spaces in communities",
            "The myth that creativity is a luxury rather than a fundamental human need"
        ],
        "de_risked_by": [
            "Universal arts education from early childhood through adulthood",
            "Public creative infrastructure: maker spaces, studios, community workshops",
            "Artist residencies and basic income experiments for creative workers",
            "Cultural policy that values creation over consumption",
            "Community-based arts organizations embedded in every neighborhood",
            "Technology democratization that puts creative tools in every hand"
        ]
    },
    {
        "id": "intellectual_growth",
        "name": "Intellectual Growth",
        "color": "#1A3D8B",
        "icon": "book-open",
        "layer": "aspiration",
        "description": (
            "The human mind is not a vessel to be filled but a fire to be kindled. "
            "Intellectual growth is the lifelong expansion of understanding — not merely "
            "the accumulation of facts or credentials, but the deepening capacity to think "
            "clearly, to question wisely, to synthesize across domains, and to hold complexity "
            "without collapsing into simplification. It is the domain where curiosity is honored "
            "as a virtue and ignorance is treated not as shame but as invitation."
        ),
        "flourishing_looks_like": (
            "A person flourishing intellectually reads — not because they must, but because "
            "the world is endlessly interesting and books are portals. They engage with ideas "
            "that challenge their assumptions. They can follow an argument, detect a fallacy, "
            "change their mind when evidence warrants it. They have access to education that "
            "is not merely vocational but genuinely liberating — exposure to history, philosophy, "
            "science, literature, mathematics, and the arts. They are part of communities of "
            "inquiry: book clubs, discussion groups, mentoring relationships, or simply "
            "friendships where ideas are exchanged with seriousness and delight. They understand "
            "that expertise is real but not infallible, that knowledge is provisional but not "
            "arbitrary. They continue to grow intellectually throughout their lives, not because "
            "the job market demands it but because understanding is itself a form of flourishing."
        ),
        "threats": [
            "Educational systems that prioritize compliance and credentialing over genuine learning",
            "Information ecosystems designed to manipulate rather than inform",
            "Economic pressure that reduces education to vocational training",
            "Anti-intellectual cultural currents that stigmatize curiosity and expertise",
            "Digital distraction that fragments attention and degrades deep thinking",
            "Knowledge gatekeeping that restricts access to ideas based on ability to pay"
        ],
        "de_risked_by": [
            "Public libraries as the cornerstone of intellectual infrastructure",
            "Education reform that centers inquiry, critical thinking, and wonder",
            "Open access to knowledge: free textbooks, open journals, public lectures",
            "Lifelong learning programs accessible to adults at every stage",
            "Media literacy education that equips people to navigate information environments",
            "Mentorship networks that connect learners with thinkers across generations"
        ]
    },
    {
        "id": "spiritual_depth",
        "name": "Spiritual Depth",
        "color": "#5A1A6B",
        "icon": "sparkles",
        "layer": "transcendence",
        "description": (
            "Spiritual depth is the dimension of human experience that reaches beyond the "
            "material and the measurable toward the numinous, the sacred, and the ultimately "
            "meaningful. It is not confined to religion, though religion is one of its vessels. "
            "It encompasses meditation, contemplation, awe before nature, the experience of "
            "transcendence in art or music, and the quiet conviction that existence itself "
            "is more than an accident to be endured."
        ),
        "flourishing_looks_like": (
            "A person flourishing in spiritual depth has a practice — formal or informal — "
            "that connects them to something larger than their individual concerns. This might "
            "be prayer, meditation, time in nature, artistic practice, philosophical reflection, "
            "or communal ritual. They experience moments of awe, gratitude, and wonder with "
            "some regularity. They have grappled with the great questions — Why are we here? "
            "What happens when we die? What do we owe each other? — not necessarily arriving "
            "at answers but developing the capacity to hold the questions with honesty and "
            "courage. They belong to communities where the inner life is valued, where silence "
            "is not awkward, where depth is not embarrassing. They have a relationship with "
            "mystery that is neither credulous nor dismissive. Suffering, when it comes, is "
            "met not with empty positivity but with frameworks of meaning that make endurance "
            "possible and even transformative."
        ),
        "threats": [
            "Hyper-materialist cultures that dismiss the inner life as irrelevant",
            "Religious institutions that weaponize spirituality for control and exclusion",
            "The acceleration of modern life that eliminates contemplative space",
            "Commodification of spiritual practices stripped of depth and context",
            "Loneliness epidemics that sever people from communal spiritual life",
            "Trauma that damages the capacity to trust existence as fundamentally good"
        ],
        "de_risked_by": [
            "Protected contemplative spaces — gardens, sanctuaries, quiet rooms — in every community",
            "Interfaith and secular spiritual programming accessible to all",
            "Education that includes philosophical and ethical inquiry from early ages",
            "Mental health care that integrates existential and spiritual dimensions",
            "Community rituals that mark transitions, losses, and celebrations",
            "Cultural respect for silence, stillness, and the unproductive"
        ]
    },
    {
        "id": "community_belonging",
        "name": "Community Belonging",
        "color": "#1A6B6B",
        "icon": "users",
        "layer": "foundation",
        "description": (
            "Human beings are irreducibly social. We are not monads who happen to live near "
            "each other but relational creatures whose very selfhood is constituted in "
            "connection with others. Community belonging is the experience of being known, "
            "valued, and needed by a group of people who share space, purpose, or identity. "
            "It is the antidote to the epidemic of loneliness that corrodes modern life as "
            "surely as any disease."
        ),
        "flourishing_looks_like": (
            "A person flourishing in community belonging knows their neighbors. Not all of "
            "them, but enough that the street or the building feels like a place, not just a "
            "location. They participate in something communal — a congregation, a sports league, "
            "a mutual aid network, a garden, a volunteer corps, a neighborhood association. "
            "They are missed when they are absent. They have people they can call at 2 AM — not "
            "many, but more than zero. They contribute to the wellbeing of others in ways that "
            "feel meaningful rather than obligatory. They experience the particular joy of "
            "collective endeavor: the potluck, the barn-raising, the neighborhood cleanup, "
            "the shared celebration. They are not identical to their community; they have "
            "privacy, autonomy, and the right to dissent. But they are not alone. The fabric "
            "of social connection is strong enough to hold them when they stumble and flexible "
            "enough to let them grow."
        ),
        "threats": [
            "Suburban sprawl and car-dependent design that isolate people in private boxes",
            "Social media that simulates connection while deepening loneliness",
            "Economic mobility that uproots people from established communities",
            "Institutional distrust that erodes the willingness to join and participate",
            "Overwork culture that leaves no time for civic and communal life",
            "Segregation by race, class, and ideology that fragments the commons"
        ],
        "de_risked_by": [
            "Third places — cafes, parks, libraries, plazas — where people gather without paying",
            "Community organizing infrastructure that builds power from the ground up",
            "Urban design that prioritizes walkability, density, and shared spaces",
            "Mutual aid networks that formalize neighborly interdependence",
            "Civic education that cultivates the skills and habits of democratic life",
            "Intergenerational programming that connects elders and young people"
        ]
    },
    {
        "id": "environmental_harmony",
        "name": "Environmental Harmony",
        "color": "#2D5A1A",
        "icon": "leaf",
        "layer": "foundation",
        "description": (
            "We do not live on the earth; we live in it. The air we breathe, the water we "
            "drink, the soil that grows our food, the climate that governs the seasons — these "
            "are not external resources to be managed but the living body of the world of which "
            "we are part. Environmental harmony is the recognition that human flourishing is "
            "impossible on a dying planet, and that our relationship with the natural world "
            "is not merely instrumental but constitutive of who we are."
        ),
        "flourishing_looks_like": (
            "A person flourishing in environmental harmony lives in a place where the air is "
            "clean, the water is safe, and green spaces are abundant and accessible. They have "
            "a relationship with the natural world that goes beyond tourism — they know the "
            "names of local trees, the patterns of local weather, the rhythms of the seasons. "
            "They eat food whose origin they can trace. Their home is energy-efficient and "
            "comfortable without being wasteful. They participate in the stewardship of their "
            "local environment — tending a garden, cleaning a waterway, protecting a habitat. "
            "They understand that their individual choices matter but that systemic change "
            "matters more. They live in a society that has organized itself around sustainability "
            "rather than extraction, that treats the natural world as a partner rather than "
            "a commodity. Their children will inherit an earth that is at least as beautiful "
            "and life-giving as the one they were born into."
        ),
        "threats": [
            "Climate change accelerating beyond the capacity of communities to adapt",
            "Pollution concentrated in marginalized communities through environmental racism",
            "Biodiversity collapse that degrades the ecosystems on which all life depends",
            "Disconnection from nature that produces ecological illiteracy and apathy",
            "Extractive economic models that treat the earth as an infinite resource",
            "Urban heat islands and concrete deserts that sever people from the living world"
        ],
        "de_risked_by": [
            "Green infrastructure in every neighborhood: parks, trees, gardens, waterways",
            "Environmental justice frameworks that protect the most vulnerable communities",
            "Regenerative agriculture and local food systems that heal the soil",
            "Renewable energy transition that is rapid, equitable, and community-owned",
            "Environmental education that cultivates ecological literacy from childhood",
            "Urban design that integrates nature into the built environment"
        ]
    },
    {
        "id": "physical_space_beauty",
        "name": "Physical Space & Beauty",
        "color": "#8B6B1A",
        "icon": "building",
        "layer": "aspiration",
        "description": (
            "The spaces we inhabit shape who we become. A child who grows up surrounded by "
            "beauty — by thoughtful architecture, by well-maintained public spaces, by art "
            "on the walls and flowers in the yard — develops a different relationship to the "
            "world than one raised amid ugliness and neglect. Physical space is not merely "
            "functional shelter; it is the material expression of how seriously a society "
            "takes the dignity and delight of its people."
        ),
        "flourishing_looks_like": (
            "A person flourishing in physical space and beauty lives in a home that is safe, "
            "warm, dry, and beautiful in its own way — not opulent, but cared for. They walk "
            "through streets that are maintained with attention, past buildings that were designed "
            "with craft, through public spaces that invite lingering. There is art in their daily "
            "environment — murals, sculptures, thoughtful signage, well-designed objects. Public "
            "buildings — schools, libraries, transit stations, government offices — communicate "
            "through their design that the people who use them matter. The built environment is "
            "accessible to people of all abilities. There are places of grandeur — a great public "
            "building, a magnificent park, a soaring bridge — that remind people they belong to "
            "something larger than themselves. Beauty is not reserved for the wealthy; it is "
            "woven into the fabric of everyday life as a public good."
        ),
        "threats": [
            "Decades of disinvestment that leave public infrastructure crumbling and ugly",
            "Housing policy that prioritizes units over quality of life",
            "Car-centric planning that produces landscapes hostile to human presence",
            "The elimination of craft and beauty from public buildings through cost-cutting",
            "Homelessness and housing instability that deny people any space of their own",
            "Aesthetic inequality where beauty is abundant in wealthy areas and absent elsewhere"
        ],
        "de_risked_by": [
            "Public architecture that treats beauty as a requirement, not a luxury",
            "Housing policy that includes design standards for dignity and delight",
            "Public art programs integrated into every infrastructure project",
            "Universal design principles that make spaces accessible to all bodies",
            "Community land trusts that preserve affordable, beautiful neighborhoods",
            "Urban planning that creates human-scale streets, plazas, and gathering spaces"
        ]
    },
    {
        "id": "love_relationships",
        "name": "Love & Relationships",
        "color": "#8B1A1A",
        "icon": "heart",
        "layer": "transcendence",
        "description": (
            "At the deepest level, human flourishing is inseparable from love. Not romantic "
            "love alone, but the full spectrum of human attachment: the love of parents for "
            "children, of friends for each other, of partners in life, of mentors and mentees, "
            "of neighbors who watch out for one another. Love is not a feeling; it is a practice, "
            "a commitment, a way of being present to another person that says: you matter, you "
            "are not alone, I see you."
        ),
        "flourishing_looks_like": (
            "A person flourishing in love and relationships has at least a few people in their "
            "life who know them deeply — who know their history, their fears, their humor, "
            "their contradictions. They have experienced being chosen: someone has said, in "
            "effect, 'Of all the people in the world, I choose to be in your life.' They know "
            "how to repair a relationship after conflict, to apologize genuinely, to forgive "
            "without pretending. If they are parents, they have sufficient support to be "
            "present and patient with their children. If they are children, they have at least "
            "one adult who is unconditionally committed to their wellbeing. They have experienced "
            "the reciprocity of care: being held when they are broken, and holding someone else. "
            "They are not trapped in relationships that diminish them, and they are not so isolated "
            "that they go weeks without meaningful human contact. Love, in all its forms, is the "
            "thread that weaves individual flourishing into collective flourishing."
        ),
        "threats": [
            "Loneliness epidemic driven by social fragmentation and geographic isolation",
            "Domestic violence and intimate partner abuse that corrupt love into control",
            "Overwork culture that starves relationships of the time they require",
            "Mass incarceration that rips families apart across generations",
            "Social media replacing deep connection with performative interaction",
            "Untreated trauma that makes attachment feel dangerous rather than safe"
        ],
        "de_risked_by": [
            "Family support infrastructure: parental leave, childcare, family counseling",
            "Community spaces designed to facilitate genuine human connection",
            "Mental health services that address attachment wounds and relational trauma",
            "Criminal justice reform that preserves family bonds wherever possible",
            "Elder care systems that treat aging as a communal rather than private burden",
            "Conflict resolution education integrated into schools and communities"
        ]
    },
    {
        "id": "purpose_meaning",
        "name": "Purpose & Meaning",
        "color": "#3D1A8B",
        "icon": "compass",
        "layer": "transcendence",
        "description": (
            "Viktor Frankl observed that a person can endure almost any how if they have a "
            "why. Purpose and meaning are not luxuries of the comfortable; they are survival "
            "necessities of the human soul. This domain encompasses the experience of one's "
            "life as coherent, directed, and significant — the sense that one's existence makes "
            "a difference, that one's work matters, that one's suffering is not pointless."
        ),
        "flourishing_looks_like": (
            "A person flourishing in purpose and meaning can articulate — however imperfectly — "
            "what they are living for. This need not be grandiose; it might be raising their "
            "children well, mastering a craft, serving their community, pursuing a question, "
            "or simply being a good friend. They experience their daily activities as connected "
            "to something larger than mere survival or consumption. Their work, whether paid or "
            "unpaid, engages their capacities and contributes to something they value. They can "
            "make sense of their past — including its suffering — as part of a coherent narrative. "
            "They are oriented toward the future with some combination of hope and intention. "
            "They have encountered role models, mentors, or traditions that helped them develop "
            "their sense of purpose. They do not feel interchangeable, disposable, or irrelevant. "
            "They know — in their bones, not just their intellect — that they matter."
        ),
        "threats": [
            "Meaningless work that reduces human beings to interchangeable labor units",
            "Consumerism as a substitute for genuine purpose and fulfillment",
            "Loss of traditional meaning-making structures without adequate replacements",
            "Nihilistic cultural currents that frame purpose as naive self-deception",
            "Retirement and aging without frameworks for continued contribution",
            "Youth disconnection from mentorship, tradition, and intergenerational wisdom"
        ],
        "de_risked_by": [
            "Work redesign that gives people autonomy, mastery, and purpose in their labor",
            "National service and volunteer infrastructure that channels energy into meaning",
            "Mentorship programs that connect seekers with those who have found their way",
            "Philosophical and ethical education accessible across the lifespan",
            "Community institutions that honor every person's capacity to contribute",
            "Narrative therapy and meaning-making support integrated into mental health care"
        ]
    },
    {
        "id": "play_joy",
        "name": "Play & Joy",
        "color": "#1A8B3D",
        "icon": "sun",
        "layer": "aspiration",
        "description": (
            "Play is not the opposite of seriousness; it is the opposite of depression. "
            "Joy is not the absence of suffering; it is the presence of vitality even in "
            "the midst of difficulty. This domain honors the truth that human beings need "
            "delight, laughter, games, festivals, celebrations, silliness, adventure, and "
            "the pure unproductive pleasure of being alive. A society that has no room for "
            "play has no room for the human spirit."
        ),
        "flourishing_looks_like": (
            "A person flourishing in play and joy laughs regularly — not politely, but "
            "from the belly. They have hobbies that serve no purpose other than delight. "
            "They play — sports, games, music, make-believe with children, improvisational "
            "cooking, dancing in the kitchen. They celebrate: birthdays, holidays, seasons, "
            "achievements, survivals. They have access to recreation that does not require "
            "wealth: public parks, swimming pools, playgrounds, sports fields, hiking trails. "
            "They experience spontaneity — days that unfold without a schedule, conversations "
            "that go nowhere important, afternoons wasted gloriously. Their culture values "
            "leisure not as laziness but as a fundamental human right. They know the difference "
            "between entertainment (which is consumed) and play (which is created), and they "
            "have ample access to both. Joy is not a reward for productivity; it is a birthright."
        ),
        "threats": [
            "Hustle culture that stigmatizes rest and play as laziness or weakness",
            "Commercialization of leisure that turns play into consumption",
            "Elimination of recess, free play, and unstructured time from childhood",
            "Economic precarity that leaves no margin for recreation or adventure",
            "Screen-based entertainment replacing embodied, social, creative play",
            "Public recreation infrastructure underfunded and allowed to decay"
        ],
        "de_risked_by": [
            "Public recreation infrastructure: parks, pools, playgrounds, courts, trails",
            "Shorter work weeks that create genuine leisure time for all workers",
            "Free public festivals, concerts, and cultural events in every community",
            "Protected unstructured play time in schools and early childhood settings",
            "Intergenerational play spaces and programming",
            "Cultural narratives that honor rest, celebration, and the unproductive"
        ]
    },
    {
        "id": "legacy_contribution",
        "name": "Legacy & Contribution",
        "color": "#6B3D1A",
        "icon": "trophy",
        "layer": "transcendence",
        "description": (
            "Every human life, however modest, leaves a mark on the world. Legacy and "
            "contribution is the domain where a person reckons with the question: What will "
            "I leave behind? Not in the grandiose sense of monuments and endowments, but in "
            "the intimate sense of influence, teaching, creation, and care. It is the domain "
            "of generativity — Erik Erikson's term for the deep human need to nurture and "
            "guide the next generation."
        ),
        "flourishing_looks_like": (
            "A person flourishing in legacy and contribution knows that their life has "
            "mattered to someone beyond themselves. They have taught something — a skill, "
            "a recipe, a way of seeing the world — to someone younger. They have contributed "
            "to institutions or communities that will outlast them: planted a tree, built an "
            "organization, written something down, created a tradition. They have prepared "
            "for the end of their life not with denial but with intentionality: their affairs "
            "are in order, their wishes are known, their stories have been told. They have "
            "experienced the particular satisfaction of generosity — of giving time, money, "
            "knowledge, or care without expectation of return. They understand that legacy is "
            "not fame; it is the ripple effect of a life lived with integrity and love. The "
            "grandmother who taught her grandchild to garden, the teacher who changed a life "
            "with a single sentence, the neighbor who organized the block — these are the "
            "architects of legacy, and their contributions echo through time."
        ),
        "threats": [
            "Individualism that frames legacy as personal achievement rather than collective contribution",
            "Economic insecurity that makes generosity feel impossible",
            "Ageism that discards elders rather than honoring their accumulated wisdom",
            "Loss of oral tradition and intergenerational storytelling",
            "Institutional instability that makes long-term investment feel futile",
            "Death-denying culture that prevents people from planning meaningful endings"
        ],
        "de_risked_by": [
            "Mentorship infrastructure that connects elders with youth in every community",
            "Community foundations that channel local generosity into lasting impact",
            "Oral history and storytelling programs that preserve lived wisdom",
            "Estate planning and end-of-life support accessible to all, not just the wealthy",
            "Volunteer and service programs designed for people at every life stage",
            "Cultural celebration of ordinary contributions alongside extraordinary ones"
        ]
    }
]


DOMAIN_RESOURCES: dict[str, list[dict[str, Any]]] = {
    "health_vitality": [
        {"name": "Community Health Centers", "type": "public", "description": "Federally qualified health centers providing primary care regardless of ability to pay, serving as the first line of defense against health inequity.", "coverage": 62},
        {"name": "Public Water & Sanitation", "type": "public", "description": "Municipal water treatment and distribution systems that provide safe drinking water — the single most important public health intervention in human history.", "coverage": 94},
        {"name": "Mutual Aid Health Networks", "type": "communal", "description": "Community-organized networks for sharing health knowledge, providing meals during illness, accompanying people to appointments, and filling gaps the system ignores.", "coverage": 28},
        {"name": "Community Gardens & Food Co-ops", "type": "communal", "description": "Collectively managed food production and distribution that provides fresh produce while building community and food sovereignty.", "coverage": 18},
        {"name": "Health Insurance", "type": "private", "description": "Private health coverage that, despite its limitations, provides access to specialist care, prescription drugs, and emergency treatment.", "coverage": 72},
        {"name": "Personal Health Knowledge", "type": "personal", "description": "An individual's understanding of their own body, family health history, nutritional needs, and capacity for self-care and prevention.", "coverage": 45},
        {"name": "Clean Air & Green Space", "type": "natural", "description": "Access to uncontaminated air and natural environments that reduce stress, improve respiratory health, and restore mental wellbeing.", "coverage": 55},
        {"name": "Medicinal Plants & Traditional Knowledge", "type": "natural", "description": "The vast pharmacopoeia of the natural world and the indigenous knowledge systems that have catalogued healing plants for millennia.", "coverage": 12}
    ],
    "economic_prosperity": [
        {"name": "Public Banking & Credit Unions", "type": "public", "description": "Community-owned financial institutions that recirculate deposits locally rather than extracting wealth to distant shareholders.", "coverage": 22},
        {"name": "Social Security & Safety Net", "type": "public", "description": "The foundational public commitment that no one will fall into absolute destitution — however imperfectly realized in practice.", "coverage": 68},
        {"name": "Cooperative Enterprises", "type": "communal", "description": "Worker-owned and community-owned businesses that distribute profits to those who create value rather than concentrating them among investors.", "coverage": 8},
        {"name": "Mutual Aid Funds", "type": "communal", "description": "Community lending circles, emergency funds, and collective savings pools that provide financial resilience outside institutional systems.", "coverage": 15},
        {"name": "Personal Savings & Assets", "type": "private", "description": "Individual and family wealth — savings accounts, home equity, retirement funds — that provides a buffer against economic shocks.", "coverage": 42},
        {"name": "Employer Benefits", "type": "private", "description": "Health insurance, retirement matching, paid leave, and other benefits provided through employment — the primary channel of economic security in American life.", "coverage": 52},
        {"name": "Financial Literacy", "type": "personal", "description": "The knowledge and skills to manage money, understand debt, invest wisely, and navigate financial systems without being exploited.", "coverage": 34},
        {"name": "Natural Resource Commons", "type": "natural", "description": "Shared access to fisheries, forests, waterways, and land that provides subsistence and livelihood outside the cash economy.", "coverage": 16}
    ],
    "creative_expression": [
        {"name": "Public Arts Funding", "type": "public", "description": "Government investment in the arts through grants, public art commissions, and support for cultural institutions — treating creativity as essential infrastructure.", "coverage": 18},
        {"name": "Public Libraries & Media Labs", "type": "public", "description": "Free access to books, computers, recording equipment, 3D printers, and creative tools through the most democratic institution in civic life.", "coverage": 72},
        {"name": "Community Arts Organizations", "type": "communal", "description": "Local theater companies, music collectives, art cooperatives, and cultural centers that make creation accessible outside elite institutions.", "coverage": 32},
        {"name": "Maker Spaces & Workshops", "type": "communal", "description": "Shared facilities with tools and equipment for woodworking, metalwork, electronics, textiles, and digital fabrication.", "coverage": 14},
        {"name": "Personal Creative Tools", "type": "private", "description": "Individual access to instruments, art supplies, cameras, software, and other tools of creative production.", "coverage": 48},
        {"name": "Digital Platforms", "type": "private", "description": "Online marketplaces and distribution channels that allow creators to share work and earn income from a global audience.", "coverage": 56},
        {"name": "Innate Creativity", "type": "personal", "description": "The fundamental human capacity for imagination, improvisation, and aesthetic expression that exists in every person from birth.", "coverage": 100},
        {"name": "Natural Beauty & Inspiration", "type": "natural", "description": "Landscapes, seasons, organisms, and natural phenomena that have inspired human creativity since the first cave paintings.", "coverage": 65}
    ],
    "intellectual_growth": [
        {"name": "Public Education System", "type": "public", "description": "Universal free education from kindergarten through high school — the most ambitious intellectual infrastructure project in human history, despite its imperfections.", "coverage": 88},
        {"name": "Public Libraries", "type": "public", "description": "Free lending libraries that embody the radical proposition that knowledge should be available to everyone, not just those who can afford to buy it.", "coverage": 72},
        {"name": "Study Groups & Book Clubs", "type": "communal", "description": "Self-organized learning communities where people read, discuss, and think together — the oldest form of intellectual infrastructure.", "coverage": 22},
        {"name": "Community Colleges & Adult Ed", "type": "communal", "description": "Accessible institutions of higher learning that serve working adults, career changers, and lifelong learners.", "coverage": 45},
        {"name": "Personal Book Collections", "type": "private", "description": "Individual libraries — physical or digital — that reflect a person's intellectual journey and provide constant access to ideas.", "coverage": 58},
        {"name": "Online Learning Platforms", "type": "private", "description": "Digital courses, lectures, and tutorials that democratize access to knowledge from world-class institutions and thinkers.", "coverage": 42},
        {"name": "Curiosity & Critical Thinking", "type": "personal", "description": "The innate human drive to understand, question, and make sense of the world — the engine of all intellectual growth.", "coverage": 100},
        {"name": "The Observable World", "type": "natural", "description": "The universe itself as a source of wonder and inquiry — from the behavior of insects to the structure of galaxies.", "coverage": 100}
    ],
    "spiritual_depth": [
        {"name": "Houses of Worship", "type": "public", "description": "Churches, mosques, synagogues, temples, and other sacred spaces that provide communal spiritual practice, pastoral care, and contemplative refuge.", "coverage": 58},
        {"name": "Public Parks & Natural Sanctuaries", "type": "public", "description": "Protected natural spaces that provide encounters with beauty, silence, and scale that many people experience as spiritual.", "coverage": 52},
        {"name": "Meditation & Contemplative Groups", "type": "communal", "description": "Sitting groups, retreats, and contemplative communities that support regular spiritual practice outside institutional religion.", "coverage": 16},
        {"name": "Interfaith Organizations", "type": "communal", "description": "Communities that bridge religious and spiritual traditions, fostering dialogue and mutual understanding across difference.", "coverage": 12},
        {"name": "Personal Spiritual Practice", "type": "personal", "description": "An individual's own practice of prayer, meditation, journaling, contemplation, or whatever discipline sustains their inner life.", "coverage": 38},
        {"name": "Spiritual Direction & Counseling", "type": "private", "description": "One-on-one guidance from trained spiritual directors, chaplains, or counselors who help people navigate existential questions.", "coverage": 8},
        {"name": "Sacred Texts & Wisdom Literature", "type": "private", "description": "The accumulated spiritual wisdom of humanity — scriptures, poetry, philosophy, mystical writings — available to anyone who seeks them.", "coverage": 62},
        {"name": "Silence & Solitude", "type": "natural", "description": "The natural conditions of quiet and aloneness that allow the inner life to surface — increasingly rare and increasingly precious.", "coverage": 32}
    ],
    "community_belonging": [
        {"name": "Public Spaces & Parks", "type": "public", "description": "Plazas, parks, recreation centers, and public squares designed to bring people together across lines of difference.", "coverage": 62},
        {"name": "Public Transit", "type": "public", "description": "Shared transportation systems that create encounters between strangers and connect neighborhoods to each other and to opportunity.", "coverage": 38},
        {"name": "Neighborhood Associations", "type": "communal", "description": "Block clubs, civic associations, and neighborhood councils that give residents a voice in shaping their shared environment.", "coverage": 28},
        {"name": "Mutual Aid Networks", "type": "communal", "description": "Informal and formal networks of reciprocal care — meal trains, tool libraries, babysitting cooperatives, emergency funds.", "coverage": 22},
        {"name": "Social Clubs & Organizations", "type": "private", "description": "Voluntary associations — sports leagues, hobby groups, professional organizations — that create bonds of shared interest.", "coverage": 42},
        {"name": "Digital Community Platforms", "type": "private", "description": "Online spaces — neighborhood apps, interest forums, social media groups — that extend community beyond physical proximity.", "coverage": 55},
        {"name": "Social Skills & Emotional Intelligence", "type": "personal", "description": "The personal capacity for empathy, communication, conflict resolution, and genuine presence with others.", "coverage": 48},
        {"name": "Shared Geography & Place", "type": "natural", "description": "The land, waterways, and ecosystems that define a community's physical context and create shared relationship with place.", "coverage": 75}
    ],
    "environmental_harmony": [
        {"name": "EPA & Environmental Regulation", "type": "public", "description": "Federal and state environmental protections that set minimum standards for air quality, water safety, and toxic waste management.", "coverage": 58},
        {"name": "National & State Parks", "type": "public", "description": "Protected natural areas that preserve ecosystems, provide recreation, and maintain the wild spaces that sustain biological and spiritual health.", "coverage": 42},
        {"name": "Community Gardens", "type": "communal", "description": "Shared growing spaces that reconnect urban dwellers with the soil, produce fresh food, and build community around ecological stewardship.", "coverage": 14},
        {"name": "Watershed Associations", "type": "communal", "description": "Community organizations that monitor, protect, and restore local waterways — the circulatory system of the landscape.", "coverage": 18},
        {"name": "Home Energy Efficiency", "type": "private", "description": "Individual investments in insulation, solar panels, efficient appliances, and sustainable home systems.", "coverage": 32},
        {"name": "Personal Environmental Practice", "type": "personal", "description": "Individual habits of conservation, recycling, composting, and consumption reduction that reduce ecological footprint.", "coverage": 38},
        {"name": "Ecological Literacy", "type": "personal", "description": "Understanding of ecological systems, food webs, nutrient cycles, and the interdependence of all living things.", "coverage": 22},
        {"name": "Intact Ecosystems", "type": "natural", "description": "Functioning forests, wetlands, prairies, and marine systems that provide clean air, water filtration, pollination, and climate regulation.", "coverage": 48}
    ],
    "physical_space_beauty": [
        {"name": "Zoning & Urban Planning", "type": "public", "description": "Public governance of land use that shapes whether communities are walkable or car-dependent, mixed or segregated, humane or hostile.", "coverage": 55},
        {"name": "Public Architecture", "type": "public", "description": "Government buildings, schools, libraries, and transit stations designed with beauty and dignity rather than mere cost efficiency.", "coverage": 35},
        {"name": "Community Land Trusts", "type": "communal", "description": "Non-profit organizations that hold land in trust for community benefit, preserving affordable housing and preventing displacement.", "coverage": 6},
        {"name": "Community Design Initiatives", "type": "communal", "description": "Participatory design processes that involve residents in shaping their built environment rather than having it imposed from above.", "coverage": 12},
        {"name": "Home Ownership & Improvement", "type": "private", "description": "Individual investment in creating beautiful, comfortable, personalized living spaces.", "coverage": 42},
        {"name": "Private Development", "type": "private", "description": "Commercial real estate development that, at its best, creates well-designed mixed-use neighborhoods and at its worst, produces soulless sprawl.", "coverage": 65},
        {"name": "Aesthetic Sensibility", "type": "personal", "description": "An individual's cultivated capacity to perceive, appreciate, and create beauty in their environment.", "coverage": 55},
        {"name": "Natural Landscape", "type": "natural", "description": "The topography, vegetation, water features, and geological character that give each place its unique beauty and identity.", "coverage": 68}
    ],
    "love_relationships": [
        {"name": "Family Court & Legal Protections", "type": "public", "description": "Legal frameworks that protect children, define parental rights, enable adoption, and provide recourse against domestic violence.", "coverage": 52},
        {"name": "Marriage & Family Policy", "type": "public", "description": "Public policies — parental leave, child tax credits, marriage recognition — that support the formation and stability of families.", "coverage": 38},
        {"name": "Faith Communities", "type": "communal", "description": "Religious congregations that provide pastoral counseling, marriage preparation, grief support, and the rituals that mark love's milestones.", "coverage": 42},
        {"name": "Support Groups", "type": "communal", "description": "Peer-led groups for people navigating relationship challenges: divorce, grief, parenting difficulties, addiction recovery.", "coverage": 28},
        {"name": "Therapy & Counseling", "type": "private", "description": "Professional support for individuals and couples working through attachment wounds, communication breakdowns, and relational trauma.", "coverage": 22},
        {"name": "Capacity for Attachment", "type": "personal", "description": "The deep human capacity for bonding, trust, vulnerability, and committed love — shaped by early experience but never fully determined by it.", "coverage": 85},
        {"name": "Communication Skills", "type": "personal", "description": "The ability to express needs, listen deeply, manage conflict, apologize, and forgive — the operational infrastructure of love.", "coverage": 42},
        {"name": "Time Together", "type": "natural", "description": "The irreducible requirement of all relationships: unhurried time in each other's presence, which no technology can substitute.", "coverage": 35}
    ],
    "purpose_meaning": [
        {"name": "Public Service Infrastructure", "type": "public", "description": "National service programs, volunteer corps, and civic institutions that channel individual energy into collective purpose.", "coverage": 18},
        {"name": "Public Education & Philosophy", "type": "public", "description": "Schools and universities that don't merely train workers but help people develop frameworks for understanding what makes a life meaningful.", "coverage": 28},
        {"name": "Religious & Spiritual Communities", "type": "communal", "description": "Congregations and spiritual groups that provide ready-made meaning frameworks and communities of shared purpose.", "coverage": 42},
        {"name": "Mentorship Networks", "type": "communal", "description": "Formal and informal relationships between experienced and emerging individuals that transmit wisdom about purposeful living.", "coverage": 22},
        {"name": "Career Counseling & Coaching", "type": "private", "description": "Professional guidance for aligning work with values, strengths, and sense of calling.", "coverage": 15},
        {"name": "Journaling & Reflection Practice", "type": "personal", "description": "Individual practices of self-examination — journaling, meditation, therapy — that help a person discern their own sense of purpose.", "coverage": 25},
        {"name": "Sense of Agency", "type": "personal", "description": "The felt conviction that one's choices matter and one's actions make a difference — the psychological foundation of purposeful living.", "coverage": 55},
        {"name": "Encounters with Need", "type": "natural", "description": "The organic discovery of purpose through encountering others' suffering and recognizing one's capacity to help.", "coverage": 72}
    ],
    "play_joy": [
        {"name": "Public Recreation Facilities", "type": "public", "description": "Municipal pools, sports fields, playgrounds, skating rinks, and recreation centers that provide free or low-cost access to play.", "coverage": 52},
        {"name": "Public Festivals & Events", "type": "public", "description": "City-sponsored celebrations, parades, fireworks, concerts in the park, and cultural festivals that create collective joy.", "coverage": 45},
        {"name": "Sports Leagues & Clubs", "type": "communal", "description": "Community-organized athletics — little leagues, adult softball, pickup basketball, running clubs — that combine movement with belonging.", "coverage": 38},
        {"name": "Game Nights & Social Gatherings", "type": "communal", "description": "Informal gatherings organized around the sheer pleasure of being together: potlucks, game nights, bonfires, block parties.", "coverage": 42},
        {"name": "Entertainment & Media", "type": "private", "description": "Access to movies, music, games, books, and streaming services that provide enjoyment and shared cultural experience.", "coverage": 72},
        {"name": "Hobbies & Pastimes", "type": "private", "description": "Individual pursuits of pleasure — gardening, fishing, crafting, gaming, cooking, collecting — that serve no purpose other than delight.", "coverage": 58},
        {"name": "Capacity for Joy", "type": "personal", "description": "The innate human ability to experience delight, wonder, humor, and spontaneous happiness — present in every child and recoverable in every adult.", "coverage": 92},
        {"name": "Natural Play Environments", "type": "natural", "description": "Rivers to swim in, trees to climb, hills to sled down, fields to run through — the original playgrounds that no designer can improve upon.", "coverage": 45}
    ],
    "legacy_contribution": [
        {"name": "Estate & Inheritance Law", "type": "public", "description": "Legal frameworks that enable the orderly transfer of assets, wishes, and responsibilities across generations.", "coverage": 48},
        {"name": "Public Archives & History", "type": "public", "description": "Libraries, museums, and archives that preserve collective memory and ensure that ordinary lives are not erased from the record.", "coverage": 35},
        {"name": "Community Foundations", "type": "communal", "description": "Local philanthropic organizations that pool resources for lasting community impact, enabling even modest givers to create enduring change.", "coverage": 22},
        {"name": "Oral History & Storytelling", "type": "communal", "description": "Community practices of recording and sharing life stories, ensuring that hard-won wisdom is transmitted to future generations.", "coverage": 18},
        {"name": "Wills, Trusts & Estate Planning", "type": "private", "description": "Individual legal instruments for directing assets and wishes beyond one's lifetime.", "coverage": 32},
        {"name": "Charitable Giving", "type": "private", "description": "Individual philanthropy — from tithing to major donations — that extends a person's impact beyond their own direct reach.", "coverage": 42},
        {"name": "Generative Drive", "type": "personal", "description": "The deep human impulse to nurture, teach, build, and create things that will outlast oneself — what Erikson called generativity.", "coverage": 78},
        {"name": "Ecosystems & Seeds", "type": "natural", "description": "The natural model of legacy: every tree drops seeds, every organism feeds the next generation, every ecosystem is an inheritance.", "coverage": 88}
    ]
}
