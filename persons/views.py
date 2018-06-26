import time
import os
import json
from django.shortcuts import render
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.files.images import get_image_dimensions
from .utils import BlankDict
 
from django.conf import settings
#models
from persons.models import Person
from face.models import Face
from tempimg.models import TempImg
#forms
from .forms import PersonForm
from face.forms import FaceForm
from tempimg.forms import TempImgForm

import cognitive_face as CF

#PERSON CERATE
@login_required
def person_create(request):
	if request.method == 'POST':
		form = PersonForm(request.POST, request.FILES)
		if form.is_valid():
			CF.Key.set(settings.MICROSOFT_KEY)
			CF.BaseUrl.set(settings.MICROSOFT_BASE_URL)

			person = form.save(commit=False)
			person_full_name = person.name + ' '+ person.last_name
			result_person = CF.person.create('test_face', person_full_name)
			person.user = request.user
			person.personid = result_person.get('personId', None)
			person.save()
			url_person = '/sujetos/%s/'%(person.pk)
			return HttpResponseRedirect(url_person)
	else:
		form = PersonForm()

	return render(request, 'persons/person_new.html', {'form': form})

#PERSON FORM
@login_required()
def person_update(request, pk):
	data = dict()
	person = get_object_or_404(Person, pk=pk)

	if request.method =='POST':
		form = PersonForm(request.POST, instance=person)
		if form.is_valid():
			person = form.save()
			data['form_is_valid'] = True
			data['html_person_detail'] = render_to_string('persons/includes/partial_box_body_detail.html',{'person': person},request= request)
		else:
			data['form_is_valid'] = False
	else:
		form = PersonForm(instance = person)

	data['html_form'] = render_to_string('persons/includes/partial_person_update.html',{'form': form}, request= request)

	return JsonResponse(data)

#PERSON DETAIL
@login_required()
def person_detail(request, pk):
	person = get_object_or_404(Person, pk=pk)
	face_count = Face.objects.filter(person=person.pk).count()
	return render(request, 'persons/person_add_file.html', {'person': person, 'face_count': face_count})

#PERSON ADD FACE
@login_required()
def person_add_face(request, pk):
	person = get_object_or_404(Person, pk=pk)
	data = dict()
	if request.method == 'POST':
		form = FaceForm(request.POST, request.FILES)
		if form.is_valid():
			CF.Key.set(settings.MICROSOFT_KEY)
			CF.BaseUrl.set(settings.MICROSOFT_BASE_URL)
			face = form.save(commit=False)
			face.user = request.user
			face.person = person
			face.save()
			person = get_object_or_404(Person, pk=pk)
			img_url = os.path.abspath(settings.MEDIA_ROOT +'/' + face.img.thumbnail['700x700'].name)
			result_face = CF.person.add_face(img_url, 'test_face', person.personid)
			face.faceid = result_face.get('persistedFaceId',None)
			face.save()
			train_m = CF.person_group.train('test_face')
			face_count = Face.objects.filter(person=person.pk).count()
			width, height = get_image_dimensions(img_url)
			data['img_height'] = height
			data['img_width'] = width
			data['is_valid'] = True
			data['html_person_button'] = render_to_string('persons/includes/partial_face_count.html', {
                        'face_count': face_count
                    })
		else:
			data['is_valid'] = False
	else:
		pass
	return JsonResponse(data)

#GET PERSON IDENT
@login_required
def person_identify(request):
	return render(request, 'persons/person_identify.html')

#GET PERSON VERIFY
@login_required
def person_verify(request,pk):
	person = get_object_or_404(Person, pk=pk)
	return render(request, 'persons/person_verify.html',{'person': person})

#ONLY POST PERSON IDENTIFY
@login_required
def person_identify_by_face(request):

	data = dict()
	if request.method == 'POST':
		
		form = TempImgForm(request.POST, request.FILES)
		if form.is_valid():
			face = form.save(commit=False)
			face.user = request.user
			face.save()
			CF.Key.set(settings.MICROSOFT_KEY)
			CF.BaseUrl.set(settings.MICROSOFT_BASE_URL)
			img_url = os.path.abspath(settings.MEDIA_ROOT +'/' + face.img.thumbnail['700x700'].name)
			result_face = CF.face.detect(img_url)
			json_result_face = result_face
			

			face_ids = []
			person_ids = []
			rectangles = []
			for face_cloud in json_result_face:
				if face_cloud.get("faceId",""):
					faceId = face_cloud.get("faceId","")
					data_rectangle = dict()
					data_rectangle['rectangle_x'] = face_cloud["faceRectangle"].get('left',None)
					data_rectangle['rectangle_y'] = face_cloud["faceRectangle"].get('top',None)
					data_rectangle['rectangle_w'] = face_cloud["faceRectangle"].get('width',None)
					data_rectangle['rectangle_h'] = face_cloud["faceRectangle"].get('height',None)
					face_ids.append(faceId)
					rectangles.append(data_rectangle)
					
			result_list = CF.face.identify(face_ids,'test_face',4)
			json_result_list = result_list

			for identify_r in json_result_list:
				if identify_r.get("candidates",""):
					person_list_id = identify_r.get("candidates","")

					for item in person_list_id:
						person_ids.append(item.get("personId","00"))

			person_list = Person.objects.filter(personid__in=person_ids)
			print(person_list)
			data['rectangles'] = rectangles
			data['html_person_list'] = render_to_string('persons/includes/partial_identify_list_results.html', {
                        'person_list': person_list
                    })
			data['html_person_scream'] = render_to_string('persons/includes/partial_scream.html', {
                        'face': face
                    })
			data['is_valid'] = True
		else:
			data['is_valid'] = False
	else:
		pass
	return JsonResponse(data)

#ONLY POST PERSON IDENTIFY
@login_required
def person_verify_by_face(request, pk):

	data = dict()
	if request.method == 'POST':
		person = get_object_or_404(Person, pk=pk)
		form = TempImgForm(request.POST, request.FILES)
		if form.is_valid():
			face = form.save(commit=False)
			face.user = request.user
			face.save()
			CF.Key.set(settings.MICROSOFT_KEY)
			CF.BaseUrl.set(settings.MICROSOFT_BASE_URL)
			img_url = os.path.abspath(settings.MEDIA_ROOT +'/' + face.img.thumbnail['700x700'].name)
			result_face = CF.face.detect(img_url)
			json_result_face = result_face
			print(json_result_face)

			face_ids = []
			person_ids = []
			rectangles = []
			for face_cloud in json_result_face:
				if face_cloud.get("faceId",""):
					faceId = face_cloud.get("faceId","")
					data_rectangle = dict()
					data_rectangle['rectangle_x'] = face_cloud["faceRectangle"].get('left',None)
					data_rectangle['rectangle_y'] = face_cloud["faceRectangle"].get('top',None)
					data_rectangle['rectangle_w'] = face_cloud["faceRectangle"].get('width',None)
					data_rectangle['rectangle_h'] = face_cloud["faceRectangle"].get('height',None)
					face_ids.append(faceId)
					rectangles.append(data_rectangle)
			
			id_face = face_ids[0]
			person_id = person.personid
			result_list = CF.face.verify(id_face,None,'test_face', person_id)
			json_result_identy = result_list
			print(json_result_identy)
			data['rectangles'] = rectangles
			data['isIdentical'] =json_result_identy.get("isIdentical","")
			data['confidence'] =json_result_identy.get("confidence","")

			data['html_person_scream'] = render_to_string('persons/includes/partial_scream.html', {
                        'face': face
                    })
			data['is_valid'] = True
		else:
			data['is_valid'] = False
	else:
		pass
	return JsonResponse(data)

#ONLY POST PERSON SEACH
@login_required
def person_search(request):
	data = dict()
	if request.method == 'GET':
		search_query = request.GET.get('search_box', "hola")
		if search_query:
			try:
				person = Person.objects.get(id_person=search_query)
				print(person)
				url = "/sujetos/%s/verificar/"%(person.pk)
				data['redirect'] = url
			except Person.DoesNotExist:
				data['form_is_valid'] = False
		else:
			data['form_is_valid'] = False
	return JsonResponse(data)

#PERSON LIST
@login_required()
def person_list(request):
	persons = Person.objects.all().order_by('-created_at')
	context = {
		'persons': persons,
	}
	return render(request, 'persons/person_list.html', context)

def person_add_cloud(request):
	CF.Key.set(settings.MICROSOFT_KEY)
	BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'

	CF.BaseUrl.set(settings.MICROSOFT_BASE_URL)
	result = CF.person.create('test_face','JONATAN PEREZ')
	return HttpResponse(result)

def person_get_cloud(request):
	CF.Key.set(settings.MICROSOFT_KEY)
	

	CF.BaseUrl.set(settings.MICROSOFT_BASE_URL)
	result = CF.person.lists('test_face')
	print(result)
	for item in result:
		print(item.get('personId', '--'))
	return HttpResponse(result)

def person_test(request):
	face = get_object_or_404(Face, pk=1)
	
	CF.Key.set(settings.MICROSOFT_KEY)
	CF.BaseUrl.set(settings.MICROSOFT_BASE_URL)
	
	img_url = os.path.abspath(settings.MEDIA_ROOT +'/' + face.img.thumbnail['800x800'].name)

	print(img_url)
	result_face = CF.person.add_face(img_url, 'test_face', '62a127f4-92e1-4b88-a028-901a28d2a0c3')
	print(result_face)
	return HttpResponse('ok')