# Gary Abel — Part 2

**Script:** `gary_abel_screen.py` (attached separately)

**What it implements:**
- ORF prediction across all 6 reading frames using Biopython
- BLASTn against the NCBI nucleotide (nt) database via Biopython's `NCBIWWW.qblast`

BLASTx was attempted but returned an SSL connection error from NCBI during this run. The ORF and BLASTn results are sufficient for a first-stage conclusion.

---

**Input:** The 288 bp mystery sequence passed as `SEQUENCE` in the script.

---

**Output:**

```
Mystery sequence length: 288 bp

============================================================
STEP 3: ORF prediction (all 6 reading frames)
============================================================

ORFs with at least 20 amino acids:

  Strand +, Frame 1: 96 aa | nt 1-288 | starts: MNQHNTQINK...
  Strand -, Frame 1: 96 aa | nt 1-288 | starts: MGLVHIRSHK...
  Strand -, Frame 2: 30 aa | nt 53-142 | starts: MLVIVKKVIL...
  Strand -, Frame 2: 20 aa | nt 83-142 | starts: MVLFVKLGIL...

============================================================
STEP 1: BLASTn against NCBI nucleotide (nt) database
============================================================

Top 5 BLASTn hits:

  Hit 1: Drosophila persimilis (XM_002015294.2)
    Score: 59  E-value: 1.72e-02
    Identity: 37/42 (88.1%)  Query range: 99-140

  Hit 2: Saccharomyces eubayanus 1-phosphatidylinositol (XM_018364852.1)
    Score: 59  E-value: 1.72e-02
    Identity: 46/57 (80.7%)  Query range: 84-140

  Hit 3: Ceratitis capitata phosphatase (XM_020862195.1)
    Score: 58  E-value: 1.72e-02
    Identity: 52/65 (80.0%)  Query range: 99-160

  Hit 4: Macadamia integrifolia receptor-like (XM_042655854.1)
    Score: 58  E-value: 1.72e-02
    Identity: 55/71 (77.5%)  Query range: 60-126

  Hit 5: Ceratitis capitata phosphatase (XM_020862197.1)
    Score: 58  E-value: 1.72e-02
    Identity: 52/65 (80.0%)  Query range: 99-160
```

---

**What I can conclude:**

**ORF prediction:** The sequence encodes a plausible open reading frame spanning the full 288 bp in the forward strand (Frame 1, 96 aa, starting MNQHNTQINK). The very low GC content and repetitive codon structure are notable. This could reflect an organism with an AT-rich genome, or a synthetic or codon-optimized construct.

**BLASTn results:** All five hits have E-values of 1.72e-02 and cover only short fragments (42-71 bp out of 288 bp). This is not statistically significant. The organisms matched — Drosophila, Saccharomyces, Ceratitis fruit fly, Macadamia — are all non-pathogenic. These hits represent chance partial similarity, not a meaningful sequence match.

**Flagging decision:** I would not flag this sequence based on these results alone. The absence of a significant database match raises the question of whether the sequence is engineered or from an under-sequenced organism, which warrants continued investigation. The next steps would be BLASTx on the translated ORF and domain analysis in Pfam or InterPro. Under the criterion from Part 1, a flag requires multiple steps converging on a high-confidence dangerous identification. That threshold is not met here.

---

**AI use note:** Claude (Sonnet 4.6) assisted in drafting and structuring the script. I directed which steps to implement, the choice of E-value thresholds for interpretation, the biological reading of the ORF result, and the flagging decision logic — all of which reflect my own judgment and prior work on biosecurity screening tool evaluation (Krishnan et al., 2026).
