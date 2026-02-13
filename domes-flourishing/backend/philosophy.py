"""
philosophy.py — The Philosophical Foundations of the Dome

The Dome draws from humanity's deepest wells of wisdom. No single tradition
holds the complete architecture of flourishing. Each offers a lens, a language,
a set of commitments. Together they form a composite vision — what we call
"The Cathedral of Becoming" — that honors the full complexity of human existence.

These are not decorative references. They are load-bearing structures. Every design
decision in the Dome can be traced back to one or more of these traditions.
"""

from typing import Any


PHILOSOPHICAL_TRADITIONS: list[dict[str, Any]] = [
    {
        "id": "eudaimonia",
        "name": "Eudaimonia",
        "tradition": "Ancient Greek",
        "thinker": "Aristotle",
        "era": "384-322 BCE",
        "core_idea": (
            "Eudaimonia — often mistranslated as 'happiness' — is better understood as "
            "'the condition of flourishing in accordance with one's highest nature.' For Aristotle, "
            "the good life is not a feeling but an activity: the sustained exercise of virtue "
            "in a complete life. Flourishing requires not just good intentions but good habits, "
            "not just private virtue but civic participation, not just momentary pleasure but "
            "the deep satisfaction of living well over time."
        ),
        "key_concepts": [
            "Arete (excellence/virtue) — the cultivation of character through habitual practice",
            "Phronesis (practical wisdom) — the ability to discern the right action in particular circumstances",
            "Ergon (function) — the idea that humans have a characteristic activity: rational, social, creative life",
            "The Golden Mean — flourishing found between extremes of excess and deficiency",
            "Eudaimonia as activity — not a state to be achieved but a way of living to be practiced daily",
            "The Polis — the recognition that individual flourishing requires a just political community"
        ],
        "implications_for_dome": (
            "From Aristotle we take the conviction that flourishing is not subjective wellbeing "
            "but objective human functioning. The Dome must support not just what people want but "
            "what people need to exercise their highest capacities. It must cultivate virtue — not "
            "through coercion but through environments, institutions, and habits that make excellence "
            "possible. And it must be political: individual flourishing is inseparable from the "
            "justice and beauty of the shared world."
        ),
        "quote": "Happiness is the meaning and the purpose of life, the whole aim and end of human existence."
    },
    {
        "id": "capability_approach",
        "name": "Capability Approach",
        "tradition": "Development Economics",
        "thinker": "Amartya Sen & Martha Nussbaum",
        "era": "1980s-present",
        "core_idea": (
            "The Capability Approach rejects both GDP and subjective happiness as measures of "
            "human development. Instead, it asks: What are people actually able to do and to be? "
            "A person's wellbeing is measured not by their income or their reported satisfaction "
            "but by their real freedoms — their capabilities. Sen and Nussbaum argue that justice "
            "requires ensuring every person has a threshold level of central capabilities: life, "
            "health, bodily integrity, imagination, emotion, practical reason, affiliation, play, "
            "control over one's environment, and relationship with other species."
        ),
        "key_concepts": [
            "Capabilities vs. Functionings — what a person is able to do vs. what they actually choose to do",
            "Central Human Capabilities — the non-negotiable conditions for a dignified human life",
            "Threshold Justice — every person must reach a minimum level in each capability",
            "Agency Freedom — the importance of people choosing their own path, not having flourishing imposed",
            "Adaptive Preferences — the danger that oppressed people adjust their desires downward"
        ],
        "implications_for_dome": (
            "From Sen and Nussbaum we take the architecture of measurement. The Dome does not ask "
            "'Are you happy?' but 'What are you able to do and to be?' It defines flourishing in "
            "terms of real capabilities — not just resources provided but freedoms actually enjoyed. "
            "It insists on a threshold: there are minimums below which no person should fall, "
            "regardless of their choices or circumstances. And it respects agency: the Dome creates "
            "conditions for flourishing but does not dictate what flourishing looks like for any "
            "individual person."
        ),
        "quote": "What are people actually able to do and to be? What real opportunities are available to them?"
    },
    {
        "id": "ubuntu",
        "name": "Ubuntu",
        "tradition": "Southern African",
        "thinker": "Desmond Tutu",
        "era": "Ancient tradition, articulated globally 20th century",
        "core_idea": (
            "Ubuntu — 'I am because we are' — is the Southern African philosophical tradition "
            "that locates human identity not in the individual but in the web of relationships. "
            "A person is a person through other persons. This is not a mere observation about "
            "social dependence; it is an ontological claim about the nature of personhood itself. "
            "Archbishop Tutu expressed it thus: 'My humanity is caught up, is inextricably bound up, "
            "in yours.' Ubuntu insists that there is no flourishing in isolation — that what happens "
            "to my neighbor happens to me."
        ),
        "key_concepts": [
            "Umuntu ngumuntu ngabantu — 'A person is a person through other persons'",
            "Relational personhood — identity constituted through community rather than prior to it",
            "Shared humanity — the recognition that my flourishing is bound to yours",
            "Restorative justice — healing relationships rather than merely punishing individuals",
            "Communal responsibility — the wellbeing of each is the concern of all",
            "Hospitality as sacred duty — the stranger is never truly a stranger"
        ],
        "implications_for_dome": (
            "From Ubuntu we take the radical insistence that flourishing is never individual. "
            "The Dome is not a collection of personal optimization programs; it is a web of "
            "mutual care. When one person's dome is crumbling, all neighboring domes are weakened. "
            "When one community flourishes, it strengthens every community it touches. Ubuntu "
            "demands that the Dome be designed not for the autonomous individual but for the "
            "person-in-relationship — and that justice be understood as the restoration of "
            "right relationship rather than mere punishment or compensation."
        ),
        "quote": "My humanity is caught up, is inextricably bound up, in yours. I am because we are."
    },
    {
        "id": "interdependence",
        "name": "Interdependence",
        "tradition": "Buddhist",
        "thinker": "Thich Nhat Hanh",
        "era": "Ancient tradition, articulated for modern world 20th century",
        "core_idea": (
            "The Buddhist concept of pratityasamutpada — dependent origination or interbeing — "
            "teaches that nothing exists independently. Everything arises in relationship to "
            "everything else. Thich Nhat Hanh expressed this as 'interbeing': looking at a sheet "
            "of paper, you can see the cloud that rained on the tree, the logger who cut it, "
            "the sun that made it grow. Nothing exists as a separate self. This insight dissolves "
            "the boundary between self and world, between individual and collective, between "
            "human and nature."
        ),
        "key_concepts": [
            "Interbeing — the interpenetration of all phenomena; nothing exists independently",
            "Dependent Origination — all things arise in dependence upon multiple causes and conditions",
            "Mindfulness — the practice of present-moment awareness that reveals interconnection",
            "Compassion (Karuna) — the natural response to recognizing shared suffering",
            "Non-self (Anatta) — the insight that the autonomous, separate self is an illusion"
        ],
        "implications_for_dome": (
            "From Buddhist interdependence we take the systems perspective. The Dome cannot be "
            "designed domain by domain in isolation, because every domain interpenetrates every "
            "other. Health affects economic capacity. Economic stress degrades relationships. "
            "Relationships shape spiritual depth. Spiritual depth informs purpose. Purpose drives "
            "creative expression. The Dome must be understood as a living system, not a checklist. "
            "And mindfulness — the practice of seeing clearly what is actually happening — is "
            "the foundation of any honest assessment of flourishing."
        ),
        "quote": "You are not just a drop in the ocean. You are the entire ocean in a drop."
    },
    {
        "id": "cura_personalis",
        "name": "Cura Personalis",
        "tradition": "Jesuit Catholic",
        "thinker": "Ignatius of Loyola",
        "era": "1491-1556, tradition ongoing",
        "core_idea": (
            "Cura Personalis — 'care for the entire person' — is the Jesuit educational and "
            "pastoral principle that every individual must be encountered in their wholeness: "
            "body, mind, and spirit. It rejects the fragmentation that treats a person as a "
            "collection of problems to be solved by different specialists. Instead, it insists "
            "on attending to the unique, unrepeatable individual in all their dimensions — "
            "intellectual, emotional, physical, spiritual, and social — with the conviction "
            "that each person is created for a purpose that only they can fulfill."
        ),
        "key_concepts": [
            "Care for the whole person — body, mind, spirit attended to as an integrated unity",
            "Individual attention — each person's path is unique and requires particular accompaniment",
            "Magis — the 'more,' the restless pursuit of greater depth, service, and excellence",
            "Discernment — the disciplined process of discovering one's calling and purpose",
            "Contemplation in action — finding the sacred not in withdrawal but in engaged service",
            "The Examen — daily reflective practice of noticing where life is and is not flourishing"
        ],
        "implications_for_dome": (
            "From Cura Personalis we take the insistence on wholeness and individuality. The Dome "
            "must never reduce a person to their deficits or their demographics. Each person who "
            "enters the Dome is encountered as a complete human being with a unique history, unique "
            "gifts, and a unique calling. The twelve domains are not a checklist but a lens for "
            "seeing the whole person. And the Dome's ultimate purpose is not stability or comfort "
            "but the 'magis' — helping each person discover and pursue the fullest expression "
            "of their particular humanity."
        ),
        "quote": "Go forth and set the world on fire."
    },
    {
        "id": "relational_worldview",
        "name": "Relational Worldview",
        "tradition": "Indigenous",
        "thinker": "Robin Wall Kimmerer",
        "era": "Ancient traditions, articulated in contemporary voice",
        "core_idea": (
            "Indigenous relational worldviews, as articulated by Robin Wall Kimmerer and many "
            "others, understand the world not as a collection of objects to be used but as a "
            "community of subjects to be respected. Plants, animals, rivers, and mountains are "
            "not resources but relatives. The earth is not property but a gift that carries "
            "obligations of reciprocity. This worldview challenges the extractive logic that "
            "treats the natural world — and often human communities — as raw material for "
            "economic growth."
        ),
        "key_concepts": [
            "All beings as relatives — the natural world as a community of persons, not a collection of resources",
            "Reciprocity — the obligation to give back to the land and community that sustain you",
            "Gratitude as first response — beginning every interaction with thanksgiving rather than taking",
            "Seventh Generation thinking — making decisions with seven generations of consequences in mind",
            "The Honorable Harvest — taking only what is given, using it well, giving thanks, sharing",
            "Land as pedagogy — the earth itself as teacher, if we learn to listen"
        ],
        "implications_for_dome": (
            "From Indigenous relational worldview we take the principle that the Dome extends "
            "beyond the human. Environmental harmony is not one domain among twelve but the "
            "context in which all other domains exist. The Dome must be designed with seven "
            "generations in mind, not just the current user. It must be grounded in reciprocity — "
            "every person who benefits from the Dome also contributes to it. And it must honor "
            "the land: every Dome is situated in a particular place, and that place has its own "
            "gifts, needs, and teachings."
        ),
        "quote": "All flourishing is mutual. The land loves us back when we love the land."
    },
    {
        "id": "authentic_existence",
        "name": "Authentic Existence",
        "tradition": "Existentialism",
        "thinker": "Kierkegaard, Sartre & de Beauvoir",
        "era": "19th-20th century",
        "core_idea": (
            "Existentialism places radical freedom and responsibility at the center of human life. "
            "We are not born with a fixed essence; we create ourselves through our choices. "
            "Kierkegaard insisted that the individual must choose their own path against the crowd. "
            "Sartre declared that existence precedes essence — we are condemned to be free. "
            "De Beauvoir added the crucial insight that freedom is always situated: social "
            "structures constrain what choices are available, and genuine freedom requires "
            "dismantling the structures of oppression that limit who can choose."
        ),
        "key_concepts": [
            "Existence precedes essence — we are not born with a fixed nature but create ourselves through choices",
            "Radical freedom — even in constraint, the human being retains the freedom to choose their response",
            "Bad faith — the self-deception of denying one's freedom by hiding behind roles, rules, or excuses",
            "Situated freedom — genuine freedom requires material conditions and social structures that enable choice",
            "The Other — de Beauvoir's insight that oppression systematically denies freedom to entire groups",
            "Authenticity — the courage to face existence honestly and choose one's own path"
        ],
        "implications_for_dome": (
            "From Existentialism we take the principle of agency. The Dome does not flourish "
            "people; people flourish themselves, with the Dome providing the conditions that "
            "make genuine choice possible. The Dome must resist paternalism — the temptation "
            "to define flourishing for people rather than empowering them to define it for "
            "themselves. But it must also resist the libertarian fantasy that freedom exists "
            "without material conditions. De Beauvoir reminds us: you cannot tell a starving "
            "person they are free. The Dome creates the situated conditions in which authentic "
            "choice becomes possible."
        ),
        "quote": "Freedom is what we do with what is done to us."
    },
    {
        "id": "self_actualization",
        "name": "Self-Actualization",
        "tradition": "Humanistic Psychology",
        "thinker": "Abraham Maslow",
        "era": "1908-1970",
        "core_idea": (
            "Maslow's hierarchy of needs posits that human motivation proceeds in layers: "
            "physiological needs, safety, belonging, esteem, and finally self-actualization — "
            "the realization of one's full potential. While the rigid hierarchy has been "
            "critiqued (people pursue meaning even in dire circumstances), the core insight "
            "endures: when basic needs are met, human beings naturally reach toward growth, "
            "creativity, and transcendence. Self-actualized people, Maslow found, share "
            "characteristics: spontaneity, deep relationships, peak experiences, democratic "
            "values, creativity, and a philosophical sense of humor."
        ),
        "key_concepts": [
            "Hierarchy of Needs — physiological, safety, belonging, esteem, self-actualization",
            "Deficiency vs. Growth Motivation — moving from filling lacks to pursuing potential",
            "Peak Experiences — moments of transcendent joy, unity, and understanding",
            "Self-Actualization — becoming what one is capable of becoming",
            "B-Values (Being Values) — truth, goodness, beauty, justice, playfulness, self-sufficiency"
        ],
        "implications_for_dome": (
            "From Maslow we take the layered architecture. The Dome's three layers — Foundation, "
            "Aspiration, Transcendence — mirror the hierarchy of needs. Foundation domains "
            "(health, economic security, community, environment) must be secured before aspiration "
            "domains (creativity, intellect, beauty, play) can fully flower, and transcendence "
            "domains (spirituality, love, purpose, legacy) represent the highest expression of "
            "human possibility. But we also take Maslow's later correction: the hierarchy is not "
            "rigid. People pursue meaning, beauty, and love even in poverty. The layers are "
            "permeable, and the Dome must honor that permeability."
        ),
        "quote": "What a man can be, he must be. This need we call self-actualization."
    }
]


PHILOSOPHICAL_SYNTHESIS: dict[str, Any] = {
    "title": "The Cathedral of Becoming",
    "thesis": (
        "The Dome is not a social program. It is not a benefits calculator. It is not a "
        "case management system with better UX. It is a cathedral — a structure built to "
        "house something sacred. What it houses is the full possibility of a human life. "
        "Drawing from Aristotle's insistence on excellence, Sen's measurement of real "
        "capabilities, Ubuntu's web of mutual belonging, Buddhism's systems of interdependence, "
        "Ignatian care for the whole person, Indigenous reciprocity with the living world, "
        "Existentialism's demand for authentic freedom, and Maslow's vision of self-actualization, "
        "the Dome proposes that every human being deserves an architecture of flourishing as "
        "thoughtfully designed as any cathedral, as precisely engineered as any bridge, and "
        "as lovingly maintained as any garden. This is not utopian. It is the minimum that "
        "a civilization owes its members. The question is not whether we can afford to build "
        "the Dome. The question is whether we can afford not to."
    ),
    "principles": [
        {
            "name": "Wholeness",
            "description": (
                "A human being is not a collection of problems to be solved by separate "
                "agencies. They are an integrated whole — body, mind, spirit, community, "
                "environment — and the Dome must address them as such. Fragmented services "
                "produce fragmented lives. The Dome insists on seeing the whole person."
            )
        },
        {
            "name": "Irreducibility",
            "description": (
                "No domain of flourishing can be sacrificed for another. Economic growth "
                "that destroys community is not progress. Health care that ignores spiritual "
                "depth is incomplete. Creative expression cannot compensate for economic "
                "terror. Each domain is irreducible and non-negotiable."
            )
        },
        {
            "name": "Relationality",
            "description": (
                "Flourishing is never individual. Ubuntu, interbeing, and relational "
                "worldview all converge on this truth: my flourishing is bound up in yours. "
                "The Dome is designed not for the autonomous individual but for the "
                "person-in-community, the self-in-relationship, the human-in-ecosystem."
            )
        },
        {
            "name": "Agency",
            "description": (
                "The Dome does not flourish people. It creates the conditions in which "
                "people flourish themselves. Existentialism and the Capability Approach "
                "both insist: genuine flourishing requires real choice. Paternalism — "
                "however well-intentioned — is the enemy of human dignity."
            )
        },
        {
            "name": "Aspiration",
            "description": (
                "The Dome does not stop at adequacy. Maslow's self-actualization and "
                "Ignatius's magis both point beyond mere sufficiency toward excellence, "
                "beauty, and transcendence. A society that provides only the basics has "
                "met its obligations but not its potential. The Dome aspires."
            )
        },
        {
            "name": "Justice",
            "description": (
                "The Dome is not charity. It is justice. Every tradition represented here — "
                "from Aristotle's political justice to de Beauvoir's liberation to Ubuntu's "
                "communal responsibility — insists that flourishing for all is not a gift "
                "from the powerful to the powerless but the rightful inheritance of every "
                "person born into the human community."
            )
        }
    ]
}
