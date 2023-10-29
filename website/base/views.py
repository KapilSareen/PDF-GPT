from django.shortcuts import render,redirect
from django.http import JsonResponse
from gpt_integration.utils import generate_text

from gpt_integration.forms import PdfUploadForm
from .models import ExtractedText
from PyPDF2 import PdfFileReader
import requests
from flask import Flask,jsonify

import openai



openai_api_key= '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response= openai.Completion.create( model= "text-davinci-003",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
           
    answer = response.choices[0].text.strip()
    return answer



def home(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response =  ask_openai(message)

        return JsonResponse({message: 'message', response: 'response'})
    
    return render(request,'home.html')




def generate_response(request):
    prompt = request.POST.get('prompt')
    if prompt:
        response = generate_text(prompt)
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({'error': 'No prompt provided'}, status=400)



def extract_pdf_and_send_to_api(request):
    if request.method == 'POST':
        form = PdfUploadForm(request.POST, request.FILES)

        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']

            try:
                pdf_reader = PdfFileReader(pdf_file)
                extracted_text = ''

                for page_num in range(pdf_reader.getNumPages()):
                    page = pdf_reader.getPage(page_num)
                    extracted_text += page.extractText()

                # Define the API endpoint
                api_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'

                # Define the data to send to the API
                data = {'text': extracted_text}

                # Send a POST request to the API
                response = requests.post(api_url, data=data)

                if response.status_code == 200:
                    # Save the extracted text in your database
                    ExtractedText.objects.create(pdf_file=pdf_file, extracted_text=extracted_text)
                    return JsonResponse({'message': 'Text extracted from the PDF and saved successfully.'})
                else:
                    return JsonResponse({'error': 'Failed to send the text to the API. Status code: ' + str(response.status_code)})
            except Exception as e:
                return JsonResponse({'error': 'Error extracting text from the PDF: ' + str(e)})
        else:
            return JsonResponse({'error': 'Invalid form data.'})
    else:
        form = PdfUploadForm()
    return render(request, 'upload_form.html', {'form': form})


app = Flask(__name__)

@app.route('/get_text', methods=['GET'])
def get_text():
    return jsonify({"text": extracted_text})

if __name__ == "__main__":
    app.run()    