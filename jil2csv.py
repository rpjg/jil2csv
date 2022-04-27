import os,re,csv, sys

temp = open('temp.txt','w+')
f = open(sys.argv[1], 'r')

for line in f:
    line = line.replace('job_type:','\njob_type:') #puts job_type on own line
    line = line.replace('insert_job', 'job_name')  #changing name of field
    line = re.sub('^ |\t', '',line)                 #trims only leading spaces/tabs (newlines are needed)

f.close()
temp.seek(0) #move position back to start of file

#all headers, used to reset "data" variable and populate csv headers
default_data = {'job_name': '','days_of_week': ''}

jils = [] #list to hold dictionaries of jobs
data = default_data.copy()
outputString=''

for line in temp:
    if line[0:8] == 'Exported':         #line not needed
        continue
    elif line[0:2] == '/*':             #job separator, not needed
        continue
    elif line == '\n':                  #checks for blank line, which is end of job, so it writes to jils list and resets
        if outputString:                #if outputString has any values from else stmt, proceeds
            jils.append(data.copy())    #save values to final list
            data = default_data.copy()  #reset data dictionary
            outputString=''             #reset outputString
            continue
    else:
        parameter, value = line.split(':', 1)   #seprates line into two values at the first ':'
        data[parameter] = value.strip()         #removes white space and add value to corresponding key in dictionary
        outputString=data['job_name']+"\t"+data['job_type']+"\n"

with open(sys.argv[2], 'w', newline='') as jil_csv:
    fieldnames = [str(k) for k in default_data]             #take the key from default_data as headers
    cw = csv.DictWriter(jil_csv, fieldnames=fieldnames)     #set up csv writer
    cw.writeheader()                                        #output the headers
    for job in jils:                                        #loop through jil list and write value to csv
        cw.writerow(job)

temp.close()