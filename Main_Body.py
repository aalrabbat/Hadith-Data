import re
from itertools import product

rawi_1a = input("Enter the said transmitter's name:")
rawi_1b = rawi_1a.replace("بن", "ابن")

def name_permutations_letters(rawi_1a):
    combos = [(c,) if c not in options else options[c] for c in rawi_1a]
    return (''.join(o) for o in product(*combos))

def name_permutations_ibn(rawi_1b):
    combos = [(c,) if c not in options else options[c] for c in rawi_1b]
    return (''.join(o) for o in product(*combos))

options = {
    'أ': ['ا', 'أ'],
    'إ': ['ا', 'إ'],
    'آ': ['ا', 'آ'],  
'ي': ['ي', 'ى'],
    'ى': ['ي', 'ى'],
    'ئ': ['ي', 'ى', 'ئ'],
    'ة': ["ه", "ة"],
    'ه': ["ه", "ة"],
    'ؤ': ["و", "ؤ"],
}
#Till now, Only works with characters, not strings

rawi_name_list = list(name_permutations_letters(rawi_1a))

ibn_list = list(name_permutations_ibn(rawi_1b))

name_combo_list = rawi_name_list + ibn_list

# Accounts for instances where names that include عبد do not inclue
# spaces between عبد and the following word; i.e: عبدالله instead of عبد الله
old = "عبد "
new = "عبد"
 
def replaced(name_combo_list, old, new):
    return (x.replace(old, new) if old in x else x for x in name_combo_list)


abd_list = list(replaced(name_combo_list, old, new))

# Accounts for typos where بن in the middle of a name is incorrectly
# merged into the previous word with no space; i.e إبراهيمبن هاشم instead 
# of إبراهيم بن هاشم

old = " بن"
new = "بن"

ibn_space1_list = list(replaced(name_combo_list, old, new))

# Accounts for typos where بن in the middle of a name is incorrectly
# merged into the next word with no space; i.e إبراهيم بنهاشم instead 
# of إبراهيم بن هاشم

old = "بن "
new = "بن"
ibn_space2_list = list(replaced(name_combo_list, old, new))

name_combo_list = name_combo_list + abd_list + ibn_space1_list + ibn_space2_list

##########################################
##########################################
#Baṣāʾir al-Darajāt of al-Ṣaffār

#File Cleaner: Code that is intended to clean the relevant text file(s)
# by removing unncessary strings that result in false positives
# (i.e footnote data, duplicate delimiters in the text etc.)

#Removes footnote text
with open('basair_darajat.txt') as f_in, open('basair_darajat.clean.txt', "w") as f_out: 
    lines = f_in.read()
    #The line beneath this comment removes the footnote text from the book,
    #which starts with a "---" seperator and usually ends with 
    # the string, "اللاحق السابق" etc.
    bas_footnote_pattern = re.compile(r"---.*?... اللاحق السابق فهرست الكتاب الحديث وعلومه", re.DOTALL)
    new_lines = re.sub(bas_footnote_pattern, "", lines)
    # Line below removes redundant footnote delimeter instances of  
    # the string, "اللاحق" and "بصائر الدرجات ج1 " etc., that were not 
    # removed in the earlier lines.
    new_lines = new_lines.replace("... اللاحق السابق فهرست الكتاب الحديث وعلومه", "")
    new_lines = new_lines.replace("بصائر الدرجات ج1", "")
    # The line below aims to remove the vestigial footnote numbering found
    # within the text, as it often leads to false positives.
    old_numbering = re.compile(r"(\S)\(\d+\)")
    new_lines = re.sub(old_numbering, r"\1", new_lines)
    # Lines below seeks to remove the unnecessary volume and page numbers in
    # the file
    page_volume = re.compile(r"\(\w+?/\w\)")
    new_lines = re.sub(page_volume, "", new_lines)
    new_lines = new_lines.replace("(/1)", "")
    new_lines = new_lines.replace("(/2)", "")
    # The lines below seek to remove added periods in between hadiths that
    # lead to unncessary splitting. Groups 1 and 4 refer refer to any
    # character that is a letter and excludes "(" as well
    excessive_periods = re.compile(r"([^\W\d\(])(\.)(\n+)([^\W\d\(])")
    new_lines = re.sub(excessive_periods, r"\1 \4", new_lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"([^\W\d])\n+([^\W\d])") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s)(\(\d+\))")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)
 
file= open('basair_darajat.clean.txt', 'r') 
    
lines= file.read()
    
# Search for all elements of in rawi_main_list as individual strings, and 
# return the string that occurs between "(#)" and a period whilst also 
# containing the string rawi_main_list. The  delimiters will vary from 
# book to book depending on the format used by each's publisher. 

pattern = rf"\(\d+\)([^.]*(?:{'|'.join(name_combo_list)})[^.]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "قال الصفار في >بصائر الدرجات<:" + actual_line + "."+"\n"


with open("results.txt", "w") as txt_file:
    print(printed, file = txt_file)

file.close()

##########################################
##########################################
#Al-Maḥāsin of al-Barqī


with open('mahasin.txt') as f_in, open('mahasin.clean.txt', "w") as f_out: 
    lines = f_in.read()
    #The line beneath this comment removes the unncessary headings that
    #lead to false positives, since they start with numbers and dashes.
    mah_heading_pattern = re.compile(r"\d+.*?:")
    new_lines = re.sub(mah_heading_pattern, "", lines)
    new_lines = new_lines.replace("back page ... fehrest page ... next page", "") 
    new_lines = new_lines.replace("... fehrest page ... next page", "")
    new_lines = new_lines.replace("back page ... fehrest page ...", "")
    mah_page_numbers = re.compile(r"\[\d+\]")
    new_lines = re.sub(mah_page_numbers, "", new_lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"([^\W\d])\n+([^\W\d])") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    f_out.write(new_lines)


file= open('mahasin.clean.txt', 'r') 
    
lines= file.read()


pattern = rf"\d+\s?\-?([^.]*(?:{'|'.join(name_combo_list)})[^.]*)"

find = re.findall(pattern, lines)

printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "البرقي في >المحاسن<:" + actual_line + "."+"\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)
  
file.close()

##########################################
##########################################
# Qurb al-Isnād of al-Ḥimyarī

with open('qurb.txt') as f_in, open('qurb.clean.txt', "w") as f_out: 
    lines = f_in.read()
    #The line beneath this comment removes the footnotes, which split
    #the hadiths whilst containing many periods, hence regularly leading
    #to missing chunks in the hadith and potential false positives.
    qurb_footnotes_pattern = re.compile(r"(_).*?\[\d+\]", re.DOTALL)
    new_lines = re.sub(qurb_footnotes_pattern , "", lines)
    #Removes some excessive consecutive linebreaks in the file. Not all
    #redundant linebreaks can be successfully removed without resulting
    #in emergent defects in the text file.
    double_line_break = re.compile(r"\s{3}", re.DOTALL)
    new_lines = re.sub(double_line_break, "", new_lines)
    footnote_signs = re.compile(r"\(\d\)")
    new_lines = re.sub(footnote_signs, "", new_lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"([^\W\d])\n+([^\W\d])") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    f_out.write(new_lines)
    
file= open('qurb.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\d+\s\-([^.]*(?:{'|'.join(name_combo_list)})" + r"[^\d]*)"


find = re.findall(pattern, lines)

printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "الحميري في >قرب الإسناد<:" + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)
    
file.close()

##########################################
##########################################
# The 16 Uṣūl :
# For the sake of efficiency and accuracy, I have opted to break down the
# book into 16 different text files, each of which comprises a different Aṣl.

# Aṣl Zayd al-Zarrād

with open('asl_alzarrad.txt') as f_in, open('asl_al_zarrad.clean.txt', "w") as f_out: 
    lines = f_in.read()
    zarrad_footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(zarrad_footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    f_out.write(new_lines)

file= open('asl_al_zarrad.clean.txt', 'r') 
    
lines= file.read()
    
# The pattern in this text file (and the following Uṣūl) utilizes the greedy
# qualifiers, .*?, since the delimiters I manually inserted into the text files
# are predictable and consistent.

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >أصل زيد الزراد< عن " + actual_line + "."+"\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# Aṣl Zayd al-Narsī

with open('asl_alnarsi.txt') as f_in, open('asl_alnarsi.clean.txt', "w") as f_out: 
    lines = f_in.read()
    zarrad_footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(zarrad_footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)


file= open('asl_alnarsi.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >أصل زيد النرسي< عن " + actual_line + "."+"\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()


# Aṣl Jaʿfar al-Ḥaḍramī

with open('asl_jafar_alhadrami.txt') as f_in, open('asl_jafar_alhadhrami.clean.txt', "w") as f_out: 
    lines = f_in.read()
    zarrad_footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(zarrad_footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)


file= open('asl_jafar_alhadhrami.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >أصل جعفر بن محمد الحضرمي<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()



# Aṣl Muḥammad b. al-Muthannā al-Ḥaḍramī

with open('asl_muhammad_ibn_almuthanna.txt') as f_in, open('asl_muhammad_ibn_almuthanna.clean.txt', "w") as f_out: 
    lines = f_in.read()
    ibn_muthanna_footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(ibn_muthanna_footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('asl_muhammad_ibn_almuthanna.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >أصل محمد بن المثنى الحضرمي<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()


# Kitāb AbdilMalik ibn Hakim


with open('kitab_abdilmalik.txt') as f_in, open('kitab_abdilmalik.clean.txt', "w") as f_out: 
    lines = f_in.read()
    abdilmalik_footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(abdilmalik_footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('kitab_abdilmalik.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب عبد الملك بن بن حكيم<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

#Kitab al-Muthannā b. Walīd

with open('muthanna_ibn_walid.txt') as f_in, open('muthanna_ibn_walid.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('muthanna_ibn_walid.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب المثنى بن الوليد الحناط<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()


# Kitāb Khallād al-Sindī

with open('khallad_alsindi.txt') as f_in, open('khallad_alsindi.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('khallad_alsindi.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب خلّاد السندي<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# Kitāb al-Ḥusayn b. Uthmān b. Sharīk

with open('husayn_ibn_uthman.txt') as f_in, open('husayn_ibn_uthman.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('husayn_ibn_uthman.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب حسين بن عثمان بن شريك<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# Kitāb Abdillāh b. Yaḥyā al-Kāhilī

with open('abdullah_alkahili.txt') as f_in, open('abdullah_alkahili.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('abdullah_alkahili.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب عبد الله بن يحيى الكاهلي<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# Kitāb Sallām b. Abī Amra

with open('kitab_sallam.txt') as f_in, open('kitab_sallam.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('kitab_sallam.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب سلام بن أبي عمرة<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()


# Nawādir Alī b. Asbāṭ

with open('nawadir_ali.txt') as f_in, open('nawadir_ali.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('nawadir_ali.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >نوادر علي بن أسباط<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# A tradition on the Malāḥim

with open('malahim.txt') as f_in, open('malahim.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('malahim.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >خبر في الملاحم< من رواية الشيخ هارون بن موسى التلعكبري: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

#Mukhtaṣār al-Alaʾ b. Razīn

with open('asl_alaa.txt') as f_in, open('asl_alaa.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('asl_alaa.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >أصل العلاء بن رزين<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# Kitāb Durust 

with open('durust.txt') as f_in, open('durust.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('durust.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب درست بن أبي منصور<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# Aṣl Abbād

with open('asl_abbad.txt') as f_in, open('asl_abbad.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('asl_abbad.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >أصل أبي سعيد عباد العصفري<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

# Aṣl Aṣim b. Ḥumayd

with open('asim_ibn_humayd.txt') as f_in, open('asim_ibn_humayd.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"---.*?\(\s\d+\s\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    # Lines below seek to add periods at the ends of ḥadīths where a period
    # expected. The absence of such periods in such instances leads to the 
    # return of larger strings that consist of multiple ḥadīths, as opposed
    # to the one desired ḥadīth.
    missing_period = re.compile(r"()(\s+)(\[\])")
    new_lines = re.sub(missing_period, "." + r"\2 \3", new_lines)
    f_out.write(new_lines)

file= open('asim_ibn_humayd.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"\[\]([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\[\]]*)"

find = re.findall(pattern, lines)


printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >أصل عاصم بن حميد الحنّاط<: " + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()

##########################################
##########################################
# Tafsīr al-Qummī

# Tafsir al-Qummī will have to be manually cleaned, parsed and organized.




##########################################
##########################################
# Al-Kāfī of al-Kulaynī

# The file for al-Kāfi was a generally clean file from the start, 
# so not much cleaning was needed.

with open('kafi.txt') as f_in, open('kafi.clean.txt', "w") as f_out: 
    new_lines = f_in.read()
    excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    f_out.write(new_lines)

file= open('kafi.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"-([^.].*?(?:{'|'.join(name_combo_list)})" + r"[^\d]*)"

find = re.findall(pattern, lines)

printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >كتاب الكافي< للكليني:" + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()


##########################################
##########################################
# Al-Imāma wa-l-Tabṣira of Ibn Bābawayh Sr.

#with open('tabsira.txt') as f_in, open('tabsira.clean.txt', "w") as f_out: 
   # new_lines = f_in.read()
    #excessive_linebreak = re.compile(r"(\w)\n+(\w)") 
    #new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    #f_out.write(new_lines)

##########################################
##########################################
# Kāmil al-Ziyārāt of Ibn Qūlawayh

##########################################
##########################################
# Al-Amālī of al-Sadūq

with open('amali_saduq.txt') as f_in, open('amali_saduq.clean.txt', "w") as f_out: 
    lines = f_in.read()
    footnote_pattern = re.compile(r"____________________.*?\n\(\d{2,3}\)", re.DOTALL)
    new_lines = re.sub(footnote_pattern, "", lines)
    # The lines below seeks to remove unnecessary linebreaks in the middle 
    # of ḥadīths.
    excessive_linebreak = re.compile(r"([^\W\d])\n+([^\W\d])") 
    new_lines = re.sub(excessive_linebreak, r"\1 \2", new_lines)
    additional_linebreak_1 = re.compile(r"(،)\n+([^\W\d])") 
    new_lines = re.sub(additional_linebreak_1 , r"\1 \2", new_lines)
    additional_linebreak_2 = re.compile(r"(\.)\n+([^\W\d])") 
    new_lines = re.sub(additional_linebreak_2 , r"\1 \2", new_lines)
    additional_linebreak_3 = re.compile(r"(:)\n+([^\W\d])") 
    new_lines = re.sub(additional_linebreak_3 , r"\1 \2", new_lines)
    additional_linebreak_4 = re.compile(r"(\؟)\n+([^\W\d])") 
    new_lines = re.sub(additional_linebreak_4 , r"\1 \2", new_lines)
    additional_linebreak_5 = re.compile(r"(\!)\n+([^\W\d])") 
    new_lines = re.sub(additional_linebreak_5 , r"\1 \2", new_lines)
    additional_linebreak_6 = re.compile(r"(\))\n+([^\W\d])") 
    new_lines = re.sub(additional_linebreak_6 , r"\1 \2", new_lines)
    # The lines below remove redundant numberings of the majālis within the file
    majlis_number = re.compile(r"\]\d+\[")
    new_lines = re.sub(majlis_number, "", new_lines)
    # The lines below remove the vestigial footnote numbers within the text
    foot_number = re.compile(r"\(\d\)")
    new_lines = re.sub(foot_number, "", new_lines)
    foot_number_2 = re.compile(r"\(\d \)")
    new_lines = re.sub(foot_number_2, "", new_lines)
    foot_number_3 = re.compile(r"\( \d\)")
    new_lines = re.sub(foot_number_3, "", new_lines)
    f_out.write(new_lines)



file= open('amali_saduq.clean.txt', 'r') 
    
lines= file.read()

pattern = rf"-([^.].*?(?:{'|'.join(name_combo_list)})[^\d]*)"

find = re.findall(pattern, lines)

printed = ""

for i in range(0,len(find)):
    actual_line = find[i]
    printed += "وفي >الأمالي< لابن بابويه:" + actual_line + "\n"


with open("results.txt", "a") as txt_file:
    print(printed, file = txt_file)

file.close()