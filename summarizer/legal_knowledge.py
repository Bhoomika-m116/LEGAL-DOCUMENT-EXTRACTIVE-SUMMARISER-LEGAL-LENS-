import re

# Comprehensive Legal Dictionary: Original + 100 Indian Legal Terms
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
        "plain": "An action taken by a company or official outside their legitimate powers.",
        "risk_weight": 2
    },
    "bona fide": {
        "formal": "In good faith; without fraud, deceit, or intent to take unfair advantage.",
        "plain": "Honest, sincere, and genuine intent.",
        "risk_weight": 1
    },
    "caveat emptor": {
        "formal": "Let the buyer beware; the principle that the buyer alone is responsible for checking quality.",
        "plain": "Buyer assumes certain risks and should examine the property or goods before purchase.",
        "risk_weight": 2
    },
    "estoppel": {
        "formal": "A legal rule preventing a person from asserting something contrary to what is implied by previous actions.",
        "plain": "You cannot go back on your word or contradictory previous statement in circumstances where the law prevents it.",
        "risk_weight": 2
    },
    "severability": {
        "formal": "A provision that if one clause is found invalid, the remainder of the contract remains in force.",
        "plain": "If a judge invalidates one sentence, the rest of the agreement may still survive.",
        "risk_weight": 1
    },
    "arbitration": {
        "formal": "The resolution of disputes outside judicial courts by an impartial third-party arbitrator.",
        "plain": "Settling disagreements through an arbitrator instead of ordinary court proceedings.",
        "risk_weight": 2
    },
    "jurisdiction": {
        "formal": "The practical authority granted to a legal body to administer justice within a defined territory.",
        "plain": "The specific state, city, or court system where a legal case may be heard.",
        "risk_weight": 2
    },
    "joint and several liability": {
        "formal": "Liability shared by two or more parties, where each is independently liable for the full obligation.",
        "plain": "A claimant may be able to recover the entire amount from any one liable party.",
        "risk_weight": 4
    },
    "non-disclosure": {
        "formal": "A binding legal duty to protect proprietary, confidential, or sensitive trade information.",
        "plain": "A secrecy requirement restricting the sharing of confidential information.",
        "risk_weight": 2
    },
    "non-compete": {
        "formal": "A covenant prohibiting a party from engaging in similar business or employment.",
        "plain": "A clause attempting to restrict someone from working for competitors or starting a competing business.",
        "risk_weight": 3
    },
    "vicarious liability": {
        "formal": "Liability assigned to a party for the torts or omissions of an agent or employee.",
        "plain": "An employer being held legally responsible for certain acts of an employee.",
        "risk_weight": 2
    },
    "quantum meruit": {
        "formal": "As much as he has deserved; an equitable remedy awarded for work completed.",
        "plain": "Reasonable payment for work already performed, where legally recoverable.",
        "risk_weight": 1
    },
    "res judicata": {
        "formal": "A matter that has been finally adjudicated on merits and may not be pursued again.",
        "plain": "A matter already finally decided generally cannot be litigated again between the same parties.",
        "risk_weight": 1
    },
    "tortfeasor": {
        "formal": "An individual or entity who commits a civil wrong (tort) causing harm or injury.",
        "plain": "The person or entity responsible for a civil wrong.",
        "risk_weight": 2
    },
    "covenant": {
        "formal": "A formal and solemn binding promise in a deed or other legal instrument.",
        "plain": "A binding promise or obligation to do or not do something.",
        "risk_weight": 2
    },
    "encumbrance": {
        "formal": "A right to, interest in, or legal liability upon real property.",
        "plain": "A legal claim, lien, mortgage, or other burden affecting property.",
        "risk_weight": 2
    },
    "unilateral termination": {
        "formal": "The power of one contracting party to cancel the agreement without mutual consent.",
        "plain": "One side can cancel the contract without obtaining the other side's agreement, subject to the contract and applicable law.",
        "risk_weight": 4
    },

    # ==========================================================
    # 100 ADDITIONAL INDIAN LEGAL TERMS
    # ==========================================================

    # Traditional Indian legal and court terminology (1-20)

    "vakalatnama": {
        "formal": "A written instrument authorising an advocate to represent a party in legal proceedings.",
        "plain": "A document that gives a lawyer permission to represent someone in court.",
        "risk_weight": 1
    },
    "plaint": {
        "formal": "A formal written statement of claim filed by a plaintiff to institute a civil suit.",
        "plain": "The document that starts a civil case by explaining the claimant's allegations and requested relief.",
        "risk_weight": 2
    },
    "written statement": {
        "formal": "A defendant's formal written response to the allegations contained in a plaint.",
        "plain": "The defendant's written reply explaining their side of a civil case.",
        "risk_weight": 2
    },
    "affidavit": {
        "formal": "A written statement of facts sworn or affirmed before an authorised person.",
        "plain": "A written declaration confirmed under oath or affirmation.",
        "risk_weight": 2
    },
    "deposition": {
        "formal": "A formal statement given under oath, generally recorded as evidence.",
        "plain": "A person's statement recorded under oath for legal proceedings.",
        "risk_weight": 2
    },
    "summons": {
        "formal": "A formal court process requiring a person to appear or respond to legal proceedings.",
        "plain": "An official court notice asking someone to appear or reply.",
        "risk_weight": 2
    },
    "warrant": {
        "formal": "A written authorisation issued by a competent judicial authority for a specified legal action.",
        "plain": "An official order authorising a particular legal action, such as an arrest or search.",
        "risk_weight": 3
    },
    "decree": {
        "formal": "The formal expression of an adjudication conclusively determining the rights of parties in a civil suit.",
        "plain": "The court's formal decision determining the legal rights of the parties in a civil case.",
        "risk_weight": 2
    },
    "judgment": {
        "formal": "The statement given by a judge setting out the grounds and reasons for a judicial decision.",
        "plain": "The judge's reasoned decision in a case.",
        "risk_weight": 1
    },
    "order sheet": {
        "formal": "The official court record documenting orders and proceedings on successive hearing dates.",
        "plain": "A record showing what happened and what the court ordered on each hearing date.",
        "risk_weight": 1
    },
    "mahazar": {
        "formal": "A written record prepared by authorised officials or witnesses documenting an inspection, seizure, or other proceedings.",
        "plain": "An official record, commonly used in police and revenue proceedings, describing what was observed or collected.",
        "risk_weight": 2
    },
    "panchnama": {
        "formal": "A contemporaneous record of proceedings prepared in the presence of independent witnesses, commonly called panch witnesses.",
        "plain": "A written record of an inspection, search, or seizure witnessed by independent persons.",
        "risk_weight": 2
    },
    "roznamcha": {
        "formal": "A daily register maintained by an authority to record events, reports, or official proceedings.",
        "plain": "An official daily diary recording events and activities.",
        "risk_weight": 1
    },
    "darkhast": {
        "formal": "An application or petition submitted to a competent authority seeking a specified legal or administrative remedy.",
        "plain": "A formal application requesting an authority to take action or grant relief.",
        "risk_weight": 1
    },
    "vakil": {
        "formal": "A legal representative or advocate authorised to act on behalf of a client.",
        "plain": "A lawyer who represents someone in legal matters.",
        "risk_weight": 1
    },
    "mukhtarnama": {
        "formal": "A written instrument authorising another person to act on behalf of its executant.",
        "plain": "A document giving another person authority to act for you.",
        "risk_weight": 2
    },
    "sanad": {
        "formal": "An official certificate, grant, or instrument recognising a right, status, or authority.",
        "plain": "An official document proving a particular grant, qualification, or recognised right.",
        "risk_weight": 1
    },
    "kabuliat": {
        "formal": "A written acceptance or undertaking, historically used in land revenue and tenancy arrangements.",
        "plain": "A written acceptance of specified conditions, often connected with land or tenancy.",
        "risk_weight": 2
    },
    "taluk": {
        "formal": "An administrative subdivision of a district used for revenue and local administration.",
        "plain": "A local administrative area within a district.",
        "risk_weight": 1
    },
    "tehsildar": {
        "formal": "A revenue officer responsible for specified land revenue and administrative functions within a tehsil.",
        "plain": "A government officer who handles certain land and revenue matters.",
        "risk_weight": 1
    },

    # Indian land and property terminology (21-45)

    "khasra": {
        "formal": "A land-record identifier or register describing individual agricultural plots and related particulars.",
        "plain": "A number or record used to identify a particular piece of land.",
        "risk_weight": 2
    },
    "khata": {
        "formal": "A revenue account or property account recording land or property holdings.",
        "plain": "An official account identifying property holdings for revenue or municipal purposes.",
        "risk_weight": 2
    },
    "khatauni": {
        "formal": "A revenue record containing details of cultivators, tenure holders, and land holdings.",
        "plain": "A government land record showing who holds or cultivates particular land.",
        "risk_weight": 2
    },
    "jamabandi": {
        "formal": "A record of rights maintained in certain states containing ownership, tenancy, and land revenue particulars.",
        "plain": "An official record showing land ownership and related revenue details.",
        "risk_weight": 2
    },
    "fard": {
        "formal": "An extract or certified copy of relevant entries from land or revenue records.",
        "plain": "A government-issued copy of land-record information.",
        "risk_weight": 2
    },
    "girdawari": {
        "formal": "A periodic revenue inspection record documenting crop cultivation and possession particulars.",
        "plain": "A land record showing what crops are being grown and who is cultivating the land.",
        "risk_weight": 1
    },
    "patta": {
        "formal": "An instrument or official grant evidencing a right to occupy, possess, or hold specified land.",
        "plain": "An official document granting or recording rights over a piece of land.",
        "risk_weight": 3
    },
    "mutation": {
        "formal": "The process of recording a change in ownership or interest in revenue records following a relevant transaction or event.",
        "plain": "Updating government land records when property ownership changes.",
        "risk_weight": 2
    },
    "record of rights": {
        "formal": "An official revenue record containing particulars of landholders, rights, liabilities, and interests in land.",
        "plain": "A government record showing who holds rights over a particular property.",
        "risk_weight": 2
    },
    "encumbrance certificate": {
        "formal": "A certificate recording registered transactions affecting a property during a specified period.",
        "plain": "A document used to check registered transactions and certain financial or legal claims connected with property.",
        "risk_weight": 3
    },
    "sale deed": {
        "formal": "A registered instrument evidencing the transfer of ownership of immovable property by sale.",
        "plain": "The legal document recording the sale and transfer of property ownership.",
        "risk_weight": 3
    },
    "gift deed": {
        "formal": "A legal instrument recording a voluntary transfer of existing property without consideration, subject to applicable law.",
        "plain": "A document used to legally give property to another person without payment.",
        "risk_weight": 2
    },
    "partition deed": {
        "formal": "An instrument recording the division of jointly held property among persons entitled to shares.",
        "plain": "A document that records how shared property is divided among its owners.",
        "risk_weight": 3
    },
    "release deed": {
        "formal": "An instrument by which a person releases or relinquishes a right or interest in favour of another.",
        "plain": "A document through which someone gives up their legal share or claim in property.",
        "risk_weight": 3
    },
    "relinquishment deed": {
        "formal": "A legal instrument by which a person voluntarily gives up an existing right or share in property.",
        "plain": "A document recording that someone gives up their share in a property.",
        "risk_weight": 3
    },
    "lease deed": {
        "formal": "An instrument creating or recording the transfer of a right to enjoy immovable property for a specified period in consideration of rent or other value.",
        "plain": "A legal document allowing someone to use a property for an agreed period in return for rent or other consideration.",
        "risk_weight": 2
    },
    "rent agreement": {
        "formal": "An agreement recording the terms and conditions governing a tenancy or rental arrangement.",
        "plain": "A written agreement between a landlord and tenant explaining rent, duration, and responsibilities.",
        "risk_weight": 2
    },
    "power of attorney": {
        "formal": "A legal instrument authorising another person to act on behalf of the executant within specified powers.",
        "plain": "A document allowing someone to handle specified legal or financial matters on another person's behalf.",
        "risk_weight": 3
    },
    "general power of attorney": {
        "formal": "An instrument conferring broad specified agency powers upon an appointed attorney.",
        "plain": "A document giving another person several specified powers to act on your behalf.",
        "risk_weight": 3
    },
    "special power of attorney": {
        "formal": "An instrument granting authority to an attorney for a particular transaction or specified purpose.",
        "plain": "A document giving someone permission to handle one particular task or transaction.",
        "risk_weight": 2
    },
    "easement": {
        "formal": "A right enjoyed by one landowner over another person's land for a specified purpose.",
        "plain": "A legal right to use another person's land in a limited way, such as a pathway.",
        "risk_weight": 2
    },
    "adverse possession": {
        "formal": "A doctrine under which possession meeting legally prescribed conditions may result in acquisition of title.",
        "plain": "In certain circumstances, long and legally qualifying possession may lead to a claim of ownership.",
        "risk_weight": 4
    },
    "lis pendens": {
        "formal": "The doctrine that a transfer of property during pending litigation is subject to the outcome of that litigation.",
        "plain": "Property involved in an ongoing court case cannot generally be transferred free from the result of that case.",
        "risk_weight": 3
    },
    "ancestral property": {
        "formal": "Property classified as ancestral under applicable personal and succession law principles.",
        "plain": "Property that may have passed through generations and may carry inheritance rights.",
        "risk_weight": 3
    },
    "benami transaction": {
        "formal": "A transaction falling within the statutory definition of a benami transaction under Indian law.",
        "plain": "A property arrangement in which the person providing consideration and the person in whose name it is held may differ, subject to statutory exceptions.",
        "risk_weight": 4
    },

    # Indian civil, family and succession terminology (46-65)

    "stridhan": {
        "formal": "Property recognised under applicable Hindu law as belonging to a woman, subject to the governing legal principles.",
        "plain": "Property and gifts that legally belong to a woman in her own right.",
        "risk_weight": 2
    },
    "coparcenary": {
        "formal": "A form of joint family ownership recognised under Hindu law in which coparceners acquire specified rights by birth.",
        "plain": "A legal family property arrangement in which qualifying family members have rights in ancestral joint family property.",
        "risk_weight": 3
    },
    "succession": {
        "formal": "The devolution of a deceased person's estate upon persons entitled under applicable law or a valid testament.",
        "plain": "The legal process of passing a deceased person's property to heirs or beneficiaries.",
        "risk_weight": 2
    },
    "probate": {
        "formal": "A judicial grant establishing the validity of a will and authorising administration by the executor where required.",
        "plain": "A court process that confirms a will and recognises the executor's authority where applicable.",
        "risk_weight": 2
    },
    "letters of administration": {
        "formal": "A grant issued by a competent court authorising a person to administer the estate of a deceased person.",
        "plain": "A court document giving someone authority to manage a deceased person's estate.",
        "risk_weight": 2
    },
    "succession certificate": {
        "formal": "A certificate granted by a competent court authorising collection of specified debts and securities of a deceased person.",
        "plain": "A court-issued certificate that helps an entitled person collect certain debts and financial securities.",
        "risk_weight": 2
    },
    "legal heir certificate": {
        "formal": "An administrative certificate identifying persons recognised as legal heirs for specified official purposes.",
        "plain": "A government certificate identifying the legal heirs of a deceased person.",
        "risk_weight": 2
    },
    "will": {
        "formal": "A legal declaration of a person's intention concerning the disposition of property after death.",
        "plain": "A document stating who should receive someone's property after their death.",
        "risk_weight": 2
    },
    "codicil": {
        "formal": "A supplementary testamentary instrument made to explain, alter, or add to a will.",
        "plain": "A legal document that changes or adds instructions to an existing will.",
        "risk_weight": 2
    },
    "testator": {
        "formal": "A person who makes a will.",
        "plain": "The person who creates a will.",
        "risk_weight": 1
    },
    "executor": {
        "formal": "A person appointed under a will to carry out its provisions and administer the estate.",
        "plain": "The person responsible for carrying out the instructions in a will.",
        "risk_weight": 2
    },
    "beneficiary": {
        "formal": "A person entitled to receive a benefit, property, or interest under a legal instrument or arrangement.",
        "plain": "A person who receives property, money, or another benefit.",
        "risk_weight": 1
    },
    "maintenance": {
        "formal": "Financial support legally payable to a person entitled to claim it under applicable law.",
        "plain": "Money that a person may be legally required to provide for another person's support.",
        "risk_weight": 2
    },
    "alimony": {
        "formal": "Financial support payable by one spouse to another pursuant to a court order or legally recognised arrangement.",
        "plain": "Financial support that may be ordered for a spouse after separation or divorce.",
        "risk_weight": 2
    },
    "restitution of conjugal rights": {
        "formal": "A matrimonial remedy under which a spouse may seek a decree requiring the other spouse to resume cohabitation, subject to applicable law.",
        "plain": "A legal remedy through which a spouse asks the court to order the other spouse to resume marital cohabitation.",
        "risk_weight": 3
    },
    "guardianship": {
        "formal": "The legal authority and responsibility to care for a minor or person requiring a guardian, as determined under applicable law.",
        "plain": "Legal responsibility for looking after a child or another person who needs a guardian.",
        "risk_weight": 2
    },
    "adoption deed": {
        "formal": "An instrument recording an adoption where such documentation is recognised or required under applicable law.",
        "plain": "A document recording the legal adoption of a child where applicable.",
        "risk_weight": 2
    },
    "partition": {
        "formal": "The division of jointly held property into separate shares or interests among persons entitled to it.",
        "plain": "Dividing jointly owned property among the people who have rights in it.",
        "risk_weight": 3
    },
    "injunction": {
        "formal": "A judicial order directing a party to perform or refrain from performing a specified act.",
        "plain": "A court order requiring someone to do something or stop doing something.",
        "risk_weight": 3
    },
    "specific performance": {
        "formal": "An equitable remedy compelling performance of a contractual obligation where legally available.",
        "plain": "A court order requiring a party to fulfil a contract rather than merely pay damages.",
        "risk_weight": 3
    },

    # Indian criminal and procedural terminology (66-85)

    "first information report": {
        "formal": "Information recorded by police under the applicable criminal procedure law concerning a cognizable offence.",
        "plain": "The initial police report recording information about a suspected cognizable offence.",
        "risk_weight": 3
    },
    "charge sheet": {
        "formal": "A police report submitted to the competent court upon completion of investigation, as provided by criminal procedure law.",
        "plain": "A formal police report filed after investigation describing the alleged offence and evidence.",
        "risk_weight": 3
    },
    "cognizable offence": {
        "formal": "An offence for which police may arrest without warrant and investigate without prior court order, as provided by law.",
        "plain": "A category of offence where police have specific powers to arrest and investigate without first obtaining a court warrant or order.",
        "risk_weight": 3
    },
    "non-cognizable offence": {
        "formal": "An offence for which police generally cannot arrest without warrant and require the prescribed judicial order to investigate.",
        "plain": "An offence where police investigation generally requires permission from the competent magistrate.",
        "risk_weight": 2
    },
    "bailable offence": {
        "formal": "An offence classified as bailable under the applicable criminal procedure law.",
        "plain": "An offence for which bail is generally available as a legal right, subject to statutory requirements.",
        "risk_weight": 2
    },
    "non-bailable offence": {
        "formal": "An offence classified as non-bailable under the applicable criminal procedure law.",
        "plain": "An offence where bail is decided by the competent court or authority under applicable legal conditions.",
        "risk_weight": 3
    },
    "anticipatory bail": {
        "formal": "A direction for release on bail in anticipation of arrest, granted under the applicable criminal procedure law.",
        "plain": "A court order protecting an eligible person from being taken into custody in specified circumstances if arrested.",
        "risk_weight": 3
    },
    "regular bail": {
        "formal": "An order releasing an accused person from custody subject to conditions imposed by a competent court.",
        "plain": "Court-approved release from custody while the case continues, subject to conditions.",
        "risk_weight": 2
    },
    "remand": {
        "formal": "An order authorising continued custody of an accused person under the applicable criminal procedure law.",
        "plain": "A court-authorised period during which an accused person remains in custody.",
        "risk_weight": 3
    },
    "surety": {
        "formal": "A person who undertakes legal responsibility for the fulfilment of specified bail or bond conditions.",
        "plain": "A person who promises to ensure that an accused person follows the court's bail conditions.",
        "risk_weight": 2
    },
    "bail bond": {
        "formal": "A bond executed to secure release on bail and compliance with prescribed conditions.",
        "plain": "A legal undertaking given for release from custody, with conditions that must be followed.",
        "risk_weight": 3
    },
    "seizure memo": {
        "formal": "A written record documenting the seizure of property or articles by an authorised official.",
        "plain": "An official document listing items taken by police or another authorised authority.",
        "risk_weight": 2
    },
    "search warrant": {
        "formal": "A judicial authorisation permitting a search in accordance with statutory requirements.",
        "plain": "A court-issued permission to search a specified place or property.",
        "risk_weight": 3
    },
    "arrest memo": {
        "formal": "A record documenting the arrest of an individual and relevant particulars of the arrest.",
        "plain": "An official record showing when and under what circumstances a person was arrested.",
        "risk_weight": 2
    },
    "prosecution": {
        "formal": "The institution and conduct of criminal proceedings against an accused person before a competent court.",
        "plain": "The legal process of presenting a criminal case against an accused person.",
        "risk_weight": 2
    },
    "acquittal": {
        "formal": "A judicial determination that an accused person is not guilty of the charge.",
        "plain": "A court decision finding that the accused is not guilty.",
        "risk_weight": 1
    },
    "conviction": {
        "formal": "A judicial finding that an accused person is guilty of an offence.",
        "plain": "A court's decision that a person is guilty of an offence.",
        "risk_weight": 3
    },
    "compounding of offence": {
        "formal": "The lawful settlement of specified offences by the prescribed persons in accordance with statutory provisions.",
        "plain": "Settling certain offences through a legally permitted compromise.",
        "risk_weight": 2
    },
    "quashing of proceedings": {
        "formal": "The setting aside of criminal proceedings by a competent court exercising its lawful jurisdiction.",
        "plain": "A higher court cancels legal proceedings where the law permits it.",
        "risk_weight": 3
    },
    "discharge": {
        "formal": "A judicial order releasing an accused from a criminal charge at the relevant procedural stage where grounds are established.",
        "plain": "A court decision ending the case against an accused person at an appropriate stage because the legal requirements for proceeding are not met.",
        "risk_weight": 2
    },

    # Indian administrative, revenue and constitutional terminology (86-100)

    "gram panchayat": {
        "formal": "A village-level institution of local self-government constituted under applicable state Panchayat laws.",
        "plain": "The elected local government body responsible for administration in a village.",
        "risk_weight": 1
    },
    "municipal khata": {
        "formal": "A municipal property-account entry maintained for taxation and civic administration purposes.",
        "plain": "A municipal record used to identify a property for local tax and administrative purposes.",
        "risk_weight": 2
    },
    "property tax assessment": {
        "formal": "The determination of the taxable value or tax liability of property by the competent local authority.",
        "plain": "The process of calculating the property tax payable to the local authority.",
        "risk_weight": 2
    },
    "stamp duty": {
        "formal": "A duty imposed by law on specified instruments and transactions, payable in the prescribed manner.",
        "plain": "A government charge payable on certain legal documents and property transactions.",
        "risk_weight": 3
    },
    "registration deed": {
        "formal": "An instrument presented for registration under applicable registration laws to record a transaction or legal right.",
        "plain": "A legal document registered with the relevant government registration office.",
        "risk_weight": 2
    },
    "sub-registrar": {
        "formal": "An officer appointed under registration law to perform statutory registration functions within an assigned jurisdiction.",
        "plain": "A government officer who registers property documents and certain other legal instruments.",
        "risk_weight": 1
    },
    "circle rate": {
        "formal": "A minimum value notified by the relevant authority for specified property transactions and valuation purposes.",
        "plain": "A government-notified minimum property value used for certain registration and stamp-duty calculations.",
        "risk_weight": 2
    },
    "guidance value": {
        "formal": "A value notified by the competent state authority for property valuation and registration-related purposes.",
        "plain": "The government reference value used for certain property registration and stamp-duty purposes.",
        "risk_weight": 2
    },
    "land acquisition": {
        "formal": "The compulsory acquisition of land by the state or authorised body in accordance with applicable law.",
        "plain": "The government legally obtains private land for a permitted public purpose, subject to legal safeguards and compensation rules.",
        "risk_weight": 4
    },
    "right of way": {
        "formal": "A legal right to pass through or across another person's land under an applicable grant, easement, or law.",
        "plain": "A legal right to use a route across someone else's property.",
        "risk_weight": 2
    },
    "public notice": {
        "formal": "A notice published or displayed to inform the public of a matter in accordance with legal requirements.",
        "plain": "An official announcement informing the public about a legal or administrative matter.",
        "risk_weight": 1
    },
    "show cause notice": {
        "formal": "A notice requiring a person to explain why a proposed action should not be taken against them.",
        "plain": "An official notice asking someone to explain their actions before a decision is made.",
        "risk_weight": 3
    },
    "natural justice": {
        "formal": "Fundamental principles of fair procedure, including impartial decision-making and an opportunity to be heard.",
        "plain": "The principle that decisions should be fair and that affected people should get an opportunity to explain their side.",
        "risk_weight": 2
    },
    "writ petition": {
        "formal": "A petition invoking the constitutional writ jurisdiction of a competent High Court or the Supreme Court.",
        "plain": "A petition asking a constitutional court to protect legal or fundamental rights through an appropriate writ.",
        "risk_weight": 3
    },
    "mandamus": {
        "formal": "A writ issued by a competent court directing a public authority to perform a public or statutory duty.",
        "plain": "A court order requiring a public authority to perform a legal duty.",
        "risk_weight": 2
    }
}
