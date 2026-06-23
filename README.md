# DNA Sequence Screening Exercise — Part 2

## What the script does

`sequence_screen.py` takes a 280+ bp mystery sequence as input and runs two investigation steps.

**Step 1 — ORF prediction** across all 6 reading frames using Biopython. This identifies whether the sequence plausibly encodes a protein and in which frame.

**Step 2 — BLASTn** against the NCBI nucleotide database via Biopython's `NCBIWWW.qblast`. This checks for nucleotide-level matches to any known organism or gene.

BLASTx was also attempted but returned an SSL connection error from NCBI during this run. The ORF and BLASTn results are sufficient for a first-stage conclusion.

## Dependency

```
pip install biopython
```

Replace the email placeholder in the script with a valid email address. NCBI requires this for Entrez queries but no API key is needed.

## Input

The 288 bp mystery sequence is hardcoded as `SEQUENCE` in the script. It can be replaced with any sequence of interest.

## Output

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

## Interpretation

**ORF prediction.** The sequence encodes a plausible open reading frame across the full 288 bp in the forward strand (Frame 1, 96 aa, starting MNQHNTQINK). The very low GC content and repetitive codon structure are notable. This could reflect an organism with an AT-rich genome or a synthetic, codon-optimized construct.

**BLASTn results.** All five hits have E-values of 1.72e-02 and cover only short fragments (42-71 bp) of the 288 bp query. This is not statistically significant. The matched organisms are Drosophila, Saccharomyces, Ceratitis fruit fly, and Macadamia, all non-pathogenic. These hits represent chance partial similarity, not a meaningful sequence match.

**Flagging decision.** This sequence would not be flagged based on these results alone. The absence of a significant database match raises the question of whether the sequence is engineered or from an under-sequenced organism. The next steps would be BLASTx on the translated ORF and domain analysis in Pfam or InterPro. A flag requires multiple investigation steps converging on a high-confidence dangerous identification. That threshold is not met here.

## AI use

This exercise was completed with AI assistance, in line with the instructions provided for this task. Claude (Sonnet 4.6) assisted in drafting and structuring the script. I directed which steps to implement, the choice of E-value thresholds for interpretation, the biological reading of the ORF output, and the flagging decision logic. These reflect my own judgment and prior work on biosecurity screening tool evaluation (Krishnan et al., 2026).

## References

Krishnan J, Rangarajan AM, Loehr A, Hoelscher-Obermaier J. Adversarial Genomic Sequences Could Evade Biosecurity Screening. Accepted for a plenary talk at CyberBio 2026 (workshop collocated with IEEE Symposium on Security and Privacy 2026), with publication in Cyberbiosecurity Quarterly. In press.

Krishnan J, Rangarajan AM, Loehr A, Hoelscher-Obermaier J. Adversarial Genomic Sequences Could Evade Biosecurity Screening. ICLR 2026 Workshop on Machine Learning for Genomics Explorations (MLGenX), 2026. https://openreview.net/forum?id=j0o93ydeGW
