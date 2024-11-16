from django.shortcuts import render
# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.exceptions import NotFound

class InvoiceView(APIView):
    
    def post(self, request, *args, **kwargs):
        """
        Handle creating a new invoice along with its details.
        """
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()  # This will create the invoice and the invoice details
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        """
        Handle updating an existing invoice and its details.
        """
        invoice_number = request.data.get('invoice_number')
        if not invoice_number:
            return Response({'error': 'invoice_number is required for update'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invoice = Invoice.objects.get(invoice_number=invoice_number)  # Fetch the existing invoice
        except Invoice.DoesNotExist:
            raise NotFound(detail="Invoice not found.")
        
        # Use the serializer to update the invoice and its details
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            invoice = serializer.save()  # This will update the invoice and replace its details
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
