# # from .utils import load_image_from_url, resize_image
# # from .ocr import extract_text_score
# # from .face import face_match_score
# # import cv2



# from .utils import load_image_from_url
# from .ocr import extract_kyc_data
# from .compare_doc import compare_docs


# def run_kyc_pipeline(kyc):
#     try:
#         # -------------------------
#         # LOAD IMAGES
#         # -------------------------
#         doc1 = load_image_from_url(kyc.document1)
#         doc2 = load_image_from_url(kyc.document2)

#         if doc1 is None or doc2 is None:
#             return {
#                 "status": "rejected",
#                 "confidence": 0,
#                 "reason": "Image load failed"
#             }

#         # -------------------------
#         # OCR EXTRACTION
#         # -------------------------
#         data1 = extract_kyc_data(doc1)
#         data2 = extract_kyc_data(doc2)

#         # -------------------------
#         # COMPARE
#         # -------------------------
#         confidence = compare_docs(data1, data2)

#         # -------------------------
#         # FINAL DECISION
#         # -------------------------
#         if confidence >= 0.8:
#             status = "verified"
#         elif confidence >= 0.4:
#             status = "review"
#         else:
#             status = "rejected"

#         return {
#             "status": status,
#             "confidence": round(confidence, 2),
#             # "doc1": data1,
#             # "doc2": data2
#         }

#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e)
#         }

















# # def image_quality_score(image):
# #     try:
# #         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #         variance = cv2.Laplacian(gray, cv2.CV_64F).var()

# #         if variance < 50:
# #             return 0.3
# #         elif variance < 100:
# #             return 0.5
# #         else:
# #             return 0.8
# #     except:
# #         return 0.2


# # def run_kyc_pipeline(kyc):
# #     try:
# #         # 1. Load images
# #         doc_img = load_image_from_url(kyc.document1)
# #         selfie_img = load_image_from_url(kyc.selfie)

# #         if doc_img is None or selfie_img is None:
# #             return {"status": "rejected", "confidence": 0}

# #         # 2. Resize
# #         doc_img = resize_image(doc_img)
# #         selfie_img = resize_image(selfie_img)

# #         # 3. AI checks
# #         ocr_score = extract_text_score(doc_img)
# #         face_score = face_match_score(doc_img, selfie_img)
# #         quality_score = image_quality_score(doc_img)
        
        
# #         if face_score >= 0.8 and ocr_score >=0.6:
# #             status ='verified'
# #         elif face_score >=0.5 or ocr_score >= 6.5 and quality_score >= 6.5:
# #             status = 'review'
# #         else:
# #             status ='rejected'

# #         # 4. Combine
# #         confidence = (
# #             ocr_score * 0.3 +
# #             face_score * 0.5 +
# #             quality_score * 0.2
# #         )
        
# #         if face_score >= 0.8 and ocr_score>=0.7:
# #             confidence+=1

        

# #         return {
# #             "status": status,
# #             "confidence": round(confidence, 2),
# #             "ocr_score": round(ocr_score, 2),
# #             "face_score": face_score,
# #             "quality_score": round(quality_score, 2)
# #         }

# #     except Exception as e:
# #         return {
# #             "status": "error",
# #             "confidence": 0,
# #             "error": str(e)
# #         }