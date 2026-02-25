"""
BATHS Intelligence — Cross-Project Learning Memory

This is the core of how the system gets smarter. Every completed project
deposits learnings. Every new project queries for relevant prior learnings.

Domes learn from domes. Spheres learn from spheres. And cross-pollination
happens when a sphere discovery informs a dome approach, or vice versa.

This is REAL CODE that EXECUTES. It stores, retrieves, and evolves learnings.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime

from intelligence.models import (
    Learning, LearningType, ProjectMemory, WorldModelDomain,
    PersonKnowledge, PlaceKnowledge, IntelligenceMetrics,
)


class ProjectMemoryStore:
    """
    The system's memory. Stores learnings from every completed project
    and retrieves relevant ones for new projects.

    This is an in-memory store that can be serialized to disk or database.
    The retrieval system uses keyword overlap + domain matching + reliability
    scoring — not embeddings (yet), but genuinely functional matching.
    """

    def __init__(self):
        self.memories: Dict[str, ProjectMemory] = {}
        self.all_learnings: Dict[str, Learning] = {}
        self.person_knowledge: Dict[str, PersonKnowledge] = {}
        self.place_knowledge: Dict[str, PlaceKnowledge] = {}
        self._metrics_history: List[IntelligenceMetrics] = []

    # ── Deposit ─────────────────────────────────────────────────

    def deposit(self, memory: ProjectMemory) -> None:
        """
        Deposit a completed project's learnings into the memory system.
        This is called after every play_full_game completion.
        """
        self.memories[memory.project_id] = memory

        for learning in memory.learnings:
            self.all_learnings[learning.learning_id] = learning
            # Check if this corroborates or contradicts existing learnings
            self._cross_reference(learning)

        # Update world models
        if memory.game_type == "domes":
            self._update_person_knowledge(memory)
        elif memory.game_type == "spheres":
            self._update_place_knowledge(memory)

    # ── Retrieve ────────────────────────────────────────────────

    def query_relevant_learnings(
        self,
        game_type: str,
        keywords: List[str],
        domains: Optional[List[WorldModelDomain]] = None,
        capability: Optional[str] = None,
        stage: Optional[str] = None,
        limit: int = 10,
        min_reliability: float = 0.3,
    ) -> List[Learning]:
        """
        Find learnings relevant to a new project or stage.

        Uses keyword overlap scoring weighted by reliability and transferability.
        Returns the most relevant learnings, sorted by relevance score.
        """
        if not self.all_learnings:
            return []

        scored: List[Tuple[float, Learning]] = []
        keywords_lower = set(k.lower() for k in keywords)

        for learning in self.all_learnings.values():
            if learning.reliability < min_reliability:
                continue

            score = 0.0

            # Keyword overlap (primary signal)
            learning_kw = set(k.lower() for k in learning.keywords)
            overlap = keywords_lower & learning_kw
            if not overlap:
                # Also check if any keyword appears in the insight text
                insight_lower = learning.insight.lower()
                text_hits = sum(1 for kw in keywords_lower if kw in insight_lower)
                if text_hits == 0:
                    continue
                score += text_hits * 2.0
            else:
                score += len(overlap) * 5.0

            # Game type match (strong signal)
            if game_type in learning.applicable_game_types:
                score += 10.0
            elif game_type == learning.source_game_type:
                score += 8.0
            else:
                # Cross-pollination: lower score but still valuable
                score += 2.0

            # Domain match
            if domains:
                domain_overlap = set(domains) & set(learning.applicable_domains)
                score += len(domain_overlap) * 3.0

            # Capability match
            if capability and capability == learning.source_capability:
                score += 5.0

            # Stage match
            if stage and stage == learning.source_stage:
                score += 3.0

            # Reliability boost
            score *= (0.5 + learning.reliability * 0.5)

            # Transferability boost
            score *= (0.5 + learning.transferability * 0.5)

            # Recency boost (newer learnings weighted slightly higher)
            age_days = (datetime.utcnow() - learning.created_at).days
            recency = max(0.5, 1.0 - (age_days / 365.0) * 0.3)
            score *= recency

            scored.append((score, learning))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [l for _, l in scored[:limit]]

    def query_person_knowledge(
        self,
        system_tags: List[str],
        dimension_tags: Optional[List[str]] = None,
        circumstance_tags: Optional[List[str]] = None,
    ) -> List[PersonKnowledge]:
        """
        Find accumulated knowledge about people in similar circumstances.
        Used by dome projects to benefit from prior dome learnings.
        """
        if not self.person_knowledge:
            return []

        scored: List[Tuple[float, PersonKnowledge]] = []
        sys_set = set(t.lower() for t in system_tags)

        for pk in self.person_knowledge.values():
            score = 0.0
            pk_sys = set(t.lower() for t in pk.system_tags)
            overlap = sys_set & pk_sys
            score += len(overlap) * 10.0

            if dimension_tags:
                dim_set = set(t.lower() for t in dimension_tags)
                pk_dims = set(t.lower() for t in pk.dimension_tags)
                score += len(dim_set & pk_dims) * 5.0

            if circumstance_tags:
                circ_set = set(t.lower() for t in circumstance_tags)
                pk_circ = set(t.lower() for t in pk.circumstance_tags)
                score += len(circ_set & pk_circ) * 7.0

            # More observations = more reliable
            score *= (1.0 + min(pk.observation_count, 10) * 0.1)

            if score > 0:
                scored.append((score, pk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [pk for _, pk in scored[:5]]

    def query_place_knowledge(
        self,
        zoning_tags: Optional[List[str]] = None,
        neighborhood_tags: Optional[List[str]] = None,
        site_tags: Optional[List[str]] = None,
        lot_size_sqft: Optional[float] = None,
    ) -> List[PlaceKnowledge]:
        """
        Find accumulated knowledge about places with similar characteristics.
        Used by sphere projects to benefit from prior sphere learnings.
        """
        if not self.place_knowledge:
            return []

        scored: List[Tuple[float, PlaceKnowledge]] = []

        for plk in self.place_knowledge.values():
            score = 0.0

            if zoning_tags:
                z_set = set(t.lower() for t in zoning_tags)
                plk_z = set(t.lower() for t in plk.zoning_tags)
                score += len(z_set & plk_z) * 10.0

            if neighborhood_tags:
                n_set = set(t.lower() for t in neighborhood_tags)
                plk_n = set(t.lower() for t in plk.neighborhood_tags)
                score += len(n_set & plk_n) * 8.0

            if site_tags:
                s_set = set(t.lower() for t in site_tags)
                plk_s = set(t.lower() for t in plk.site_tags)
                score += len(s_set & plk_s) * 6.0

            if lot_size_sqft is not None:
                lo, hi = plk.size_range
                if lo <= lot_size_sqft <= hi:
                    score += 5.0

            score *= (1.0 + min(plk.observation_count, 10) * 0.1)

            if score > 0:
                scored.append((score, plk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [plk for _, plk in scored[:5]]

    # ── Learning Extraction ─────────────────────────────────────

    def extract_learnings_from_stage(
        self,
        project_id: str,
        project_title: str,
        game_type: str,
        stage: str,
        deliverables: List[Dict],
        cosm_delta: float = 0.0,
        chron_delta: float = 0.0,
    ) -> List[Learning]:
        """
        Extract learnings from a completed stage's deliverables.
        This is the intelligence extraction engine — it reads what was produced
        and identifies transferable insights.

        Uses keyword density, structural patterns, and content analysis
        to generate learnings that other projects can use.
        """
        learnings = []

        for deliverable in deliverables:
            desc = deliverable.get("description", "")
            cap = deliverable.get("capability", "")
            talent_name = deliverable.get("talent_name", "")
            is_unlikely = deliverable.get("is_unlikely", False)

            # Extract keywords from the deliverable
            keywords = self._extract_keywords(desc, cap, game_type)

            # Determine applicable domains
            domains = self._infer_domains(cap, desc, game_type)

            # Generate learning based on content analysis
            generated = self._analyze_deliverable(
                desc, cap, stage, game_type, talent_name, is_unlikely,
            )

            for insight_text, learning_type, confidence, transferability in generated:
                learning = Learning(
                    learning_type=learning_type,
                    source_project_id=project_id,
                    source_project_title=project_title,
                    source_game_type=game_type,
                    source_stage=stage,
                    source_capability=cap,
                    source_practitioner=talent_name,
                    insight=insight_text,
                    evidence=desc[:300],
                    confidence=confidence,
                    applicable_domains=domains,
                    applicable_game_types=[game_type],
                    transferability=transferability,
                    keywords=keywords,
                )
                learnings.append(learning)

        return learnings

    # ── Internal Analysis ───────────────────────────────────────

    def _analyze_deliverable(
        self,
        description: str,
        capability: str,
        stage: str,
        game_type: str,
        practitioner: str,
        is_unlikely: bool,
    ) -> List[Tuple[str, LearningType, float, float]]:
        """
        Analyze a deliverable's content and extract transferable insights.
        Returns list of (insight_text, learning_type, confidence, transferability).
        """
        results = []
        desc_lower = description.lower()

        # Pattern: System coordination insights
        coordination_signals = [
            "coordination", "link", "connect", "integrate", "pathway",
            "navigator", "single application", "shared data",
        ]
        coord_hits = sum(1 for s in coordination_signals if s in desc_lower)
        if coord_hits >= 2:
            # Extract the specific coordination insight
            results.append((
                f"Coordination pattern ({capability}, {stage}): "
                f"{practitioner}'s approach to linking systems — "
                f"applied at {game_type} level. "
                f"{self._extract_sentence_with(description, 'coordination', 'pathway', 'link')}",
                LearningType.METHOD,
                min(0.4 + coord_hits * 0.1, 0.9),
                0.7,  # Coordination insights transfer well
            ))

        # Pattern: Cost/economic insights
        cost_signals = [
            "cost", "savings", "invest", "returns", "fragmentation tax",
            "bond", "financial", "economic multiplier",
        ]
        cost_hits = sum(1 for s in cost_signals if s in desc_lower)
        if cost_hits >= 2:
            results.append((
                f"Cost pattern ({capability}, {stage}): "
                f"Economic structure from {practitioner}. "
                f"{self._extract_sentence_with(description, 'cost', 'savings', 'invest')}",
                LearningType.COST_INSIGHT,
                min(0.4 + cost_hits * 0.1, 0.85),
                0.8,  # Cost insights transfer very well
            ))

        # Pattern: Awe design insights
        awe_signals = [
            "awe", "vastness", "accommodation", "collective effervescence",
            "moral beauty", "epiphany", "keltner", "awe-s", "prosocial",
            "time expansion", "piloerection",
        ]
        awe_hits = sum(1 for s in awe_signals if s in desc_lower)
        if awe_hits >= 2:
            results.append((
                f"Awe design pattern ({capability}, {stage}): "
                f"{practitioner}'s awe trigger deployment. "
                f"{self._extract_sentence_with(description, 'awe', 'vastness', 'accommodation', 'effervescence')}",
                LearningType.AWE_INSIGHT,
                min(0.3 + awe_hits * 0.08, 0.85),
                0.6,  # Awe insights are somewhat site/person-specific
            ))

        # Pattern: Policy insights
        policy_signals = [
            "policy", "replicable", "municipal", "template", "ordinance",
            "variance", "zoning", "regulatory",
        ]
        policy_hits = sum(1 for s in policy_signals if s in desc_lower)
        if policy_hits >= 2:
            results.append((
                f"Policy pattern ({capability}, {stage}): "
                f"Regulatory insight from {practitioner}. "
                f"{self._extract_sentence_with(description, 'policy', 'replicable', 'municipal', 'template')}",
                LearningType.POLICY_INSIGHT,
                min(0.4 + policy_hits * 0.1, 0.9),
                0.75,
            ))

        # Pattern: Unlikely collision insights (high transfer value)
        if is_unlikely:
            results.append((
                f"Unlikely collision ({capability}): "
                f"{practitioner}'s unexpected contribution — "
                f"a discipline not on the production plan producing "
                f"transferable IP. {description[:200]}",
                LearningType.CONNECTION,
                0.5,
                0.9,  # Unlikely collisions have very high transfer potential
            ))

        # Pattern: Failure/constraint navigation
        failure_signals = [
            "broke", "failed", "didn't work", "breaks when",
            "depends on", "discretion", "conflict", "duplicate",
        ]
        failure_hits = sum(1 for s in failure_signals if s in desc_lower)
        if failure_hits >= 2:
            results.append((
                f"Constraint pattern ({capability}, {stage}): "
                f"What breaks under real conditions. "
                f"{self._extract_sentence_with(description, 'breaks', 'conflict', 'failed', 'discretion')}",
                LearningType.FAILURE,
                min(0.5 + failure_hits * 0.1, 0.9),
                0.85,  # Failure learnings are extremely transferable
            ))

        # Default: always extract at least one finding per deliverable
        if not results:
            results.append((
                f"Finding ({capability}, {stage}): "
                f"{practitioner}'s contribution to {game_type}. "
                f"{description[:200]}",
                LearningType.FINDING,
                0.3,
                0.4,
            ))

        return results

    def _cross_reference(self, new_learning: Learning) -> None:
        """
        Check if a new learning corroborates or contradicts existing learnings.
        This is how the system builds confidence over time.
        """
        new_kw = set(k.lower() for k in new_learning.keywords)

        for existing in self.all_learnings.values():
            if existing.learning_id == new_learning.learning_id:
                continue

            existing_kw = set(k.lower() for k in existing.keywords)
            overlap = new_kw & existing_kw

            # Need significant keyword overlap to be related
            if len(overlap) < 3:
                continue

            # Same type of learning with high keyword overlap = corroboration
            if existing.learning_type == new_learning.learning_type:
                existing.times_corroborated += 1
                # Boost transferability when corroborated
                existing.transferability = min(1.0, existing.transferability + 0.05)

            # Check for contradiction (opposite findings)
            new_lower = new_learning.insight.lower()
            existing_lower = existing.insight.lower()
            contradiction_pairs = [
                ("works", "doesn't work"), ("succeeded", "failed"),
                ("efficient", "inefficient"), ("effective", "ineffective"),
            ]
            for pos, neg in contradiction_pairs:
                if (pos in new_lower and neg in existing_lower) or \
                   (neg in new_lower and pos in existing_lower):
                    existing.times_contradicted += 1
                    break

    def _update_person_knowledge(self, memory: ProjectMemory) -> None:
        """Update the person world model with learnings from a dome project."""
        # Build a compound key from the project's characteristics
        system_tags = []
        dimension_tags = []
        for learning in memory.learnings:
            system_tags.extend(learning.keywords)

        key = "|".join(sorted(set(t.lower() for t in system_tags[:5])))
        if not key:
            return

        if key not in self.person_knowledge:
            self.person_knowledge[key] = PersonKnowledge(
                system_tags=list(set(system_tags)),
                dimension_tags=dimension_tags,
            )

        pk = self.person_knowledge[key]
        pk.source_project_ids.append(memory.project_id)
        pk.observation_count += 1
        pk.last_updated = datetime.utcnow()

        # Accumulate coordination insights
        for learning in memory.learnings:
            if learning.learning_type == LearningType.METHOD:
                pk.coordination_insights.append(learning.insight)
            elif learning.learning_type == LearningType.COST_INSIGHT:
                pk.cost_patterns[learning.source_capability] = learning.confidence
            elif learning.learning_type == LearningType.AWE_INSIGHT:
                pk.awe_design_insights.append(learning.insight)

    def _update_place_knowledge(self, memory: ProjectMemory) -> None:
        """Update the place world model with learnings from a sphere project."""
        zoning_tags = []
        for learning in memory.learnings:
            zoning_tags.extend(learning.keywords)

        key = "|".join(sorted(set(t.lower() for t in zoning_tags[:5])))
        if not key:
            return

        if key not in self.place_knowledge:
            self.place_knowledge[key] = PlaceKnowledge(
                zoning_tags=list(set(zoning_tags)),
            )

        plk = self.place_knowledge[key]
        plk.source_project_ids.append(memory.project_id)
        plk.observation_count += 1
        plk.last_updated = datetime.utcnow()

        for learning in memory.learnings:
            if learning.learning_type == LearningType.METHOD:
                plk.activation_patterns.append(learning.insight)
            elif learning.learning_type == LearningType.AWE_INSIGHT:
                plk.awe_trigger_effectiveness[learning.source_capability] = learning.confidence
            elif learning.learning_type == LearningType.POLICY_INSIGHT:
                plk.regulatory_patterns[learning.source_capability] = learning.insight
            elif learning.learning_type == LearningType.COST_INSIGHT:
                plk.economics_patterns[learning.source_capability] = learning.confidence

    # ── Utility ─────────────────────────────────────────────────

    def _extract_keywords(
        self, description: str, capability: str, game_type: str,
    ) -> List[str]:
        """Extract searchable keywords from a deliverable description."""
        # Domain-specific terms that matter for cross-project learning
        significant_terms = {
            # Legal/regulatory
            "entitlement", "eligibility", "variance", "permit", "zoning",
            "recertification", "compliance", "navigator", "coordination",
            # Systems
            "fragmentation", "integration", "interoperability", "data-sharing",
            "duplicate", "cascade", "handoff",
            # Economic
            "bond", "investment", "returns", "multiplier", "savings",
            "cost-of-fragmentation", "activation-cost",
            # Awe
            "vastness", "accommodation", "effervescence", "moral-beauty",
            "epiphany", "awe-s", "prosocial", "piloerection", "hrv",
            # Community
            "gathering", "belonging", "foot-traffic", "adjacent",
            "catalyst", "displacement", "resilience",
            # Housing
            "eviction", "voucher", "shelter", "stability", "housing-first",
            # Health
            "medicaid", "chip", "behavioral-health", "substance-abuse",
        }

        desc_lower = description.lower()
        found = [term for term in significant_terms if term in desc_lower]

        # Add capability and game type
        found.append(capability)
        found.append(game_type)

        # Add any government system names mentioned
        system_names = [
            "tanf", "snap", "medicaid", "chip", "section 8", "eitc",
            "housing court", "family court", "juvenile justice",
        ]
        for sys_name in system_names:
            if sys_name in desc_lower:
                found.append(sys_name)

        return list(set(found))

    def _infer_domains(
        self, capability: str, description: str, game_type: str,
    ) -> List[WorldModelDomain]:
        """Infer which world model domains a deliverable is relevant to."""
        domains = []
        desc_lower = description.lower()

        cap_to_domains = {
            "legal_navigation": [WorldModelDomain.LEGAL],
            "spatial_legal": [WorldModelDomain.LEGAL, WorldModelDomain.ZONING],
            "data_systems": [WorldModelDomain.FISCAL],
            "economics": [WorldModelDomain.ECONOMICS],
            "narrative": [WorldModelDomain.CULTURE],
            "flourishing_design": [WorldModelDomain.COMMUNITY, WorldModelDomain.AWE],
            "activation_design": [WorldModelDomain.AWE, WorldModelDomain.COMMUNITY],
        }
        domains.extend(cap_to_domains.get(capability, []))

        # Content-based inference
        domain_signals = {
            WorldModelDomain.HEALTH: ["health", "medicaid", "chip", "medical", "wellness"],
            WorldModelDomain.HOUSING: ["housing", "eviction", "shelter", "voucher", "rent"],
            WorldModelDomain.EDUCATION: ["education", "school", "credential", "learning"],
            WorldModelDomain.EMPLOYMENT: ["employment", "job", "workforce", "income"],
            WorldModelDomain.ENVIRONMENT: ["environment", "soil", "air quality", "ecology"],
            WorldModelDomain.INFRASTRUCTURE: ["infrastructure", "utility", "transit"],
            WorldModelDomain.DEMOGRAPHICS: ["demographics", "population", "census"],
        }

        for domain, signals in domain_signals.items():
            if any(s in desc_lower for s in signals) and domain not in domains:
                domains.append(domain)

        return domains

    @staticmethod
    def _extract_sentence_with(text: str, *target_words: str) -> str:
        """Extract the most relevant sentence containing target words."""
        sentences = text.replace("\n", ". ").split(". ")
        best_sentence = ""
        best_hits = 0

        for sentence in sentences:
            s_lower = sentence.lower()
            hits = sum(1 for w in target_words if w in s_lower)
            if hits > best_hits:
                best_hits = hits
                best_sentence = sentence.strip()

        if best_sentence:
            # Trim to reasonable length
            if len(best_sentence) > 250:
                best_sentence = best_sentence[:250] + "..."
            return best_sentence
        return ""

    # ── Metrics ─────────────────────────────────────────────────

    def compute_metrics(self) -> IntelligenceMetrics:
        """Compute current intelligence metrics snapshot."""
        total_applied = sum(
            l.times_applied for l in self.all_learnings.values()
        )
        total_corroborated = sum(
            l.times_corroborated for l in self.all_learnings.values()
        )

        avg_confidence = 0.0
        avg_reliability = 0.0
        if self.all_learnings:
            avg_confidence = sum(
                l.confidence for l in self.all_learnings.values()
            ) / len(self.all_learnings)
            avg_reliability = sum(
                l.reliability for l in self.all_learnings.values()
            ) / len(self.all_learnings)

        return IntelligenceMetrics(
            total_projects_completed=len(self.memories),
            total_learnings_stored=len(self.all_learnings),
            total_cross_project_transfers=total_applied,
            avg_learning_confidence=round(avg_confidence, 3),
            avg_learning_reliability=round(avg_reliability, 3),
            corroboration_rate=round(
                total_corroborated / max(total_applied, 1), 3
            ),
            person_knowledge_entries=len(self.person_knowledge),
            place_knowledge_entries=len(self.place_knowledge),
            insight_reuse_rate=round(
                sum(1 for l in self.all_learnings.values() if l.times_applied > 0)
                / max(len(self.all_learnings), 1),
                3,
            ),
        )

    # ── Serialization ───────────────────────────────────────────

    def to_dict(self) -> Dict:
        """Serialize the entire memory store."""
        return {
            "memories": {
                k: v.model_dump() for k, v in self.memories.items()
            },
            "all_learnings": {
                k: v.model_dump() for k, v in self.all_learnings.items()
            },
            "person_knowledge": {
                k: v.model_dump() for k, v in self.person_knowledge.items()
            },
            "place_knowledge": {
                k: v.model_dump() for k, v in self.place_knowledge.items()
            },
            "metrics": self.compute_metrics().model_dump(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ProjectMemoryStore":
        """Deserialize a memory store."""
        store = cls()
        for k, v in data.get("memories", {}).items():
            store.memories[k] = ProjectMemory(**v)
        for k, v in data.get("all_learnings", {}).items():
            store.all_learnings[k] = Learning(**v)
        for k, v in data.get("person_knowledge", {}).items():
            store.person_knowledge[k] = PersonKnowledge(**v)
        for k, v in data.get("place_knowledge", {}).items():
            store.place_knowledge[k] = PlaceKnowledge(**v)
        return store
