# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Document
# from .serializers import DocumentSerializer
# from .pii_detector import detect_pii  # we will create this soon


# class DocumentUploadView(APIView):
#     def post(self, request, *args, **kwargs):
#         file_serializer = DocumentSerializer(data=request.data)
#         if file_serializer.is_valid():
#             document = file_serializer.save()

#             # Read uploaded file content
#             try:
#                 with open(document.file.path, 'r', encoding='utf-8') as f:
#                     content = f.read()
#             except Exception as e:
#                 return Response({'error': f'File read error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#             # Run PII Detection
#             pii_results = detect_pii(content)

#             return Response({
#                 'file': file_serializer.data,
#                 'pii_detection': pii_results
#             }, status=status.HTTP_201_CREATED)
        
#         return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .pii_detector import IDValidator

class DocumentUploadView(APIView):
    def post(self, request, format=None):
        uploaded_file = request.FILES.get('file')
        
        if not uploaded_file:
            return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Read file contents
        try:
            file_data = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response({"error": "Unable to decode file content. Please upload a valid text file."},
                            status=status.HTTP_400_BAD_REQUEST)

        # PII Detection
        validator = IDValidator()
        results = validator.find_ids(file_data)

        return Response({"results": results}, status=status.HTTP_200_OK)
