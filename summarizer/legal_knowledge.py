import re

# Comprehensive Legal Dictionary: Latin, Archaisms, and Complex Terminology
LEGAL_GLOSSARY = {
    "indemnification": {
        "formal": "An obligation by which one party promises to compensate another for any loss or harm sustained.",
        "plain": "A promise to pay for damages, legal fees, or losses if something goes wrong.",
        "risk_weight": 3
    },
    "indemnify": {
        "formal": "To hold harmless and secure against loss or damage.",
        "plain": "Agreeing to cover legal costs and claims on someone else's behalf.",
        "risk_weight": 3
    },
    "force majeure": {
        "formal": "An unforeseen, unavoidable event (e.g., natural disasters, war) that frees parties from contractual liability.",
        "plain": "'Act of God' clause allowing contract suspension or exit during uncontrollable catastrophes.",
        "risk_weight": 1
    },
    "liquidated damages": {
        "formal": "A predetermined monetary sum agreed upon by parties to be paid upon breach of contract.",
        "plain": "A pre-fixed cash penalty you must pay immediately if you fail to meet an obligation.",
        "risk_weight": 3
    },
    "subrogation": {
        "formal": "The substitution of one person or entity in the place of another in respect of a lawful claim.",
        "plain": "Allowing an insurer or third party to step into your shoes and sue someone on your behalf.",
        "risk_weight": 2
    },
    "mutatis mutandis": {
        "formal": "Latin phrase meaning 'with the necessary changes having been made'.",
        "plain": "Applying the same rules or terms to a new situation with minor appropriate alterations.",
        "risk_weight": 1
    },
    "prima facie": {
        "formal": "Latin phrase meaning 'at first sight' or sufficient to establish a fact unless rebutted.",
        "plain": "Evidence that appears obvious and legally accepted as true until proven otherwise.",
        "risk_weight": 1
    },
    "inter alia": {
        "formal": "Latin phrase meaning 'among other things'.",
        "plain": "Including but not limited to; indicates an illustrative rather than exhaustive list.",
        "risk_weight": 1
    },
    "without prejudice": {
        "formal": "Without abandonment or detriment to an existing right or claim.",
        "plain": "Communications or offers made to settle disputes that cannot be used against you in court.",
        "risk_weight": 1
    },
    "ultra vires": {
        "formal": "Beyond the scope, powers, or legal authority granted by law or charter.",
        "plain": "An illegal action taken by a company or official outside their legitimate powers.",
        "risk_weight": 2
    },
    "bona fide": {
        "formal": "In good faith; without fraud, deceit, or intent to take unfair advantage.",
        "plain": "Honest, sincere, and genuine intent.",
        "risk_weight": 1
    },
    "caveat emptor": {
        "formal": "Let the buyer beware; the principle that the buyer alone is responsible for checking quality.",
        "plain": "Buyer assumes all risks; the seller does not guarantee perfection unless written.",
        "risk_weight": 2
    },
    "estoppel": {
        "formal": "A legal rule preventing a person from asserting something contrary to what is implied by previous actions.",
        "plain": "You cannot go back on your word or contradictory previous statement.",
        "risk_weight": 2
    },
    "severability": {
        "formal": "A provision that if one clause is found invalid, the remainder of the contract remains in force.",
        "plain": "If a judge invalidates one sentence, the rest of the agreement still survives.",
        "risk_weight": 1
    },
    "arbitration": {
        "formal": "The resolution of disputes outside judicial courts by an impartial third-party arbitrator.",
        "plain": "Settling disagreements in private arbitration instead of going before an open court of law.",
        "risk_weight": 2
    },
    "jurisdiction": {
        "formal": "The practical authority granted to a legal body to administer justice within a defined territory.",
        "plain": "The specific state, city, or court system where any legal battle must take place.",
        "risk_weight": 2
    },
    "joint and several liability": {
        "formal": "Liability shared by two or more parties, where each is independently liable for the full obligation.",
        "plain": "If your partner defaults, the other party can collect 100% of the entire debt solely from you.",
        "risk_weight": 4
    },
    "non-disclosure": {
        "formal": "A binding legal duty to protect proprietary, confidential, or sensitive trade information.",
        "plain": "Strict secrecy requirement; sharing trade secrets or data triggers heavy legal penalties.",
        "risk_weight": 2
    },
    "non-compete": {
        "formal": "A covenant prohibiting a party from engaging in similar business or employment.",
        "plain": "Clause restricting you from working for competitors or starting a competing company.",
        "risk_weight": 3
    },
    "vicarious liability": {
        "formal": "Liability assigned to a party for the torts or omissions of an agent or employee.",
        "plain": "An employer being held legally and financially responsible for their employee's blunders.",
        "risk_weight": 2
    },
    "quantum meruit": {
        "formal": "As much as he has deserved; an equitable remedy awarded for work completed.",
        "plain": "A court ordering reasonable payment for work already performed, even if contract is void.",
        "risk_weight": 1
    },
    "res judicata": {
        "formal": "A matter that has been finally adjudicated on merits and may not be pursued again.",
        "plain": "Case is closed permanently; the same lawsuit cannot be filed a second time.",
        "risk_weight": 1
    },
    "tortfeasor": {
        "formal": "An individual or entity who commits a civil wrong (tort) causing harm or injury.",
        "plain": "The wrongdoer responsible for inflicting damage or breach of civil duty.",
        "risk_weight": 2
    },
    "covenant": {
        "formal": "A formal and solemn binding promise in a deed or other legal instrument.",
        "plain": "A strict mandatory promise or obligation to do (or not do) an action.",
        "risk_weight": 2
    },
    "encumbrance": {
        "formal": "A right to, interest in, or legal liability upon real property.",
        "plain": "A legal claim, lien, or mortgage attached to property that complicates ownership.",
        "risk_weight": 2
    },
    "unilateral termination": {
        "formal": "The power of one contracting party to cancel the agreement without mutual consent.",
        "plain": "One side can cancel the contract at will, potentially leaving the other party stranded.",
        "risk_weight": 4
    }
}

# Legal Clause Categories and Regex Matchers
CLAUSE_DEFINITIONS = {
    "Confidentiality & Non-Disclosure": {
        "icon": "shield-lock",
        "badge_color": "info",
        "description": "Protects trade secrets, proprietary business information, and defines disclosure boundaries.",
        "regex": r"(?i)\b(confidential(?:ity)?|non-disclosure|proprietary\s+information|trade\s+secret|restricted\s+data|secrecy)\b"
    },
    "Indemnification & Hold Harmless": {
        "icon": "shield-check",
        "badge_color": "danger",
        "description": "Shifts legal liability, defense costs, and damage obligations from one party to another.",
        "regex": r"(?i)\b(indemnif(?:y|ication|ied)|hold\s+harmless|defend\s+and\s+indemnify|reimburse\s+against\s+losses)\b"
    },
    "Limitation of Liability": {
        "icon": "exclamation-triangle",
        "badge_color": "warning",
        "description": "Caps monetary damages, consequential losses, or excludes punitive damages.",
        "regex": r"(?i)\b(limitation\s+of\s+liability|aggregate\s+liability|consequential\s+damages|indirect\s+damages|punitive\s+damages|cap\s+on\s+liability)\b"
    },
    "Termination & Cancellation": {
        "icon": "door-open",
        "badge_color": "danger",
        "description": "Defines breach conditions, notice periods, cure intervals, and exit rights.",
        "regex": r"(?i)\b(terminat(?:e|ion)|immediate\s+cancellation|breach\s+of\s+contract|right\s+to\s+terminate|notice\s+of\s+default)\b"
    },
    "Dispute Resolution & Arbitration": {
        "icon": "hammer",
        "badge_color": "primary",
        "description": "Prescribes binding arbitration, mediation procedures, and dispute escalation steps.",
        "regex": r"(?i)\b(arbitrat(?:e|ion)|mediat(?:e|ion)|dispute\s+resolution|arbitral\s+tribunal|amicable\s+settlement)\b"
    },
    "Governing Law & Jurisdiction": {
        "icon": "bank",
        "badge_color": "secondary",
        "description": "Specifies territorial courts and legal framework applicable to enforce the agreement.",
        "regex": r"(?i)\b(governing\s+law|jurisdiction|courts\s+of|applicable\s+law|exclusive\s+jurisdiction|subject\s+to\s+the\s+laws\s+of)\b"
    },
    "Payment Terms & Financial Penalties": {
        "icon": "cash-coin",
        "badge_color": "success",
        "description": "Governs consideration, invoice timelines, milestone disbursements, and interest penalties.",
        "regex": r"(?i)\b(payment\s+terms|invoic(?:e|ing)|consideration|liquidated\s+damages|penalty\s+interest|late\s+fee|disbursement)\b"
    },
    "Force Majeure": {
        "icon": "cloud-lightning",
        "badge_color": "dark",
        "description": "Exempts fulfillment due to acts of God, war, pandemic, embargo, or civil unrest.",
        "regex": r"(?i)\b(force\s+majeure|act\s+of\s+god|unforeseen\s+event|epidemic|war|natural\s+disaster|civil\s+commotion)\b"
    },
    "Intellectual Property & Ownership": {
        "icon": "lightbulb",
        "badge_color": "info",
        "description": "Governs copyrights, patents, trademarks, work-for-hire, and licensing rights.",
        "regex": r"(?i)\b(intellectual\s+property|copyright|patent|trademark|ownership\s+of\s+work|work\s+made\s+for\s+hire|licens(?:e|ing))\b"
    },
    "Non-Compete & Restrictive Covenants": {
        "icon": "person-x",
        "badge_color": "warning",
        "description": "Restricts post-contractual competitive employment, solicitation, or poaching of staff/clients.",
        "regex": r"(?i)\b(non-compete|non-solicitation|restrictive\s+covenant|poaching|restraint\s+of\s+trade)\b"
    },
    "Severability & Survival": {
        "icon": "puzzle",
        "badge_color": "light text-dark",
        "description": "Ensures surviving terms remain enforceable even if specific clauses are struck down.",
        "regex": r"(?i)\b(severability|severable|survival\s+of\s+clauses|entire\s+agreement|merger\s+clause)\b"
    }
}

class LegalKnowledgeEngine:
    def __init__(self):
        self.glossary = LEGAL_GLOSSARY
        self.clause_defs = CLAUSE_DEFINITIONS

    def detect_legalese(self, text):
        """
        Scans document text for complex legal terms and retrieves plain-English explanations.
        Returns: list of dicts with term, formal def, plain def, and detected text snippets.
        """
        detected = []
        text_lower = text.lower()
        
        for term, details in self.glossary.items():
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            if matches:
                # Extract surrounding context snippet (around 120 chars)
                first_match = matches[0]
                start = max(0, first_match.start() - 50)
                end = min(len(text), first_match.end() + 70)
                snippet = text[start:end].replace('\n', ' ').strip()
                
                detected.append({
                    "term": term.title(),
                    "formal": details["formal"],
                    "plain": details["plain"],
                    "occurrences": len(matches),
                    "context_snippet": f"...{snippet}...",
                    "risk_weight": details.get("risk_weight", 1)
                })
                
        # Sort by occurrences and risk weight
        detected.sort(key=lambda x: (x["risk_weight"], x["occurrences"]), reverse=True)
        return detected

    def extract_important_clauses(self, sentences):
        """
        Maps sentences to specific legal clause categories and selects prime clauses.
        Returns: dict of {clause_title: [matching_sentences]}
        """
        extracted = {}
        for category, info in self.clause_defs.items():
            pattern = re.compile(info["regex"])
            matches = []
            
            for sent in sentences:
                if pattern.search(sent):
                    # Clean up
                    clean_sent = sent.strip()
                    if clean_sent not in matches:
                        matches.append(clean_sent)
                        
            if matches:
                extracted[category] = {
                    "icon": info["icon"],
                    "badge_color": info["badge_color"],
                    "description": info["description"],
                    "sentences": matches[:3],  # Top 3 key sentences for this clause
                    "count": len(matches)
                }
                
        return extracted

    def assess_legal_risks(self, text, clauses, legalese):
        """
        Audits contract risks based on high-liability phrasing and missing protections.
        Returns: risk_score (0-100), risk_level ('Low', 'Moderate', 'High', 'Critical'), red_flags list
        """
        risk_score = 15  # Baseline
        red_flags = []
        
        text_lower = text.lower()
        
        # 1. Check for unilateral or uncapped indemnification
        if "indemnif" in text_lower:
            if "unlimited" in text_lower or "sole discretion" in text_lower:
                risk_score += 25
                red_flags.append({
                    "level": "High",
                    "title": "Uncapped or Disproportionate Indemnity",
                    "desc": "The agreement includes broad indemnification obligations without clear reciprocal protections or monetary caps."
                })
            else:
                risk_score += 10
                
        # 2. Check for unilateral termination
        if "terminate immediately" in text_lower or "without cause" in text_lower:
            risk_score += 20
            red_flags.append({
                "level": "High",
                "title": "Unilateral Immediate Termination",
                "desc": "Clauses allowing immediate cancellation without sufficient cure period or formal default notice."
            })
            
        # 3. Check for severe liquidated damages or penalties
        if "liquidated damages" in text_lower or "penalty of" in text_lower:
            risk_score += 15
            red_flags.append({
                "level": "Moderate",
                "title": "Pre-fixed Financial Damages Clause",
                "desc": "Liquidated damages are prescribed which may lead to forfeiture of deposit or automatic financial liability."
            })
            
        # 4. Check for exclusive foreign / restrictive jurisdiction
        if "exclusive jurisdiction" in text_lower:
            risk_score += 10
            red_flags.append({
                "level": "Moderate",
                "title": "Strict Exclusive Legal Forum",
                "desc": "Legal dispute jurisdiction is restricted to a predetermined court, requiring potential travel or out-of-state litigation."
            })
            
        # 5. Check if Limitation of Liability is completely missing
        if "Limitation of Liability" not in clauses:
            risk_score += 15
            red_flags.append({
                "level": "High",
                "title": "Missing Liability Limitation Cap",
                "desc": "No standard limitation of liability clause detected. Potential exposures could technically be unlimited in court."
            })
            
        # 6. Check for Non-Compete restrictions
        if "non-compete" in text_lower or "restraint of trade" in text_lower:
            risk_score += 12
            red_flags.append({
                "level": "Moderate",
                "title": "Post-Contract Restrictive Covenant",
                "desc": "Enforces non-compete covenants that may restrict future employment, client onboarding, or independent practice."
            })
            
        risk_score = min(100, max(5, risk_score))
        
        if risk_score >= 70:
            level = "Critical"
        elif risk_score >= 50:
            level = "High"
        elif risk_score >= 30:
            level = "Moderate"
        else:
            level = "Low"
            
        return {
            "score": risk_score,
            "level": level,
            "flags": red_flags,
            "safety_index": 100 - risk_score
        }
