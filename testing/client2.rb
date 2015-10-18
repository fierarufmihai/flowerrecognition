require 'rest_client'
r = RestClient.post('http://localhost:8802/checkfinished',
				:jobid => "12345", 
              )
puts r

