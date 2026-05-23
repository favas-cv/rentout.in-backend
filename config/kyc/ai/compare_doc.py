# def normalize_name(name):
#     if not name:
#         return ""

#     name = name.replace("1", "I")  # fix OCR issue
#     name = name.replace("0", "O")
#     return name.strip()


# def name_match(n1, n2):
#     if not n1 or not n2:
#         return False

#     n1 = normalize_name(n1)
#     n2 = normalize_name(n2)

#     return n1 == n2 or n1.split()[0] == n2.split()[0]


# def compare_docs(doc1_data, doc2_data):
#     score = 0

#     # -------------------------
#     # Aadhaar present
#     # -------------------------
#     if doc1_data.get("aadhaar"):
#         score += 0.3

#     # -------------------------
#     # PAN present
#     # -------------------------
#     if doc2_data.get("pan"):
#         score += 0.3

#     # -------------------------
#     # DOB match
#     # -------------------------
#     dob1 = doc1_data.get("dob")
#     dob2 = doc2_data.get("dob")

#     if dob1 and dob2:
#         if dob1 == dob2:
#             score += 0.2

#     # -------------------------
#     # NAME match
#     # -------------------------
#     name1 = doc1_data.get("name")
#     name2 = doc2_data.get("name")

#     if name_match(name1, name2):
#         score += 0.2

#     return score