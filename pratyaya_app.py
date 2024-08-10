from indic_transliteration import sanscript
from indic_transliteration.sanscript import DEVANAGARI, SLP1, transliterate

import streamlit as st

from krt_pratyaya import (get_sarupa_ya_pratyaya,
  load_dhatus,
  load_krt_pratyayas, 
  perform_krt_prakriya)


all_dhatus = load_dhatus()
all_krt_pratyayas = load_krt_pratyayas()

# Set the title of the app
st.title(f"{transliterate('pratyayayojanam', SLP1, DEVANAGARI)}")

# Create a text input widget
dhatu = st.text_input(f"{transliterate('DAtuH atra', SLP1, DEVANAGARI)}")

# Create a text input widget
pratyaya = st.text_input(f"{transliterate('pratyayaH atra', SLP1, DEVANAGARI)}")


# Create a button
if st.button("Submit"):
  if dhatu and pratyaya:
    dhatu_slp = transliterate(dhatu, DEVANAGARI, SLP1)
    pratyaya_slp = transliterate(pratyaya, DEVANAGARI, SLP1)
    is_valid_dhatu = dhatu_slp in all_dhatus
    is_valid_pratyaya = pratyaya in set([kp["krt_pratyaya"] for kp in all_krt_pratyayas])
    if not is_valid_dhatu:
        st.warning(f"{dhatu} {transliterate('OpadeSikaH DAtuH nAsti', SLP1, DEVANAGARI)}")
    
    elif not is_valid_pratyaya:
       st.warning(f"{pratyaya} {transliterate('pratyayaH nAsti', SLP1, DEVANAGARI)}")
       
    elif is_valid_dhatu and is_valid_pratyaya:
       pratyaya_full = [p for p in all_krt_pratyayas if p["krt_pratyaya"] == pratyaya][0]
       mod_pratyaya_slp = transliterate(pratyaya_full["mod_krt_pratyaya"], DEVANAGARI, SLP1)
       result = perform_krt_prakriya(dhatu_slp, pratyaya_slp, mod_pratyaya_slp)
       print(f"res {result}")
       if result is None:
           st.warning(f"{dhatu} + {pratyaya} yojanam ashakyam idAnIm")
       else:
          st.write(transliterate(result, SLP1, DEVANAGARI))
else:
   st.warning(f"{transliterate('kfpayA DAtuH pratyayaH dvayamapi dIyatAm', SLP1, DEVANAGARI)}")