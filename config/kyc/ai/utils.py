# import requests
# import numpy as np
# import cv2


# # -------------------------
# # SAFE IMAGE LOADER
# # -------------------------
# def load_image_from_url(url, preprocess=True):
#     try:
#         if not url:
#             print("❌ Empty URL")
#             return None

#         resp = requests.get(url, timeout=5)

#         # ✅ Check response
#         if resp.status_code != 200:
#             print(f"❌ Failed to fetch image: {resp.status_code}")
#             return None

#         # Convert to numpy
#         img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
#         img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#         if img is None:
#             print("❌ OpenCV failed to decode image")
#             return None

#         # Optional preprocessing
#         if preprocess:
#             img = normalize_image(img)

#         return img

#     except Exception as e:
#         print("❌ Error loading image:", str(e))
#         return None


# # -------------------------
# # IMAGE NORMALIZATION
# # -------------------------
# def normalize_image(img):
#     # Resize (keep aspect ratio)
#     img = resize_image(img, 800)

#     # Convert to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Light denoise
#     gray = cv2.GaussianBlur(gray, (3, 3), 0)

#     return gray


# # -------------------------
# # RESIZE FUNCTION
# # -------------------------
# def resize_image(image, size=800):
#     h, w = image.shape[:2]

#     if max(h, w) > size:
#         scale = size / max(h, w)
#         image = cv2.resize(image, (int(w * scale), int(h * scale)))

#     return image


# # -------------------------
# # DEBUG FUNCTION (VERY USEFUL)
# # -------------------------
# def show_image(img, title="Image"):
#     if img is None:
#         print("❌ No image to display")
#         return

#     cv2.imshow(title, img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()