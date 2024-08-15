#!/usr/bin/env python3
"""
Get which one of the sarUpa ya pratyaya can be used 
"""
import json
import csv

__author__ = "Deepan Palguna"
__version__ = "0.1.0"
__license__ = "MIT"

"""
Everything is in SLP in this file
_mod means without it
otherwise it is with it
"""

def is_ajanta(term):
   if term[-1] in {'a', 'A', 'i', 'I', 'u', 'U', 'f', 'F', 'x', 'X', 'e', 'E', 'o', 'O'}:
      return True
   return False

def is_ajadi(term):
   if term[0] in {'a', 'A', 'i', 'I', 'u', 'U', 'f', 'F', 'x', 'X', 'e', 'E', 'o', 'O'}:
      return True
   return False

def is_halanta(term):
   return not is_ajanta(term)

def is_valadi(term):
    return not is_ajadi(term) and term[0] not in set(['h', 'y'])

def perform_guna(aksharam):
   if aksharam.lower() == 'a':
     return 'a'
   elif aksharam.lower() == 'i':
      return 'e'
   elif aksharam.lower() == 'u':
      return 'o'
   elif aksharam.lower() == 'f':
      return 'ar'
   
def perform_vrddhi(aksharam):
   if aksharam in ('a', 'A'):
     return 'A'
   elif aksharam in ('i', 'I'):
      return 'E'
   elif aksharam in ('u', 'U'):
      return 'O'
   elif aksharam in ('f', 'F'):
      return 'Ar'
   
def perform_sandhi(purvapadam, uttarapadam):
   #guna
   if (purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "i"):
      return purvapadam[:-1] + "e" + uttarapadam[1:]
   elif (purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "u"):
      return purvapadam[:-1] + "o" + uttarapadam[1:]
   if (purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "f"):
      return purvapadam[:-1] + "ar" + uttarapadam[1:]
   elif (purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "x"):
      return purvapadam[:-1] + "al" + uttarapadam[1:]

   #vrddhi
   elif purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "e":
      return purvapadam[:-1].lower() + "E" + uttarapadam[1:]
   elif purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "o":
      return purvapadam[:-1] + "O" + uttarapadam[1:]
   if purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "E":
      return purvapadam[:-1] + "E" + uttarapadam[1:]
   elif purvapadam[-1].lower() == "a" and uttarapadam[0].lower() == "O":
      return purvapadam[:-1] + "O" + uttarapadam[1:]

   #yAntAvAnta
   elif (purvapadam[-1] == 'e' and is_ajadi(uttarapadam)):
      return purvapadam[:-1] + "ay" + uttarapadam
   elif (purvapadam[-1] == 'E' and is_ajadi(uttarapadam)):
      return purvapadam[:-1] + "Ay" + uttarapadam
   elif (purvapadam[-1] == 'o' and is_ajadi(uttarapadam)):
      return purvapadam[:-1] + "av" + uttarapadam
   elif (purvapadam[-1] == 'O' and is_ajadi(uttarapadam)):
      return purvapadam[:-1] + "Av" + uttarapadam
   
   #yan
   elif purvapadam[-1] in ("i", "I") and is_ajadi(uttarapadam):
      return purvapadam[:-1] + "y" + uttarapadam
   elif purvapadam[-1] in ("u", "U") and is_ajadi(uttarapadam):
      return purvapadam[:-1] + "v" + uttarapadam
   if purvapadam[-1] in ("f", "F") and is_ajadi(uttarapadam):
      return purvapadam[:-1] + "r" + uttarapadam
   elif purvapadam[-1] in ("x", "X") and is_ajadi(uttarapadam):
      return purvapadam[:-1] + "l" + uttarapadam

   #savarnadirgha
   elif purvapadam[-1] in ("a", 'A') and uttarapadam[0] in ("a", "A"):
      return purvapadam[:-1] + "A" + uttarapadam[1:]
   elif purvapadam[-1] in ("i", "I") and uttarapadam[0] in ("i", "I"):
      return purvapadam[:-1] + "I" + uttarapadam[1:]
   if purvapadam[-1] in ("u", "U") and uttarapadam[0] in ("u", "U"):
      return purvapadam[:-1] + "U" + uttarapadam[1:]
   elif purvapadam[-1] in ("f", "F", "x", "X") and uttarapadam[0] in ("f", "F", "x", "X"):
      return purvapadam[:-1] + "F" + uttarapadam[1:]
   
   else:
      return purvapadam + uttarapadam

def get_string_between(s, start_char, end_char):
    try:
        start_index = s.index(start_char) + 1
        end_index = s.index(end_char, start_index)
        return s[start_index:end_index]
    except ValueError:
        return "Characters not found in the string."

def load_dhatus():
   # Open and load the JSON file
   with open("dhaatu_patha_slp1.json", 'r') as file:
    all_dhatus = json.load(file)
    return [get_string_between(d["dhatu_mod"], '(', ')') if '(' in d["dhatu_mod"] else d["dhatu_mod"] for d in all_dhatus]
   
def find_is_dhatu_set(dhatu_mod_slp):
   # Open and load the JSON file
   with open("dhaatu_patha_slp1.json", 'r') as file:
    all_dhatus = json.load(file)
    dhatu_lookup =  list(filter(lambda d: d["dhatu_mod"] == dhatu_mod_slp, all_dhatus))[0]
    return dhatu_lookup["iT"] == "sew"
   
def is_pratyaya_set(pratyaya, pratyaya_mod):
   it_in_pratyaya = set(pratyaya) - set(pratyaya_mod)
   return (('S' not in it_in_pratyaya) and is_valadi(pratyaya_mod))


def load_krt_pratyayas():
    with open("krt-pratyayas.csv", mode='r', newline='') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return [{"krt_pratyaya": row["krt_pratyaya"], "mod_krt_pratyaya": row["mod_krt_pratyaya"]} for row in data]

def get_sarupa_ya_pratyaya(dhatu: str):
  if (is_ajanta(dhatu) and dhatu[-1] != 'f'):
     return "yat"
  elif(is_halanta(dhatu) or dhatu[-1] == 'f'):
     return "Ryat"
  elif(dhatu == "Kan"):
     return "kyap"

def join_with_sandhi(dhatu, is_dhatu_set, pratyaya, pratyaya_mod):
   updated_pratyaya = pratyaya_mod
   if is_dhatu_set and is_pratyaya_set(pratyaya, pratyaya_mod):
      updated_pratyaya = "i" + pratyaya_mod
   return perform_sandhi(dhatu, updated_pratyaya)

def apply_natvam(term):
   is_nimittam_there = ('r' in set(term) or 's' in set(term))
   result_term = term
   if not is_nimittam_there:
      return term
   index = min(term.find('r'), term.find('s'))
   for idx in range(index+1, len(term)):
      if term[idx] in {'a', 'A', 'i', 'I', 'u', 'U', 'f', 'F', 'x', 'X', 'e', 'E', 'o', 'O'} or term[idx] in {'h', 'y', 'v', 'r'} or term[idx] in {'k', 'K', 'g', 'G', 'N'}  or term[idx] in {'p','P','b','B','m'}:
         continue
      elif term[idx] == 'n':
         result_term = result_term[:idx]+'R'+result_term[idx+1:]
         return result_term
   return result_term

def perform_samanya_prakriya(dhatu, pratyaya, pratyaya_mod):
   is_dhatu_set = find_is_dhatu_set(dhatu)
   if dhatu[-1].lower() in ('i', 'u', 'f', 'x'):
      # igantasya guna
      dhatu = f"{dhatu[:len(dhatu)-1]}{perform_guna(dhatu[-1])}"
      # laghupadhasya guna
   if dhatu[-2] in ('a', 'i', 'u', 'f'):
      dhatu = f"{dhatu[:len(dhatu)-2]}{perform_guna(dhatu[-2])}{dhatu[-1]}"
   return apply_natvam(join_with_sandhi(dhatu, is_dhatu_set, pratyaya, pratyaya_mod))

def perform_Yit_Rit(dhatu, pratyaya, pratyaya_mod):
   is_dhatu_set = find_is_dhatu_set(dhatu)
   # ajantasya vrddhi
   if (is_ajanta(dhatu)):
    dhatu = f"{dhatu[:len(dhatu)-1]}{perform_vrddhi(dhatu[-1])}"
   # adupadhasya vrddhi 
   if (dhatu[-2] == 'a'):
      dhatu = f"{dhatu[:len(dhatu)-2]}{perform_vrddhi(dhatu[-2])}{dhatu[-1]}"
   # laghupadhasya guna
   elif dhatu[-2] in ('i', 'u', 'f'):
      dhatu = f"{dhatu[:len(dhatu)-2]}{perform_guna(dhatu[-2])}{dhatu[-1]}"
   # otherwise guna

   #AtaH yuk?
   return apply_natvam(join_with_sandhi(dhatu, is_dhatu_set, pratyaya, pratyaya_mod))

def perform_kit_Nit(dhatu, pratyaya, pratyaya_mod):
   is_dhatu_set = find_is_dhatu_set(dhatu)
   #guna vrddhi nishedha
   return dhatu

def perform_krt_prakriya(dhatu, pratyaya, mod_pratyaya):
   it_letters = set(pratyaya) - set(mod_pratyaya)
   if ('k' in it_letters or 'N' in it_letters):
      return perform_kit_Nit(dhatu, pratyaya, mod_pratyaya)

   if ('Y' in it_letters or 'R' in it_letters):
      return perform_Yit_Rit(dhatu, pratyaya, mod_pratyaya)
   
   else:
      return perform_samanya_prakriya(dhatu, pratyaya, mod_pratyaya)

def main():
    """ Main entry point of the app """
    all_dhatus = load_dhatus()
    while True:
      dhatu = input("Enter a dhAtu (type 'exit' to quit): ")
      if dhatu.lower() == 'exit':
        print("Exiting...")
        break
      else:
        if dhatu not in all_dhatus:
           print("Not a valid SLP dhatu... Exiting...")
           break
        selected_ya_pratyaya = get_sarupa_ya_pratyaya(dhatu)
        print(f"You entered: {dhatu}. ya pratyaya form {selected_ya_pratyaya}")




if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()