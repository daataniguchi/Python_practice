##Make a dice rolling game. If you roll a 1, 2, or 3 you lose, anything else you win.
#from random import randint

#number = randint(1,6)

#print('You rolled a ' + str(number)) ##You rolled a + the random integer converted to a string.

#if number == 1 or number == 2 or number == 3:
    #print('Lose')
#else:
    #print('Win')

##Chapter 4: Lists

#Question 1: Processing DNA in a file
file_4 = open('input.txt','r')
file_5 = file_4.readlines()
file_6 = open('new_txt_3','w')

for i in file_5:
    trimmed_dna = i[14:]
    length_trimmed_dna = len(trimmed_dna)
    print('The length is ' + str(length_trimmed_dna) + ' The sequence is ' + trimmed_dna)
    file_6.write(trimmed_dna)

file_4.close()
file_6.close()



##Question 2: Multiple Exons from Genomic DNA
##The file genomic_dna.txt contains a section of genomic DNA, and the file exons.txt contains a list of start/stop positions of exons.
##Each exon is on a separate line and the start and stop positions are separated by a comma.
##Write a program that will: 1. Extract the exon segments, concatenate them, and write them into a new file.

#file_7 = open('genomic_dna.txt','r')
#print(file_7.readlines())
#genomic_dna = 'ATCGATCGATCGATCGACTGACTAGTCATAGCTATGCATGTAGCTACTCGATCGATCGATCGATCGATCGATCGATCGATCGATCATGCTATCATCGATCGATATCGATGCATCGACTACTAT'
#length_genomic_dna = len('ATCGATCGATCGATCGACTGACTAGTCATAGCTATGCATGTAGCTACTCGATCGATCGATCGATCGATCGATCGATCGATCGATCATGCTATCATCGATCGATATCGATGCATCGACTACTAT')
#print(length_genomic_dna)
#file_7.close()

#For Loops and List Comprehensions
list_a = ['Ip Man', 'The Dark Knight', 'Star Wars', 'Rush Hour', 'Star Trek'] ##example of for loop
for i in list_a:
    if i.startswith('I'):
        print(i)

list = [i for i in list_a if i.startswith('S')] ##example of list comprehensions
print(list)

list = [1,2,3,4,5] ##another example of list comprehensions
list_b = [i**2 for i in list]
print(list_b)


##Example of function:
dna = 'GCAT'

def func_1():
    a_count = dna.count('A')
    t_count = dna.count('T')
    length = len(dna)
    proportion = (a_count + t_count) / length
    return(proportion)

print(func_1())

##BMI Calculator
##Weight/Height^2
##Note weight is in kg, height is in m
def BMI_Calculator():
    Height = 1.8
    Weight = 90
    BMI = Weight / Height**2
    return BMI

print(BMI_Calculator())




