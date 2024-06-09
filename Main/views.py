import json

import cv2
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from .forms import ContactForm, RouteFrom
from .models import Contact
from .utils import send_email_to_client
from django.contrib import messages
from .functions import get_location, get_latitude_longitude
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from .forms import RouteFrom
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from geopy import Nominatim
import logging
from django.http import JsonResponse, HttpResponseRedirect, request
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import osmnx as ox
import networkx as nx
import pandas as pd
from ultralytics import YOLO
import threading
from queue import Queue

'''
    Total 5 Routes 
        - LandingPage      : Nav, MainVideo/ MainModel, Services, Features, Contact Form, Testimonials, Footer 
        - About Page       : Nav, About Content, Footer 
        - LogInSignUp Page : AllAuth
        - GetLLs Page      : Formed based page to take start location and end location from the user along with the Start Monitoring Button 
        - Map Page         : Here the results will be displayed

    Total 2 Forms 
        - Contact Us : On LandingPage  
        - get_loc    : On GetLLs Page  


    Can Implement 
        - Dashboard ( new page ) containing the info of all the previous accidents [ Location, time ]   
'''


def potholes(cctv_id, result_queue):
    '''

    :param cctv_info_map: List of the mapped CCTV Id's
    :param result_queue: Queue to store the results
    :return: Number of detected Potholes
    :working: Input of all the CCTV Id will be given to the function, monitoring will be performed on that cctv and number of potholes
              detected will be calculated and the dict of potholes_coordinates along with the number of potholes will be detected

    '''

    # Loading the Deep Learning Model
    model = YOLO("Models/Potholes_60.pt")

    # For demo purpose
    cctv_info_map = 'static/Videos/Potholes/Potholes.mp4'
    cap = cv2.VideoCapture(cctv_id)
    pothole_details = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run batched inference on a list of images
        results = model(frame)  # return a list of Results objects

        # Process results list
        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs

            # Calculating the number of detected potholes
            if boxes is not None and probs is not None:
                for box, prob in zip(boxes, probs):
                    if prob > 0.65:  # Assuming threshold for pothole detection
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        coord = (x1, y1, x2, y2)
                        if coord in pothole_details:
                            pothole_details[coord] += 1

        # Display the frame
        cv2.imshow('Object Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_cctvs_info(from_lat_float, from_lon_float, to_lat_float, to_lon_float):
    '''

    :param from_lat_float: Floating point latitude of start location
    :param from_lon_float: Floating point longitude of start location
    :param to_lat_float: Floating point lotitude of end location
    :param to_lon_float: Floating point longitude of end location
    :return: The list of CCTV's (including Id's) that are present in the shortest path bw start and end location
    :working: Input of Source and Destination Coordinates entered by the user will be given to the function, shortest distance bw the
              Source and Destination will be calculated and the Coordinates of the shortest distance will be matched with the CCTV
              Coordinates Database and matching Coordinates will be returned

    '''

    G = ox.graph_from_point((from_lat_float, from_lon_float), dist=5000, network_type='all')

    start_node = ox.distance.nearest_nodes(G, from_lon_float, from_lat_float)
    end_node = ox.distance.nearest_nodes(G, to_lon_float, to_lat_float)

    route = nx.shortest_path(G, start_node, end_node, weight='lenght')

    route_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

    print(route_coordinates)

    # TODO: From the given locations add few coordinates in the database ( for each path )
    '''
        - On the menu page, jb user location dalta he tb wo jo autocompelete ki list he usme se saare paths ke thode coordinates database me add kro 
        - Eg. From Pune station To Aga Khan Palace 
    '''
    cctv_data = pd.read_csv('Database/CcTV.csv')

    # Filter the DataFrame based on common coordinates
    common_coordinates_df = cctv_data[
        cctv_data.apply(lambda row: (row['Latitude'], row['Longitude']) in route_coordinates, axis=1)]

    # Display the matching coordinates
    matching_coordinates_with_cam_id = common_coordinates_df['Cam_Id'].values

    return matching_coordinates_with_cam_id


class LandingPage(FormView):
    template_name = 'landingPage.html'
    form_class = ContactForm
    success_url = '/'  # Redirect URL after successful form submission

    def form_valid(self, form):
        form.save()  # This saves the form data to the database using the model

        # To send the contact mail
        ls_email = []
        email = form.cleaned_data['email']
        fname = form.cleaned_data['fname']
        # To get the latest mail
        ls_email.append(email)

        # Calling the actual function
        send_email_to_client(ls_email, fname)

        # To avoid sending mail to the previous users
        ls_email.clear()

        messages.info(self.request, 'Your message has been successfully submitted !! ')

        return super().form_valid(form)


# AboutUs is a TemplateView since we just hv to render a simple template and dont have to perform form based or data retrival frm the models operations
# Creating the About Us Page
class AboutUs(TemplateView):
    template_name = 'about.html'


@method_decorator(csrf_exempt, name='dispatch')
class Map(TemplateView):
    template_name = 'menu.html'


@csrf_exempt
def get_coordinates(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Access the data directly
            from_lat = data.get('fromLat')
            from_lon = data.get('fromLon')
            to_lat = data.get('toLat')
            to_lon = data.get('toLon')

            from_lat_float = float(from_lat)
            from_lon_float = float(from_lon)
            to_lat_float = float(to_lat)
            to_lon_float = float(to_lon)

            print(f"From Lat: {from_lat}, From Lon: {from_lon}")
            print(f"To Lat: {to_lat}, To Lon: {to_lon}")

            # Fetching the Matched CCTV ID's from the DataBase
            cctv_info_map = get_cctvs_info(from_lat_float, from_lon_float, to_lat_float, to_lon_float)

            print(cctv_info_map)

            ''' 
            detected_list = [
                                {Pothole Coordinate : Number, Pothole Coordinate : Number,..},
                                {Traffic Coordinate : Number, Traffic Coordinate : Number,...},
                                [ Accident Coordinate, Accident Coordinate,...]
                            ]
            '''

            # detected_list = {}

            # TODO: APPLY THREADING TO MONITOR ALL THE CCTV ID'S
            # Potholes Detection
            # Traffic Detection
            # Accident Detection

            # Create a demo detected_list
            detected_list = {
                "potholes": [
                    {"lat": from_lat_float + 0.001, "lon": from_lon_float + 0.001, 'num': 0.5},
                    {"lat": from_lat_float + 0.002, "lon": from_lon_float + 0.002, 'num': 0.8},
                ],
                "traffic": [
                    {"lat": to_lat_float - 0.001, "lon": to_lon_float - 0.001, 'num': 0.2},
                    {"lat": to_lat_float - 0.002, "lon": to_lon_float - 0.002, 'num': 0.7},
                ],
                "accidents": [
                    {"lat": (from_lat_float + to_lat_float) / 2, "lon": (from_lon_float + to_lon_float) / 2}
                ]
            }

            return JsonResponse({'status': 'success', 'detected_list': detected_list})

            # return JsonResponse({'status':'success'})

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid JSON format: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid Request Method'})