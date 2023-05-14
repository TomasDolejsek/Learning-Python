output_name = 'findtools_result_'

filename = 'dgsjfgdsfghjdsf\\dsfg\\dsg\\findtools_result_315.xlsx'

index = filename.find(output_name)
print(index)

if output_name in filename:
    if index != -1:
        filename = filename[index:-5]
        filename = filename.split('_')
        print(filename[-1])
    

print(filename)