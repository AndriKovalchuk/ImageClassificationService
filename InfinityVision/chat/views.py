from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from pdf_process.models import Document, QueryHistory
from transformers import pipeline

model_name = "deepset/roberta-base-squad2"  # локально

nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)  # на виході - словник


@login_required
def chat(request, document_id):
    document = Document.objects.get(id=document_id, user=request.user)

    # print(f"PDF Text: {document.text}")

    queries = QueryHistory.objects.filter(user=request.user, document=document).order_by('-created_at')

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()  # шукаємо запитання
        if question:
            answer = get_answer_from_pdf(document.text, question)
            QueryHistory.objects.create(user=request.user, document=document, question=question, answer=answer)

        return redirect('chat', document_id=document.id)

    return render(request, 'chat_ai/chat.html', {'document': document, 'queries': queries})


def get_answer_from_pdf(text, question):
    QA_input = {
        'question': question,
        'context': text  # буде здійснюватися пошук відповіді
    }
    result = nlp(QA_input)
    print(result)  # {'score': 0.3617405891418457, 'start': 0, 'end': 15, 'answer': 'Elon Reeve Musk'}

    return result['answer'] if result['answer'].strip() else "No answer found"
