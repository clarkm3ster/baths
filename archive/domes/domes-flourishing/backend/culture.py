"""
culture.py — The Cultural Infrastructure of Flourishing

Culture is not entertainment. It is the medium through which a society dreams,
remembers, argues, mourns, celebrates, and imagines alternatives. Creative
infrastructure — museums, libraries, theaters, maker spaces, public art, digital
platforms — is as essential to flourishing as roads and water pipes. A society
that invests only in economic infrastructure and neglects cultural infrastructure
produces people who are materially comfortable and spiritually starving.

This module maps the creative dimensions of the Dome: what cultural infrastructure
exists, what is missing, and what flourishing in each creative domain looks like.
"""

from typing import Any


CULTURE_DOMAINS: list[dict[str, Any]] = [
    {
        "id": "visual_arts",
        "name": "Visual Arts",
        "description": (
            "The visual arts — painting, sculpture, photography, printmaking, ceramics, "
            "textile arts, installation, and digital art — are humanity's oldest technology "
            "for making the invisible visible. From the cave paintings of Lascaux to the murals "
            "of Philadelphia, visual art transforms private experience into shared meaning. "
            "It is how a society shows itself what it values, what it fears, what it hopes for."
        ),
        "public_infrastructure": [
            "Public museums with free or low-cost admission",
            "Community art centers offering classes and studio space",
            "Public art programs integrating art into streets, buildings, and transit",
            "Art lending libraries that bring original work into homes",
            "Percent-for-art programs requiring art in every public construction project"
        ],
        "community_infrastructure": [
            "Artist cooperatives sharing studio space and resources",
            "Community galleries showcasing local work",
            "Mural programs employing local artists to transform neighborhoods",
            "Art collectives organizing exhibitions and critiques",
            "Intergenerational arts programs connecting master artists with youth"
        ],
        "what_flourishing_requires": (
            "Every neighborhood should have access to studio space, art supplies, and "
            "instruction. Every child should have sustained exposure to making and viewing "
            "art — not as enrichment but as core curriculum. Artists should be able to live "
            "in the communities they serve without being displaced by the very revitalization "
            "their presence catalyzes. Public spaces should be rich with visual art that "
            "challenges, comforts, provokes, and delights."
        )
    },
    {
        "id": "music_sound",
        "name": "Music & Sound",
        "description": (
            "Music is the most universal of human arts. Every known culture has music. "
            "It precedes language in child development and often outlasts it in dementia. "
            "Music regulates emotion, builds community, marks ritual, accompanies labor, "
            "and expresses what words cannot. A society's musical infrastructure — its "
            "concert halls, practice rooms, instrument lending programs, music education "
            "systems, and live performance venues — determines whether music is a privilege "
            "of the trained few or a practice of the living many."
        ),
        "public_infrastructure": [
            "Music education in every public school from kindergarten through 12th grade",
            "Public performance venues from neighborhood bandstands to concert halls",
            "Instrument lending libraries making instruments available regardless of income",
            "Community music schools offering affordable instruction",
            "Public radio and media supporting local and independent musicians"
        ],
        "community_infrastructure": [
            "Community choirs, bands, and orchestras open to all skill levels",
            "Open mic nights and jam sessions in neighborhood venues",
            "Music cooperatives sharing recording equipment and rehearsal space",
            "Traditional music preservation programs keeping folk traditions alive",
            "Youth music mentorship connecting experienced musicians with young learners"
        ],
        "what_flourishing_requires": (
            "Every child should learn to play an instrument or sing, not to become a "
            "professional musician but to experience the irreplaceable joy of making music. "
            "Every neighborhood should have spaces where live music happens regularly — not "
            "just consumption of recorded sound but the embodied, communal experience of "
            "people making music together. Music education should be as non-negotiable as "
            "mathematics, because it teaches listening, cooperation, emotional expression, "
            "and the experience of beauty."
        )
    },
    {
        "id": "literature_story",
        "name": "Literature & Story",
        "description": (
            "Storytelling is how human beings make sense of time. Through narrative — "
            "novels, poetry, memoir, journalism, oral tradition, sacred text — we organize "
            "the chaos of experience into meaning. Literature expands empathy: it is the "
            "only technology that allows one consciousness to temporarily inhabit another. "
            "A society rich in literary culture is a society that understands itself — its "
            "histories, its contradictions, its possibilities."
        ),
        "public_infrastructure": [
            "Public libraries as the cornerstone of literary infrastructure",
            "Literacy programs ensuring every person can read and write",
            "Writers-in-residence programs in schools, hospitals, and prisons",
            "Public readings, literary festivals, and author events",
            "Support for literary translation making world literature accessible"
        ],
        "community_infrastructure": [
            "Book clubs and reading groups in every neighborhood",
            "Community writing workshops and critique groups",
            "Oral history projects preserving community narratives",
            "Zine libraries and small press publishing cooperatives",
            "Storytelling circles that honor oral tradition and personal narrative"
        ],
        "what_flourishing_requires": (
            "Universal literacy is the foundation, but flourishing requires more: a culture "
            "of reading, writing, and storytelling that goes beyond functional literacy to "
            "literary engagement. Every person should have access to a rich library, physical "
            "or digital, of books that challenge and expand their understanding. Every community "
            "should have spaces where stories are told and heard — not just consumed from screens "
            "but shared between living people. Writers should be supported not as entertainers "
            "but as essential workers in the meaning-making infrastructure of society."
        )
    },
    {
        "id": "performance",
        "name": "Performance",
        "description": (
            "Performance — theater, dance, spoken word, comedy, circus, ritual — is the "
            "art of shared presence. Unlike recorded media, performance requires bodies in "
            "a room together, breathing the same air, responding to each other in real time. "
            "It is inherently communal, inherently ephemeral, inherently alive. Theater has "
            "been central to civic life since Athens; dance has been central to human culture "
            "since before recorded history. A society without live performance is a society "
            "that has forgotten how to be together."
        ),
        "public_infrastructure": [
            "Publicly funded theaters and performance spaces in every community",
            "Dance education in schools, treating movement as fundamental as reading",
            "Theater-in-education programs bringing drama into classrooms",
            "Subsidized ticket programs ensuring live performance is not a luxury good",
            "Public festivals and street performance traditions"
        ],
        "community_infrastructure": [
            "Community theater companies where anyone can audition and participate",
            "Dance studios and rehearsal spaces available at community rates",
            "Improv and comedy troupes creating spaces for risk and laughter",
            "Cultural performance traditions maintained by community practitioners",
            "Spoken word and poetry slam events as democratic performance platforms"
        ],
        "what_flourishing_requires": (
            "Every person should experience live performance regularly — as audience and, "
            "ideally, as participant. Community theater, dance classes, spoken word nights, "
            "and comedy shows should be as common as coffee shops. Performance spaces — from "
            "grand theaters to neighborhood stages — should be abundant, affordable, and "
            "distributed equitably across communities. The performing arts should not be "
            "identified primarily with elite institutions in wealthy neighborhoods but with "
            "the living creative practice of everyday people."
        )
    },
    {
        "id": "design_architecture",
        "name": "Design & Architecture",
        "description": (
            "Design is the art of intention. Architecture is the art of inhabitable meaning. "
            "Together they shape the material world through which human beings move every day "
            "— the buildings, streets, objects, interfaces, and environments that either "
            "support flourishing or degrade it. Design is not decoration; it is the discipline "
            "of making things work beautifully. Architecture is not construction; it is the "
            "discipline of creating spaces that elevate the human experience."
        ),
        "public_infrastructure": [
            "Urban planning departments with genuine design expertise and community input",
            "Design review boards ensuring public buildings meet standards of beauty and function",
            "Architecture education exposing all students to the principles of built environment",
            "Publicly funded design services for community organizations and nonprofits",
            "Historic preservation programs protecting architectural heritage"
        ],
        "community_infrastructure": [
            "Community design charettes involving residents in neighborhood planning",
            "Design cooperatives offering affordable services to local organizations",
            "Architecture for Humanity-style pro bono design for underserved communities",
            "Community fabrication labs and design studios",
            "Participatory budgeting for public space design"
        ],
        "what_flourishing_requires": (
            "Every person deserves a built environment designed with care. Public buildings — "
            "schools, libraries, transit stations, government offices — should communicate "
            "through their design that the people who use them matter. Housing should be not "
            "merely adequate but beautiful, because beauty is not a luxury but a human need. "
            "Design education should be universal, teaching every person to see their "
            "environment critically and to imagine how it might be better."
        )
    },
    {
        "id": "digital_creation",
        "name": "Digital Creation",
        "description": (
            "Digital creation encompasses the vast and rapidly evolving landscape of "
            "computer-mediated creative work: game design, animation, interactive media, "
            "web development, AI art, VR experiences, digital music production, and more. "
            "Digital tools have democratized creative production in unprecedented ways — a "
            "teenager with a laptop can make a film, compose a symphony, design a game, or "
            "publish a novel. But digital creation also concentrates power in platform companies "
            "that extract value from creators while controlling distribution."
        ),
        "public_infrastructure": [
            "Universal broadband access as a prerequisite for digital creative participation",
            "Digital literacy education covering creative tools, not just consumption",
            "Public media labs with professional-grade digital production equipment",
            "Open source creative software development funded as public infrastructure",
            "Public digital archives preserving born-digital creative work"
        ],
        "community_infrastructure": [
            "Coding bootcamps and creative technology workshops",
            "Game design collectives and game jams",
            "Digital storytelling labs in libraries and community centers",
            "Open source communities collaboratively building creative tools",
            "Youth digital media programs teaching production, not just consumption"
        ],
        "what_flourishing_requires": (
            "Digital creation tools and skills should be accessible to everyone, not just "
            "those who can afford expensive software and fast internet. Digital literacy must "
            "go beyond using apps to creating with technology — everyone should understand "
            "enough code, design, and media production to be a maker, not just a consumer, "
            "in the digital world. And the economics of digital creation must be restructured "
            "so that creators capture the value of their work rather than surrendering it to "
            "platforms."
        )
    },
    {
        "id": "craft_making",
        "name": "Craft & Making",
        "description": (
            "Craft — woodworking, pottery, weaving, blacksmithing, leatherwork, glassblowing, "
            "quilting, knitting, cooking — is the art of the hand. In a world increasingly "
            "mediated by screens, craft reconnects human beings with the material world, with "
            "the satisfactions of skilled physical work, with traditions passed from hand to "
            "hand across generations. Craft is not nostalgia; it is a form of knowledge that "
            "cannot be reduced to information, a form of intelligence that lives in the body."
        ),
        "public_infrastructure": [
            "Vocational education that treats craft as art, not consolation prize",
            "Public maker spaces with tools for wood, metal, textile, and ceramic work",
            "Apprenticeship programs preserving traditional crafts and trades",
            "Public markets where artisans can sell directly to their communities",
            "Craft education integrated into school curricula at every level"
        ],
        "community_infrastructure": [
            "Tool libraries lending specialized equipment to community members",
            "Cooperative workshops shared by multiple artisans",
            "Craft circles and guilds maintaining quality standards and community",
            "Repair cafes teaching people to fix rather than discard",
            "Farm-to-table and maker-to-market networks connecting creators with consumers"
        ],
        "what_flourishing_requires": (
            "Every person should have the opportunity to work with their hands — to shape "
            "wood, throw clay, grow food, repair a machine, sew a garment. This is not "
            "vocational training in the narrow sense but a fundamental dimension of human "
            "experience. Craft spaces — workshops, kitchens, gardens, studios — should be "
            "as common in neighborhoods as gyms. The knowledge of skilled makers should be "
            "honored and transmitted, not allowed to disappear as 'outdated.'"
        )
    },
    {
        "id": "film_media",
        "name": "Film & Media",
        "description": (
            "Film, television, documentary, podcast, and multimedia journalism shape the "
            "stories a society tells about itself. They are the most powerful tools of "
            "empathy and propaganda, capable of expanding understanding or reinforcing "
            "prejudice. Media infrastructure determines whose stories are told, who tells "
            "them, and who controls the means of production and distribution."
        ),
        "public_infrastructure": [
            "Public broadcasting providing independent, non-commercial media",
            "Film commissions supporting local production and economic development",
            "Media arts education teaching critical viewing and production skills",
            "Public access channels and community media centers",
            "Documentary funding for stories the commercial market ignores"
        ],
        "community_infrastructure": [
            "Community film screening and discussion series",
            "Youth media production programs",
            "Collaborative documentary projects telling community stories",
            "Podcast cooperatives sharing equipment and distribution",
            "Citizen journalism networks training community reporters"
        ],
        "what_flourishing_requires": (
            "Every community should see itself reflected in the media it consumes — not as "
            "stereotype or spectacle but as complex, fully realized human experience. Media "
            "production skills and tools should be accessible to all, so that the stories told "
            "about a community can be told by that community. Public media should be robust "
            "enough to provide an alternative to commercial media's incentive to sensationalize, "
            "simplify, and divide. Media literacy — the ability to critically evaluate what one "
            "sees and hears — should be a core competency of every educated person."
        )
    }
]


CULTURE_ASSETS: dict[str, dict[str, Any]] = {
    "museums": {
        "count": 35000,
        "description": (
            "The United States has approximately 35,000 museums — more than Starbucks and "
            "McDonald's locations combined. Yet museum access is profoundly unequal. Major "
            "institutions cluster in wealthy urban areas while vast stretches of the country "
            "have no museum within driving distance. Free admission remains the exception "
            "rather than the rule, and collections disproportionately reflect the tastes and "
            "histories of wealthy white donors rather than the communities they serve."
        ),
        "distribution_equity": 32
    },
    "libraries": {
        "count": 17000,
        "description": (
            "America's 17,000 public library systems are the most democratic cultural "
            "institution in the country — free, open to all, trusted across political "
            "divides. They are increasingly serving as de facto community centers, social "
            "service hubs, maker spaces, and digital access points. Yet library funding "
            "has declined in real terms, forcing branches to close, reduce hours, and "
            "eliminate programming precisely when they are needed most."
        ),
        "distribution_equity": 68
    },
    "performance_spaces": {
        "count": 8500,
        "description": (
            "Formal performance spaces — theaters, concert halls, dance venues — number "
            "approximately 8,500 in the US. This figure masks enormous geographic inequality: "
            "New York City alone has more professional theater seats than most states combined. "
            "Community and amateur performance spaces — church basements, school auditoriums, "
            "park bandshells — are more distributed but often poorly maintained and "
            "underutilized."
        ),
        "distribution_equity": 28
    },
    "maker_spaces": {
        "count": 2500,
        "description": (
            "The maker movement has produced approximately 2,500 dedicated maker spaces, "
            "fab labs, and community workshops in the US. These spaces democratize access "
            "to tools that were once available only to those with personal workshops or "
            "industrial employment: 3D printers, laser cutters, CNC machines, sewing "
            "machines, woodworking tools. But they remain overwhelmingly concentrated in "
            "affluent, tech-oriented communities."
        ),
        "distribution_equity": 18
    },
    "public_art": {
        "count": 50000,
        "description": (
            "An estimated 50,000 pieces of public art — murals, sculptures, installations, "
            "monuments — exist in American public spaces. Public art programs, typically "
            "funded through percent-for-art ordinances, have transformed some cities into "
            "open-air galleries. But the distribution is wildly uneven, and public art in "
            "low-income communities is often limited to murals covering blight rather than "
            "commissioned works celebrating community identity."
        ),
        "distribution_equity": 35
    },
    "digital_platforms": {
        "count": 150,
        "description": (
            "Approximately 150 major digital platforms serve as distribution channels for "
            "creative work — from YouTube and Spotify to Etsy and Substack. These platforms "
            "have democratized access to audiences in unprecedented ways but have also "
            "concentrated power in the hands of platform owners, created a race to the bottom "
            "in creator compensation, and replaced curatorial judgment with algorithmic "
            "optimization that rewards engagement over quality."
        ),
        "distribution_equity": 72
    }
}


CULTURE_DESERTS: list[dict[str, Any]] = [
    {
        "id": "creative_deserts",
        "name": "Creative Deserts",
        "description": (
            "Creative deserts are communities where the infrastructure for making — studios, "
            "workshops, performance spaces, art supply stores, music venues, maker spaces — "
            "is absent or inaccessible. In creative deserts, people consume culture produced "
            "elsewhere but have no means to produce their own. The creative capacity of the "
            "community atrophies. Young people with creative potential leave for cities where "
            "infrastructure exists, further depleting the community's creative ecosystem."
        ),
        "affected_population": "47 million Americans live in counties with no dedicated arts facility",
        "indicators": [
            "No dedicated arts venue or gallery within 30 minutes",
            "No arts education in local schools",
            "No maker space, community workshop, or studio space available",
            "Fewer than 1 working artist per 1,000 residents",
            "No public art program or percent-for-art policy",
            "Creative professionals leave the community due to lack of infrastructure"
        ],
        "interventions": [
            "Mobile arts programs bringing studios and instruction to underserved areas",
            "Micro-grants for community-based creative projects",
            "Adaptive reuse of vacant buildings as community arts spaces",
            "Artist relocation incentives attracting creative professionals to underserved communities",
            "Digital creative hubs providing equipment and training in rural and low-income areas",
            "Community cultural planning processes that identify and address creative gaps"
        ]
    },
    {
        "id": "knowledge_deserts",
        "name": "Knowledge Deserts",
        "description": (
            "Knowledge deserts are communities where access to information, education, and "
            "intellectual engagement is severely limited. They exist where libraries have "
            "closed, bookstores have vanished, broadband is unavailable, schools are "
            "under-resourced, and the nearest institution of higher learning is hours away. "
            "In knowledge deserts, the fire of curiosity has no fuel. People are cut off from "
            "the ideas, research, and cultural production that the rest of society takes for granted."
        ),
        "affected_population": "24 million Americans lack broadband; millions more lack nearby libraries or bookstores",
        "indicators": [
            "No public library branch within 20 minutes",
            "No bookstore — new or used — within the community",
            "Broadband internet unavailable or unaffordable",
            "School libraries unstaffed or defunded",
            "No institution of higher learning within commuting distance",
            "Local newspaper has closed, leaving a news desert"
        ],
        "interventions": [
            "Universal broadband as public utility",
            "Bookmobile and mobile library programs serving remote areas",
            "Little Free Libraries and community book exchanges",
            "Community learning centers with internet access and educational programming",
            "Distance learning programs from universities and community colleges",
            "Local journalism initiatives rebuilding community information infrastructure"
        ]
    },
    {
        "id": "beauty_deserts",
        "name": "Beauty Deserts",
        "description": (
            "Beauty deserts are communities where the built environment communicates neglect, "
            "disinvestment, and indifference to the people who live there. Crumbling infrastructure, "
            "vacant lots, boarded buildings, treeless streets, and the complete absence of public "
            "art or thoughtful design create environments that are not merely unattractive but "
            "actively hostile to human dignity. Beauty deserts are the spatial expression of a "
            "society that has decided some people do not deserve to live among beautiful things."
        ),
        "affected_population": "Concentrated in formerly redlined neighborhoods, rural communities, and industrial zones",
        "indicators": [
            "Tree canopy coverage below 10%",
            "No public art or designed public space within walking distance",
            "Majority of buildings in visible disrepair",
            "Vacant and abandoned properties exceeding 15% of housing stock",
            "No park or green space within half a mile",
            "Public buildings (schools, offices) visibly neglected and institutional"
        ],
        "interventions": [
            "Tree planting programs prioritizing low-canopy neighborhoods",
            "Vacant lot transformation into community gardens and pocket parks",
            "Public art commissions specifically for beauty-desert communities",
            "Building facade improvement programs and blight remediation",
            "Community design charrettes empowering residents to reimagine their streetscapes",
            "Infrastructure investment that treats beauty as a requirement alongside function"
        ]
    },
    {
        "id": "performance_deserts",
        "name": "Performance Deserts",
        "description": (
            "Performance deserts are communities where live performance — theater, music, dance, "
            "comedy, spoken word — is absent from daily life. In performance deserts, the only "
            "entertainment available is screen-based: television, streaming, social media. The "
            "experience of shared presence — of laughing together, crying together, being surprised "
            "together in real time — is missing. The communal art forms that have bound human "
            "communities together since the beginning of civilization have been replaced by "
            "isolated consumption of corporate content."
        ),
        "affected_population": "Most rural communities and many suburban areas lack any regular live performance",
        "indicators": [
            "No live music venue within the community",
            "No theater company — professional or community — within 30 miles",
            "No regular public performance events (concerts in the park, open mics, festivals)",
            "School performing arts programs eliminated or reduced to minimal levels",
            "No comedy venue, spoken word event, or improv show accessible locally",
            "Community gathering relies entirely on screen-based entertainment"
        ],
        "interventions": [
            "Touring performance programs bringing live shows to underserved areas",
            "Community theater startup grants and technical assistance",
            "Park and public space programming with regular free performances",
            "School performing arts reinvestment as core curriculum",
            "Micro-venue development converting small spaces into intimate performance sites",
            "Performance arts residencies embedding artists in communities for extended periods"
        ]
    }
]
