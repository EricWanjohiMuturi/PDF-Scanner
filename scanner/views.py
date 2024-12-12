from django.shortcuts import render
from .forms import upload_file
import pdfplumber

# Create your views here.
def index(request):
    return render(request, "lead/index.html")

def login_view(request):
    return render(request, "auth/login.html")

def forgot_pass(request):
    return render(request, "auth/forgotpass.html")

def scan_view(request):
    if request.method == 'POST':
        upload = upload_file(request.POST, request.FILES)
        if upload.is_valid():
            pdf_file = request.FILES['file']
            keyword = upload.cleaned_data['keyword']
            try:
                keyword_count = 0
                keyword_pages = []
                keyword_contexts = []  # To store occurrences with context

                # Processing PDF file
                with pdfplumber.open(pdf_file) as pdf:
                    for page_number, page in enumerate(pdf.pages, start=1):
                        text = page.extract_text()
                        if text:
                            lower_text = text.lower()
                            lower_keyword = keyword.lower()
                            # Count occurrences of the keyword
                            count = lower_text.count(lower_keyword)
                            if count > 0:
                                keyword_count += count
                                keyword_pages.append(page_number)
                                # Extract context for each occurrence
                                start = 0
                                while True:
                                    start = lower_text.find(lower_keyword, start)
                                    if start == -1:
                                        break
                                    # Define context window
                                    context_start = max(0, start - 100)  # 30 characters before
                                    context_end = min(len(text), start + len(keyword) + 100)  # 30 characters after

                                    # Append context to list
                                    keyword_contexts.append({
                                        'page': page_number,
                                        'context': text[context_start:context_end].strip()
                                    })

                                    start += len(lower_keyword)  # Move past the current match

                # Pass results to the template
                context = {
                    'keyword': keyword,
                    'keyword_count': keyword_count,
                    'keyword_pages': keyword_pages,
                    'keyword_contexts': keyword_contexts,
                }
                return render(request, 'results/results.html', context)
            except Exception as e:
                return render(request, 'scan/scan.html', {'upload': upload, 'error': 'Error processing the PDF.'})
    else:
        upload = upload_file()
    return render(request, 'scan/scan.html', {'upload': upload})    

