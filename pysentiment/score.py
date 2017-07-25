from lm import LM
x = LM()
amd = open('amd.txt', 'r')
apl = open('apple.txt', 'r')
amdtok = x.tokenize(amd.read())
apltok = x.tokenize(apl.read())
print('Amd score: ' + str(x.get_score(amdtok)))
print('Apl score: ' + str(x.get_score(apltok)))
amd.close()
apl.close()