#!/usr/bin/env python3
import argparse
import xlsxwriter
import re
import os

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("indir", help="The directory containing all the WhatsApp chat exports")
    parser.add_argument("-y", "--year", help="Specifies a year for the script to analyse. All other years will be ignored", required=False)
    parser.add_argument("-a", "--alias-file", help="Specifies a plain text file containing the names of all groups", required=False)
    parser.add_argument("-g", "--group-list", help="Specifies a file with a list of groups to separate from DMs.", required=False)
    parser.add_argument("-o", "--output-file", help="Specifies where to output the xlsx file. Default: output.xlsx", required=False, default="output.xlsx")

    return parser.parse_args()

def getValidFiles(indir):
    indirContents = os.listdir(indir)
    for filename in indirContents: #loop through the input directory and ignore any invalid files
        if not re.search("^WhatsApp Chat with .*\.txt$", filename): #does the filename match what WA would generate
            print("Warning: file \"" + filename + "\" is invalid and will be ignored")
            indirContents.remove(filename)
    
    for i in range(len(indirContents)):
        indirContents[i] = os.path.join(indir, indirContents[i]) #convert the filename into a full path that can be recognised by other parts of the program

    if not indirContents:
        print("Error: no valid files in input directory \"" + indir + "\".")
        exit()

    return indirContents

def validateInput(args):
    #validate input directory
    if not os.path.isdir(args.indir): #check if specified directory actually exists
        print("Error: input directory \"" + args.indir + "\" does not exist")
        exit()

    #validate year
    if args.year: #there actually was a year specified
        if not re.search("\d\d\d\d", "2021"): #is it 4 digits?
            print("Error: \"" + args.year +"\" is not a valid year.")
            exit()

    #validate alias file
    if args.alias_file:
         if not os.path.isfile(args.alias_file):
            print("Error: alias file \"" + args.alias_file + "\" does not exist")
            exit()
    
    #validate group list
    if args.group_list:
         if not os.path.isfile(args.group_list):
            print("Error: group list \"" + args.group_list + "\" does not exist")
            exit()
    
    #validate output file
    if os.path.exists(args.output_file):
        print("Error: output file \"" + args.output_file + "\" already exists")
        exit()

def countMessagesFromFiles(inFiles, year):
    nameAndCount = list()
    for filePath in inFiles:
        chatName = os.path.split(filePath)[1].removeprefix("WhatsApp Chat with ").removesuffix(".txt") #get the name of the chat
        #get the full content of the chat export
        file = open(filePath, "r", encoding="utf-8")
        fileContent = file.read()
        file.close()
        if year:
            messageRegex = str(year) + "\/\d\d\/\d\d, \d\d:\d\d - " #match any message timestamp with the specified year
        else:
            messageRegex = "\d\d\d\d\/\d\d\/\d\d, \d\d:\d\d - " #match any message timestamp

        messageCount = len(re.findall(messageRegex, fileContent)) #count the regex occourances
        #print(re.search(messageRegex, fileContent))
        countForThisThread = [chatName, messageCount]
        nameAndCount.append(countForThisThread)
    return nameAndCount

def substituteNames(inTable, pathToAliasFile):
    #open the alias file and store its contents in memory
    f = open(pathToAliasFile, "r")
    contents = f.read()
    f.close()

    lines = contents.split("\n") #split the file into lines
    #split the lines into lists to put into a multidimentional list
    substitutes = list()
    for line in lines:
        substitutes.append(line.split(","))

    for i in range(len(inTable)):
        for substitute in substitutes:
            if inTable[i][0] == substitute[0]:
                inTable[i][0] = substitute[1]

    return inTable

def writeSheet(worksheet, data):
    row = 0
    worksheet.write(row, 0, "Thread Name")
    worksheet.write(row, 1, "Message Count")
    row+=1

    for name, count in data:
        worksheet.write(row, 0, name)
        worksheet.write(row, 1, count)
        row += 1
    
    worksheet.write(row, 0, "Total:")
    worksheet.write(row, 1, "=SUM(B1:B"+str(row)+")")

def main():
    args = parseArguments()
    validateInput(args)
    exportFiles = getValidFiles(args.indir)
    #if we are still running, the arguments are probably valid

    allMessageCount = countMessagesFromFiles(exportFiles, args.year) #count the messages
    #substitute contact names if file is present
    if (args.alias_file):
        allMessageCount = substituteNames(allMessageCount, args.alias_file)
    
    workbook = xlsxwriter.Workbook(args.output_file) #make the output file
    
    #write sheet for all threads
    writeSheet(workbook.add_worksheet(name="All threads"), allMessageCount)

    #if there's a group list, remove the groups from the count list
    if args.group_list:
        dmMessageCount = list()
        f = open(args.group_list, "r")
        groupList = f.read().split("\n")
        for thread in allMessageCount:
            if not thread[0] in groupList and not thread in dmMessageCount:
                dmMessageCount.append(thread)
        writeSheet(workbook.add_worksheet(name="DMs Only"), dmMessageCount)
    #save
    workbook.close()

if __name__ == "__main__":
    main()