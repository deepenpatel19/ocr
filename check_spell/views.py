from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import io
import os
from google.cloud import vision
from google.cloud.vision import types
from autocorrect import spell
import re
from .forms import UploadForm
from .models import UploadImage
# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        # print('form post method')
        # print(request.FILES)
        form = UploadForm(request.POST, request.FILES)
        # print(form)
        # print(form.data)
        # print(dir(form))
        if form.is_valid():
            # print('form is valid')
            post = form.save(commit=False)
            post.save()
            return redirect('ocr_details', pk=post.pk)
        else:
            print('form not valid')
    else:
        form = UploadForm()
    return render(request, 'upload_file.html', {'form': form})


def check_spell(line):
    words = line.split() if line else ""
    # print(words)
    for index in range(len(words)):
        # print(index)
        word = words[index]
        except_punctuation = re.match('^[^?!.]*[?.!]$', word) is not None
        # except_punctuation = re.findall(r'[.?\-",]+', word) is not None
        # print(except_punctuation)
        if except_punctuation:
            pass
        elif spell(word) != word:
            # print('spell changed.')
            # print(spell(word))
            words[index] = spell(word)
        else:
            pass
        # print(words)
    if words:
        new_line = " ".join(words)
    else:
        new_line = " "
    return new_line


class OCRDetails(View):

    def get(self, request, pk=None):
        if pk:
            print('Form uploaded and retrieve data.')
            image = UploadImage.objects.filter(id=pk)
            first_image = image[0] if image else None
            if first_image:
                # print(first_image.name)

                client = vision.ImageAnnotatorClient()
                # print(settings.MEDIA_ROOT)
                file_name = os.path.join(settings.MEDIA_ROOT, str(first_image.name))
                # file_name = first_image.name
                # print(file_name)
                # Loads the image into memory
                with io.open(file_name, 'rb') as image_file:
                    content = image_file.read()

                image = types.Image(content=content)

                # Performs label detection on the image file
                response = client.text_detection(image=image)
                # print(response)
                texts = response.text_annotations
                # print(texts)
                # for text in texts:
                #         print('\n"{}"'.format(text.description))

                google_ocr_result = texts[0].description if texts else None
                print(google_ocr_result)
                # print('-----')

                lines = google_ocr_result.split("\n")
                new_content = []
                for line in lines:
                    new_line = check_spell(line)
                    print('new line receive, ', new_line)
                    new_content.append(new_line)
                new_content = ' '.join(new_content)


        else:
            print('PK not found.')

        return render(request, 'ocr.html', locals())
