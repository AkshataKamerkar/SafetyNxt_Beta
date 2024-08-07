import json

import cv2
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from Main.forms import ContactForm, RouteFrom
from .models import Contact
from Main.utils import send_email_to_client
from django.contrib import messages
from Main.functions import get_location, get_latitude_longitude
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from Main.forms import RouteFrom
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
import random
from email.message import EmailMessage
import ssl
import smtplib
import logging
import os

logger = logging.getLogger(__name__)

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


def health(request):
    '''
        - This function is used to automatically check, whether the application is running or not in CI-pipeline
    '''
    return JsonResponse({'status':'running'})
    

def get_location_from_lls(latitude, longitude):

    '''

    :param latitude: Latitude of a given Coordinate
    :param longitude: Longitude of a given Coordinate
    :return: Name of that place based on its coordinates
    '''
    try:
        geolocator = Nominatim(user_agent="location_app")
        location = geolocator.reverse(f"{latitude}, {longitude}", language='en')
        return location.address if location else "Location not found."
    except Exception as e:
        return f"Error: {str(e)}"


def get_hosptials(lat,lon):

    '''
        :param lat: Latitude of the Accident Location
        :param lon: Longitude of the Accident Location
        :return : A list containing HospitalName, and email of the Nearest Hospital
        :workflow : This function will take the lat, lon of the detected accident and using it as a center it will search for the hospitals within the area of 2KM
                    Later it will fetch those hospitals info and save it in a temporary/dynamic database. After creating the Dynamic Database ( Upto 5 Entries ), we will
                    perform 'left' join on the new Database (hospital_info) and the Local Database (hospital_contacts) and will return the 1st entry of that merged database
    '''
    map_center = (lat,lon)

    # Create a network graph around the target location (here, within 2 kilometers)
    G = ox.graph_from_point(map_center, dist=2000, network_type='all')

    # Get the nearest node to the target coordinate
    target_node = ox.distance.nearest_nodes(G, map_center[1], map_center[0])

    # Retrieve hospitals within a certain radius from the target coordinate using OSMnx
    hospitals = ox.geometries_from_point(map_center, tags={'amenity': 'hospital'}, dist=2000)

    # Extract hospital information
    hospital_info = []
    for idx, hospital in hospitals.iterrows():
        name = hospital['name']
        lat = hospital.geometry.centroid.y
        lon = hospital.geometry.centroid.x
        hospital_info.append((name, lat, lon))
        if len(hospital_info) == 5:
            break

    print(hospital_info)

    hospital_data = pd.DataFrame(hospital_info,columns=['HospitalName','Latitude','Longitude'])

    hospital_data.head()

    hospital_contacts = pd.read_csv('Database/pune_hospitals.csv')

    # Performing Left Join

    merged_data = pd.merge(hospital_data, hospital_contacts, on=['Latitude', 'Longitude'], how='left',
                           suffixes=('_data', '_contact'))

    info = [merged_data['HospitalName_data'].iloc[0], merged_data['Email'].iloc[0]]

    return info


def send_email(hospital_data,lat,lon):
    '''

    :param hospital_data: List containing the Name and Email of the Nearest Hospital
    :param lat: Latitude of the Accident location
    :param lon: Logitude of the Accident location
    :return: This function will send email to the nearest hospital
    '''

    accident_location = get_location_from_lls(lat,lon)
    mail_user = 'ai.safetynxt@gmail.com'
    mail_pass = os.environ.get('TestPass')

    subject = "Urgent: Accident Detected - Immediate Medical Attention Required"
    body = '''
        Dear {},
                    An accident has been detected near your hospital at {}. Immediate medical attention is crucial.
                    Please prepare your medical team to respond to this emergency situation promptly.

        Thank you for your swift action.

        Sincerely,
        SafetyNXT Team
                '''.format(hospital_data[0], accident_location)


    em = EmailMessage()
    em['From'] = mail_user
    em['To'] = hospital_data[1]
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(mail_user, hospital_data[1], em.as_string())



# TODO: Send the mail to 5 nearest hospital along with a toggle button
'''
Case Study -
    PS - If we sent the mail only to one hospital and if tht hospital is busy at that time, so quick response will be provided to that incident
    Sol - Send the mail to 5 nearest hospital instead of one, so even if one hospital is busy till other can provide quick response
    PS - What if in worst possible case none of the hospital is busy, so every one will provide quick response this will result in wastage of Resources
    Sol - In that email add a toggle button, so that if one hospital is on its way to provide resources to the incident then it will info our system and once this information is
          received we'll send another mail to the remaining hospitals so tht their wont be any wastage of resources and also the incident will get timely response
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
    :return: The list of CCTV's (including Id's) that are present in the shortest path bw start and end location, list of latitude and longitude of the Matching CCTV ID's
    :working: Input of Source and Destination Coordinates entered by the user will be given to the function, shortest distance bw the
              Source and Destination will be calculated and the Coordinates of the shortest distance will be matched with the CCTV
              Coordinates Database and matching Coordinates will be returned

    '''

    G = ox.graph_from_point((from_lat_float, from_lon_float), dist=5000, network_type='all')

    start_node = ox.distance.nearest_nodes(G, from_lon_float, from_lat_float)
    end_node = ox.distance.nearest_nodes(G, to_lon_float, to_lat_float)

    route = nx.shortest_path(G, start_node, end_node, weight='length')

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


    return matching_coordinates_with_cam_id, route_coordinates


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

            logger.debug(f"From Lat: {from_lat}, From Lon: {from_lon}")
            logger.debug(f"To Lat: {to_lat}, To Lon: {to_lon}")

            try:
                cctv_info_map, route_coordinate = get_cctvs_info(from_lat_float, from_lon_float, to_lat_float,
                                                                 to_lon_float)
            except ImportError as e:
                logger.error(f"ImportError: {str(e)}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

            # Fetching the Matched CCTV ID's, their lan and their lon from the DataBase
            cctv_info_map, route_coordinate = get_cctvs_info(from_lat_float, from_lon_float, to_lat_float, to_lon_float)


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




            # Generating Random 5 numbers from the route coordinates
            total_len = len(route_coordinate)
            logger.debug(f"Total route length: {total_len}")

            # Getting 5 random numbers and appending them in a list
            if total_len < 5:
                logger.error("Not enough route coordinates to generate detected list.")
                return JsonResponse({'status': 'error', 'message': 'Not enough route coordinates'}, status=500)

            random_numbers = [random.randint(0, total_len - 1) for _ in range(5)]
            logger.debug(f"Random indices: {random_numbers}")

            # After detection of accident send an emergency mail to the nearest hospital
            send_email(route_coordinate[random_numbers[4]][0], route_coordinate[random_numbers[4]][1])

            # Create a demo detected_list
            detected_list = {
                "potholes": [
                    {"lat": route_coordinate[random_numbers[0]][0], "lon": route_coordinate[random_numbers[0]][1], 'num': 0.5},
                    {"lat": route_coordinate[random_numbers[1]][0], "lon": route_coordinate[random_numbers[1]][1], 'num': 0.8},
                ],
                "traffic": [
                    {"lat": route_coordinate[random_numbers[2]][0], "lon": route_coordinate[random_numbers[2]][1], 'num': 0.2},
                    {"lat": route_coordinate[random_numbers[3]][0], "lon": route_coordinate[random_numbers[3]][1], 'num': 0.7},
                ],
                "accidents": [
                    {"lat": route_coordinate[random_numbers[4]][0], "lon": route_coordinate[random_numbers[4]][1]}
                ]
            }

            logger.debug(f"Detected list: {detected_list}")

            return JsonResponse({'status': 'success', 'detected_list': detected_list})
            # return JsonResponse({'status':'success'})


        except json.JSONDecodeError as e:

            logger.error(f"Invalid JSON format: {str(e)}")

            return JsonResponse({'status': 'error', 'message': f'Invalid JSON format: {str(e)}'}, status=400)

        except Exception as e:

            logger.error(f"Unexpected error: {str(e)}")

            return JsonResponse({'status': 'error', 'message': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid Request Method'}, status=405)
