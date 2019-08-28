import time

start=time.clock()

def full_Cleavage(sequence):
    peptide_list = [0,]
    N = 0
    M = len(sequence)
    temp_sequence = sequence
    k = 0
    for i in range(M):
        if temp_sequence[i] == "K":
            if temp_sequence[i+1] != "P":
                peptide_list.append(i+1)
                k = i+1
        if temp_sequence[i] == "R":
            if temp_sequence[i+1] != "P":
                peptide_list.append(i+1)
                k = i+1
        if i == M-1:
            peptide_list.append(M)
    return peptide_list
seq = ""
cuts = full_Cleavage(seq)


def gen_peptides(cuts):
    peptide_coordinates_backwards = []
    peptide_coordinates_forwards = []
    missed = 0
    for i in range(1,missed+2):
        #print i-1
        #print "forward"
        for j in range(1, len(cuts)-i):
            start = cuts[j]
            max = cuts[j+i]+1
            for k in range(1,max-start):
                peptide_coordinates_forwards.append((start, start + k))
                #print seq[start:start + k]

        #print "backward"
        for j in range(0, len(cuts)-i-1):
            max = cuts[j]
            start = cuts[j+i]
            #peptide_coordinates_backwards=
            for k in range(1,start-max+1):
                peptide_coordinates_backwards.append((start - k, start))
                #print seq[start-k:start]


    peptide_coordinates = peptide_coordinates_backwards + peptide_coordinates_forwards
    return peptide_coordinates


peptides = [seq[i[0]:i[1]] for i in gen_peptides(cuts)]


#print set(peptides)
print len(set(peptides))
print time.clock()-start