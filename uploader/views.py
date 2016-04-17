from django.shortcuts import render_to_response
from django.template import RequestContext

from PIL import Image
from uploader.models import Document
from uploader.forms import DocumentForm



def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            try:
                img = Image.open(newdoc.docfile)
                imgSize = img.size
            except:
                pass

            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('uploader.views.list'))
            return render_to_response('uploader/list.html',
                {'document': newdoc, 'imgWidth': imgSize[0],
                 'imgHeight': imgSize[1], 'form': form},
                context_instance=RequestContext(request))
    else:
        form = DocumentForm()   # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response('uploader/list.html',
        {'form': form},
        context_instance=RequestContext(request)
    )
