# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from ID import IDValidator  # Corrected import statement
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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ID import IDValidator  # Corrected import statement
import pytesseract
from PIL import Image
import re
import PyPDF2
import csv
import io

class DocumentUploadView(APIView):

    def post(self, request, format=None):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        content_type = uploaded_file.content_type

        try:
            text = ""
            if content_type.startswith('image/'):
                image = Image.open(uploaded_file)
                text = pytesseract.image_to_string(image)
            elif content_type == 'text/plain':
                text = uploaded_file.read().decode('utf-8')
            elif content_type == 'application/pdf':
                reader = PyPDF2.PdfReader(uploaded_file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            elif content_type == 'text/csv':
                csv_file = io.StringIO(uploaded_file.read().decode('utf-8'))
                reader = csv.reader(csv_file)
                for row in reader:
                    text += ' '.join(row) + '\n'
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

