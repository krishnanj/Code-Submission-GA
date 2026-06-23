"""
Gary Abel — DNA Sequence Screening Exercise, Part 2
Implements BLASTn (nucleotide), BLASTx (translated), and ORF prediction
on the mystery sequence.

Usage:
    python gary_abel_screen.py

Dependencies: biopython (pip install biopython)
Note: NCBI requires a valid email for Entrez. Replace the placeholder below.
"""

from Bio.Blast import NCBIWWW, NCBIXML
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
import sys

# ── Configuration ────────────────────────────────────────────────────────────
Entrez.email = "your.email@example.com"  # replace with your email for NCBI

SEQUENCE = (
    "ATGAATCAACATAATACCCAAATCAATAAATTTATCTTTTTTAGTAGCTTCAGAATCATCAGTACC"
    "ACCCCAATTCAATTTATCAACAATAATAGGACCAGCAACAGCAATAGCAACATATTCATCATTAGAA"
    "GCAGGAGAATTCAAAACAATACCAACAGCTTTTTTATTATCAGCAGTATTCCAAGTTTTACAAACAG"
    "CACCATTAGAATTACCTTTTTCACAATCACCAGCATGCAAATTATCAATACCAGAATTTTTATGAGA"
    "TCTAATATGAACCAAACCCAT"
)

TOP_N = 5  # number of top BLAST hits to display


# ── Step 1: BLASTn (nucleotide-to-nucleotide) ────────────────────────────────
def run_blastn(sequence):
    print("=" * 60)
    print("STEP 1: BLASTn against NCBI nucleotide (nt) database")
    print("=" * 60)
    print("Submitting query... (this may take 30-90 seconds)")

    result_handle = NCBIWWW.qblast("blastn", "nt", sequence)
    blast_records = NCBIXML.parse(result_handle)
    record = next(blast_records)

    if not record.alignments:
        print("No nucleotide hits found.\n")
        return

    print(f"\nTop {min(TOP_N, len(record.alignments))} BLASTn hits:\n")
    for i, alignment in enumerate(record.alignments[:TOP_N]):
        hsp = alignment.hsps[0]
        identity_pct = (hsp.identities / hsp.align_length) * 100
        print(f"  Hit {i+1}: {alignment.title[:80]}")
        print(f"    Score: {hsp.score:.0f}  E-value: {hsp.expect:.2e}")
        print(f"    Identity: {hsp.identities}/{hsp.align_length} ({identity_pct:.1f}%)")
        print(f"    Query range: {hsp.query_start}-{hsp.query_end}")
        print()


# ── Step 2: BLASTx (nucleotide-to-protein, all 6 frames) ─────────────────────
def run_blastx(sequence):
    print("=" * 60)
    print("STEP 2: BLASTx against NCBI non-redundant protein (nr) database")
    print("=" * 60)
    print("Submitting query... (this may take 30-90 seconds)")

    result_handle = NCBIWWW.qblast("blastx", "nr", sequence)
    blast_records = NCBIXML.parse(result_handle)
    record = next(blast_records)

    if not record.alignments:
        print("No translated protein hits found.\n")
        return

    print(f"\nTop {min(TOP_N, len(record.alignments))} BLASTx hits:\n")
    for i, alignment in enumerate(record.alignments[:TOP_N]):
        hsp = alignment.hsps[0]
        identity_pct = (hsp.identities / hsp.align_length) * 100
        print(f"  Hit {i+1}: {alignment.title[:80]}")
        print(f"    Score: {hsp.score:.0f}  E-value: {hsp.expect:.2e}")
        print(f"    Identity: {hsp.identities}/{hsp.align_length} ({identity_pct:.1f}%)")
        print(f"    Frame: {hsp.frame}")
        print()


# ── Step 3: ORF prediction (all 6 reading frames) ────────────────────────────
def find_orfs(sequence, min_aa_length=20):
    print("=" * 60)
    print("STEP 3: ORF prediction (all 6 reading frames)")
    print("=" * 60)

    seq = Seq(sequence)
    strands = [(seq, "+"), (seq.reverse_complement(), "-")]
    orfs_found = []

    for strand_seq, strand_label in strands:
        for frame in range(3):
            trans = strand_seq[frame:].translate()
            aa_str = str(trans)
            start = 0
            while True:
                m_pos = aa_str.find("M", start)
                if m_pos == -1:
                    break
                stop_pos = aa_str.find("*", m_pos)
                if stop_pos == -1:
                    stop_pos = len(aa_str)
                length = stop_pos - m_pos
                if length >= min_aa_length:
                    nt_start = frame + m_pos * 3 + 1
                    nt_end = frame + stop_pos * 3
                    orfs_found.append({
                        "strand": strand_label,
                        "frame": frame + 1,
                        "aa_length": length,
                        "nt_start": nt_start,
                        "nt_end": nt_end,
                        "peptide": aa_str[m_pos:m_pos + 10] + "...",
                    })
                start = m_pos + 1

    if not orfs_found:
        print(f"No ORFs found with minimum length {min_aa_length} aa.\n")
        return

    orfs_found.sort(key=lambda x: x["aa_length"], reverse=True)
    print(f"\nORFs with at least {min_aa_length} amino acids:\n")
    for orf in orfs_found:
        print(
            f"  Strand {orf['strand']}, Frame {orf['frame']}: "
            f"{orf['aa_length']} aa | nt {orf['nt_start']}-{orf['nt_end']} | "
            f"starts: {orf['peptide']}"
        )
    print()


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nMystery sequence length:", len(SEQUENCE), "bp\n")

    find_orfs(SEQUENCE, min_aa_length=20)

    try:
        run_blastn(SEQUENCE)
    except Exception as e:
        print(f"BLASTn error: {e}\n")

    try:
        run_blastx(SEQUENCE)
    except Exception as e:
        print(f"BLASTx error: {e}\n")

    print("=" * 60)
    print("Investigation complete. Review top hits against select agent lists.")
    print("Flag only if multiple steps converge on a high-confidence dangerous identification.")
    print("=" * 60)
