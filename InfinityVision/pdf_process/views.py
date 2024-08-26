from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PDFDocumentForm
from .models import PDFDocument
from .utils import extract_text_from_pdf, add_document_to_index

FAISS_INDEX_PATH = 'faiss_index/faiss_index_file.index'


@login_required
def my_pdfs(request):
    pdfs = PDFDocument.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'pdf_process/my_pdfs.html', {"pdfs": pdfs})


@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)  # створюємо форму
        if form.is_valid():
            pdf_document = form.save(commit=False)

            # обробка файлу
            pdf_file = request.FILES['file']
            pdf_text = extract_text_from_pdf(pdf_file)
            pdf_document.text = pdf_text
            pdf_document.user = request.user
            pdf_document.original_name = pdf_file.name

            pdf_document.save()

            # перетворюємо текст на вектор і додаємо до FAISS (faiss_index_file.index)
            add_document_to_index(pdf_document.id, pdf_text)

            return redirect('pdf_process:upload_success')
    else:
        form = PDFDocumentForm()
    return render(request, 'pdf_process/upload_pdf.html', {'form': form})


@login_required
def upload_success(request):
    return render(request, 'pdf_process/upload_success.html')
