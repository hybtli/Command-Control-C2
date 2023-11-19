import requests


def get_geolocation(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Error retrieving geolocation: {e}")
        return None


def print_geolocation_details(geolocation_data):
    print("Geolocation Details:")

    ip_address = geolocation_data.get('ip')
    if ip_address:
        print(f"Public IP Address: {ip_address}")
    else:
        print("IP Address information not available.")

    # Handle missing 'City'
    city = geolocation_data.get('city')
    if city:
        print(f"City: {city}")
    else:
        print("City information not available.")

    # Handle missing 'Region'
    region = geolocation_data.get('region')
    if region:
        print(f"Region: {region}")
    else:
        print("Region information not available.")

    # Handle missing 'Country'
    country = geolocation_data.get('country')
    if country:
        print(f"Country: {country}")
    else:
        print("Country information not available.")

    # Handle missing 'Postal Code'
    postal_code = geolocation_data.get('postal')
    if postal_code:
        print(f"Postal Code: {postal_code}")
    else:
        print("Postal Code information not available.")

    # Handle missing 'Timezone'
    timezone = geolocation_data.get('timezone')
    if timezone:
        print(f"Timezone: {timezone}")
    else:
        print("Timezone information not available.")
