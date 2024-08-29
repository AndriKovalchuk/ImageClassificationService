import pathlib

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DocumentForm, EditDocumentForm
from .models import Document
from .utils import add_document_to_index, extract_text_from_document

FAISS_INDEX_PATH = 'faiss_index/faiss_index_file.index'


@login_required
def my_documents(request):
    documents = Document.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'pdf_process/my_documents.html', {"documents": documents})


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # створюємо форму
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_extension = pathlib.Path(uploaded_file.name).suffix.lower().replace('.', '')

            extract_function_map = {
                'pdf': extract_text_from_document,
                'docx': extract_text_from_document,
                'txt': extract_text_from_document,
            }

            text_extract_function = extract_function_map.get(file_extension)

            if text_extract_function:
                document_text = text_extract_function(uploaded_file)
                document = form.save(commit=False)

                # обробка файлу
                document.text = document_text
                document.user = request.user
                document.original_name = uploaded_file.name

                document.save()

                # перетворюємо текст на вектор і додаємо до FAISS (faiss_index_file.index)
                add_document_to_index(document.id, document_text)

                return redirect('pdf_process:upload_success')
            else:
                return render(request, 'pdf_process/my_documents.html',
                              {'form': form, 'error': 'Unsupported file type'})

    else:
        form = DocumentForm()
    return render(request, 'pdf_process/upload_document.html', {'form': form})


@login_required
def upload_success(request):
    return render(request, 'pdf_process/upload_success.html')


@login_required
def edit_document_view(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)

    return render(request, 'pdf_process/edit_document.html', {
        'document': document
    })


@login_required
def edit_document_name(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)

    if request.method == 'POST':
        form = EditDocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('pdf_process:my_documents')
    else:
        form = EditDocumentForm(instance=document)

    return render(request, 'pdf_process/edit_document_name.html', {'form': form, 'document': document})


@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    document.delete()
    return redirect('pdf_process:my_documents')
