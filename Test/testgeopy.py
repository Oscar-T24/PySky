from geopy.geocoders import Nominatim
# Enter the name of the department
department_name = input("Enter the name of the department: ")
# Create a geolocator object
geolocator = Nominatim(user_agent="geoapiExercises")
# Use the geolocator to get the location of the department
location = geolocator.geocode(f"{department_name}, France")
# Extract the latitude and longitude from the location object
latitude = location.latitude
longitude = location.longitude
# Print the latitude and longitude coordinates
print(f"The latitude and longitude coordinates of {department_name} are ({latitude}, {longitude})")
