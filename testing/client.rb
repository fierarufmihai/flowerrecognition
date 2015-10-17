require 'rest_client'
RestClient.post('http://localhost:8802/flowerrecognition',
		    	:callback => 'http://localhost:8802/deepsentibank',
				:mediafile => File.new('../data/before/sun.jpg'),
				:jobid => 7, 
				:modelname => "blamodel"
              )

