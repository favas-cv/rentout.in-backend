# import easyocr
# import re

# reader = easyocr.Reader(['en'], gpu=False)


# # -------------------------
# # CLEAN TEXT
# # -------------------------
# def clean_text(text):
#     text = text.upper()
#     text = re.sub(r"[^A-Z0-9/ ]", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     return text


# # -------------------------
# # EXTRACT NAME
# # -------------------------
# def extract_name(text):
#     words = text.split()

#     # Try finding name before DOB
#     for i in range(len(words)):
#         if re.match(r"\d{2}/\d{2}/\d{4}", words[i]):
#             if i >= 2:
#                 name = words[i-2] + " " + words[i-1]
#                 if name.isalpha():
#                     return name

#     # Try finding name after PAN
#     for i in range(len(words)):
#         if re.match(r"[A-Z]{5}[0-9]{4}[A-Z]", words[i]):
#             if i+2 < len(words):
#                 name = words[i+1] + " " + words[i+2]
#                 if name.isalpha():
#                     return name

#     return None

# # -------------------------
# # MAIN OCR FUNCTION
# # -------------------------
# def extract_kyc_data(image):
#     try:
#         result = reader.readtext(image, detail=1, paragraph=True)

#         raw_text = " ".join([r[1] for r in result])
#         text = clean_text(raw_text)

#         # -------------------------
#         # Aadhaar (handle OCR O->0)
#         # -------------------------
#         aadhaar_text = text.replace("O", "0")
#         aadhaar = re.findall(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text.replace("O","0"))

#         aadhaar = aadhaar[0] if aadhaar else None

#         if aadhaar:
#             aadhaar = aadhaar.replace(" ", "")
#         # -------------------------
#         # PAN
#         # -------------------------
#         pan = re.findall(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)

#         # -------------------------
#         # DOB
#         # -------------------------
#         dob = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", text)

#         if not dob:
#             yob = re.findall(r"\b(?:19|20)\d{2}\b", text)
#         # -------------------------
#         # NAME
#         # -------------------------
#         name = extract_name(text)

#         return {
#             "text": text,
#             "aadhaar": aadhaar[0] if aadhaar else None,
#             "pan": pan[0] if pan else None,
#             "dob": dob[0] if dob else None,
#             "name": name
#         }

#     except Exception as e:
#         return {
#             "error": str(e)
#         }