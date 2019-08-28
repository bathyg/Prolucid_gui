from collections import deque
from itertools import chain, product
import re
import time
#import compare_to_chainsaw
expasy_rules = {
    'arg-c':         r'R',
    'asp-n':         r'\w(?=D)',
    'bnps-skatole' : r'W',
    'caspase 1':     r'(?<=[FWYL]\w[HAT])D(?=[^PEDQKR])',
    'caspase 2':     r'(?<=DVA)D(?=[^PEDQKR])',
    'caspase 3':     r'(?<=DMQ)D(?=[^PEDQKR])',
    'caspase 4':     r'(?<=LEV)D(?=[^PEDQKR])',
    'caspase 5':     r'(?<=[LW]EH)D',
    'caspase 6':     r'(?<=VE[HI])D(?=[^PEDQKR])',
    'caspase 7':     r'(?<=DEV)D(?=[^PEDQKR])',
    'caspase 8':     r'(?<=[IL]ET)D(?=[^PEDQKR])',
    'caspase 9':     r'(?<=LEH)D',
    'caspase 10':    r'(?<=IEA)D',
    'chymotrypsin high specificity' : r'([FY](?=[^P]))|(W(?=[^MP]))',
    'chymotrypsin low specificity':
        r'([FLY](?=[^P]))|(W(?=[^MP]))|(M(?=[^PY]))|(H(?=[^DMPW]))',
    'clostripain':   r'R',
    'cnbr':          r'M',
    'enterokinase':  r'(?<=[DE]{3})K',
    'factor xa':     r'(?<=[AFGILTVM][DE]G)R',
    'formic acid':   r'D',
    'glutamyl endopeptidase': r'E',
    'granzyme b':    r'(?<=IEP)D',
    'hydroxylamine': r'N(?=G)',
    'iodosobenzoic acid': r'W',
    'lysc':          r'K',
    'ntcb':          r'\w(?=C)',
    'pepsin ph1.3':  r'((?<=[^HKR][^P])[^R](?=[FLWY][^P]))|'
                     r'((?<=[^HKR][^P])[FLWY](?=\w[^P]))',
    'pepsin ph2.0':  r'((?<=[^HKR][^P])[^R](?=[FL][^P]))|'
                     r'((?<=[^HKR][^P])[FL](?=\w[^P]))',
    'proline endopeptidase': r'(?<=[HKR])P(?=[^P])',
    'proteinase k':  r'[AEFILTVWY]',
    'staphylococcal peptidase i': r'(?<=[^E])E',
    'thermolysin':   r'[^DE](?=[AFILMV])',
    'thrombin':      r'((?<=G)R(?=G))|'
                     r'((?<=[AFGILTVM][AFGILTVWA]P)R(?=[^DE][^DE]))',
    'trypsin':       r'([KR](?=[^P]))|((?<=W)K(?=P))|((?<=M)R(?=P))'
    }
def parse_fasta(file_name):
    protein_name=[]
    protein_dict={}
    with open(file_name,'r') as fasta_file:
        for line in fasta_file:
            if line.startswith('>'):
                if len(protein_name)>1:
                    protein_dict[protein_name[1]]=[protein_name[0],protein_name[2],sequence]
                protein_name=line[1:].rstrip().split('|')
                sequence=''
            elif len(protein_name)>1 and line[0].isalpha():
                sequence+=line.rstrip()
        protein_dict[protein_name[1]] = [protein_name[0], protein_name[2], sequence]

def cleave(sequence, rule, missed_cleavages=0, overlap=False):
    """
    Docstring omitted here for brevity.
    """
    peptides = set()
    cleavage_sites = deque([0], maxlen=missed_cleavages+2)
    for i in chain(map(lambda x: x.end(), re.finditer(rule, sequence)),
                   [None]):
        cleavage_sites.append(i)
        for j in range(0, len(cleavage_sites)-1):
            peptides.add(sequence[cleavage_sites[j]:cleavage_sites[-1]])
        if overlap and i not in {0, None}:
            peptides.update(
                    cleave(sequence[i:], rule, missed_cleavages, overlap))

    if '' in peptides:
        peptides.remove('')
    return peptides

def cut_peptide_sequence(sequence,cut_list,nocut_list):
    #cut_sequence=filter(None,re.split('([A-JL-QS-Z]+[KR])',sequence))
    cut_sequence = re.findall(r".(?:(?<![RK](?!P)).)*", sequence)
    return cut_sequence



if __name__=="__main__":
    start_time=time.clock()
    #file_name='uniprot_human_2018_04_27.fasta'
    #parsed_fasta=parse_fasta(file_name)
    #print parsed_fasta['C9JX34']
    print list(cleave('MMKRPQLHRMRQLAQTGSLGRTKPETAEFLGEDL','([KR](?=[^P]))',missed_cleavages=2))
    #print cut_peptide_sequence('MVDYYEVLGVQRHASPEDIKKAYRKLALKWHPDKNPENKEEAERKFKQVAEAYEVLSDAKKRDIYD',[],[])
