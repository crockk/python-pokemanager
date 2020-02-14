

def read_file(fname):

    f_lines = []
    with open(fname, 'r') as f:
        f_lines = [l.strip() for l in f.readlines()[1:]]

    # print(f_lines)

    dik = {}

    for l in f_lines:
        L = l.split(',')
        # print(L)
        dik[L[0]] = [L[1].strip(), L[2].strip(), {j.split(':')[0]:j.split(':')[1] for j in L[3].split(';')}]

    # for i in dik.items():
    #     print(i)

    return dik


def param_dic_to_str(dik):
    out_str = ''

    if dik:
        for i in dik.items():
            if i[0].strip() != "None":

                if i[1].strip() == "None":
                    out_str += f"{i[0].strip()}, "
                else:
                    out_str += f"{i[0].strip()}: {i[1].strip()}, "
            
                
        out_str = out_str[:-2]


    return out_str



in_fname = "PMem_Func_lst.txt"
out_fname = "proto_out_file.txt"


funcs = read_file(in_fname)

with open(out_fname, 'w') as f:
    for func in funcs.items():
        # print(func)
        if func[1][0] == 'G':
            f.write(f"@property\ndef {func[0]}({param_dic_to_str(func[1][2])}) -> {func[1][1].strip()}:\n\tpass\n\n\n")
        if func[1][0] == 'S':
            # f.write(f"@property\ndef {func[0]}({param_dic_to_str(func[1][2])}) -> {func[1][1].strip()}:\n\tpass\n\n\n")
            f.write(f"@{func[0].strip('S')}.setter\ndef {func[0].strip('S')}({param_dic_to_str(func[1][2])}) -> {func[1][1].strip()}:\n\tpass\n\n\n")
        elif func[1][0] == 'N':
            f.write(f"def {func[0]}({param_dic_to_str(func[1][2])}) -> {func[1][1].strip()}:\n\tpass\n\n\n")

# "def {name}():\n\tpass\n"