"""
 -------------------------------------
| BOILERMAN - Faster Code Generation  |
|                                     |
| Author : Harvinder Singh Laliya     |
 -------------------------------------

"""

import argparse
import sys
import os

#Setting Up Parser
parser=argparse.ArgumentParser(description="Generate Boilerplate Code Faster!")

#Positional Args

#Optional Args
parser.add_argument("-f","--filename",help="create a boilerplate file")
parser.add_argument("-c","--classname",help="specify custom classname")
parser.add_argument("-a","--author",action="store_true",help="add author name")
parser.add_argument("-H","--header",action="store_true",help="create header file(for supported langs)")
parser.add_argument("-p","--project",help="create a project according to config specs")

#Some Vars
log_prefix="[LOG]: "
suc_prefix="[SUCCESS]: "
err_prefix="[ERROR]: "
wrn_prefix="[WARN]: "
comment_types={"java_st":"/*","java_end":"*/","html_st":"<!--","html_end":"-->","cpp_st":"/*","cpp_end":"*/"}
lang_supported=["java","html","cpp"]
template_tokens={"classname":"~classname~","author":"~author~"}

#Getting Args
args=parser.parse_args()


#Functions
def make_from_template(filename):
    try:
        ext=filename.split(".")
        file_ext=ext[1]
        with open("templates/temp_"+file_ext,"r") as input_file,open(filename,"x") as target_file:
            for lines in input_file:
                target_file.write(lines)

        print(log_prefix+"File has been generated")

    except FileExistsError:
            print(err_prefix+"A file with the given filename already exists!")
            sys.exit(1)

    except FileNotFoundError:
        os.remove(filename)
        print(err_prefix+"Please make sure template directory exists with appropriate files!")
        sys.exit(1)

#only fpr cpp and c
def make_header():
    try:
        ext=args.filename.split(".")
        name=ext[0]
        file_ext=ext[1]

        if file_ext=='cpp' or file_ext=='c':
            with open("templates/temp_hpp","r") as input_file,open(name+'.hpp',"x") as target_file:
                for lines in input_file:
                    target_file.write(lines)
                print(log_prefix+"Wrote Header File")

            target_file = open("templates/temp_hpp","r")
            data = target_file.read()
            target_file.close()
            #print(data)

            if template_tokens["classname"] in data:
                data=data.replace(template_tokens["classname"],name)
                print(log_prefix+"Added Classname from filename")
            else:
                print(err_prefix+"Header Template may be corrupted")
                sys.exit(1)

            target_file = open(name+".hpp","w")
            target_file.write(data)
            target_file.close()
            print(suc_prefix+"Header File Generated!")

        else:
            print(file_ext)
            print(wrn_prefix+'Header Creation not supported for',file_ext)
            sys.exit(1)

    except FileExistsError:
        print(err_prefix+"Header file with the given filename already exists!")
        sys.exit(1)

    except FileNotFoundError:
        os.remove(filename)
        print(err_prefix+"Please make sure Header template exists!")
        sys.exit(1)



#gets -c arg and puts as classname
def substitute_content(filename,class_name=""):
    try:
        target_file = open(filename,"r")
        data = target_file.read()
        target_file.close()

        #print(args.classname)
        if not args.classname:
            ext=filename.split(".")
            name=ext[0]
            if template_tokens["classname"] in data:
                data=data.replace(template_tokens["classname"],name)
                print(log_prefix+"Added Classname from filename")
            else:
                print(log_prefix+"Did not Find a Classname Token in template")
                pass
        elif args.classname:
            print(log_prefix+"Added Specified Classname from argument")
            data=data.replace(template_tokens["classname"],class_name)


        #print(args.author)
        if not args.author:
            print(log_prefix+"Deleting Author tag since no argument was specified")
            data=data.replace(template_tokens["author"],"")
        elif args.author:
            author=[]
            if ext[1] in lang_supported and ext[1]+"_st" in comment_types:
                author.append(comment_types.get(ext[1]+"_st")+"\n")
                author.append(get_author_template(filename))
                author.append(comment_types.get(ext[1]+"_end"))
                author_str="".join(author)
                data=data.replace(template_tokens["author"],author_str)
                print(log_prefix+"Added Author Description")
            else:
                print(log_prefix+"Could not comment author description(Unsupported language)")
                sys.exit(1)

        target_file = open(filename,"w")
        target_file.write(data)
        target_file.close()

        print(log_prefix+"Template Tokens Substituted!")

    except Exception as e:
        pass

#gets author file , also deletes generated file if author template is not found
def get_author_template(final_file):
    try:
        target_file = open("templates/author_desc","r")
        data = target_file.read()
        target_file.close()
        print(log_prefix+"Got Author Data from template")
        return data
    except FileNotFoundError:
        print(err_prefix+"Author Description Template does not exist")
        os.remove(final_file)
        sys.exit(1)

#Run stuff
if __name__=="__main__":
    print(args)
    make_from_template(args.filename)
    if args.classname:
        substitute_content(args.filename,class_name=args.classname)
        print(suc_prefix+"File(s) generated successfully!")
    elif args.header:
        substitute_content(args.filename)
        make_header()
        print(suc_prefix+"File(s) generated successfully!")
    else:
        substitute_content(args.filename)
        print(suc_prefix+"File(s) generated successfully!")
