# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .pii_detector import IDValidator

# class DocumentUploadView(APIView):
#     def post(self, request, format=None):
#         uploaded_file = request.FILES.get('file')
        
#         if not uploaded_file:
#             return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

#         # Read file contents
#         try:
#             file_data = uploaded_file.read().decode('utf-8')
#         except UnicodeDecodeError:
#             return Response({"error": "Unable to decode file content. Please upload a valid text file."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         # PII Detection
#         validator = IDValidator()
#         results = validator.find_ids(file_data)

#         return Response({"results": results}, status=status.HTTP_200_OK)
#----------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .pii_detector import IDValidator
# import pytesseract
# from PIL import Image
# from django.core.files.storage import default_storage

# class DocumentUploadView(APIView):
#     def post(self, request, format=None):
#         uploaded_file = request.FILES.get('file')
        
#         if not uploaded_file:
#             return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check file type and extract text accordingly
#         if uploaded_file.content_type.startswith('image'):
#             # Save uploaded image temporarily
#             file_path = default_storage.save(uploaded_file.name, uploaded_file)
#             try:
#                 image = Image.open(default_storage.open(file_path))
#                 file_data = pytesseract.image_to_string(image)
#             except Exception as e:
#                 default_storage.delete(file_path)
#                 return Response({"error": f"Failed to process image: {str(e)}"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             finally:
#                 # Clean up saved file
#                 default_storage.delete(file_path)
#         else:
#             # Assume text file and decode
#             try:
#                 file_data = uploaded_file.read().decode('utf-8')
#             except UnicodeDecodeError:
#                 return Response({"error": "Unable to decode file content. Please upload a valid text file."},
#                                 status=status.HTTP_400_BAD_REQUEST)

#         # Run PII Detection on extracted text
#         validator = IDValidator()
#         results = validator.find_ids(file_data)

#         return Response({"results": results}, status=status.HTTP_200_OK)

#----------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .pii_detector import IDValidator
# import pytesseract
# from PIL import Image
# import io

# class DocumentUploadView(APIView):
#     def post(self, request, format=None):
#         uploaded_file = request.FILES.get('file')

#         if not uploaded_file:
#             return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if uploaded file is image or text
#         content_type = uploaded_file.content_type

#         try:
#             if content_type.startswith('image/'):
#                 # Process image with OCR
#                 image = Image.open(uploaded_file)
#                 text = pytesseract.image_to_string(image)
#             elif content_type == 'text/plain':
#                 # Process text file
#                 text = uploaded_file.read().decode('utf-8')
#             else:
#                 return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": f"Failed to process file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

#         # Run PII detection on extracted text
#         validator = IDValidator()
#         results = validator.find_ids(text)

#         return Response({"results": results}, status=status.HTTP_200_OK)
#----------------------------------------------------

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .pii_detector import IDValidator
# import pytesseract
# from PIL import Image
# import io
# import re

# class DocumentUploadView(APIView):

#     def mask_pii(self, text, pii_dict):
#         # Replace each detected PII with 'x' of the same length
#         masked_text = text
#         for id_type, id_list in pii_dict.items():
#             for pii in id_list:
#                 # Escape pii to safely use in regex replacement
#                 escaped_pii = re.escape(pii)
#                 masked_text = re.sub(escaped_pii, 'x' * len(pii), masked_text)
#         return masked_text

#     def post(self, request, format=None):
#         uploaded_file = request.FILES.get('file')

#         if not uploaded_file:
#             return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

#         content_type = uploaded_file.content_type

#         try:
#             if content_type.startswith('image/'):
#                 image = Image.open(uploaded_file)
#                 text = pytesseract.image_to_string(image)
#             elif content_type == 'text/plain':
#                 text = uploaded_file.read().decode('utf-8')
#             else:
#                 return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": f"Failed to process file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

#         validator = IDValidator()
#         results = validator.find_ids(text)

#         masked_text = self.mask_pii(text, results)

#         return Response({
#             "results": results,
#             "masked_text": masked_text
#         }, status=status.HTTP_200_OK)

#----------------------------------------------------
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .pii_detector import IDValidator
# import pytesseract
# from PIL import Image
# import re

# class DocumentUploadView(APIView):

#     def post(self, request, format=None):
#         uploaded_file = request.FILES.get('file')

#         if not uploaded_file:
#             return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

#         content_type = uploaded_file.content_type

#         try:
#             if content_type.startswith('image/'):
#                 image = Image.open(uploaded_file)
#                 text = pytesseract.image_to_string(image)
#             elif content_type == 'text/plain':
#                 text = uploaded_file.read().decode('utf-8')
#             else:
#                 return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": f"Failed to process file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

#         validator = IDValidator()
#         results = validator.find_ids(text)

#         masked_text = validator.mask_ids(text)  # Use your class method for masking

#         return Response({
#             "results": results,
#             "masked_text": masked_text
#         }, status=status.HTTP_200_OK)
#----------------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ID import IDValidator  # Corrected import statement
import pytesseract
from PIL import Image
import re

class DocumentUploadView(APIView):

    def post(self, request, format=None):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        content_type = uploaded_file.content_type

        try:
            if content_type.startswith('image/'):
                image = Image.open(uploaded_file)
                text = pytesseract.image_to_string(image)
            elif content_type == 'text/plain':
                text = uploaded_file.read().decode('utf-8')
            else:
                return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to process file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        validator = IDValidator()
        results = validator.find_ids(text)

        masked_text = validator.mask_ids(text)  # Use your class method for masking

        return Response({
            "results": results,
            "masked_text": masked_text
        }, status=status.HTTP_200_OK)

