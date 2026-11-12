/**
 * OFFICIAL LEGAL PORTAL - JAVASCRIPT ENGINE
 * Handles: TTS Audio Narrator, Live Accuracy Counter, Sample Loaders, Clipboard
 */

document.addEventListener('DOMContentLoaded', function () {
    initAccuracyCounter();
    initSpeechSynthesis();
    initSummarySlider();
    initDropzone();
});

// 1. Smooth Animated Counter for Extractive Accuracy Score
function initAccuracyCounter() {
    const counterElem = document.getElementById('accuracyCounter');
    if (!counterElem) return;

    const targetVal = parseFloat(counterElem.getAttribute('data-target') || '0');
    let currentVal = 0;
    const duration = 1400; // ms
    const stepTime = 20;
    const increment = targetVal / (duration / stepTime);

    const timer = setInterval(() => {
        currentVal += increment;
        if (currentVal >= targetVal) {
            currentVal = targetVal;
            clearInterval(timer);
        }
        counterElem.innerText = currentVal.toFixed(1) + '%';
    }, stepTime);
}

// 2. Web Speech API - Legal Executive Summary Audio Narrator
let speechUtterance = null;
let isSpeaking = false;
let isPaused = false;

function initSpeechSynthesis() {
    const playBtn = document.getElementById('playTtsBtn');
    const pauseBtn = document.getElementById('pauseTtsBtn');
    const stopBtn = document.getElementById('stopTtsBtn');

    if (!playBtn) return;

    if (!('speechSynthesis' in window)) {
        const widget = document.getElementById('audioWidget');
        if (widget) widget.style.display = 'none';
        return;
    }

    playBtn.addEventListener('click', function () {
        const summaryElem = document.getElementById('summaryContentText');
        if (!summaryElem) return;

        const textToRead = summaryElem.innerText;

        if (isPaused) {
            window.speechSynthesis.resume();
            isPaused = false;
            isSpeaking = true;
            updateTtsUI('playing');
            return;
        }

        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
        }

        speechUtterance = new SpeechSynthesisUtterance(textToRead);
        speechUtterance.rate = 0.95; // Official clear cadence
        speechUtterance.pitch = 1.0;

        // Try to pick natural English voice
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('David')));
        if (preferredVoice) {
            speechUtterance.voice = preferredVoice;
        }

        speechUtterance.onstart = function () {
            isSpeaking = true;
            isPaused = false;
            updateTtsUI('playing');
        };

        speechUtterance.onend = function () {
            isSpeaking = false;
            isPaused = false;
            updateTtsUI('stopped');
        };

        speechUtterance.onerror = function () {
            isSpeaking = false;
            isPaused = false;
            updateTtsUI('stopped');
        };

        window.speechSynthesis.speak(speechUtterance);
    });

    if (pauseBtn) {
        pauseBtn.addEventListener('click', function () {
            if (window.speechSynthesis.speaking && !isPaused) {
                window.speechSynthesis.pause();
                isPaused = true;
                isSpeaking = false;
                updateTtsUI('paused');
            }
        });
    }

    if (stopBtn) {
        stopBtn.addEventListener('click', function () {
            if (window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
            }
            isSpeaking = false;
            isPaused = false;
            updateTtsUI('stopped');
        });
    }
}

function updateTtsUI(state) {
    const statusText = document.getElementById('ttsStatusText');
    const playBtn = document.getElementById('playTtsBtn');
    if (!statusText || !playBtn) return;

    if (state === 'playing') {
        statusText.innerHTML = '<span class="badge bg-success"><i class="bi bi-volume-up-fill me-1"></i>Narrating Summary...</span>';
        playBtn.classList.add('btn-light');
        playBtn.classList.remove('btn-outline-light');
    } else if (state === 'paused') {
        statusText.innerHTML = '<span class="badge bg-warning text-dark"><i class="bi bi-pause-fill me-1"></i>Narration Paused</span>';
    } else {
        statusText.innerHTML = '<span class="badge bg-secondary"><i class="bi bi-headphones me-1"></i>Audio Voice Ready</span>';
        playBtn.classList.add('btn-outline-light');
        playBtn.classList.remove('btn-light');
    }
}

// 3. Interactive Summary Ratio Slider
function initSummarySlider() {
    const slider = document.getElementById('summaryRatioSlider');
    const label = document.getElementById('summaryRatioLabel');
    if (!slider || !label) return;

    slider.addEventListener('input', function () {
        const val = Math.round(parseFloat(slider.value) * 100);
        let desc = "Balanced Executive (25%)";
        if (val <= 15) desc = "Concise Abstract (" + val + "%)";
        else if (val <= 30) desc = "Balanced Executive (" + val + "%)";
        else desc = "Comprehensive In-Depth (" + val + "%)";
        label.innerText = desc;
    });
}

// 4. File Dropzone & Drag Events
function initDropzone() {
    const dropzone = document.getElementById('fileDropzone');
    const fileInput = document.getElementById('documentFileInput');
    const fileInfo = document.getElementById('selectedFileInfo');
    if (!dropzone || !fileInput) return;

    dropzone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.add('drag-active');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.remove('drag-active');
        }, false);
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            showFileSelection(files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            showFileSelection(fileInput.files[0]);
        }
    });

    function showFileSelection(file) {
        if (fileInfo) {
            const sizeKB = (file.size / 1024).toFixed(1);
            fileInfo.innerHTML = `
                <div class="alert alert-success d-flex align-items-center justify-content-between p-2 mt-2 mb-0">
                    <div>
                        <i class="bi bi-file-earmark-check-fill text-success fs-5 me-2"></i>
                        <strong>${file.name}</strong> (${sizeKB} KB)
                    </div>
                    <span class="badge bg-primary">Ready to Extract</span>
                </div>
            `;
        }
    }
}

// 5. One-Click Copy Summary
function copySummaryToClipboard() {
    const summaryElem = document.getElementById('summaryContentText');
    if (!summaryElem) return;

    navigator.clipboard.writeText(summaryElem.innerText).then(() => {
        const copyBtn = document.getElementById('copyBtnText');
        if (copyBtn) {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="bi bi-check-lg me-1 text-success"></i>Copied!';
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
            }, 2500);
        }
    });
}

// 6. Realistic Legal Sample Document Loader
const SAMPLE_CONTRACTS = {
    nda: `NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

This Non-Disclosure Agreement (the "Agreement") is entered into on this 14th day of October, 2026, by and between Apex Global Solutions Ltd., having its principal office at Financial Towers, Bangalore (hereinafter referred to as the "Disclosing Party"), and CyberCore Technologies Pvt. Ltd., having its registered office at Cyber City, Hyderabad (hereinafter referred to as the "Receiving Party").

WHEREAS, the Disclosing Party possesses certain proprietary trade secrets, proprietary software code algorithms, source data, client portfolios, and confidential commercial evaluations relating to AI document intelligence; and

WHEREAS, the Receiving Party wishes to evaluate potential commercial collaboration and joint licensing, wherein confidential information shall necessarily be disclosed.

NOW, THEREFORE, the parties hereby agree as follows:

1. DEFINITION OF CONFIDENTIAL INFORMATION.
"Confidential Information" shall include all technical, financial, operational, and business data disclosed by the Disclosing Party, whether in oral, written, graphic, or digital form, which is designated as confidential or which reasonably ought to be understood as confidential.

2. OBLIGATIONS OF RECEIVING PARTY.
The Receiving Party agrees to hold and maintain all Confidential Information in strictest confidence. The Receiving Party shall not, without the prior written consent of the Disclosing Party, publish, copy, transmit, reverse engineer, or disclose any Confidential Information to any third party. The Receiving Party agrees to restrict access to Confidential Information strictly to employees who have a bona fide need to know and who are bound by non-disclosure covenants at least as restrictive as this Agreement.

3. INDEMNIFICATION AND LIQUIDATED DAMAGES.
The Receiving Party shall indemnify, defend, and hold harmless the Disclosing Party, its directors, officers, and agents against all losses, damages, liabilities, costs, and attorney fees incurred as a consequence of any breach of confidentiality. In the event of an intentional or unauthorized breach, the Receiving Party agrees to pay liquidated damages of Rs. 25,00,000 without prejudice to the Disclosing Party's right to seek urgent injunctive relief.

4. TERM AND TERMINATION.
This Agreement shall remain in effect for a term of three (3) years from the effective date. Either party may terminate discussions at any time upon thirty (30) days written notice; provided, however, that obligations regarding trade secrets and confidential information shall survive termination in perpetuity.

5. DISPUTE RESOLUTION AND ARBITRATION.
Any controversy or claim arising out of or relating to this Agreement shall be settled by binding arbitration in accordance with the Arbitration and Conciliation Act, 1996. The seat and venue of arbitration shall be Bangalore, Karnataka, India, and proceedings shall be conducted in English by a sole arbitrator mutually appointed by the parties.

6. GOVERNING LAW AND SEVERABILITY.
This Agreement shall be governed by and construed in accordance with the substantive laws of India. If any provision is held invalid or ultra vires by a court of competent jurisdiction, the remaining provisions mutatis mutandis shall continue in full force and effect.`,

    lease: `COMMERCIAL LEASE AND PREMISES AGREEMENT

THIS LEASE AGREEMENT is made and executed on the 1st day of November, 2026, by and between Royal Heights Realty Corporation (hereinafter called the "LESSOR") of the One Part, and Zenith Legal Associates LLP (hereinafter called the "LESSEE") of the Other Part.

1. DEMISED PREMISES AND TERM.
The Lessor hereby demises and leases to the Lessee Office Suite No. 402, measuring approximately 3,500 square feet, located at Supreme Judicial Enclave, New Delhi, for a fixed term of thirty-six (36) consecutive months commencing on November 15, 2026.

2. MONTHLY RENT AND SECURITY DEPOSIT.
The Lessee shall pay to the Lessor a monthly base rent of Rs. 1,85,000 payable in advance on or before the 5th day of each calendar month. The Lessee has furnished an interest-free refundable security deposit of Rs. 11,10,000. Late payments beyond the grace period shall incur liquidated interest penalties at 18% per annum.

3. COVENANTS AND RESTRICTIONS.
The Lessee covenants that the demised premises shall be utilized exclusively for lawful legal advisory and corporate consultancy services. The Lessee shall not assign, sublet, or create any third-party encumbrance or lien upon the premises without prior written consent from the Lessor.

4. INDEMNITY AND LIMITATION OF LIABILITY.
The Lessee agrees to indemnify and hold harmless the Lessor from all claims, civil actions, tortfeasor suits, and liabilities arising from the Lessee's use or negligence within the demised premises. The Lessor's aggregate liability under any circumstance shall be capped strictly at the equivalent of three months' rent.

5. FORCE MAJEURE AND TERMINATION.
Neither party shall be held liable for delay or default occasioned by acts of God, epidemic, war, earthquake, or governmental lockdown. Either party may terminate this lease by providing ninety (90) days advance written notice; provided that default of rent exceeding sixty days empowers the Lessor to initiate immediate unilateral termination and re-entry.

6. GOVERNING LAW AND JURISDICTION.
This Agreement is subject to the exclusive jurisdiction of the Courts of Delhi, India, in accordance with applicable tenancy legislation.`,

    sla: `ENTERPRISE SOFTWARE LICENSE AND SERVICE LEVEL AGREEMENT (SLA)

BETWEEN: NexusCloud Enterprise Systems Inc. ("Vendor") AND Horizon Banking Syndicate ("Client").

1. GRANT OF LICENSE.
Vendor hereby grants to Client a non-exclusive, non-transferable, revocable license to access and deploy the Nexus Legal Automation Suite solely for Client's internal operational requirements. Client shall not decompile, dissemble, or create derivative works.

2. SERVICE LEVEL WARRANTIES AND GUARANTEED UPTIME.
Vendor warrants a minimum 99.9% application availability during each calendar month. In the event of service disruption exceeding acceptable thresholds, Client shall be entitled to service credit disbursements equivalent to 10% of monthly licensing fees.

3. INDEMNIFICATION OF INTELLECTUAL PROPERTY.
Vendor shall defend, indemnify, and hold harmless Client against any third-party legal claims asserting that the software infringes any valid patent, copyright, or trademark.

4. MUTUAL LIMITATION OF LIABILITY.
In no event shall either party be liable for any indirect, incidental, punitive, or consequential damages, or loss of profits. The maximum total liability of either party under this agreement shall not exceed the fees paid in the preceding twelve (12) months.

5. GOVERNING LAW AND ARBITRATION.
This Agreement shall be governed by the laws of India. All disputes shall be finally resolved through expedited arbitration under Indian Arbitration rules.`
};

function loadSampleDocument(type) {
    const textArea = document.getElementById('documentTextArea');
    if (!textArea) return;

    if (SAMPLE_CONTRACTS[type]) {
        textArea.value = SAMPLE_CONTRACTS[type];
        textArea.focus();
        // Visual indicator
        textArea.classList.add('border-primary');
        setTimeout(() => textArea.classList.remove('border-primary'), 800);
    }
}
