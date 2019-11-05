from sys import argv

########################################################################################################################

print(argv)

_, path, l0, l1, c0, c1 = argv


l0 = int(l0) - 1
l1 = int(l1)
c0 = int(c0) - 1
c1 = int(c1)

with open(path) as f:
    all_lines = list(f)

slines = all_lines[l0:l1]

print(''.join(slines))

stext = ''.join(slines)[c0:( c1 - len(slines[-1]) - 1 )]

print(f"<{stext}>")

########################################################################################################################
