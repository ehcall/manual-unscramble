import os
import re

from bs4 import BeautifulSoup
lesson_folders = ["simple_XML_lessons\\validated\\BM\\2003", "simple_XML_lessons\\validated\\DC\\2003",
                  "simple_XML_lessons\\validated\\NT\\1997", "simple_XML_lessons\\validated\\OT\\2001"]

for lesson_folder in lesson_folders:
    manual = []
    folder_name = re.split("\\\\", lesson_folder)
    print(folder_name)
    manual_name = 'simple_XML_lessons\\validated\\full_manuals\\' + folder_name[2] + "_" + folder_name[3] + "_T.xml"
    for file in os.listdir(lesson_folder):
        with open(lesson_folder + "\\" + file, 'r', encoding='utf-8') as xmlreadfile:
            lesson = xmlreadfile.readlines()
            lesson_num = ""
            lesson_title = ""
            lesson_ref = ""
            if re.search('-00', file):
                lesson_num = ""
                lesson_ref = ""
            else:
                lesson_heading = lesson[0:4]
                to_pop = []
                for i, heading in enumerate(lesson_heading):
                    if re.search(r'heading num', heading):
                        lesson_num = heading
                        to_pop.append(i)
                    elif re.search(r'heading title',heading):
                        lesson_title = heading
                        to_pop.append(i)
                    elif re.search(r'heading ref', heading):
                        lesson_ref = heading
                        to_pop.append(i)
                if lesson_num == "":
                    lesson_num = "<heading num> Lesson " + file[-6:-4] + " </heading>\n"
                if lesson_ref == "":
                    lesson_ref = "<heading ref/>\n"
                    #print("uhhh missing ref in: ", file)
                for element in sorted(to_pop, reverse=True):
                    lesson.pop(element)
            manual.extend([lesson_num, lesson_title, lesson_ref])
            manual.extend(lesson)

    with open(manual_name, 'w', encoding='utf-8') as xmlwritefile:
        for line in manual:
            xmlwritefile.write(line)
#for line in manual:
 #   print(line)