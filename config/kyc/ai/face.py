# import cv2
# import numpy as np

# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
# )

# def extract_face(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Improve detection
#     gray = cv2.equalizeHist(gray)

#     faces = face_cascade.detectMultiScale(
#     gray,
#     scaleFactor=1.1,
#     minNeighbors=3,
#     minSize=(40, 40)
#     )

#     if len(faces) == 0:
#         return None

#     x, y, w, h = faces[0]

#     # Add padding
#     pad = 20
#     x = max(0, x - pad)
#     y = max(0, y - pad)

#     face = image[y:y+h+pad, x:x+w+pad]

#     return cv2.resize(face, (160, 160))


# def get_embedding(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # normalize lighting
#     gray = cv2.equalizeHist(gray)

#     # reduce noise
#     gray = cv2.GaussianBlur(gray, (3,3), 0)

#     # edge features (IMPORTANT)
#     edges = cv2.Canny(gray, 50, 150)

#     # combine features
#     combined = cv2.addWeighted(gray, 0.7, edges, 0.3, 0)

#     return cv2.resize(combined, (50, 50)).flatten()

# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# def face_match_score(doc_img, selfie_img):
#     try:
#         face1 = extract_face(doc_img)
#         face2 = extract_face(selfie_img)

#         print("Face1 detected:", face1 is not None)
#         print("Face2 detected:", face2 is not None)

#         # 🔥 Case 1: both missing
#         if face1 is None and face2 is None:
#             return 0.2

#         # 🔥 Case 2: one missing → fallback
#         if face1 is None or face2 is None:
#             emb1 = get_embedding(cv2.resize(doc_img, (160, 160)))
#             emb2 = get_embedding(cv2.resize(selfie_img, (160, 160)))

#             similarity = cosine_similarity(emb1, emb2)
#             print("Fallback similarity:", similarity)

#             return 0.5 if similarity > 0.6 else 0.3

#         # 🔥 Case 3: both detected → real match
#         emb1 = get_embedding(face1)
#         emb2 = get_embedding(face2)

#         similarity = cosine_similarity(emb1, emb2)
#         print("Face similarity:", similarity)

#         if similarity > 0.65:
#             return 0.9
#         elif similarity > 0.5:
#             return 0.7
#         elif similarity > 0.35:
#             return 0.5
#         else:
#             return 0.3

#     except Exception as e:
#         print("Face error:", e)
#         return 0.2