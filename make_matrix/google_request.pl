import googlemaps
import numpy

gmaps = googlemaps.Client(key='AIzaSyBN-UulFeXqjqECo628iWwY9pEZyGRUltA')

addresses_of_employees = [  'Snunit St 51 Karmiel',
                            'Sarig St 5 Karmiel',
                            'Ha-Dekel St 56 Karmiel',
                            'Ramim St 37 Karmiel',
                            'Arava St 10 Karmiel',
                            'HaShoshanim Street 4 Karmiel',
                            'Sderot Jabotinsky 10 Kiryat Yam']
_A = [[0 for x in range(7)] for y in range(7)] 
print ("number of adresses is " ,len(addresses_of_employees))
print ()
# distance_matrix an address
distance_result = gmaps.distance_matrix(addresses_of_employees,addresses_of_employees)

#data = json.loads(distance_result)


for i,rows in enumerate(distance_result['rows']):
    
    for j,element in enumerate(rows['elements']):
        #print (element['distance']['value'] , i,j)
        _A[i][j] = element['distance']['value']
        #print (element['distance']['value'])


print  (numpy.matrix(_A))




