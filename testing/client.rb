require 'rest_client'
RestClient.post('http://localhost:8802/flowerrecognition',
				:mediafile => File.new('../data/before/sun.jpg'),
				:jobid => "12345", 
              )

